from typing import List
from cloudrail.knowledge.context.aws.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.service_name import AwsServiceName


class CodeBuildReportGroup(AwsResource):

    def __init__(self,
                 account: str,
                 region: str,
                 name: str,
                 export_config_type: str,
                 export_config_s3_destination_bucket: str,
                 export_config_s3_destination_encryption_key: str,
                 export_config_s3_destination_encryption_disabled: bool,
                 arn: str):
        super().__init__(account, region, AwsServiceName.AWS_CODEBUILD_REPORT_GROUP)
        self.name: str = name
        self.export_config_type: str = export_config_type
        self.export_config_s3_destination_bucket: str = export_config_s3_destination_bucket
        self.export_config_s3_destination_encryption_disabled: bool = export_config_s3_destination_encryption_disabled
        self.export_config_s3_destination_encryption_key: str = export_config_s3_destination_encryption_key
        self.arn: str = arn
        self.export_config_s3_destination_kms_data: KmsKey = None

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.name

    def get_arn(self) -> str:
        return self.arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'CodeBuild Report Group'
        else:
            return 'CodeBuild Report Groups'

    def get_cloud_resource_url(self) -> str:
        return 'https://console.aws.amazon.com/codesuite/codebuild/{0}/testReports/reportGroups/{1}'\
            .format(self.account, self.name)

    @property
    def is_tagable(self) -> bool:
        return True
