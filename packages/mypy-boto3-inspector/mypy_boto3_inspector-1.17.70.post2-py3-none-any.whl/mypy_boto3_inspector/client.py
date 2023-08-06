"""
Type annotations for inspector service client.

[Open documentation](./client.md)

Usage::

    ```python
    import boto3
    from mypy_boto3_inspector import InspectorClient

    client: InspectorClient = boto3.client("inspector")
    ```
"""
import sys
from typing import Any, Dict, List, Type, overload

from botocore.client import ClientMeta

from mypy_boto3_inspector.paginator import (
    ListAssessmentRunAgentsPaginator,
    ListAssessmentRunsPaginator,
    ListAssessmentTargetsPaginator,
    ListAssessmentTemplatesPaginator,
    ListEventSubscriptionsPaginator,
    ListExclusionsPaginator,
    ListFindingsPaginator,
    ListRulesPackagesPaginator,
    PreviewAgentsPaginator,
)

from .literals import InspectorEvent, ReportFileFormat, ReportType, StopAction
from .type_defs import (
    AddAttributesToFindingsResponseTypeDef,
    AgentFilterTypeDef,
    AssessmentRunFilterTypeDef,
    AssessmentTargetFilterTypeDef,
    AssessmentTemplateFilterTypeDef,
    AttributeTypeDef,
    CreateAssessmentTargetResponseTypeDef,
    CreateAssessmentTemplateResponseTypeDef,
    CreateExclusionsPreviewResponseTypeDef,
    CreateResourceGroupResponseTypeDef,
    DescribeAssessmentRunsResponseTypeDef,
    DescribeAssessmentTargetsResponseTypeDef,
    DescribeAssessmentTemplatesResponseTypeDef,
    DescribeCrossAccountAccessRoleResponseTypeDef,
    DescribeExclusionsResponseTypeDef,
    DescribeFindingsResponseTypeDef,
    DescribeResourceGroupsResponseTypeDef,
    DescribeRulesPackagesResponseTypeDef,
    FindingFilterTypeDef,
    GetAssessmentReportResponseTypeDef,
    GetExclusionsPreviewResponseTypeDef,
    GetTelemetryMetadataResponseTypeDef,
    ListAssessmentRunAgentsResponseTypeDef,
    ListAssessmentRunsResponseTypeDef,
    ListAssessmentTargetsResponseTypeDef,
    ListAssessmentTemplatesResponseTypeDef,
    ListEventSubscriptionsResponseTypeDef,
    ListExclusionsResponseTypeDef,
    ListFindingsResponseTypeDef,
    ListRulesPackagesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    PreviewAgentsResponseTypeDef,
    RemoveAttributesFromFindingsResponseTypeDef,
    ResourceGroupTagTypeDef,
    StartAssessmentRunResponseTypeDef,
    TagTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("InspectorClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    AgentsAlreadyRunningAssessmentException: Type[BotocoreClientError]
    AssessmentRunInProgressException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalException: Type[BotocoreClientError]
    InvalidCrossAccountRoleException: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NoSuchEntityException: Type[BotocoreClientError]
    PreviewGenerationInProgressException: Type[BotocoreClientError]
    ServiceTemporarilyUnavailableException: Type[BotocoreClientError]
    UnsupportedFeatureException: Type[BotocoreClientError]


class InspectorClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client)
    [Show boto3-stubs documentation](./client.md)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def add_attributes_to_findings(
        self, findingArns: List[str], attributes: List["AttributeTypeDef"]
    ) -> AddAttributesToFindingsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.add_attributes_to_findings)
        [Show boto3-stubs documentation](./client.md#add-attributes-to-findings)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.can_paginate)
        [Show boto3-stubs documentation](./client.md#can-paginate)
        """

    def create_assessment_target(
        self, assessmentTargetName: str, resourceGroupArn: str = None
    ) -> CreateAssessmentTargetResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.create_assessment_target)
        [Show boto3-stubs documentation](./client.md#create-assessment-target)
        """

    def create_assessment_template(
        self,
        assessmentTargetArn: str,
        assessmentTemplateName: str,
        durationInSeconds: int,
        rulesPackageArns: List[str],
        userAttributesForFindings: List["AttributeTypeDef"] = None,
    ) -> CreateAssessmentTemplateResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.create_assessment_template)
        [Show boto3-stubs documentation](./client.md#create-assessment-template)
        """

    def create_exclusions_preview(
        self, assessmentTemplateArn: str
    ) -> CreateExclusionsPreviewResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.create_exclusions_preview)
        [Show boto3-stubs documentation](./client.md#create-exclusions-preview)
        """

    def create_resource_group(
        self, resourceGroupTags: List["ResourceGroupTagTypeDef"]
    ) -> CreateResourceGroupResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.create_resource_group)
        [Show boto3-stubs documentation](./client.md#create-resource-group)
        """

    def delete_assessment_run(self, assessmentRunArn: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.delete_assessment_run)
        [Show boto3-stubs documentation](./client.md#delete-assessment-run)
        """

    def delete_assessment_target(self, assessmentTargetArn: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.delete_assessment_target)
        [Show boto3-stubs documentation](./client.md#delete-assessment-target)
        """

    def delete_assessment_template(self, assessmentTemplateArn: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.delete_assessment_template)
        [Show boto3-stubs documentation](./client.md#delete-assessment-template)
        """

    def describe_assessment_runs(
        self, assessmentRunArns: List[str]
    ) -> DescribeAssessmentRunsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.describe_assessment_runs)
        [Show boto3-stubs documentation](./client.md#describe-assessment-runs)
        """

    def describe_assessment_targets(
        self, assessmentTargetArns: List[str]
    ) -> DescribeAssessmentTargetsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.describe_assessment_targets)
        [Show boto3-stubs documentation](./client.md#describe-assessment-targets)
        """

    def describe_assessment_templates(
        self, assessmentTemplateArns: List[str]
    ) -> DescribeAssessmentTemplatesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.describe_assessment_templates)
        [Show boto3-stubs documentation](./client.md#describe-assessment-templates)
        """

    def describe_cross_account_access_role(self) -> DescribeCrossAccountAccessRoleResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.describe_cross_account_access_role)
        [Show boto3-stubs documentation](./client.md#describe-cross-account-access-role)
        """

    def describe_exclusions(
        self, exclusionArns: List[str], locale: Literal["EN_US"] = None
    ) -> DescribeExclusionsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.describe_exclusions)
        [Show boto3-stubs documentation](./client.md#describe-exclusions)
        """

    def describe_findings(
        self, findingArns: List[str], locale: Literal["EN_US"] = None
    ) -> DescribeFindingsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.describe_findings)
        [Show boto3-stubs documentation](./client.md#describe-findings)
        """

    def describe_resource_groups(
        self, resourceGroupArns: List[str]
    ) -> DescribeResourceGroupsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.describe_resource_groups)
        [Show boto3-stubs documentation](./client.md#describe-resource-groups)
        """

    def describe_rules_packages(
        self, rulesPackageArns: List[str], locale: Literal["EN_US"] = None
    ) -> DescribeRulesPackagesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.describe_rules_packages)
        [Show boto3-stubs documentation](./client.md#describe-rules-packages)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.generate_presigned_url)
        [Show boto3-stubs documentation](./client.md#generate-presigned-url)
        """

    def get_assessment_report(
        self, assessmentRunArn: str, reportFileFormat: ReportFileFormat, reportType: ReportType
    ) -> GetAssessmentReportResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.get_assessment_report)
        [Show boto3-stubs documentation](./client.md#get-assessment-report)
        """

    def get_exclusions_preview(
        self,
        assessmentTemplateArn: str,
        previewToken: str,
        nextToken: str = None,
        maxResults: int = None,
        locale: Literal["EN_US"] = None,
    ) -> GetExclusionsPreviewResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.get_exclusions_preview)
        [Show boto3-stubs documentation](./client.md#get-exclusions-preview)
        """

    def get_telemetry_metadata(self, assessmentRunArn: str) -> GetTelemetryMetadataResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.get_telemetry_metadata)
        [Show boto3-stubs documentation](./client.md#get-telemetry-metadata)
        """

    def list_assessment_run_agents(
        self,
        assessmentRunArn: str,
        filter: AgentFilterTypeDef = None,
        nextToken: str = None,
        maxResults: int = None,
    ) -> ListAssessmentRunAgentsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.list_assessment_run_agents)
        [Show boto3-stubs documentation](./client.md#list-assessment-run-agents)
        """

    def list_assessment_runs(
        self,
        assessmentTemplateArns: List[str] = None,
        filter: AssessmentRunFilterTypeDef = None,
        nextToken: str = None,
        maxResults: int = None,
    ) -> ListAssessmentRunsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.list_assessment_runs)
        [Show boto3-stubs documentation](./client.md#list-assessment-runs)
        """

    def list_assessment_targets(
        self,
        filter: AssessmentTargetFilterTypeDef = None,
        nextToken: str = None,
        maxResults: int = None,
    ) -> ListAssessmentTargetsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.list_assessment_targets)
        [Show boto3-stubs documentation](./client.md#list-assessment-targets)
        """

    def list_assessment_templates(
        self,
        assessmentTargetArns: List[str] = None,
        filter: AssessmentTemplateFilterTypeDef = None,
        nextToken: str = None,
        maxResults: int = None,
    ) -> ListAssessmentTemplatesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.list_assessment_templates)
        [Show boto3-stubs documentation](./client.md#list-assessment-templates)
        """

    def list_event_subscriptions(
        self, resourceArn: str = None, nextToken: str = None, maxResults: int = None
    ) -> ListEventSubscriptionsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.list_event_subscriptions)
        [Show boto3-stubs documentation](./client.md#list-event-subscriptions)
        """

    def list_exclusions(
        self, assessmentRunArn: str, nextToken: str = None, maxResults: int = None
    ) -> ListExclusionsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.list_exclusions)
        [Show boto3-stubs documentation](./client.md#list-exclusions)
        """

    def list_findings(
        self,
        assessmentRunArns: List[str] = None,
        filter: FindingFilterTypeDef = None,
        nextToken: str = None,
        maxResults: int = None,
    ) -> ListFindingsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.list_findings)
        [Show boto3-stubs documentation](./client.md#list-findings)
        """

    def list_rules_packages(
        self, nextToken: str = None, maxResults: int = None
    ) -> ListRulesPackagesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.list_rules_packages)
        [Show boto3-stubs documentation](./client.md#list-rules-packages)
        """

    def list_tags_for_resource(self, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](./client.md#list-tags-for-resource)
        """

    def preview_agents(
        self, previewAgentsArn: str, nextToken: str = None, maxResults: int = None
    ) -> PreviewAgentsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.preview_agents)
        [Show boto3-stubs documentation](./client.md#preview-agents)
        """

    def register_cross_account_access_role(self, roleArn: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.register_cross_account_access_role)
        [Show boto3-stubs documentation](./client.md#register-cross-account-access-role)
        """

    def remove_attributes_from_findings(
        self, findingArns: List[str], attributeKeys: List[str]
    ) -> RemoveAttributesFromFindingsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.remove_attributes_from_findings)
        [Show boto3-stubs documentation](./client.md#remove-attributes-from-findings)
        """

    def set_tags_for_resource(self, resourceArn: str, tags: List["TagTypeDef"] = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.set_tags_for_resource)
        [Show boto3-stubs documentation](./client.md#set-tags-for-resource)
        """

    def start_assessment_run(
        self, assessmentTemplateArn: str, assessmentRunName: str = None
    ) -> StartAssessmentRunResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.start_assessment_run)
        [Show boto3-stubs documentation](./client.md#start-assessment-run)
        """

    def stop_assessment_run(self, assessmentRunArn: str, stopAction: StopAction = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.stop_assessment_run)
        [Show boto3-stubs documentation](./client.md#stop-assessment-run)
        """

    def subscribe_to_event(self, resourceArn: str, event: InspectorEvent, topicArn: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.subscribe_to_event)
        [Show boto3-stubs documentation](./client.md#subscribe-to-event)
        """

    def unsubscribe_from_event(
        self, resourceArn: str, event: InspectorEvent, topicArn: str
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.unsubscribe_from_event)
        [Show boto3-stubs documentation](./client.md#unsubscribe-from-event)
        """

    def update_assessment_target(
        self, assessmentTargetArn: str, assessmentTargetName: str, resourceGroupArn: str = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Client.update_assessment_target)
        [Show boto3-stubs documentation](./client.md#update-assessment-target)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_assessment_run_agents"]
    ) -> ListAssessmentRunAgentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Paginator.ListAssessmentRunAgents)[Show boto3-stubs documentation](./paginators.md#listassessmentrunagentspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_assessment_runs"]
    ) -> ListAssessmentRunsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Paginator.ListAssessmentRuns)[Show boto3-stubs documentation](./paginators.md#listassessmentrunspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_assessment_targets"]
    ) -> ListAssessmentTargetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Paginator.ListAssessmentTargets)[Show boto3-stubs documentation](./paginators.md#listassessmenttargetspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_assessment_templates"]
    ) -> ListAssessmentTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Paginator.ListAssessmentTemplates)[Show boto3-stubs documentation](./paginators.md#listassessmenttemplatespaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_event_subscriptions"]
    ) -> ListEventSubscriptionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Paginator.ListEventSubscriptions)[Show boto3-stubs documentation](./paginators.md#listeventsubscriptionspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_exclusions"]) -> ListExclusionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Paginator.ListExclusions)[Show boto3-stubs documentation](./paginators.md#listexclusionspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_findings"]) -> ListFindingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Paginator.ListFindings)[Show boto3-stubs documentation](./paginators.md#listfindingspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_rules_packages"]
    ) -> ListRulesPackagesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Paginator.ListRulesPackages)[Show boto3-stubs documentation](./paginators.md#listrulespackagespaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["preview_agents"]) -> PreviewAgentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/inspector.html#Inspector.Paginator.PreviewAgents)[Show boto3-stubs documentation](./paginators.md#previewagentspaginator)
        """
