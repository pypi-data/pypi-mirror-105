from typing import List, Optional

from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.aws_connection import ConnectionInstance

from cloudrail.knowledge.context.aws.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.rds.rds_instance import RdsInstance


class RdsCluster(ConnectionInstance, AwsResource):
    def __init__(self,
                 account: str,
                 region: str,
                 cluster_id: str,
                 arn: str,
                 port: int,
                 db_subnet_group_name: str,
                 security_group_ids: List[str],
                 encrypted_at_rest: bool):
        ConnectionInstance.__init__(self)
        AwsResource.__init__(self, account, region, AwsServiceName.AWS_RDS_CLUSTER)
        self.cluster_id: str = cluster_id
        self.arn: str = arn
        self.port: int = port
        self.db_subnet_group_name: str = db_subnet_group_name
        self.is_in_default_vpc: bool = db_subnet_group_name is None
        self.cluster_instances: List[RdsInstance] = []
        self.security_group_ids: List[str] = security_group_ids
        self.encrypted_at_rest: bool = encrypted_at_rest

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_id(self) -> str:
        return self.cluster_id

    def get_arn(self) -> str:
        return self.arn

    def get_extra_data(self) -> str:
        port = 'port: {}'.format(self.port) if self.port else ''
        db_subnet_group_name = 'db_subnet_group_name: {}'.format(self.db_subnet_group_name) if self.db_subnet_group_name else ''
        return ', '.join([port, db_subnet_group_name])

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'RDS DB cluster'
        else:
            return 'RDS DB clusters'

    def get_cloud_resource_url(self) -> Optional[str]:
        return '{0}rds/home?region={1}#database:id={2};is-cluster=true' \
            .format(self.AWS_CONSOLE_URL, self.region, self.cluster_id)

    @property
    def is_tagable(self) -> bool:
        return True
