from typing import List, Dict

from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.utils.connection_utils import ConnectionUtils
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class PublicAccessEksApiRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'public_access_eks_api'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for eks_cluster in env_context.eks_clusters:
            violating_security_group = ConnectionUtils.get_allowing_public_access_on_ports(eks_cluster, [eks_cluster.port])
            if violating_security_group:
                issues.append(Issue(
                    f'~Internet~. '
                    f'{eks_cluster.get_type()} `{eks_cluster.get_friendly_name()}` '
                    f'is on {eks_cluster.network_resource.vpc.get_type()}'
                    f' `{eks_cluster.network_resource.vpc.get_friendly_name()}`. '
                    f'Master is protected by security groups '
                    f'`{", ".join([x.get_friendly_name() for x in eks_cluster.network_resource.security_groups])}`. '
                    f'{eks_cluster.get_type()} uses subnets'
                    f' `{", ".join([x.get_friendly_name() for x in eks_cluster.network_resource.subnets])}`. '
                    f"Subnets rely on Network ACL's "
                    f'`{", ".join([x.network_acl.get_friendly_name() for x in eks_cluster.network_resource.subnets])}`. '
                    f'They also rely on Route tables '
                    f'`{", ".join([x.route_table.get_friendly_name() for x in eks_cluster.network_resource.subnets])}`. '
                    f'{eks_cluster.get_type()} is set to be publicly accessible',
                    eks_cluster,
                    violating_security_group))

        return issues

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.eks_clusters)
