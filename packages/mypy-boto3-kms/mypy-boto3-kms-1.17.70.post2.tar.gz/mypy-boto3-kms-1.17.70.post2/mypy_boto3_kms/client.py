"""
Type annotations for kms service client.

[Open documentation](./client.md)

Usage::

    ```python
    import boto3
    from mypy_boto3_kms import KMSClient

    client: KMSClient = boto3.client("kms")
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Type, Union, overload

from botocore.client import ClientMeta

from mypy_boto3_kms.paginator import (
    ListAliasesPaginator,
    ListGrantsPaginator,
    ListKeyPoliciesPaginator,
    ListKeysPaginator,
)

from .literals import (
    AlgorithmSpec,
    CustomerMasterKeySpec,
    DataKeyPairSpec,
    DataKeySpec,
    EncryptionAlgorithmSpec,
    ExpirationModelType,
    GrantOperation,
    KeyUsageType,
    MessageType,
    OriginType,
    SigningAlgorithmSpec,
)
from .type_defs import (
    CancelKeyDeletionResponseTypeDef,
    CreateCustomKeyStoreResponseTypeDef,
    CreateGrantResponseTypeDef,
    CreateKeyResponseTypeDef,
    DecryptResponseTypeDef,
    DescribeCustomKeyStoresResponseTypeDef,
    DescribeKeyResponseTypeDef,
    EncryptResponseTypeDef,
    GenerateDataKeyPairResponseTypeDef,
    GenerateDataKeyPairWithoutPlaintextResponseTypeDef,
    GenerateDataKeyResponseTypeDef,
    GenerateDataKeyWithoutPlaintextResponseTypeDef,
    GenerateRandomResponseTypeDef,
    GetKeyPolicyResponseTypeDef,
    GetKeyRotationStatusResponseTypeDef,
    GetParametersForImportResponseTypeDef,
    GetPublicKeyResponseTypeDef,
    GrantConstraintsTypeDef,
    ListAliasesResponseTypeDef,
    ListGrantsResponseTypeDef,
    ListKeyPoliciesResponseTypeDef,
    ListKeysResponseTypeDef,
    ListResourceTagsResponseTypeDef,
    ReEncryptResponseTypeDef,
    ScheduleKeyDeletionResponseTypeDef,
    SignResponseTypeDef,
    TagTypeDef,
    VerifyResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("KMSClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AlreadyExistsException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    CloudHsmClusterInUseException: Type[BotocoreClientError]
    CloudHsmClusterInvalidConfigurationException: Type[BotocoreClientError]
    CloudHsmClusterNotActiveException: Type[BotocoreClientError]
    CloudHsmClusterNotFoundException: Type[BotocoreClientError]
    CloudHsmClusterNotRelatedException: Type[BotocoreClientError]
    CustomKeyStoreHasCMKsException: Type[BotocoreClientError]
    CustomKeyStoreInvalidStateException: Type[BotocoreClientError]
    CustomKeyStoreNameInUseException: Type[BotocoreClientError]
    CustomKeyStoreNotFoundException: Type[BotocoreClientError]
    DependencyTimeoutException: Type[BotocoreClientError]
    DisabledException: Type[BotocoreClientError]
    ExpiredImportTokenException: Type[BotocoreClientError]
    IncorrectKeyException: Type[BotocoreClientError]
    IncorrectKeyMaterialException: Type[BotocoreClientError]
    IncorrectTrustAnchorException: Type[BotocoreClientError]
    InvalidAliasNameException: Type[BotocoreClientError]
    InvalidArnException: Type[BotocoreClientError]
    InvalidCiphertextException: Type[BotocoreClientError]
    InvalidGrantIdException: Type[BotocoreClientError]
    InvalidGrantTokenException: Type[BotocoreClientError]
    InvalidImportTokenException: Type[BotocoreClientError]
    InvalidKeyUsageException: Type[BotocoreClientError]
    InvalidMarkerException: Type[BotocoreClientError]
    KMSInternalException: Type[BotocoreClientError]
    KMSInvalidSignatureException: Type[BotocoreClientError]
    KMSInvalidStateException: Type[BotocoreClientError]
    KeyUnavailableException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MalformedPolicyDocumentException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    TagException: Type[BotocoreClientError]
    UnsupportedOperationException: Type[BotocoreClientError]


class KMSClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client)
    [Show boto3-stubs documentation](./client.md)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.can_paginate)
        [Show boto3-stubs documentation](./client.md#can-paginate)
        """

    def cancel_key_deletion(self, KeyId: str) -> CancelKeyDeletionResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.cancel_key_deletion)
        [Show boto3-stubs documentation](./client.md#cancel-key-deletion)
        """

    def connect_custom_key_store(self, CustomKeyStoreId: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.connect_custom_key_store)
        [Show boto3-stubs documentation](./client.md#connect-custom-key-store)
        """

    def create_alias(self, AliasName: str, TargetKeyId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.create_alias)
        [Show boto3-stubs documentation](./client.md#create-alias)
        """

    def create_custom_key_store(
        self,
        CustomKeyStoreName: str,
        CloudHsmClusterId: str,
        TrustAnchorCertificate: str,
        KeyStorePassword: str,
    ) -> CreateCustomKeyStoreResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.create_custom_key_store)
        [Show boto3-stubs documentation](./client.md#create-custom-key-store)
        """

    def create_grant(
        self,
        KeyId: str,
        GranteePrincipal: str,
        Operations: List[GrantOperation],
        RetiringPrincipal: str = None,
        Constraints: "GrantConstraintsTypeDef" = None,
        GrantTokens: List[str] = None,
        Name: str = None,
    ) -> CreateGrantResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.create_grant)
        [Show boto3-stubs documentation](./client.md#create-grant)
        """

    def create_key(
        self,
        Policy: str = None,
        Description: str = None,
        KeyUsage: KeyUsageType = None,
        CustomerMasterKeySpec: CustomerMasterKeySpec = None,
        Origin: OriginType = None,
        CustomKeyStoreId: str = None,
        BypassPolicyLockoutSafetyCheck: bool = None,
        Tags: List["TagTypeDef"] = None,
    ) -> CreateKeyResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.create_key)
        [Show boto3-stubs documentation](./client.md#create-key)
        """

    def decrypt(
        self,
        CiphertextBlob: Union[bytes, IO[bytes]],
        EncryptionContext: Dict[str, str] = None,
        GrantTokens: List[str] = None,
        KeyId: str = None,
        EncryptionAlgorithm: EncryptionAlgorithmSpec = None,
    ) -> DecryptResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.decrypt)
        [Show boto3-stubs documentation](./client.md#decrypt)
        """

    def delete_alias(self, AliasName: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.delete_alias)
        [Show boto3-stubs documentation](./client.md#delete-alias)
        """

    def delete_custom_key_store(self, CustomKeyStoreId: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.delete_custom_key_store)
        [Show boto3-stubs documentation](./client.md#delete-custom-key-store)
        """

    def delete_imported_key_material(self, KeyId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.delete_imported_key_material)
        [Show boto3-stubs documentation](./client.md#delete-imported-key-material)
        """

    def describe_custom_key_stores(
        self,
        CustomKeyStoreId: str = None,
        CustomKeyStoreName: str = None,
        Limit: int = None,
        Marker: str = None,
    ) -> DescribeCustomKeyStoresResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.describe_custom_key_stores)
        [Show boto3-stubs documentation](./client.md#describe-custom-key-stores)
        """

    def describe_key(self, KeyId: str, GrantTokens: List[str] = None) -> DescribeKeyResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.describe_key)
        [Show boto3-stubs documentation](./client.md#describe-key)
        """

    def disable_key(self, KeyId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.disable_key)
        [Show boto3-stubs documentation](./client.md#disable-key)
        """

    def disable_key_rotation(self, KeyId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.disable_key_rotation)
        [Show boto3-stubs documentation](./client.md#disable-key-rotation)
        """

    def disconnect_custom_key_store(self, CustomKeyStoreId: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.disconnect_custom_key_store)
        [Show boto3-stubs documentation](./client.md#disconnect-custom-key-store)
        """

    def enable_key(self, KeyId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.enable_key)
        [Show boto3-stubs documentation](./client.md#enable-key)
        """

    def enable_key_rotation(self, KeyId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.enable_key_rotation)
        [Show boto3-stubs documentation](./client.md#enable-key-rotation)
        """

    def encrypt(
        self,
        KeyId: str,
        Plaintext: Union[bytes, IO[bytes]],
        EncryptionContext: Dict[str, str] = None,
        GrantTokens: List[str] = None,
        EncryptionAlgorithm: EncryptionAlgorithmSpec = None,
    ) -> EncryptResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.encrypt)
        [Show boto3-stubs documentation](./client.md#encrypt)
        """

    def generate_data_key(
        self,
        KeyId: str,
        EncryptionContext: Dict[str, str] = None,
        NumberOfBytes: int = None,
        KeySpec: DataKeySpec = None,
        GrantTokens: List[str] = None,
    ) -> GenerateDataKeyResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.generate_data_key)
        [Show boto3-stubs documentation](./client.md#generate-data-key)
        """

    def generate_data_key_pair(
        self,
        KeyId: str,
        KeyPairSpec: DataKeyPairSpec,
        EncryptionContext: Dict[str, str] = None,
        GrantTokens: List[str] = None,
    ) -> GenerateDataKeyPairResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.generate_data_key_pair)
        [Show boto3-stubs documentation](./client.md#generate-data-key-pair)
        """

    def generate_data_key_pair_without_plaintext(
        self,
        KeyId: str,
        KeyPairSpec: DataKeyPairSpec,
        EncryptionContext: Dict[str, str] = None,
        GrantTokens: List[str] = None,
    ) -> GenerateDataKeyPairWithoutPlaintextResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.generate_data_key_pair_without_plaintext)
        [Show boto3-stubs documentation](./client.md#generate-data-key-pair-without-plaintext)
        """

    def generate_data_key_without_plaintext(
        self,
        KeyId: str,
        EncryptionContext: Dict[str, str] = None,
        KeySpec: DataKeySpec = None,
        NumberOfBytes: int = None,
        GrantTokens: List[str] = None,
    ) -> GenerateDataKeyWithoutPlaintextResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.generate_data_key_without_plaintext)
        [Show boto3-stubs documentation](./client.md#generate-data-key-without-plaintext)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.generate_presigned_url)
        [Show boto3-stubs documentation](./client.md#generate-presigned-url)
        """

    def generate_random(
        self, NumberOfBytes: int = None, CustomKeyStoreId: str = None
    ) -> GenerateRandomResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.generate_random)
        [Show boto3-stubs documentation](./client.md#generate-random)
        """

    def get_key_policy(self, KeyId: str, PolicyName: str) -> GetKeyPolicyResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.get_key_policy)
        [Show boto3-stubs documentation](./client.md#get-key-policy)
        """

    def get_key_rotation_status(self, KeyId: str) -> GetKeyRotationStatusResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.get_key_rotation_status)
        [Show boto3-stubs documentation](./client.md#get-key-rotation-status)
        """

    def get_parameters_for_import(
        self, KeyId: str, WrappingAlgorithm: AlgorithmSpec, WrappingKeySpec: Literal["RSA_2048"]
    ) -> GetParametersForImportResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.get_parameters_for_import)
        [Show boto3-stubs documentation](./client.md#get-parameters-for-import)
        """

    def get_public_key(
        self, KeyId: str, GrantTokens: List[str] = None
    ) -> GetPublicKeyResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.get_public_key)
        [Show boto3-stubs documentation](./client.md#get-public-key)
        """

    def import_key_material(
        self,
        KeyId: str,
        ImportToken: Union[bytes, IO[bytes]],
        EncryptedKeyMaterial: Union[bytes, IO[bytes]],
        ValidTo: datetime = None,
        ExpirationModel: ExpirationModelType = None,
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.import_key_material)
        [Show boto3-stubs documentation](./client.md#import-key-material)
        """

    def list_aliases(
        self, KeyId: str = None, Limit: int = None, Marker: str = None
    ) -> ListAliasesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.list_aliases)
        [Show boto3-stubs documentation](./client.md#list-aliases)
        """

    def list_grants(
        self,
        KeyId: str,
        Limit: int = None,
        Marker: str = None,
        GrantId: str = None,
        GranteePrincipal: str = None,
    ) -> ListGrantsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.list_grants)
        [Show boto3-stubs documentation](./client.md#list-grants)
        """

    def list_key_policies(
        self, KeyId: str, Limit: int = None, Marker: str = None
    ) -> ListKeyPoliciesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.list_key_policies)
        [Show boto3-stubs documentation](./client.md#list-key-policies)
        """

    def list_keys(self, Limit: int = None, Marker: str = None) -> ListKeysResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.list_keys)
        [Show boto3-stubs documentation](./client.md#list-keys)
        """

    def list_resource_tags(
        self, KeyId: str, Limit: int = None, Marker: str = None
    ) -> ListResourceTagsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.list_resource_tags)
        [Show boto3-stubs documentation](./client.md#list-resource-tags)
        """

    def list_retirable_grants(
        self, RetiringPrincipal: str, Limit: int = None, Marker: str = None
    ) -> ListGrantsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.list_retirable_grants)
        [Show boto3-stubs documentation](./client.md#list-retirable-grants)
        """

    def put_key_policy(
        self, KeyId: str, PolicyName: str, Policy: str, BypassPolicyLockoutSafetyCheck: bool = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.put_key_policy)
        [Show boto3-stubs documentation](./client.md#put-key-policy)
        """

    def re_encrypt(
        self,
        CiphertextBlob: Union[bytes, IO[bytes]],
        DestinationKeyId: str,
        SourceEncryptionContext: Dict[str, str] = None,
        SourceKeyId: str = None,
        DestinationEncryptionContext: Dict[str, str] = None,
        SourceEncryptionAlgorithm: EncryptionAlgorithmSpec = None,
        DestinationEncryptionAlgorithm: EncryptionAlgorithmSpec = None,
        GrantTokens: List[str] = None,
    ) -> ReEncryptResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.re_encrypt)
        [Show boto3-stubs documentation](./client.md#re-encrypt)
        """

    def retire_grant(self, GrantToken: str = None, KeyId: str = None, GrantId: str = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.retire_grant)
        [Show boto3-stubs documentation](./client.md#retire-grant)
        """

    def revoke_grant(self, KeyId: str, GrantId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.revoke_grant)
        [Show boto3-stubs documentation](./client.md#revoke-grant)
        """

    def schedule_key_deletion(
        self, KeyId: str, PendingWindowInDays: int = None
    ) -> ScheduleKeyDeletionResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.schedule_key_deletion)
        [Show boto3-stubs documentation](./client.md#schedule-key-deletion)
        """

    def sign(
        self,
        KeyId: str,
        Message: Union[bytes, IO[bytes]],
        SigningAlgorithm: SigningAlgorithmSpec,
        MessageType: MessageType = None,
        GrantTokens: List[str] = None,
    ) -> SignResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.sign)
        [Show boto3-stubs documentation](./client.md#sign)
        """

    def tag_resource(self, KeyId: str, Tags: List["TagTypeDef"]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.tag_resource)
        [Show boto3-stubs documentation](./client.md#tag-resource)
        """

    def untag_resource(self, KeyId: str, TagKeys: List[str]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.untag_resource)
        [Show boto3-stubs documentation](./client.md#untag-resource)
        """

    def update_alias(self, AliasName: str, TargetKeyId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.update_alias)
        [Show boto3-stubs documentation](./client.md#update-alias)
        """

    def update_custom_key_store(
        self,
        CustomKeyStoreId: str,
        NewCustomKeyStoreName: str = None,
        KeyStorePassword: str = None,
        CloudHsmClusterId: str = None,
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.update_custom_key_store)
        [Show boto3-stubs documentation](./client.md#update-custom-key-store)
        """

    def update_key_description(self, KeyId: str, Description: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.update_key_description)
        [Show boto3-stubs documentation](./client.md#update-key-description)
        """

    def verify(
        self,
        KeyId: str,
        Message: Union[bytes, IO[bytes]],
        Signature: Union[bytes, IO[bytes]],
        SigningAlgorithm: SigningAlgorithmSpec,
        MessageType: MessageType = None,
        GrantTokens: List[str] = None,
    ) -> VerifyResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Client.verify)
        [Show boto3-stubs documentation](./client.md#verify)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_aliases"]) -> ListAliasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Paginator.ListAliases)[Show boto3-stubs documentation](./paginators.md#listaliasespaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_grants"]) -> ListGrantsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Paginator.ListGrants)[Show boto3-stubs documentation](./paginators.md#listgrantspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_key_policies"]
    ) -> ListKeyPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Paginator.ListKeyPolicies)[Show boto3-stubs documentation](./paginators.md#listkeypoliciespaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_keys"]) -> ListKeysPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/kms.html#KMS.Paginator.ListKeys)[Show boto3-stubs documentation](./paginators.md#listkeyspaginator)
        """
