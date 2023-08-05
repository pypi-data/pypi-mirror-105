from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.autoscaling.launch_template import LaunchTemplate
from cloudrail.knowledge.context.aws.aws_resource import AwsResource


class LaunchConfiguration(AwsResource):

    def __init__(self,
                 arn: str,
                 image_id: str,
                 instance_type: str,
                 key_name: str,
                 name: str,
                 security_group_ids: List[str],
                 http_tokens: str,
                 iam_instance_profile: Optional[str],
                 region: str,
                 account: str,
                 associate_public_ip_address: Optional[bool]):
        super().__init__(account, region, AwsServiceName.AWS_LAUNCH_CONFIGURATION)
        self.arn: str = arn
        self.image_id: str = image_id
        self.instance_type: str = instance_type
        self.key_name: str = key_name
        self.name: str = name
        self.security_group_ids: List[str] = security_group_ids
        self.http_tokens: str = http_tokens
        self.associate_public_ip_address: Optional[bool] = associate_public_ip_address
        self.aliases.add(self.name)
        self.iam_instance_profile: Optional[str] = iam_instance_profile

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Launch configuration'
        else:
            return 'Launch configurations'

    def get_cloud_resource_url(self) -> str:
        return '{0}ec2autoscaling/home?region={1}#/lc?launchConfigurationName={2}' \
            .format(self.AWS_CONSOLE_URL, self.region, self.name)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False


@dataclass
class LaunchTemplateData:
    template_id: str
    version: str


@dataclass
class AutoScalingGroupRawData:
    launch_configuration_name: Optional[str] = None
    launch_template_data: Optional[LaunchTemplateData] = None


class AutoScalingGroup(AwsResource):

    def __init__(self,
                 arn: str,
                 target_group_arns: List[str],
                 name: str,
                 availability_zones: List[str],
                 subnet_ids: List[str],
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_AUTO_SCALING_GROUP)
        self.arn = arn  # todo - network attributes are missing
        self.target_group_arns = target_group_arns
        self.name = name
        self.availability_zones = availability_zones
        self.subnet_ids = subnet_ids
        self.launch_configuration: Optional[LaunchConfiguration] = None
        self.launch_template: Optional[LaunchTemplate] = None
        self.raw_data: AutoScalingGroupRawData = AutoScalingGroupRawData()
        self.region: str = region
        self.account: str = account

    def get_keys(self) -> List[str]:
        return [self.arn]

    def with_raw_data(self, launch_configuration_name: Optional[str] = None,
                      launch_template_id: Optional[str] = None,
                      launch_template_version: Optional[str] = None) -> AutoScalingGroup:
        self.raw_data.launch_configuration_name = launch_configuration_name
        if launch_template_id and launch_template_version:
            self.raw_data.launch_template_data = LaunchTemplateData(launch_template_id, launch_template_version)
        return self

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Auto Scaling group'
        else:
            return 'Auto Scaling groups'

    def get_cloud_resource_url(self) -> str:
        return 'https://console.aws.amazon.com/ec2autoscaling/home?region={0}#/details/{1}?view=details' \
            .format(self.region, self.name)

    def get_arn(self) -> str:
        return self.arn

    @property
    def is_tagable(self) -> bool:
        return True
