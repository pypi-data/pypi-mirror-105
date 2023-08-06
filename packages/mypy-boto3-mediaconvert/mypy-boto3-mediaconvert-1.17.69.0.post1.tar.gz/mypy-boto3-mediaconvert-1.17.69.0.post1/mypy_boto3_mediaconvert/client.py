"""
Type annotations for mediaconvert service client.

[Open documentation](./client.md)

Usage::

    ```python
    import boto3
    from mypy_boto3_mediaconvert import MediaConvertClient

    client: MediaConvertClient = boto3.client("mediaconvert")
    ```
"""
import sys
from typing import Any, Dict, List, Type, overload

from botocore.client import ClientMeta

from mypy_boto3_mediaconvert.paginator import (
    DescribeEndpointsPaginator,
    ListJobsPaginator,
    ListJobTemplatesPaginator,
    ListPresetsPaginator,
    ListQueuesPaginator,
)

from .literals import (
    BillingTagsSource,
    DescribeEndpointsMode,
    JobStatus,
    JobTemplateListBy,
    Order,
    PresetListBy,
    PricingPlan,
    QueueListBy,
    QueueStatus,
    SimulateReservedQueue,
    StatusUpdateInterval,
)
from .type_defs import (
    AccelerationSettingsTypeDef,
    CreateJobResponseTypeDef,
    CreateJobTemplateResponseTypeDef,
    CreatePresetResponseTypeDef,
    CreateQueueResponseTypeDef,
    DescribeEndpointsResponseTypeDef,
    GetJobResponseTypeDef,
    GetJobTemplateResponseTypeDef,
    GetPresetResponseTypeDef,
    GetQueueResponseTypeDef,
    HopDestinationTypeDef,
    JobSettingsTypeDef,
    JobTemplateSettingsTypeDef,
    ListJobsResponseTypeDef,
    ListJobTemplatesResponseTypeDef,
    ListPresetsResponseTypeDef,
    ListQueuesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    PresetSettingsTypeDef,
    ReservationPlanSettingsTypeDef,
    UpdateJobTemplateResponseTypeDef,
    UpdatePresetResponseTypeDef,
    UpdateQueueResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("MediaConvertClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]


class MediaConvertClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client)
    [Show boto3-stubs documentation](./client.md)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def associate_certificate(self, Arn: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client.associate_certificate)
        [Show boto3-stubs documentation](./client.md#associate-certificate)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client.can_paginate)
        [Show boto3-stubs documentation](./client.md#can-paginate)
        """

    def cancel_job(self, Id: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client.cancel_job)
        [Show boto3-stubs documentation](./client.md#cancel-job)
        """

    def create_job(
        self,
        Role: str,
        Settings: "JobSettingsTypeDef",
        AccelerationSettings: "AccelerationSettingsTypeDef" = None,
        BillingTagsSource: BillingTagsSource = None,
        ClientRequestToken: str = None,
        HopDestinations: List["HopDestinationTypeDef"] = None,
        JobTemplate: str = None,
        Priority: int = None,
        Queue: str = None,
        SimulateReservedQueue: SimulateReservedQueue = None,
        StatusUpdateInterval: StatusUpdateInterval = None,
        Tags: Dict[str, str] = None,
        UserMetadata: Dict[str, str] = None,
    ) -> CreateJobResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client.create_job)
        [Show boto3-stubs documentation](./client.md#create-job)
        """

    def create_job_template(
        self,
        Name: str,
        Settings: "JobTemplateSettingsTypeDef",
        AccelerationSettings: "AccelerationSettingsTypeDef" = None,
        Category: str = None,
        Description: str = None,
        HopDestinations: List["HopDestinationTypeDef"] = None,
        Priority: int = None,
        Queue: str = None,
        StatusUpdateInterval: StatusUpdateInterval = None,
        Tags: Dict[str, str] = None,
    ) -> CreateJobTemplateResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client.create_job_template)
        [Show boto3-stubs documentation](./client.md#create-job-template)
        """

    def create_preset(
        self,
        Name: str,
        Settings: "PresetSettingsTypeDef",
        Category: str = None,
        Description: str = None,
        Tags: Dict[str, str] = None,
    ) -> CreatePresetResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client.create_preset)
        [Show boto3-stubs documentation](./client.md#create-preset)
        """

    def create_queue(
        self,
        Name: str,
        Description: str = None,
        PricingPlan: PricingPlan = None,
        ReservationPlanSettings: ReservationPlanSettingsTypeDef = None,
        Status: QueueStatus = None,
        Tags: Dict[str, str] = None,
    ) -> CreateQueueResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client.create_queue)
        [Show boto3-stubs documentation](./client.md#create-queue)
        """

    def delete_job_template(self, Name: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client.delete_job_template)
        [Show boto3-stubs documentation](./client.md#delete-job-template)
        """

    def delete_preset(self, Name: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client.delete_preset)
        [Show boto3-stubs documentation](./client.md#delete-preset)
        """

    def delete_queue(self, Name: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client.delete_queue)
        [Show boto3-stubs documentation](./client.md#delete-queue)
        """

    def describe_endpoints(
        self, MaxResults: int = None, Mode: DescribeEndpointsMode = None, NextToken: str = None
    ) -> DescribeEndpointsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client.describe_endpoints)
        [Show boto3-stubs documentation](./client.md#describe-endpoints)
        """

    def disassociate_certificate(self, Arn: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client.disassociate_certificate)
        [Show boto3-stubs documentation](./client.md#disassociate-certificate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client.generate_presigned_url)
        [Show boto3-stubs documentation](./client.md#generate-presigned-url)
        """

    def get_job(self, Id: str) -> GetJobResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client.get_job)
        [Show boto3-stubs documentation](./client.md#get-job)
        """

    def get_job_template(self, Name: str) -> GetJobTemplateResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client.get_job_template)
        [Show boto3-stubs documentation](./client.md#get-job-template)
        """

    def get_preset(self, Name: str) -> GetPresetResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client.get_preset)
        [Show boto3-stubs documentation](./client.md#get-preset)
        """

    def get_queue(self, Name: str) -> GetQueueResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client.get_queue)
        [Show boto3-stubs documentation](./client.md#get-queue)
        """

    def list_job_templates(
        self,
        Category: str = None,
        ListBy: JobTemplateListBy = None,
        MaxResults: int = None,
        NextToken: str = None,
        Order: Order = None,
    ) -> ListJobTemplatesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client.list_job_templates)
        [Show boto3-stubs documentation](./client.md#list-job-templates)
        """

    def list_jobs(
        self,
        MaxResults: int = None,
        NextToken: str = None,
        Order: Order = None,
        Queue: str = None,
        Status: JobStatus = None,
    ) -> ListJobsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client.list_jobs)
        [Show boto3-stubs documentation](./client.md#list-jobs)
        """

    def list_presets(
        self,
        Category: str = None,
        ListBy: PresetListBy = None,
        MaxResults: int = None,
        NextToken: str = None,
        Order: Order = None,
    ) -> ListPresetsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client.list_presets)
        [Show boto3-stubs documentation](./client.md#list-presets)
        """

    def list_queues(
        self,
        ListBy: QueueListBy = None,
        MaxResults: int = None,
        NextToken: str = None,
        Order: Order = None,
    ) -> ListQueuesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client.list_queues)
        [Show boto3-stubs documentation](./client.md#list-queues)
        """

    def list_tags_for_resource(self, Arn: str) -> ListTagsForResourceResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](./client.md#list-tags-for-resource)
        """

    def tag_resource(self, Arn: str, Tags: Dict[str, str]) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client.tag_resource)
        [Show boto3-stubs documentation](./client.md#tag-resource)
        """

    def untag_resource(self, Arn: str, TagKeys: List[str] = None) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client.untag_resource)
        [Show boto3-stubs documentation](./client.md#untag-resource)
        """

    def update_job_template(
        self,
        Name: str,
        AccelerationSettings: "AccelerationSettingsTypeDef" = None,
        Category: str = None,
        Description: str = None,
        HopDestinations: List["HopDestinationTypeDef"] = None,
        Priority: int = None,
        Queue: str = None,
        Settings: "JobTemplateSettingsTypeDef" = None,
        StatusUpdateInterval: StatusUpdateInterval = None,
    ) -> UpdateJobTemplateResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client.update_job_template)
        [Show boto3-stubs documentation](./client.md#update-job-template)
        """

    def update_preset(
        self,
        Name: str,
        Category: str = None,
        Description: str = None,
        Settings: "PresetSettingsTypeDef" = None,
    ) -> UpdatePresetResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client.update_preset)
        [Show boto3-stubs documentation](./client.md#update-preset)
        """

    def update_queue(
        self,
        Name: str,
        Description: str = None,
        ReservationPlanSettings: ReservationPlanSettingsTypeDef = None,
        Status: QueueStatus = None,
    ) -> UpdateQueueResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Client.update_queue)
        [Show boto3-stubs documentation](./client.md#update-queue)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_endpoints"]
    ) -> DescribeEndpointsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Paginator.DescribeEndpoints)[Show boto3-stubs documentation](./paginators.md#describeendpointspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_job_templates"]
    ) -> ListJobTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Paginator.ListJobTemplates)[Show boto3-stubs documentation](./paginators.md#listjobtemplatespaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_jobs"]) -> ListJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Paginator.ListJobs)[Show boto3-stubs documentation](./paginators.md#listjobspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_presets"]) -> ListPresetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Paginator.ListPresets)[Show boto3-stubs documentation](./paginators.md#listpresetspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_queues"]) -> ListQueuesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/mediaconvert.html#MediaConvert.Paginator.ListQueues)[Show boto3-stubs documentation](./paginators.md#listqueuespaginator)
        """
