from typing import List
from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.ecr.ecr_repository_policy import EcrRepositoryPolicy
from cloudrail.knowledge.context.aws.aws_resource import AwsResource


class EcrRepository(AwsResource):

    def __init__(self,
                 repo_name: str,
                 arn: str,
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_ECR_REPOSITORY)
        self.repo_name: str = repo_name
        self.arn: str = arn
        self.policy: EcrRepositoryPolicy = None

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.repo_name

    def get_arn(self) -> str:
        return self.arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'ECR repository'
        else:
            return 'ECR repositories'

    def get_cloud_resource_url(self) -> str:
        return '{0}ecr/repositories/private/{1}/{2}?region={3}'\
            .format(self.AWS_CONSOLE_URL, self.account, self.repo_name, self.region)

    @property
    def is_tagable(self) -> bool:
        return True
