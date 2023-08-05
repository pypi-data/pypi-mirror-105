from typing import List

from cloudrail.knowledge.context.aws.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.aws_resource import AwsResource


class CloudWatchLogGroup(AwsResource):

    def __init__(self,
                 name: str,
                 kms_encryption: str,
                 arn: str,
                 retention_in_days: int,
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_CLOUDWATCH_LOG_GROUP)
        self.name: str = name
        self.kms_encryption: str = kms_encryption
        self.arn: str = arn
        self.kms_data: KmsKey = None
        self.retention_in_days: int = retention_in_days

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.name

    def get_arn(self) -> str:
        return self.arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'CloudWatch Logs Group'
        else:
            return 'CloudWatch Logs Groups'

    def get_cloud_resource_url(self) -> str:
        return '{0}cloudwatch/home?region={1}#logsV2:log-groups/log-group/{2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.name.replace('/', '$252F'))

    @property
    def is_tagable(self) -> bool:
        return True
