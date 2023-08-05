"""
Type annotations for elb service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html)

Usage::

    ```python
    import boto3
    from mypy_boto3_elb import ElasticLoadBalancingClient

    client: ElasticLoadBalancingClient = boto3.client("elb")
    ```
"""
import sys
from typing import Any, Dict, List, Type, overload

from botocore.client import ClientMeta

from mypy_boto3_elb.paginator import DescribeAccountLimitsPaginator, DescribeLoadBalancersPaginator
from mypy_boto3_elb.type_defs import (
    AddAvailabilityZonesOutputTypeDef,
    ApplySecurityGroupsToLoadBalancerOutputTypeDef,
    AttachLoadBalancerToSubnetsOutputTypeDef,
    ConfigureHealthCheckOutputTypeDef,
    CreateAccessPointOutputTypeDef,
    DeregisterEndPointsOutputTypeDef,
    DescribeAccessPointsOutputTypeDef,
    DescribeAccountLimitsOutputTypeDef,
    DescribeEndPointStateOutputTypeDef,
    DescribeLoadBalancerAttributesOutputTypeDef,
    DescribeLoadBalancerPoliciesOutputTypeDef,
    DescribeLoadBalancerPolicyTypesOutputTypeDef,
    DescribeTagsOutputTypeDef,
    DetachLoadBalancerFromSubnetsOutputTypeDef,
    HealthCheckTypeDef,
    InstanceTypeDef,
    ListenerTypeDef,
    LoadBalancerAttributesTypeDef,
    ModifyLoadBalancerAttributesOutputTypeDef,
    PolicyAttributeTypeDef,
    RegisterEndPointsOutputTypeDef,
    RemoveAvailabilityZonesOutputTypeDef,
    TagKeyOnlyTypeDef,
    TagTypeDef,
)
from mypy_boto3_elb.waiter import (
    AnyInstanceInServiceWaiter,
    InstanceDeregisteredWaiter,
    InstanceInServiceWaiter,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ElasticLoadBalancingClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessPointNotFoundException: Type[BotocoreClientError]
    CertificateNotFoundException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DependencyThrottleException: Type[BotocoreClientError]
    DuplicateAccessPointNameException: Type[BotocoreClientError]
    DuplicateListenerException: Type[BotocoreClientError]
    DuplicatePolicyNameException: Type[BotocoreClientError]
    DuplicateTagKeysException: Type[BotocoreClientError]
    InvalidConfigurationRequestException: Type[BotocoreClientError]
    InvalidEndPointException: Type[BotocoreClientError]
    InvalidSchemeException: Type[BotocoreClientError]
    InvalidSecurityGroupException: Type[BotocoreClientError]
    InvalidSubnetException: Type[BotocoreClientError]
    ListenerNotFoundException: Type[BotocoreClientError]
    LoadBalancerAttributeNotFoundException: Type[BotocoreClientError]
    OperationNotPermittedException: Type[BotocoreClientError]
    PolicyNotFoundException: Type[BotocoreClientError]
    PolicyTypeNotFoundException: Type[BotocoreClientError]
    SubnetNotFoundException: Type[BotocoreClientError]
    TooManyAccessPointsException: Type[BotocoreClientError]
    TooManyPoliciesException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    UnsupportedProtocolException: Type[BotocoreClientError]


class ElasticLoadBalancingClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def add_tags(self, LoadBalancerNames: List[str], Tags: List["TagTypeDef"]) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.add_tags)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#add-tags)
        """

    def apply_security_groups_to_load_balancer(
        self, LoadBalancerName: str, SecurityGroups: List[str]
    ) -> ApplySecurityGroupsToLoadBalancerOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.apply_security_groups_to_load_balancer)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#apply-security-groups-to-load-balancer)
        """

    def attach_load_balancer_to_subnets(
        self, LoadBalancerName: str, Subnets: List[str]
    ) -> AttachLoadBalancerToSubnetsOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.attach_load_balancer_to_subnets)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#attach-load-balancer-to-subnets)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#can-paginate)
        """

    def configure_health_check(
        self, LoadBalancerName: str, HealthCheck: "HealthCheckTypeDef"
    ) -> ConfigureHealthCheckOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.configure_health_check)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#configure-health-check)
        """

    def create_app_cookie_stickiness_policy(
        self, LoadBalancerName: str, PolicyName: str, CookieName: str
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.create_app_cookie_stickiness_policy)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#create-app-cookie-stickiness-policy)
        """

    def create_lb_cookie_stickiness_policy(
        self, LoadBalancerName: str, PolicyName: str, CookieExpirationPeriod: int = None
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.create_lb_cookie_stickiness_policy)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#create-lb-cookie-stickiness-policy)
        """

    def create_load_balancer(
        self,
        LoadBalancerName: str,
        Listeners: List["ListenerTypeDef"],
        AvailabilityZones: List[str] = None,
        Subnets: List[str] = None,
        SecurityGroups: List[str] = None,
        Scheme: str = None,
        Tags: List["TagTypeDef"] = None,
    ) -> CreateAccessPointOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.create_load_balancer)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#create-load-balancer)
        """

    def create_load_balancer_listeners(
        self, LoadBalancerName: str, Listeners: List["ListenerTypeDef"]
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.create_load_balancer_listeners)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#create-load-balancer-listeners)
        """

    def create_load_balancer_policy(
        self,
        LoadBalancerName: str,
        PolicyName: str,
        PolicyTypeName: str,
        PolicyAttributes: List[PolicyAttributeTypeDef] = None,
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.create_load_balancer_policy)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#create-load-balancer-policy)
        """

    def delete_load_balancer(self, LoadBalancerName: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.delete_load_balancer)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#delete-load-balancer)
        """

    def delete_load_balancer_listeners(
        self, LoadBalancerName: str, LoadBalancerPorts: List[int]
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.delete_load_balancer_listeners)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#delete-load-balancer-listeners)
        """

    def delete_load_balancer_policy(self, LoadBalancerName: str, PolicyName: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.delete_load_balancer_policy)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#delete-load-balancer-policy)
        """

    def deregister_instances_from_load_balancer(
        self, LoadBalancerName: str, Instances: List["InstanceTypeDef"]
    ) -> DeregisterEndPointsOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.deregister_instances_from_load_balancer)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#deregister-instances-from-load-balancer)
        """

    def describe_account_limits(
        self, Marker: str = None, PageSize: int = None
    ) -> DescribeAccountLimitsOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.describe_account_limits)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#describe-account-limits)
        """

    def describe_instance_health(
        self, LoadBalancerName: str, Instances: List["InstanceTypeDef"] = None
    ) -> DescribeEndPointStateOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.describe_instance_health)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#describe-instance-health)
        """

    def describe_load_balancer_attributes(
        self, LoadBalancerName: str
    ) -> DescribeLoadBalancerAttributesOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.describe_load_balancer_attributes)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#describe-load-balancer-attributes)
        """

    def describe_load_balancer_policies(
        self, LoadBalancerName: str = None, PolicyNames: List[str] = None
    ) -> DescribeLoadBalancerPoliciesOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.describe_load_balancer_policies)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#describe-load-balancer-policies)
        """

    def describe_load_balancer_policy_types(
        self, PolicyTypeNames: List[str] = None
    ) -> DescribeLoadBalancerPolicyTypesOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.describe_load_balancer_policy_types)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#describe-load-balancer-policy-types)
        """

    def describe_load_balancers(
        self, LoadBalancerNames: List[str] = None, Marker: str = None, PageSize: int = None
    ) -> DescribeAccessPointsOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.describe_load_balancers)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#describe-load-balancers)
        """

    def describe_tags(self, LoadBalancerNames: List[str]) -> DescribeTagsOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.describe_tags)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#describe-tags)
        """

    def detach_load_balancer_from_subnets(
        self, LoadBalancerName: str, Subnets: List[str]
    ) -> DetachLoadBalancerFromSubnetsOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.detach_load_balancer_from_subnets)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#detach-load-balancer-from-subnets)
        """

    def disable_availability_zones_for_load_balancer(
        self, LoadBalancerName: str, AvailabilityZones: List[str]
    ) -> RemoveAvailabilityZonesOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.disable_availability_zones_for_load_balancer)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#disable-availability-zones-for-load-balancer)
        """

    def enable_availability_zones_for_load_balancer(
        self, LoadBalancerName: str, AvailabilityZones: List[str]
    ) -> AddAvailabilityZonesOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.enable_availability_zones_for_load_balancer)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#enable-availability-zones-for-load-balancer)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#generate-presigned-url)
        """

    def modify_load_balancer_attributes(
        self, LoadBalancerName: str, LoadBalancerAttributes: "LoadBalancerAttributesTypeDef"
    ) -> ModifyLoadBalancerAttributesOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.modify_load_balancer_attributes)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#modify-load-balancer-attributes)
        """

    def register_instances_with_load_balancer(
        self, LoadBalancerName: str, Instances: List["InstanceTypeDef"]
    ) -> RegisterEndPointsOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.register_instances_with_load_balancer)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#register-instances-with-load-balancer)
        """

    def remove_tags(
        self, LoadBalancerNames: List[str], Tags: List[TagKeyOnlyTypeDef]
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.remove_tags)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#remove-tags)
        """

    def set_load_balancer_listener_ssl_certificate(
        self, LoadBalancerName: str, LoadBalancerPort: int, SSLCertificateId: str
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.set_load_balancer_listener_ssl_certificate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#set-load-balancer-listener-ssl-certificate)
        """

    def set_load_balancer_policies_for_backend_server(
        self, LoadBalancerName: str, InstancePort: int, PolicyNames: List[str]
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.set_load_balancer_policies_for_backend_server)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#set-load-balancer-policies-for-backend-server)
        """

    def set_load_balancer_policies_of_listener(
        self, LoadBalancerName: str, LoadBalancerPort: int, PolicyNames: List[str]
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Client.set_load_balancer_policies_of_listener)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/client.html#set-load-balancer-policies-of-listener)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_account_limits"]
    ) -> DescribeAccountLimitsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Paginator.DescribeAccountLimits)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/paginators.html#describeaccountlimitspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_load_balancers"]
    ) -> DescribeLoadBalancersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Paginator.DescribeLoadBalancers)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/paginators.html#describeloadbalancerspaginator)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["any_instance_in_service"]
    ) -> AnyInstanceInServiceWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Waiter.any_instance_in_service)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/waiters.html#anyinstanceinservicewaiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["instance_deregistered"]
    ) -> InstanceDeregisteredWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Waiter.instance_deregistered)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/waiters.html#instancederegisteredwaiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["instance_in_service"]) -> InstanceInServiceWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/elb.html#ElasticLoadBalancing.Waiter.instance_in_service)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_elb/waiters.html#instanceinservicewaiter)
        """
