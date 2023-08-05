"""
Type annotations for support service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html)

Usage::

    ```python
    import boto3
    from mypy_boto3_support import SupportClient

    client: SupportClient = boto3.client("support")
    ```
"""
import sys
from typing import Any, Dict, List, Type, overload

from botocore.client import ClientMeta

from mypy_boto3_support.paginator import DescribeCasesPaginator, DescribeCommunicationsPaginator
from mypy_boto3_support.type_defs import (
    AddAttachmentsToSetResponseTypeDef,
    AddCommunicationToCaseResponseTypeDef,
    AttachmentTypeDef,
    CreateCaseResponseTypeDef,
    DescribeAttachmentResponseTypeDef,
    DescribeCasesResponseTypeDef,
    DescribeCommunicationsResponseTypeDef,
    DescribeServicesResponseTypeDef,
    DescribeSeverityLevelsResponseTypeDef,
    DescribeTrustedAdvisorCheckRefreshStatusesResponseTypeDef,
    DescribeTrustedAdvisorCheckResultResponseTypeDef,
    DescribeTrustedAdvisorChecksResponseTypeDef,
    DescribeTrustedAdvisorCheckSummariesResponseTypeDef,
    RefreshTrustedAdvisorCheckResponseTypeDef,
    ResolveCaseResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("SupportClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AttachmentIdNotFound: Type[BotocoreClientError]
    AttachmentLimitExceeded: Type[BotocoreClientError]
    AttachmentSetExpired: Type[BotocoreClientError]
    AttachmentSetIdNotFound: Type[BotocoreClientError]
    AttachmentSetSizeLimitExceeded: Type[BotocoreClientError]
    CaseCreationLimitExceeded: Type[BotocoreClientError]
    CaseIdNotFound: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DescribeAttachmentLimitExceeded: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]


class SupportClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/support.html#Support.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def add_attachments_to_set(
        self, attachments: List["AttachmentTypeDef"], attachmentSetId: str = None
    ) -> AddAttachmentsToSetResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/support.html#Support.Client.add_attachments_to_set)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#add-attachments-to-set)
        """

    def add_communication_to_case(
        self,
        communicationBody: str,
        caseId: str = None,
        ccEmailAddresses: List[str] = None,
        attachmentSetId: str = None,
    ) -> AddCommunicationToCaseResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/support.html#Support.Client.add_communication_to_case)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#add-communication-to-case)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/support.html#Support.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#can-paginate)
        """

    def create_case(
        self,
        subject: str,
        communicationBody: str,
        serviceCode: str = None,
        severityCode: str = None,
        categoryCode: str = None,
        ccEmailAddresses: List[str] = None,
        language: str = None,
        issueType: str = None,
        attachmentSetId: str = None,
    ) -> CreateCaseResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/support.html#Support.Client.create_case)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#create-case)
        """

    def describe_attachment(self, attachmentId: str) -> DescribeAttachmentResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/support.html#Support.Client.describe_attachment)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#describe-attachment)
        """

    def describe_cases(
        self,
        caseIdList: List[str] = None,
        displayId: str = None,
        afterTime: str = None,
        beforeTime: str = None,
        includeResolvedCases: bool = None,
        nextToken: str = None,
        maxResults: int = None,
        language: str = None,
        includeCommunications: bool = None,
    ) -> DescribeCasesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/support.html#Support.Client.describe_cases)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#describe-cases)
        """

    def describe_communications(
        self,
        caseId: str,
        beforeTime: str = None,
        afterTime: str = None,
        nextToken: str = None,
        maxResults: int = None,
    ) -> DescribeCommunicationsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/support.html#Support.Client.describe_communications)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#describe-communications)
        """

    def describe_services(
        self, serviceCodeList: List[str] = None, language: str = None
    ) -> DescribeServicesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/support.html#Support.Client.describe_services)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#describe-services)
        """

    def describe_severity_levels(
        self, language: str = None
    ) -> DescribeSeverityLevelsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/support.html#Support.Client.describe_severity_levels)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#describe-severity-levels)
        """

    def describe_trusted_advisor_check_refresh_statuses(
        self, checkIds: List[str]
    ) -> DescribeTrustedAdvisorCheckRefreshStatusesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/support.html#Support.Client.describe_trusted_advisor_check_refresh_statuses)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#describe-trusted-advisor-check-refresh-statuses)
        """

    def describe_trusted_advisor_check_result(
        self, checkId: str, language: str = None
    ) -> DescribeTrustedAdvisorCheckResultResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/support.html#Support.Client.describe_trusted_advisor_check_result)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#describe-trusted-advisor-check-result)
        """

    def describe_trusted_advisor_check_summaries(
        self, checkIds: List[str]
    ) -> DescribeTrustedAdvisorCheckSummariesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/support.html#Support.Client.describe_trusted_advisor_check_summaries)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#describe-trusted-advisor-check-summaries)
        """

    def describe_trusted_advisor_checks(
        self, language: str
    ) -> DescribeTrustedAdvisorChecksResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/support.html#Support.Client.describe_trusted_advisor_checks)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#describe-trusted-advisor-checks)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/support.html#Support.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#generate-presigned-url)
        """

    def refresh_trusted_advisor_check(
        self, checkId: str
    ) -> RefreshTrustedAdvisorCheckResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/support.html#Support.Client.refresh_trusted_advisor_check)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#refresh-trusted-advisor-check)
        """

    def resolve_case(self, caseId: str = None) -> ResolveCaseResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/support.html#Support.Client.resolve_case)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#resolve-case)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_cases"]) -> DescribeCasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/support.html#Support.Paginator.DescribeCases)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/paginators.html#describecasespaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_communications"]
    ) -> DescribeCommunicationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/support.html#Support.Paginator.DescribeCommunications)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/paginators.html#describecommunicationspaginator)
        """
