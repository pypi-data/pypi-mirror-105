"""
Type annotations for cloudformation service ServiceResource

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html)

Usage::

    ```python
    import boto3

    from mypy_boto3_cloudformation import CloudFormationServiceResource
    import mypy_boto3_cloudformation.service_resource as cloudformation_resources

    resource: CloudFormationServiceResource = boto3.resource("cloudformation")

    my_event: cloudformation_resources.Event = resource.Event(...)
    my_stack: cloudformation_resources.Stack = resource.Stack(...)
    my_stack_resource: cloudformation_resources.StackResource = resource.StackResource(...)
    my_stack_resource_summary: cloudformation_resources.StackResourceSummary = resource.StackResourceSummary(...)
```
"""
from datetime import datetime
from typing import Any, Dict, Iterator, List

from boto3.resources.base import ServiceResource as Boto3ServiceResource
from boto3.resources.collection import ResourceCollection

from mypy_boto3_cloudformation.literals import Capability, OnFailure
from mypy_boto3_cloudformation.type_defs import (
    ParameterTypeDef,
    RollbackConfigurationTypeDef,
    TagTypeDef,
    UpdateStackOutputTypeDef,
)

__all__ = (
    "CloudFormationServiceResource",
    "Event",
    "Stack",
    "StackResource",
    "StackResourceSummary",
    "ServiceResourceStacksCollection",
    "StackEventsCollection",
    "StackResourceSummariesCollection",
)


class ServiceResourceStacksCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.ServiceResource.stacks)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html#serviceresourcestackscollection)
    """

    def all(self) -> "ServiceResourceStacksCollection":
        pass

    def filter(  # type: ignore
        self, StackName: str = None, NextToken: str = None
    ) -> "ServiceResourceStacksCollection":
        pass

    def limit(self, count: int) -> "ServiceResourceStacksCollection":
        pass

    def page_size(self, count: int) -> "ServiceResourceStacksCollection":
        pass

    def pages(self) -> Iterator[List["Stack"]]:
        pass

    def __iter__(self) -> Iterator["Stack"]:
        pass


class StackEventsCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.Stack.events)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html#stackeventscollection)
    """

    def all(self) -> "StackEventsCollection":
        pass

    def filter(  # type: ignore
        self, StackName: str = None, NextToken: str = None
    ) -> "StackEventsCollection":
        pass

    def limit(self, count: int) -> "StackEventsCollection":
        pass

    def page_size(self, count: int) -> "StackEventsCollection":
        pass

    def pages(self) -> Iterator[List["Event"]]:
        pass

    def __iter__(self) -> Iterator["Event"]:
        pass


class StackResourceSummariesCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.Stack.resource_summaries)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html#stackresourcesummariescollection)
    """

    def all(self) -> "StackResourceSummariesCollection":
        pass

    def filter(self, NextToken: str = None) -> "StackResourceSummariesCollection":  # type: ignore
        pass

    def limit(self, count: int) -> "StackResourceSummariesCollection":
        pass

    def page_size(self, count: int) -> "StackResourceSummariesCollection":
        pass

    def pages(self) -> Iterator[List["StackResourceSummary"]]:
        pass

    def __iter__(self) -> Iterator["StackResourceSummary"]:
        pass


class Event(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.ServiceResource.Event)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html#event)
    """

    stack_id: str
    event_id: str
    stack_name: str
    logical_resource_id: str
    physical_resource_id: str
    resource_type: str
    timestamp: datetime
    resource_status: str
    resource_status_reason: str
    resource_properties: str
    client_request_token: str
    id: str

    def get_available_subresources(self) -> List[str]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.Event.get_available_subresources)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html#eventget-available-subresourcesmethod)
        """


_Event = Event


class Stack(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.ServiceResource.Stack)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html#stack)
    """

    stack_id: str
    stack_name: str
    change_set_id: str
    description: str
    parameters: List[Any]
    creation_time: datetime
    deletion_time: datetime
    last_updated_time: datetime
    rollback_configuration: Dict[str, Any]
    stack_status: str
    stack_status_reason: str
    disable_rollback: bool
    notification_arns: List[Any]
    timeout_in_minutes: int
    capabilities: List[Any]
    outputs: List[Any]
    role_arn: str
    tags: List[Any]
    enable_termination_protection: bool
    parent_id: str
    root_id: str
    drift_information: Dict[str, Any]
    name: str
    events: StackEventsCollection
    resource_summaries: StackResourceSummariesCollection

    def Resource(self, logical_id: str) -> "_StackResource":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.Stack.Resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html#stackresourcemethod)
        """

    def cancel_update(self, ClientRequestToken: str = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.Stack.cancel_update)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html#stackcancel-updatemethod)
        """

    def delete(
        self, RetainResources: List[str] = None, RoleARN: str = None, ClientRequestToken: str = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.Stack.delete)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html#stackdeletemethod)
        """

    def get_available_subresources(self) -> List[str]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.Stack.get_available_subresources)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html#stackget-available-subresourcesmethod)
        """

    def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.Stack.load)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html#stackloadmethod)
        """

    def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.Stack.reload)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html#stackreloadmethod)
        """

    def update(
        self,
        TemplateBody: str = None,
        TemplateURL: str = None,
        UsePreviousTemplate: bool = None,
        StackPolicyDuringUpdateBody: str = None,
        StackPolicyDuringUpdateURL: str = None,
        Parameters: List["ParameterTypeDef"] = None,
        Capabilities: List[Capability] = None,
        ResourceTypes: List[str] = None,
        RoleARN: str = None,
        RollbackConfiguration: "RollbackConfigurationTypeDef" = None,
        StackPolicyBody: str = None,
        StackPolicyURL: str = None,
        NotificationARNs: List[str] = None,
        Tags: List["TagTypeDef"] = None,
        ClientRequestToken: str = None,
    ) -> UpdateStackOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.Stack.update)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html#stackupdatemethod)
        """


_Stack = Stack


class StackResource(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.ServiceResource.StackResource)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html#stackresource)
    """

    stack_id: str
    logical_resource_id: str
    physical_resource_id: str
    resource_type: str
    last_updated_timestamp: datetime
    resource_status: str
    resource_status_reason: str
    description: str
    metadata: str
    drift_information: Dict[str, Any]
    module_info: Dict[str, Any]
    stack_name: str
    logical_id: str

    def Stack(self) -> _Stack:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.StackResource.Stack)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html#stackresourcestackmethod)
        """

    def get_available_subresources(self) -> List[str]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.StackResource.get_available_subresources)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html#stackresourceget-available-subresourcesmethod)
        """

    def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.StackResource.load)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html#stackresourceloadmethod)
        """

    def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.StackResource.reload)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html#stackresourcereloadmethod)
        """


