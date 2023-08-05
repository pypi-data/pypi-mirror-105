from __future__ import annotations
from enum import Enum
from typing import List, Tuple

from cloudrail.knowledge.utils.range_util import get_range_numbers_overlap, EMPTY_RANGE
from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.aws_resource import AwsResource

from cloudrail.knowledge.utils.utils import get_overlap_cidr, normalize_port_range, is_port_in_range


class SecurityGroupRulePropertyType(Enum):
    SECURITY_GROUP_ID = ('UserIdGroupPairs', 'GroupId')
    IP_RANGES = ('IpRanges', 'CidrIp')
    PREFIX_LIST_ID = ('PrefixListIds', 'PrefixListId')


class ConnectionType(Enum):
    Inbound = 'inbound'
    Outbound = 'outbound'


class SecurityGroupRule(AwsResource):

    def __init__(self, from_port: int, to_port: int, ip_protocol: str, property_type: SecurityGroupRulePropertyType,
                 property_value: str, has_description: bool, connection_type: ConnectionType,
                 security_group_id: str, region: str, account: str):
        super().__init__(account, region, AwsServiceName.AWS_SECURITY_GROUP_RULE)
        normalized_from_port, normalized_to_port = normalize_port_range(from_port, to_port)
        self.from_port: int = normalized_from_port
        self.to_port: int = normalized_to_port
        self.ip_protocol: str = ip_protocol
        self.property_type: SecurityGroupRulePropertyType = property_type
        self.property_value: str = property_value
        self.has_description: bool = has_description
        self.connection_type: ConnectionType = connection_type
        self.security_group_id: str = security_group_id

    def __str__(self) -> str:
        return "SG permission: from_port={}, to_port={}, ip_protocol={}, property_type={}, property_value={}".format(
            self.from_port,
            self.to_port,
            self.ip_protocol,
            self.property_type.__str__(),
            self.property_value)

    def is_in_range(self, port: int) -> bool:
        return is_port_in_range((self.from_port, self.to_port), port)

    def get_keys(self) -> List[str]:
        return [self.security_group_id, self.from_port, self.to_port,
                self.property_type, self.property_value, self.connection_type.value]

    def get_friendly_name(self) -> str:
        return '{} rule of {} for ports {}:{} using protocol {}'\
            .format('ingress' if self.connection_type == ConnectionType.Inbound else 'egress',
                    self.property_value or self.security_group_id,
                    self.from_port,
                    self.to_port,
                    self.ip_protocol)

    def get_extra_data(self) -> str:
        return str(self)

    def is_match(self, rule: SecurityGroupRule) -> bool:
        # todo - need to support pl id type and cross account peering instance
        if self.ip_protocol == '-1' or rule.ip_protocol == '-1' or self.ip_protocol == rule.ip_protocol:
            is_ports_overlap: bool = get_range_numbers_overlap(self.get_ports_range(), rule.get_ports_range()) != EMPTY_RANGE
            if self.property_type == SecurityGroupRulePropertyType.SECURITY_GROUP_ID and self.property_value == rule.security_group_id:
                return is_ports_overlap
            elif rule.property_type == SecurityGroupRulePropertyType.IP_RANGES and \
                    get_overlap_cidr(rule.property_value, self.property_value).size > 0:
                return is_ports_overlap
        return False

    def get_ports_range(self) -> Tuple[int, int]:
        return self.from_port, self.to_port

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Security group rule'
        else:
            return 'Security group rules'

    def get_cloud_resource_url(self) -> str:
        return '{0}vpc/home?region={1}#SecurityGroup:groupId={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.security_group_id)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False
