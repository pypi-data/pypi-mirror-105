from typing import List, Optional

from cloudrail.knowledge.context.aws.networking_config.inetwork_configuration import INetworkConfiguration
from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.networking_config.network_entity import NetworkEntity


class NeptuneInstance(NetworkEntity, INetworkConfiguration):

    def __init__(self,
                 account: str,
                 region: str,
                 name: str,
                 arn: str,
                 port: int,
                 cluster_identifier: str,
                 publicly_accessible: bool,
                 instance_identifier: str,
                 tf_resource_type: AwsServiceName = AwsServiceName.AWS_NEPTUNE_CLUSTER_INSTANCE):
        super().__init__(name, account, region, tf_resource_type)
        self.port: int = port
        self.arn: str = arn
        self.neptune_subnet_group_name: str = None
        self.is_in_default_vpc: bool = None
        self.network_configuration: NetworkConfiguration = NetworkConfiguration(publicly_accessible, [], None)
        self.instance_identifier: str = instance_identifier
        self.cluster_identifier: str = cluster_identifier

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.name

    def get_id(self) -> str:
        return self.instance_identifier

    def get_arn(self) -> str:
        return self.arn

    def get_all_network_configurations(self) -> List[NetworkConfiguration]:
        return [self.network_configuration]

    def get_cloud_resource_url(self) -> Optional[str]:
        return '{0}neptune/home?region={1}#database:id={2};is-cluster=false' \
            .format(self.AWS_CONSOLE_URL, self.region, self.instance_identifier)

    @property
    def is_tagable(self) -> bool:
        return True
