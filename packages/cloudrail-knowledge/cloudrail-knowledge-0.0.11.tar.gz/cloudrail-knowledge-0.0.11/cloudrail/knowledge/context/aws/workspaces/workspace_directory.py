from typing import List, Optional

from cloudrail.knowledge.context.aws.ds.directory_service import DirectoryService
from cloudrail.knowledge.context.aws.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.service_name import AwsServiceName


class WorkspaceDirectory(NetworkEntity):

    def __init__(self,
                 account: str,
                 region: str,
                 directory_id: str,
                 subnet_ids: Optional[list],
                 security_group_ids: list):
        super().__init__(directory_id, account, region, AwsServiceName.AWS_WORKSPACES_DIRECTORY)
        self.directory_id: str = directory_id
        self.subnet_ids: Optional[list] = subnet_ids
        self.security_group_ids: list = security_group_ids
        self.arn: str = f'arn:aws:workspaces:{self.region}:{self.account}:directory/{self.directory_id}'
        self.workspace_security_groups: List[SecurityGroup] = []
        self.cloud_directory: DirectoryService = None

    def get_keys(self) -> List[str]:
        return [self.directory_id]

    def get_id(self) -> str:
        return self.directory_id

    def get_arn(self) -> str:
        return self.arn

    def get_all_network_configurations(self) -> List[NetworkConfiguration]:
        return [NetworkConfiguration(False, self.security_group_ids, self.subnet_ids)]

    def get_cloud_resource_url(self) -> str:
        return '{0}workspaces/home?region={1}#directories:directories'\
            .format(self.AWS_CONSOLE_URL, self.region)

    @property
    def is_tagable(self) -> bool:
        return True
