from typing import List, Optional
from cloudrail.knowledge.context.aws.apigateway.rest_api_gw_mapping import RestApiGwMapping
from cloudrail.knowledge.context.aws.service_name import AwsServiceName, AwsServiceType, AwsServiceAttributes
from cloudrail.knowledge.context.aws.aws_resource import AwsResource


class RestApiGwDomain(AwsResource):

    def __init__(self,
                 domain_name: str,
                 security_policy: str,
                 account: str,
                 region: str):
        super().__init__(account, region, AwsServiceName.AWS_API_GATEWAY_DOMAIN_NAME,
                         AwsServiceAttributes(aws_service_type=AwsServiceType.APIGATEWAY.value, region=region))
        self.domain_name: str = domain_name
        self.security_policy: str = security_policy
        self.map_data: Optional[RestApiGwMapping] = None

    def get_keys(self) -> List[str]:
        return [self.domain_name, self.account, self.region]

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'API domain'
        else:
            return 'API domains'

    def get_arn(self) -> str:
        pass

    def get_cloud_resource_url(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return True
