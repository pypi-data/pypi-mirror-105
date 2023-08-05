from typing import List

from cloudrail.knowledge.context.aws.iam.policy import Policy
from cloudrail.knowledge.context.aws.iam.policy_statement import PolicyStatement
from cloudrail.knowledge.context.aws.service_name import AwsServiceName


class EfsPolicy(Policy):

    def __init__(self,
                 efs_id: str,
                 policy_statements: List[PolicyStatement],
                 raw_document: str,
                 account: str):
        super().__init__(account, policy_statements, raw_document, AwsServiceName.AWS_EFS_FILE_SYSTEM_POLICY)
        self.efs_id: str = efs_id

    def get_keys(self) -> List[str]:
        return [self.efs_id, self.region, self.account]

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'EFS file system resource policy'
        else:
            return 'EFS file system resource policies'
