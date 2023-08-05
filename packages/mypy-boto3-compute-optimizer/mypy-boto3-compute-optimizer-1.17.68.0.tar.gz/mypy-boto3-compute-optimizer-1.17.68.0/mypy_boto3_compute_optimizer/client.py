"""
Type annotations for compute-optimizer service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client.html)

Usage::

    ```python
    import boto3
    from mypy_boto3_compute_optimizer import ComputeOptimizerClient

    client: ComputeOptimizerClient = boto3.client("compute-optimizer")
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Type

from botocore.client import ClientMeta

from mypy_boto3_compute_optimizer.literals import (
    ExportableAutoScalingGroupField,
    ExportableInstanceField,
    MetricStatistic,
    Status,
)
from mypy_boto3_compute_optimizer.type_defs import (
    DescribeRecommendationExportJobsResponseTypeDef,
    EBSFilterTypeDef,
    ExportAutoScalingGroupRecommendationsResponseTypeDef,
    ExportEC2InstanceRecommendationsResponseTypeDef,
    FilterTypeDef,
    GetAutoScalingGroupRecommendationsResponseTypeDef,
    GetEBSVolumeRecommendationsResponseTypeDef,
    GetEC2InstanceRecommendationsResponseTypeDef,
    GetEC2RecommendationProjectedMetricsResponseTypeDef,
    GetEnrollmentStatusResponseTypeDef,
    GetLambdaFunctionRecommendationsResponseTypeDef,
    GetRecommendationSummariesResponseTypeDef,
    JobFilterTypeDef,
    LambdaFunctionRecommendationFilterTypeDef,
    S3DestinationConfigTypeDef,
    UpdateEnrollmentStatusResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ComputeOptimizerClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidParameterValueException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MissingAuthenticationToken: Type[BotocoreClientError]
    OptInRequiredException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]


class ComputeOptimizerClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/compute-optimizer.html#ComputeOptimizer.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client.html)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/compute-optimizer.html#ComputeOptimizer.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client.html#can-paginate)
        """

    def describe_recommendation_export_jobs(
        self,
        jobIds: List[str] = None,
        filters: List[JobFilterTypeDef] = None,
        nextToken: str = None,
        maxResults: int = None,
    ) -> DescribeRecommendationExportJobsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/compute-optimizer.html#ComputeOptimizer.Client.describe_recommendation_export_jobs)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client.html#describe-recommendation-export-jobs)
        """

    def export_auto_scaling_group_recommendations(
        self,
        s3DestinationConfig: S3DestinationConfigTypeDef,
        accountIds: List[str] = None,
        filters: List[FilterTypeDef] = None,
        fieldsToExport: List[ExportableAutoScalingGroupField] = None,
        fileFormat: Literal["Csv"] = None,
        includeMemberAccounts: bool = None,
    ) -> ExportAutoScalingGroupRecommendationsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/compute-optimizer.html#ComputeOptimizer.Client.export_auto_scaling_group_recommendations)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client.html#export-auto-scaling-group-recommendations)
        """

    def export_ec2_instance_recommendations(
        self,
        s3DestinationConfig: S3DestinationConfigTypeDef,
        accountIds: List[str] = None,
        filters: List[FilterTypeDef] = None,
        fieldsToExport: List[ExportableInstanceField] = None,
        fileFormat: Literal["Csv"] = None,
        includeMemberAccounts: bool = None,
    ) -> ExportEC2InstanceRecommendationsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/compute-optimizer.html#ComputeOptimizer.Client.export_ec2_instance_recommendations)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client.html#export-ec2-instance-recommendations)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/compute-optimizer.html#ComputeOptimizer.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client.html#generate-presigned-url)
        """

    def get_auto_scaling_group_recommendations(
        self,
        accountIds: List[str] = None,
        autoScalingGroupArns: List[str] = None,
        nextToken: str = None,
        maxResults: int = None,
        filters: List[FilterTypeDef] = None,
    ) -> GetAutoScalingGroupRecommendationsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/compute-optimizer.html#ComputeOptimizer.Client.get_auto_scaling_group_recommendations)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client.html#get-auto-scaling-group-recommendations)
        """

    def get_ebs_volume_recommendations(
        self,
        volumeArns: List[str] = None,
        nextToken: str = None,
        maxResults: int = None,
        filters: List[EBSFilterTypeDef] = None,
        accountIds: List[str] = None,
    ) -> GetEBSVolumeRecommendationsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/compute-optimizer.html#ComputeOptimizer.Client.get_ebs_volume_recommendations)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client.html#get-ebs-volume-recommendations)
        """

    def get_ec2_instance_recommendations(
        self,
        instanceArns: List[str] = None,
        nextToken: str = None,
        maxResults: int = None,
        filters: List[FilterTypeDef] = None,
        accountIds: List[str] = None,
    ) -> GetEC2InstanceRecommendationsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/compute-optimizer.html#ComputeOptimizer.Client.get_ec2_instance_recommendations)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client.html#get-ec2-instance-recommendations)
        """

    def get_ec2_recommendation_projected_metrics(
        self,
        instanceArn: str,
        stat: MetricStatistic,
        period: int,
        startTime: datetime,
        endTime: datetime,
    ) -> GetEC2RecommendationProjectedMetricsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/compute-optimizer.html#ComputeOptimizer.Client.get_ec2_recommendation_projected_metrics)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client.html#get-ec2-recommendation-projected-metrics)
        """

    def get_enrollment_status(self) -> GetEnrollmentStatusResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/compute-optimizer.html#ComputeOptimizer.Client.get_enrollment_status)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client.html#get-enrollment-status)
        """

    def get_lambda_function_recommendations(
        self,
        functionArns: List[str] = None,
        accountIds: List[str] = None,
        filters: List[LambdaFunctionRecommendationFilterTypeDef] = None,
        nextToken: str = None,
        maxResults: int = None,
    ) -> GetLambdaFunctionRecommendationsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/compute-optimizer.html#ComputeOptimizer.Client.get_lambda_function_recommendations)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client.html#get-lambda-function-recommendations)
        """

    def get_recommendation_summaries(
        self, accountIds: List[str] = None, nextToken: str = None, maxResults: int = None
    ) -> GetRecommendationSummariesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/compute-optimizer.html#ComputeOptimizer.Client.get_recommendation_summaries)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client.html#get-recommendation-summaries)
        """

    def update_enrollment_status(
        self, status: Status, includeMemberAccounts: bool = None
    ) -> UpdateEnrollmentStatusResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/compute-optimizer.html#ComputeOptimizer.Client.update_enrollment_status)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/client.html#update-enrollment-status)
        """
