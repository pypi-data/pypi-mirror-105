from typing import List, Optional
from cloudrail.knowledge.context.aws.service_name import AwsServiceName, AwsServiceType, AwsServiceAttributes
from cloudrail.knowledge.context.aws.ecs.ecs_constants import LaunchType
from cloudrail.knowledge.context.aws.ecs.ecs_task_definition import IEcsInstance, EcsTaskDefinition
from cloudrail.knowledge.context.aws.networking_config.inetwork_configuration import INetworkConfiguration
from cloudrail.knowledge.context.aws.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.networking_config.network_entity import NetworkEntity


class EcsTarget(NetworkEntity, INetworkConfiguration, IEcsInstance):

    def __init__(self, name: str, target_id: str, launch_type: LaunchType, account: str, region: str,
                 cluster_arn: str, role_arn: str, network_conf_list: List[NetworkConfiguration],
                 task_definition_arn: str = None) -> None:
        NetworkEntity.__init__(self, name, account, region, AwsServiceName.NONE,
                               AwsServiceAttributes(aws_service_type=AwsServiceType.ECS.value, region=region))
        IEcsInstance.__init__(self)
        INetworkConfiguration.__init__(self)
        self.target_id: str = target_id
        self.launch_type: LaunchType = launch_type
        self.cluster_arn: str = cluster_arn
        self.role_arn: str = role_arn
        self.network_conf_list: List[NetworkConfiguration] = network_conf_list
        self.task_definition_arn: str = task_definition_arn
        self._task_definition: Optional[EcsTaskDefinition] = None
        self.cluster_name: str = None

    def get_all_network_configurations(self) -> List[NetworkConfiguration]:
        return self.network_conf_list

    def get_task_definition(self) -> EcsTaskDefinition:
        return self._task_definition

    def set_task_definition(self, task: EcsTaskDefinition) -> None:
        self._task_definition = task

    def get_task_definition_arn(self) -> str:
        return self.task_definition_arn

    def get_keys(self) -> List[str]:
        return [self.target_id]

    def __str__(self) -> str:
        return "EcsTarget name={}".format(self.name)

    def get_name(self) -> str:
        return self.name

    def get_id(self) -> str:
        return self.target_id

    def get_arn(self) -> str:
        return self.cluster_arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'ECS target'
        else:
            return 'ECS targets'

    def get_cloud_resource_url(self) -> str:
        return '{0}ecs/home?region={1}#/clusters/{2}/tasks' \
            .format(self.AWS_CONSOLE_URL, self.region, self.cluster_name)

    @property
    def is_tagable(self) -> bool:
        return False
