from typing import List, Optional
from cloudrail.knowledge.context.aws.resource_based_policy import ResourceBasedPolicy
from cloudrail.knowledge.context.aws.s3.s3_bucket_object import S3BucketObject
from cloudrail.knowledge.context.aws.service_name import AwsServiceName, AwsServiceType, AwsServiceAttributes
from cloudrail.knowledge.context.aws.aws_connection import ConnectionInstance
from cloudrail.knowledge.context.aws.iam.policy import S3Policy
from cloudrail.knowledge.context.aws.s3.public_access_block_settings import PublicAccessBlockSettings
from cloudrail.knowledge.context.aws.s3.s3_acl import S3ACL
from cloudrail.knowledge.context.aws.s3.s3_bucket_access_point import S3BucketAccessPoint, S3BucketAccessPointNetworkOriginType
from cloudrail.knowledge.context.aws.s3.s3_bucket_encryption import S3BucketEncryption


class S3Bucket(ConnectionInstance, ResourceBasedPolicy):

    def __init__(self, account: str, bucket_name: str, arn: str, region: str = None,
                 policy: S3Policy = None):
        ResourceBasedPolicy.__init__(self, account, region, AwsServiceName.AWS_S3_BUCKET,
                                     AwsServiceAttributes(aws_service_type=AwsServiceType.S3.value, region=region))
        ConnectionInstance.__init__(self)
        self.resource_based_policy = policy
        self.bucket_name = bucket_name
        self.arn = arn
        self.bucket_domain_name = bucket_name + ".s3.amazonaws.com"
        self.with_aliases(bucket_name, arn, self.bucket_domain_name)
        self.acls: List[S3ACL] = []
        self.public_access_block_settings: Optional[PublicAccessBlockSettings] = None
        self.access_points: List[S3BucketAccessPoint] = []
        self.encryption_data: Optional[S3BucketEncryption] = None
        self.bucket_objects: List[S3BucketObject] = []

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_vpc_access_points(self, vpc_id: str):
        return [x for x in self.access_points
                if x.network_origin.access_type == S3BucketAccessPointNetworkOriginType.VPC and
                x.network_origin.vpc_id == vpc_id]

    def get_arn(self) -> str:
        return self.arn

    def get_name(self) -> str:
        return self.bucket_name

    def __str__(self) -> str:
        return self.bucket_name

    def get_cloud_resource_url(self) -> str:
        return 'https://s3.console.aws.amazon.com/s3/buckets/{0}?region={1}&tab=objects'\
            .format(self.bucket_name, self.region)

    @property
    def is_tagable(self) -> bool:
        return True
