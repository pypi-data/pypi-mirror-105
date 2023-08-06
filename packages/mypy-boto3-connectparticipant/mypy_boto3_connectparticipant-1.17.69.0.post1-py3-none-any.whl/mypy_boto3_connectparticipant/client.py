"""
Type annotations for connectparticipant service client.

[Open documentation](./client.md)

Usage::

    ```python
    import boto3
    from mypy_boto3_connectparticipant import ConnectParticipantClient

    client: ConnectParticipantClient = boto3.client("connectparticipant")
    ```
"""
from typing import Any, Dict, List, Type

from botocore.client import ClientMeta

from .literals import ConnectionType, ScanDirection, SortKey
from .type_defs import (
    CreateParticipantConnectionResponseTypeDef,
    GetAttachmentResponseTypeDef,
    GetTranscriptResponseTypeDef,
    SendEventResponseTypeDef,
    SendMessageResponseTypeDef,
    StartAttachmentUploadResponseTypeDef,
    StartPositionTypeDef,
)

__all__ = ("ConnectParticipantClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ConnectParticipantClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/connectparticipant.html#ConnectParticipant.Client)
    [Show boto3-stubs documentation](./client.md)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/connectparticipant.html#ConnectParticipant.Client.can_paginate)
        [Show boto3-stubs documentation](./client.md#can-paginate)
        """

    def complete_attachment_upload(
        self, AttachmentIds: List[str], ClientToken: str, ConnectionToken: str
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/connectparticipant.html#ConnectParticipant.Client.complete_attachment_upload)
        [Show boto3-stubs documentation](./client.md#complete-attachment-upload)
        """

    def create_participant_connection(
        self, Type: List[ConnectionType], ParticipantToken: str
    ) -> CreateParticipantConnectionResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/connectparticipant.html#ConnectParticipant.Client.create_participant_connection)
        [Show boto3-stubs documentation](./client.md#create-participant-connection)
        """

    def disconnect_participant(
        self, ConnectionToken: str, ClientToken: str = None
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/connectparticipant.html#ConnectParticipant.Client.disconnect_participant)
        [Show boto3-stubs documentation](./client.md#disconnect-participant)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/connectparticipant.html#ConnectParticipant.Client.generate_presigned_url)
        [Show boto3-stubs documentation](./client.md#generate-presigned-url)
        """

    def get_attachment(
        self, AttachmentId: str, ConnectionToken: str
    ) -> GetAttachmentResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/connectparticipant.html#ConnectParticipant.Client.get_attachment)
        [Show boto3-stubs documentation](./client.md#get-attachment)
        """

    def get_transcript(
        self,
        ConnectionToken: str,
        ContactId: str = None,
        MaxResults: int = None,
        NextToken: str = None,
        ScanDirection: ScanDirection = None,
        SortOrder: SortKey = None,
        StartPosition: StartPositionTypeDef = None,
    ) -> GetTranscriptResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/connectparticipant.html#ConnectParticipant.Client.get_transcript)
        [Show boto3-stubs documentation](./client.md#get-transcript)
        """

    def send_event(
        self, ContentType: str, ConnectionToken: str, Content: str = None, ClientToken: str = None
    ) -> SendEventResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/connectparticipant.html#ConnectParticipant.Client.send_event)
        [Show boto3-stubs documentation](./client.md#send-event)
        """

    def send_message(
        self, ContentType: str, Content: str, ConnectionToken: str, ClientToken: str = None
    ) -> SendMessageResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/connectparticipant.html#ConnectParticipant.Client.send_message)
        [Show boto3-stubs documentation](./client.md#send-message)
        """

    def start_attachment_upload(
        self,
        ContentType: str,
        AttachmentSizeInBytes: int,
        AttachmentName: str,
        ClientToken: str,
        ConnectionToken: str,
    ) -> StartAttachmentUploadResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/connectparticipant.html#ConnectParticipant.Client.start_attachment_upload)
        [Show boto3-stubs documentation](./client.md#start-attachment-upload)
        """
