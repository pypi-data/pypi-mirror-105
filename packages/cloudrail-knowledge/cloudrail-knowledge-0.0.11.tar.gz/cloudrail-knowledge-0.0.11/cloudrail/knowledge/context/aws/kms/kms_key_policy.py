from typing import List, Optional
from cloudrail.knowledge.context.aws.iam.policy import Policy
from cloudrail.knowledge.context.aws.iam.policy_statement import PolicyStatement
from cloudrail.knowledge.context.aws.service_name import AwsServiceName


class KmsKeyPolicy(Policy):

    def __init__(self,
                 key_id: str,
                 policy_statements: Optional[List[PolicyStatement]],
                 raw_document: str,
                 account: str):
        super().__init__(account, policy_statements, raw_document, AwsServiceName.AWS_KMS_KEY)
        self.key_id: str = key_id

    def get_keys(self) -> List[str]:
        return [self.key_id]

    def get_id(self) -> str:
        return self.key_id

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'KMS key resource policy'
        else:
            return 'KMS key resource policies'

    @property
    def is_tagable(self) -> bool:
        return False
