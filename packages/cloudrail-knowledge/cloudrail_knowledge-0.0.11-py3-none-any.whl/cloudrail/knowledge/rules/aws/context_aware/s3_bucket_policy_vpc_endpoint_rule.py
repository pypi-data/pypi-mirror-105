from typing import Dict, List

from cloudrail.knowledge.context.aws.aws_connection import PolicyEvaluation
from cloudrail.knowledge.context.aws.iam.policy import S3Policy
from cloudrail.knowledge.context.aws.iam.policy_statement import StatementEffect
from cloudrail.knowledge.context.aws.s3.s3_bucket import S3Bucket
from cloudrail.knowledge.context.aws.ec2.vpc import Vpc
from cloudrail.knowledge.context.aws.ec2.vpc_endpoint import VpcEndpoint
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from cloudrail.knowledge.utils.policy_utils import is_any_resource_based_action_allowed
from cloudrail.knowledge.utils.s3_public_access_evaluator import S3PublicAccessEvaluator


class S3BucketPolicyVpcEndpointRule(AwsBaseRule):

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues_list: List[Issue] = []
        vpc_to_buckets_map: Dict[Vpc, List[S3Bucket]] = self._create_vpc_to_buckets_map(env_context)
        for vpc, bucket_list in vpc_to_buckets_map.items():
            for s3_vpce in self._filter_by_service_name(vpc):
                for bucket in bucket_list:
                    if bucket.resource_based_policy is None or \
                            not self._is_restrict_to_s3_vpce(bucket.resource_based_policy, s3_vpce):
                        issues_list.append(Issue(f"~{bucket.get_type()}~. `{bucket.get_friendly_name()}` is accessible via"
                                                 f" VPC endpoint `{s3_vpce.get_friendly_name()}`. "
                                                 f"~in VPC~. `{vpc.get_friendly_name()}` "
                                                 f"with a policy that is not restricting requests sourced from"
                                                 f" a VPC Endpoint.", bucket, bucket))

        return issues_list

    def get_id(self) -> str:
        return "s3_bucket_policy_vpce"

    @staticmethod
    def _create_vpc_to_buckets_map(env_context: EnvironmentContext) -> Dict[Vpc, List[S3Bucket]]:
        region_to_buckets_map: Dict[str, List[S3Bucket]] = {}
        vpc_to_buckets_map: Dict[Vpc, List[S3Bucket]] = {}

        for bucket in env_context.s3_buckets:
            evaluator: S3PublicAccessEvaluator = S3PublicAccessEvaluator(bucket)
            if not any(is_any_resource_based_action_allowed(PolicyEvaluation(resource_allowed_actions=result.allowed_actions,
                                                                             resource_denied_actions=result.denied_actions))
                       for result in evaluator.evaluate().values()):  # add private buckets only
                if bucket.region not in region_to_buckets_map:
                    region_to_buckets_map[bucket.region] = []
                region_to_buckets_map[bucket.region].append(bucket)

        for vpc in env_context.vpcs.values():
            if vpc.region in region_to_buckets_map:
                vpc_to_buckets_map[vpc] = region_to_buckets_map[vpc.region]

        return vpc_to_buckets_map

    @staticmethod
    def _is_restrict_to_s3_vpce(policy: S3Policy, s3_vpce: VpcEndpoint) -> bool:
        for statement in policy.get_all_statements():
            expected_operator_prefix: str = "String" if statement.effect == StatementEffect.ALLOW else "StringNot"
            for condition_block in statement.condition_block:
                if condition_block.operator.startswith(expected_operator_prefix) and \
                        condition_block.key == "aws:SourceVpce" and \
                        s3_vpce.vpce_id in condition_block.values:
                    return True
        return False

    @staticmethod
    def _filter_by_service_name(vpc: Vpc, service_name: str = "s3"):
        return [s3_vpce for s3_vpce in vpc.endpoints if s3_vpce.service_name.endswith(f".{service_name}")]

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.s3_buckets)
