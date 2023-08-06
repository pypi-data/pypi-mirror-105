"""
Type annotations for network-firewall service client.

[Open documentation](./client.md)

Usage::

    ```python
    import boto3
    from mypy_boto3_network_firewall import NetworkFirewallClient

    client: NetworkFirewallClient = boto3.client("network-firewall")
    ```
"""
import sys
from typing import Any, Dict, List, Type, overload

from botocore.client import ClientMeta

from mypy_boto3_network_firewall.paginator import (
    ListFirewallPoliciesPaginator,
    ListFirewallsPaginator,
    ListRuleGroupsPaginator,
    ListTagsForResourcePaginator,
)

from .literals import RuleGroupType
from .type_defs import (
    AssociateFirewallPolicyResponseTypeDef,
    AssociateSubnetsResponseTypeDef,
    CreateFirewallPolicyResponseTypeDef,
    CreateFirewallResponseTypeDef,
    CreateRuleGroupResponseTypeDef,
    DeleteFirewallPolicyResponseTypeDef,
    DeleteFirewallResponseTypeDef,
    DeleteRuleGroupResponseTypeDef,
    DescribeFirewallPolicyResponseTypeDef,
    DescribeFirewallResponseTypeDef,
    DescribeLoggingConfigurationResponseTypeDef,
    DescribeResourcePolicyResponseTypeDef,
    DescribeRuleGroupResponseTypeDef,
    DisassociateSubnetsResponseTypeDef,
    FirewallPolicyTypeDef,
    ListFirewallPoliciesResponseTypeDef,
    ListFirewallsResponseTypeDef,
    ListRuleGroupsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    LoggingConfigurationTypeDef,
    RuleGroupTypeDef,
    SubnetMappingTypeDef,
    TagTypeDef,
    UpdateFirewallDeleteProtectionResponseTypeDef,
    UpdateFirewallDescriptionResponseTypeDef,
    UpdateFirewallPolicyChangeProtectionResponseTypeDef,
    UpdateFirewallPolicyResponseTypeDef,
    UpdateLoggingConfigurationResponseTypeDef,
    UpdateRuleGroupResponseTypeDef,
    UpdateSubnetChangeProtectionResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("NetworkFirewallClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InsufficientCapacityException: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]
    InvalidOperationException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    InvalidResourcePolicyException: Type[BotocoreClientError]
    InvalidTokenException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    LogDestinationPermissionException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceOwnerCheckException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnsupportedOperationException: Type[BotocoreClientError]


class NetworkFirewallClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client)
    [Show boto3-stubs documentation](./client.md)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def associate_firewall_policy(
        self,
        FirewallPolicyArn: str,
        UpdateToken: str = None,
        FirewallArn: str = None,
        FirewallName: str = None,
    ) -> AssociateFirewallPolicyResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.associate_firewall_policy)
        [Show boto3-stubs documentation](./client.md#associate-firewall-policy)
        """

    def associate_subnets(
        self,
        SubnetMappings: List["SubnetMappingTypeDef"],
        UpdateToken: str = None,
        FirewallArn: str = None,
        FirewallName: str = None,
    ) -> AssociateSubnetsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.associate_subnets)
        [Show boto3-stubs documentation](./client.md#associate-subnets)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.can_paginate)
        [Show boto3-stubs documentation](./client.md#can-paginate)
        """

    def create_firewall(
        self,
        FirewallName: str,
        FirewallPolicyArn: str,
        VpcId: str,
        SubnetMappings: List["SubnetMappingTypeDef"],
        DeleteProtection: bool = None,
        SubnetChangeProtection: bool = None,
        FirewallPolicyChangeProtection: bool = None,
        Description: str = None,
        Tags: List["TagTypeDef"] = None,
    ) -> CreateFirewallResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.create_firewall)
        [Show boto3-stubs documentation](./client.md#create-firewall)
        """

    def create_firewall_policy(
        self,
        FirewallPolicyName: str,
        FirewallPolicy: "FirewallPolicyTypeDef",
        Description: str = None,
        Tags: List["TagTypeDef"] = None,
        DryRun: bool = None,
    ) -> CreateFirewallPolicyResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.create_firewall_policy)
        [Show boto3-stubs documentation](./client.md#create-firewall-policy)
        """

    def create_rule_group(
        self,
        RuleGroupName: str,
        Type: RuleGroupType,
        Capacity: int,
        RuleGroup: "RuleGroupTypeDef" = None,
        Rules: str = None,
        Description: str = None,
        Tags: List["TagTypeDef"] = None,
        DryRun: bool = None,
    ) -> CreateRuleGroupResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.create_rule_group)
        [Show boto3-stubs documentation](./client.md#create-rule-group)
        """

    def delete_firewall(
        self, FirewallName: str = None, FirewallArn: str = None
    ) -> DeleteFirewallResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.delete_firewall)
        [Show boto3-stubs documentation](./client.md#delete-firewall)
        """

    def delete_firewall_policy(
        self, FirewallPolicyName: str = None, FirewallPolicyArn: str = None
    ) -> DeleteFirewallPolicyResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.delete_firewall_policy)
        [Show boto3-stubs documentation](./client.md#delete-firewall-policy)
        """

    def delete_resource_policy(self, ResourceArn: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.delete_resource_policy)
        [Show boto3-stubs documentation](./client.md#delete-resource-policy)
        """

    def delete_rule_group(
        self, RuleGroupName: str = None, RuleGroupArn: str = None, Type: RuleGroupType = None
    ) -> DeleteRuleGroupResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.delete_rule_group)
        [Show boto3-stubs documentation](./client.md#delete-rule-group)
        """

    def describe_firewall(
        self, FirewallName: str = None, FirewallArn: str = None
    ) -> DescribeFirewallResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.describe_firewall)
        [Show boto3-stubs documentation](./client.md#describe-firewall)
        """

    def describe_firewall_policy(
        self, FirewallPolicyName: str = None, FirewallPolicyArn: str = None
    ) -> DescribeFirewallPolicyResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.describe_firewall_policy)
        [Show boto3-stubs documentation](./client.md#describe-firewall-policy)
        """

    def describe_logging_configuration(
        self, FirewallArn: str = None, FirewallName: str = None
    ) -> DescribeLoggingConfigurationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.describe_logging_configuration)
        [Show boto3-stubs documentation](./client.md#describe-logging-configuration)
        """

    def describe_resource_policy(self, ResourceArn: str) -> DescribeResourcePolicyResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.describe_resource_policy)
        [Show boto3-stubs documentation](./client.md#describe-resource-policy)
        """

    def describe_rule_group(
        self, RuleGroupName: str = None, RuleGroupArn: str = None, Type: RuleGroupType = None
    ) -> DescribeRuleGroupResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.describe_rule_group)
        [Show boto3-stubs documentation](./client.md#describe-rule-group)
        """

    def disassociate_subnets(
        self,
        SubnetIds: List[str],
        UpdateToken: str = None,
        FirewallArn: str = None,
        FirewallName: str = None,
    ) -> DisassociateSubnetsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.disassociate_subnets)
        [Show boto3-stubs documentation](./client.md#disassociate-subnets)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.generate_presigned_url)
        [Show boto3-stubs documentation](./client.md#generate-presigned-url)
        """

    def list_firewall_policies(
        self, NextToken: str = None, MaxResults: int = None
    ) -> ListFirewallPoliciesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.list_firewall_policies)
        [Show boto3-stubs documentation](./client.md#list-firewall-policies)
        """

    def list_firewalls(
        self, NextToken: str = None, VpcIds: List[str] = None, MaxResults: int = None
    ) -> ListFirewallsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.list_firewalls)
        [Show boto3-stubs documentation](./client.md#list-firewalls)
        """

    def list_rule_groups(
        self, NextToken: str = None, MaxResults: int = None
    ) -> ListRuleGroupsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.list_rule_groups)
        [Show boto3-stubs documentation](./client.md#list-rule-groups)
        """

    def list_tags_for_resource(
        self, ResourceArn: str, NextToken: str = None, MaxResults: int = None
    ) -> ListTagsForResourceResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](./client.md#list-tags-for-resource)
        """

    def put_resource_policy(self, ResourceArn: str, Policy: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.put_resource_policy)
        [Show boto3-stubs documentation](./client.md#put-resource-policy)
        """

    def tag_resource(self, ResourceArn: str, Tags: List["TagTypeDef"]) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.tag_resource)
        [Show boto3-stubs documentation](./client.md#tag-resource)
        """

    def untag_resource(self, ResourceArn: str, TagKeys: List[str]) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.untag_resource)
        [Show boto3-stubs documentation](./client.md#untag-resource)
        """

    def update_firewall_delete_protection(
        self,
        DeleteProtection: bool,
        UpdateToken: str = None,
        FirewallArn: str = None,
        FirewallName: str = None,
    ) -> UpdateFirewallDeleteProtectionResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.update_firewall_delete_protection)
        [Show boto3-stubs documentation](./client.md#update-firewall-delete-protection)
        """

    def update_firewall_description(
        self,
        UpdateToken: str = None,
        FirewallArn: str = None,
        FirewallName: str = None,
        Description: str = None,
    ) -> UpdateFirewallDescriptionResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.update_firewall_description)
        [Show boto3-stubs documentation](./client.md#update-firewall-description)
        """

    def update_firewall_policy(
        self,
        UpdateToken: str,
        FirewallPolicy: "FirewallPolicyTypeDef",
        FirewallPolicyArn: str = None,
        FirewallPolicyName: str = None,
        Description: str = None,
        DryRun: bool = None,
    ) -> UpdateFirewallPolicyResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.update_firewall_policy)
        [Show boto3-stubs documentation](./client.md#update-firewall-policy)
        """

    def update_firewall_policy_change_protection(
        self,
        FirewallPolicyChangeProtection: bool,
        UpdateToken: str = None,
        FirewallArn: str = None,
        FirewallName: str = None,
    ) -> UpdateFirewallPolicyChangeProtectionResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.update_firewall_policy_change_protection)
        [Show boto3-stubs documentation](./client.md#update-firewall-policy-change-protection)
        """

    def update_logging_configuration(
        self,
        FirewallArn: str = None,
        FirewallName: str = None,
        LoggingConfiguration: "LoggingConfigurationTypeDef" = None,
    ) -> UpdateLoggingConfigurationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.update_logging_configuration)
        [Show boto3-stubs documentation](./client.md#update-logging-configuration)
        """

    def update_rule_group(
        self,
        UpdateToken: str,
        RuleGroupArn: str = None,
        RuleGroupName: str = None,
        RuleGroup: "RuleGroupTypeDef" = None,
        Rules: str = None,
        Type: RuleGroupType = None,
        Description: str = None,
        DryRun: bool = None,
    ) -> UpdateRuleGroupResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.update_rule_group)
        [Show boto3-stubs documentation](./client.md#update-rule-group)
        """

    def update_subnet_change_protection(
        self,
        SubnetChangeProtection: bool,
        UpdateToken: str = None,
        FirewallArn: str = None,
        FirewallName: str = None,
    ) -> UpdateSubnetChangeProtectionResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Client.update_subnet_change_protection)
        [Show boto3-stubs documentation](./client.md#update-subnet-change-protection)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_firewall_policies"]
    ) -> ListFirewallPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Paginator.ListFirewallPolicies)[Show boto3-stubs documentation](./paginators.md#listfirewallpoliciespaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_firewalls"]) -> ListFirewallsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Paginator.ListFirewalls)[Show boto3-stubs documentation](./paginators.md#listfirewallspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_rule_groups"]) -> ListRuleGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Paginator.ListRuleGroups)[Show boto3-stubs documentation](./paginators.md#listrulegroupspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/network-firewall.html#NetworkFirewall.Paginator.ListTagsForResource)[Show boto3-stubs documentation](./paginators.md#listtagsforresourcepaginator)
        """
