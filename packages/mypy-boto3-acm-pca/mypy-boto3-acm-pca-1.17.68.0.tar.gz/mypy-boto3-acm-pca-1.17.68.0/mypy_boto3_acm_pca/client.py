"""
Type annotations for acm-pca service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/client.html)

Usage::

    ```python
    import boto3
    from mypy_boto3_acm_pca import ACMPCAClient

    client: ACMPCAClient = boto3.client("acm-pca")
    ```
"""
import sys
from typing import IO, Any, Dict, List, Type, Union, overload

from botocore.client import ClientMeta

from mypy_boto3_acm_pca.literals import (
    ActionType,
    AuditReportResponseFormat,
    CertificateAuthorityStatus,
    CertificateAuthorityType,
    KeyStorageSecurityStandard,
    ResourceOwner,
    RevocationReason,
    SigningAlgorithm,
)
from mypy_boto3_acm_pca.paginator import (
    ListCertificateAuthoritiesPaginator,
    ListPermissionsPaginator,
    ListTagsPaginator,
)
from mypy_boto3_acm_pca.type_defs import (
    ApiPassthroughTypeDef,
    CertificateAuthorityConfigurationTypeDef,
    CreateCertificateAuthorityAuditReportResponseTypeDef,
    CreateCertificateAuthorityResponseTypeDef,
    DescribeCertificateAuthorityAuditReportResponseTypeDef,
    DescribeCertificateAuthorityResponseTypeDef,
    GetCertificateAuthorityCertificateResponseTypeDef,
    GetCertificateAuthorityCsrResponseTypeDef,
    GetCertificateResponseTypeDef,
    GetPolicyResponseTypeDef,
    IssueCertificateResponseTypeDef,
    ListCertificateAuthoritiesResponseTypeDef,
    ListPermissionsResponseTypeDef,
    ListTagsResponseTypeDef,
    RevocationConfigurationTypeDef,
    TagTypeDef,
    ValidityTypeDef,
)
from mypy_boto3_acm_pca.waiter import (
    AuditReportCreatedWaiter,
    CertificateAuthorityCSRCreatedWaiter,
    CertificateIssuedWaiter,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ACMPCAClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    CertificateMismatchException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    InvalidArgsException: Type[BotocoreClientError]
    InvalidArnException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidPolicyException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    InvalidStateException: Type[BotocoreClientError]
    InvalidTagException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    LockoutPreventedException: Type[BotocoreClientError]
    MalformedCSRException: Type[BotocoreClientError]
    MalformedCertificateException: Type[BotocoreClientError]
    PermissionAlreadyExistsException: Type[BotocoreClientError]
    RequestAlreadyProcessedException: Type[BotocoreClientError]
    RequestFailedException: Type[BotocoreClientError]
    RequestInProgressException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]


class ACMPCAClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/client.html)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/client.html#can-paginate)
        """

    def create_certificate_authority(
        self,
        CertificateAuthorityConfiguration: "CertificateAuthorityConfigurationTypeDef",
        CertificateAuthorityType: CertificateAuthorityType,
        RevocationConfiguration: "RevocationConfigurationTypeDef" = None,
        IdempotencyToken: str = None,
        KeyStorageSecurityStandard: KeyStorageSecurityStandard = None,
        Tags: List["TagTypeDef"] = None,
    ) -> CreateCertificateAuthorityResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Client.create_certificate_authority)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/client.html#create-certificate-authority)
        """

    def create_certificate_authority_audit_report(
        self,
        CertificateAuthorityArn: str,
        S3BucketName: str,
        AuditReportResponseFormat: AuditReportResponseFormat,
    ) -> CreateCertificateAuthorityAuditReportResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Client.create_certificate_authority_audit_report)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/client.html#create-certificate-authority-audit-report)
        """

    def create_permission(
        self,
        CertificateAuthorityArn: str,
        Principal: str,
        Actions: List[ActionType],
        SourceAccount: str = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Client.create_permission)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/client.html#create-permission)
        """

    def delete_certificate_authority(
        self, CertificateAuthorityArn: str, PermanentDeletionTimeInDays: int = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Client.delete_certificate_authority)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/client.html#delete-certificate-authority)
        """

    def delete_permission(
        self, CertificateAuthorityArn: str, Principal: str, SourceAccount: str = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Client.delete_permission)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/client.html#delete-permission)
        """

    def delete_policy(self, ResourceArn: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Client.delete_policy)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/client.html#delete-policy)
        """

    def describe_certificate_authority(
        self, CertificateAuthorityArn: str
    ) -> DescribeCertificateAuthorityResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Client.describe_certificate_authority)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/client.html#describe-certificate-authority)
        """

    def describe_certificate_authority_audit_report(
        self, CertificateAuthorityArn: str, AuditReportId: str
    ) -> DescribeCertificateAuthorityAuditReportResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Client.describe_certificate_authority_audit_report)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/client.html#describe-certificate-authority-audit-report)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/client.html#generate-presigned-url)
        """

    def get_certificate(
        self, CertificateAuthorityArn: str, CertificateArn: str
    ) -> GetCertificateResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Client.get_certificate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/client.html#get-certificate)
        """

    def get_certificate_authority_certificate(
        self, CertificateAuthorityArn: str
    ) -> GetCertificateAuthorityCertificateResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Client.get_certificate_authority_certificate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/client.html#get-certificate-authority-certificate)
        """

    def get_certificate_authority_csr(
        self, CertificateAuthorityArn: str
    ) -> GetCertificateAuthorityCsrResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Client.get_certificate_authority_csr)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/client.html#get-certificate-authority-csr)
        """

    def get_policy(self, ResourceArn: str) -> GetPolicyResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Client.get_policy)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/client.html#get-policy)
        """

    def import_certificate_authority_certificate(
        self,
        CertificateAuthorityArn: str,
        Certificate: Union[bytes, IO[bytes]],
        CertificateChain: Union[bytes, IO[bytes]] = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Client.import_certificate_authority_certificate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/client.html#import-certificate-authority-certificate)
        """

    def issue_certificate(
        self,
        CertificateAuthorityArn: str,
        Csr: Union[bytes, IO[bytes]],
        SigningAlgorithm: SigningAlgorithm,
        Validity: ValidityTypeDef,
        ApiPassthrough: ApiPassthroughTypeDef = None,
        TemplateArn: str = None,
        ValidityNotBefore: ValidityTypeDef = None,
        IdempotencyToken: str = None,
    ) -> IssueCertificateResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Client.issue_certificate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/client.html#issue-certificate)
        """

    def list_certificate_authorities(
        self, NextToken: str = None, MaxResults: int = None, ResourceOwner: ResourceOwner = None
    ) -> ListCertificateAuthoritiesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Client.list_certificate_authorities)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/client.html#list-certificate-authorities)
        """

    def list_permissions(
        self, CertificateAuthorityArn: str, NextToken: str = None, MaxResults: int = None
    ) -> ListPermissionsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Client.list_permissions)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/client.html#list-permissions)
        """

    def list_tags(
        self, CertificateAuthorityArn: str, NextToken: str = None, MaxResults: int = None
    ) -> ListTagsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Client.list_tags)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/client.html#list-tags)
        """

    def put_policy(self, ResourceArn: str, Policy: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Client.put_policy)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/client.html#put-policy)
        """

    def restore_certificate_authority(self, CertificateAuthorityArn: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Client.restore_certificate_authority)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/client.html#restore-certificate-authority)
        """

    def revoke_certificate(
        self,
        CertificateAuthorityArn: str,
        CertificateSerial: str,
        RevocationReason: RevocationReason,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Client.revoke_certificate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/client.html#revoke-certificate)
        """

    def tag_certificate_authority(
        self, CertificateAuthorityArn: str, Tags: List["TagTypeDef"]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Client.tag_certificate_authority)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/client.html#tag-certificate-authority)
        """

    def untag_certificate_authority(
        self, CertificateAuthorityArn: str, Tags: List["TagTypeDef"]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Client.untag_certificate_authority)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/client.html#untag-certificate-authority)
        """

    def update_certificate_authority(
        self,
        CertificateAuthorityArn: str,
        RevocationConfiguration: "RevocationConfigurationTypeDef" = None,
        Status: CertificateAuthorityStatus = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Client.update_certificate_authority)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/client.html#update-certificate-authority)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_certificate_authorities"]
    ) -> ListCertificateAuthoritiesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Paginator.ListCertificateAuthorities)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/paginators.html#listcertificateauthoritiespaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_permissions"]
    ) -> ListPermissionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Paginator.ListPermissions)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/paginators.html#listpermissionspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tags"]) -> ListTagsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Paginator.ListTags)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/paginators.html#listtagspaginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["audit_report_created"]) -> AuditReportCreatedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Waiter.audit_report_created)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/waiters.html#auditreportcreatedwaiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["certificate_authority_csr_created"]
    ) -> CertificateAuthorityCSRCreatedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Waiter.certificate_authority_csr_created)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/waiters.html#certificateauthoritycsrcreatedwaiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["certificate_issued"]) -> CertificateIssuedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/acm-pca.html#ACMPCA.Waiter.certificate_issued)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/waiters.html#certificateissuedwaiter)
        """
