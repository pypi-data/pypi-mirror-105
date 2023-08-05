"""
Type annotations for appintegrations service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/client.html)

Usage::

    ```python
    import boto3
    from mypy_boto3_appintegrations import AppIntegrationsServiceClient

    client: AppIntegrationsServiceClient = boto3.client("appintegrations")
    ```
"""
from typing import Any, Dict, List, Type

from botocore.client import ClientMeta

from mypy_boto3_appintegrations.type_defs import (
    CreateEventIntegrationResponseTypeDef,
    EventFilterTypeDef,
    GetEventIntegrationResponseTypeDef,
    ListEventIntegrationAssociationsResponseTypeDef,
    ListEventIntegrationsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
)

__all__ = ("AppIntegrationsServiceClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str
    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DuplicateResourceException: Type[BotocoreClientError]
    InternalServiceError: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]

class AppIntegrationsServiceClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/appintegrations.html#AppIntegrationsService.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/client.html)
    """

    meta: ClientMeta
    exceptions: Exceptions
    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/appintegrations.html#AppIntegrationsService.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/client.html#can-paginate)
        """
    def create_event_integration(
        self,
        Name: str,
        EventFilter: "EventFilterTypeDef",
        EventBridgeBus: str,
        Description: str = None,
        ClientToken: str = None,
        Tags: Dict[str, str] = None,
    ) -> CreateEventIntegrationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/appintegrations.html#AppIntegrationsService.Client.create_event_integration)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/client.html#create-event-integration)
        """
    def delete_event_integration(self, Name: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/appintegrations.html#AppIntegrationsService.Client.delete_event_integration)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/client.html#delete-event-integration)
        """
    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/appintegrations.html#AppIntegrationsService.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/client.html#generate-presigned-url)
        """
    def get_event_integration(self, Name: str) -> GetEventIntegrationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/appintegrations.html#AppIntegrationsService.Client.get_event_integration)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/client.html#get-event-integration)
        """
    def list_event_integration_associations(
        self, EventIntegrationName: str, NextToken: str = None, MaxResults: int = None
    ) -> ListEventIntegrationAssociationsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/appintegrations.html#AppIntegrationsService.Client.list_event_integration_associations)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/client.html#list-event-integration-associations)
        """
    def list_event_integrations(
        self, NextToken: str = None, MaxResults: int = None
    ) -> ListEventIntegrationsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/appintegrations.html#AppIntegrationsService.Client.list_event_integrations)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/client.html#list-event-integrations)
        """
    def list_tags_for_resource(self, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/appintegrations.html#AppIntegrationsService.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/client.html#list-tags-for-resource)
        """
    def tag_resource(self, resourceArn: str, tags: Dict[str, str]) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/appintegrations.html#AppIntegrationsService.Client.tag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/client.html#tag-resource)
        """
    def untag_resource(self, resourceArn: str, tagKeys: List[str]) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/appintegrations.html#AppIntegrationsService.Client.untag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/client.html#untag-resource)
        """
    def update_event_integration(self, Name: str, Description: str = None) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/appintegrations.html#AppIntegrationsService.Client.update_event_integration)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/client.html#update-event-integration)
        """
