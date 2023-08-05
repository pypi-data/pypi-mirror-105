from typing import List

from cloudrail.knowledge.context.aws.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.aws_resource import AwsResource


class KmsAlias(AwsResource):

    def __init__(self,
                 alias_name: str,
                 target_key_id: str,
                 alias_arn: str,
                 account: str,
                 region: str):
        super().__init__(account, region, AwsServiceName.AWS_KMS_KEY)
        self.alias_name: str = alias_name
        self.target_key_id: str = target_key_id
        self.alias_arn: str = alias_arn
        self.key_manager = None

    def get_keys(self) -> List[str]:
        return [self.alias_arn]

    def get_name(self) -> str:
        return self.alias_name

    def get_arn(self) -> str:
        return self.alias_arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'KMS alias'
        else:
            return 'KMS aliases'

    def get_cloud_resource_url(self) -> str:
        if self.key_manager == KeyManager.CUSTOMER:
            return '{0}kms/home?region={1}#/kms/keys/{2}' \
                .format(self.AWS_CONSOLE_URL, self.region, self.target_key_id)
        else:
            return '{0}kms/home?region={1}#/kms/defaultKeys/{2}' \
                .format(self.AWS_CONSOLE_URL, self.region, self.target_key_id)

    @property
    def is_tagable(self) -> bool:
        return False
