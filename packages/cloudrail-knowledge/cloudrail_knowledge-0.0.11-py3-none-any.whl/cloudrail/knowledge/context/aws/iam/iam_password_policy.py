from typing import List
from cloudrail.knowledge.context.aws.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.service_name import AwsServiceName


class IamPasswordPolicy(AwsResource):

    def __init__(self,
                 min_pass_length: int,
                 require_low_case_characters: bool,
                 require_numbers: bool,
                 require_upper_case_characters: bool,
                 require_symbols: bool,
                 allow_users_to_change_pass: bool,
                 max_pass_age: int,
                 password_reuse_prevention: int,
                 account: str):
        super().__init__(account=account, region=self.GLOBAL_REGION, tf_resource_type=AwsServiceName.AWS_IAM_ACCOUNT_PASSWORD_POLICY)
        self.min_pass_length: int = min_pass_length
        self.require_low_case_characters: bool = require_low_case_characters
        self.require_numbers: bool = require_numbers
        self.require_upper_case_characters: bool = require_upper_case_characters
        self.require_symbols: bool = require_symbols
        self.allow_users_to_change_pass: bool = allow_users_to_change_pass
        self.max_pass_age: int = max_pass_age
        self.password_reuse_prevention: int = password_reuse_prevention

    def get_keys(self) -> List[str]:
        return [self.account]

    def get_name(self) -> str:
        return self.account + ' policy'

    def get_type(self, is_plural: bool = False) -> str:
        return 'IAM Password Policy'

    def get_cloud_resource_url(self) -> str:
        return '{0}iam/home?region={1}#/account_settings$editPasswordPolicy?step=passwordPolicy' \
            .format(self.AWS_CONSOLE_URL, 'us-east-1')

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False