_StackResource = StackResource


class StackResourceSummary(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.ServiceResource.StackResourceSummary)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html#stackresourcesummary)
    """

    logical_resource_id: str
    physical_resource_id: str
    resource_type: str
    last_updated_timestamp: datetime
    resource_status: str
    resource_status_reason: str
    drift_information: Dict[str, Any]
    module_info: Dict[str, Any]
    stack_name: str
    logical_id: str

    def Resource(self) -> _StackResource:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.StackResourceSummary.Resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html#stackresourcesummaryresourcemethod)
        """

    def get_available_subresources(self) -> List[str]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.StackResourceSummary.get_available_subresources)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html#stackresourcesummaryget-available-subresourcesmethod)
        """


_StackResourceSummary = StackResourceSummary


class CloudFormationServiceResource(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.ServiceResource)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html)
    """

    stacks: ServiceResourceStacksCollection

    def Event(self, id: str) -> _Event:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.ServiceResource.Event)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html#cloudformationserviceresourceeventmethod)
        """

    def Stack(self, name: str) -> _Stack:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.ServiceResource.Stack)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html#cloudformationserviceresourcestackmethod)
        """

    def StackResource(self, stack_name: str, logical_id: str) -> _StackResource:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.ServiceResource.StackResource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html#cloudformationserviceresourcestackresourcemethod)
        """

    def StackResourceSummary(self, stack_name: str, logical_id: str) -> _StackResourceSummary:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.ServiceResource.StackResourceSummary)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html#cloudformationserviceresourcestackresourcesummarymethod)
        """

    def create_stack(
        self,
        StackName: str,
        TemplateBody: str = None,
        TemplateURL: str = None,
        Parameters: List["ParameterTypeDef"] = None,
        DisableRollback: bool = None,
        RollbackConfiguration: "RollbackConfigurationTypeDef" = None,
        TimeoutInMinutes: int = None,
        NotificationARNs: List[str] = None,
        Capabilities: List[Capability] = None,
        ResourceTypes: List[str] = None,
        RoleARN: str = None,
        OnFailure: OnFailure = None,
        StackPolicyBody: str = None,
        StackPolicyURL: str = None,
        Tags: List["TagTypeDef"] = None,
        ClientRequestToken: str = None,
        EnableTerminationProtection: bool = None,
    ) -> _Stack:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.ServiceResource.create_stack)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html#cloudformationserviceresourcecreate-stackmethod)
        """

    def get_available_subresources(self) -> List[str]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/cloudformation.html#CloudFormation.ServiceResource.get_available_subresources)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudformation/service_resource.html#cloudformationserviceresourceget-available-subresourcesmethod)
        """
