"""
Type annotations for batch service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html)

Usage::

    ```python
    import boto3
    from mypy_boto3_batch import BatchClient

    client: BatchClient = boto3.client("batch")
    ```
"""
import sys
from typing import Any, Dict, List, Type, overload

from botocore.client import ClientMeta

from mypy_boto3_batch.literals import (
    CEState,
    CEType,
    JobDefinitionType,
    JobStatus,
    JQState,
    PlatformCapability,
)
from mypy_boto3_batch.paginator import (
    DescribeComputeEnvironmentsPaginator,
    DescribeJobDefinitionsPaginator,
    DescribeJobQueuesPaginator,
    ListJobsPaginator,
)
from mypy_boto3_batch.type_defs import (
    ArrayPropertiesTypeDef,
    ComputeEnvironmentOrderTypeDef,
    ComputeResourceTypeDef,
    ComputeResourceUpdateTypeDef,
    ContainerOverridesTypeDef,
    ContainerPropertiesTypeDef,
    CreateComputeEnvironmentResponseTypeDef,
    CreateJobQueueResponseTypeDef,
    DescribeComputeEnvironmentsResponseTypeDef,
    DescribeJobDefinitionsResponseTypeDef,
    DescribeJobQueuesResponseTypeDef,
    DescribeJobsResponseTypeDef,
    JobDependencyTypeDef,
    JobTimeoutTypeDef,
    ListJobsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    NodeOverridesTypeDef,
    NodePropertiesTypeDef,
    RegisterJobDefinitionResponseTypeDef,
    RetryStrategyTypeDef,
    SubmitJobResponseTypeDef,
    UpdateComputeEnvironmentResponseTypeDef,
    UpdateJobQueueResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("BatchClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ClientException: Type[BotocoreClientError]
    ServerException: Type[BotocoreClientError]


class BatchClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/batch.html#Batch.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/batch.html#Batch.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#can-paginate)
        """

    def cancel_job(self, jobId: str, reason: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/batch.html#Batch.Client.cancel_job)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#cancel-job)
        """

    def create_compute_environment(
        self,
        computeEnvironmentName: str,
        type: CEType,
        state: CEState = None,
        computeResources: "ComputeResourceTypeDef" = None,
        serviceRole: str = None,
        tags: Dict[str, str] = None,
    ) -> CreateComputeEnvironmentResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/batch.html#Batch.Client.create_compute_environment)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#create-compute-environment)
        """

    def create_job_queue(
        self,
        jobQueueName: str,
        priority: int,
        computeEnvironmentOrder: List["ComputeEnvironmentOrderTypeDef"],
        state: JQState = None,
        tags: Dict[str, str] = None,
    ) -> CreateJobQueueResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/batch.html#Batch.Client.create_job_queue)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#create-job-queue)
        """

    def delete_compute_environment(self, computeEnvironment: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/batch.html#Batch.Client.delete_compute_environment)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#delete-compute-environment)
        """

    def delete_job_queue(self, jobQueue: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/batch.html#Batch.Client.delete_job_queue)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#delete-job-queue)
        """

    def deregister_job_definition(self, jobDefinition: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/batch.html#Batch.Client.deregister_job_definition)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#deregister-job-definition)
        """

    def describe_compute_environments(
        self, computeEnvironments: List[str] = None, maxResults: int = None, nextToken: str = None
    ) -> DescribeComputeEnvironmentsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/batch.html#Batch.Client.describe_compute_environments)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#describe-compute-environments)
        """

    def describe_job_definitions(
        self,
        jobDefinitions: List[str] = None,
        maxResults: int = None,
        jobDefinitionName: str = None,
        status: str = None,
        nextToken: str = None,
    ) -> DescribeJobDefinitionsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/batch.html#Batch.Client.describe_job_definitions)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#describe-job-definitions)
        """

    def describe_job_queues(
        self, jobQueues: List[str] = None, maxResults: int = None, nextToken: str = None
    ) -> DescribeJobQueuesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/batch.html#Batch.Client.describe_job_queues)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#describe-job-queues)
        """

    def describe_jobs(self, jobs: List[str]) -> DescribeJobsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/batch.html#Batch.Client.describe_jobs)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#describe-jobs)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/batch.html#Batch.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#generate-presigned-url)
        """

    def list_jobs(
        self,
        jobQueue: str = None,
        arrayJobId: str = None,
        multiNodeJobId: str = None,
        jobStatus: JobStatus = None,
        maxResults: int = None,
        nextToken: str = None,
    ) -> ListJobsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/batch.html#Batch.Client.list_jobs)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#list-jobs)
        """

    def list_tags_for_resource(self, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/batch.html#Batch.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#list-tags-for-resource)
        """

    def register_job_definition(
        self,
        jobDefinitionName: str,
        type: JobDefinitionType,
        parameters: Dict[str, str] = None,
        containerProperties: "ContainerPropertiesTypeDef" = None,
        nodeProperties: "NodePropertiesTypeDef" = None,
        retryStrategy: "RetryStrategyTypeDef" = None,
        propagateTags: bool = None,
        timeout: "JobTimeoutTypeDef" = None,
        tags: Dict[str, str] = None,
        platformCapabilities: List[PlatformCapability] = None,
    ) -> RegisterJobDefinitionResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/batch.html#Batch.Client.register_job_definition)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#register-job-definition)
        """

    def submit_job(
        self,
        jobName: str,
        jobQueue: str,
        jobDefinition: str,
        arrayProperties: ArrayPropertiesTypeDef = None,
        dependsOn: List["JobDependencyTypeDef"] = None,
        parameters: Dict[str, str] = None,
        containerOverrides: "ContainerOverridesTypeDef" = None,
        nodeOverrides: NodeOverridesTypeDef = None,
        retryStrategy: "RetryStrategyTypeDef" = None,
        propagateTags: bool = None,
        timeout: "JobTimeoutTypeDef" = None,
        tags: Dict[str, str] = None,
    ) -> SubmitJobResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/batch.html#Batch.Client.submit_job)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#submit-job)
        """

    def tag_resource(self, resourceArn: str, tags: Dict[str, str]) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/batch.html#Batch.Client.tag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#tag-resource)
        """

    def terminate_job(self, jobId: str, reason: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/batch.html#Batch.Client.terminate_job)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#terminate-job)
        """

    def untag_resource(self, resourceArn: str, tagKeys: List[str]) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/batch.html#Batch.Client.untag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#untag-resource)
        """

    def update_compute_environment(
        self,
        computeEnvironment: str,
        state: CEState = None,
        computeResources: ComputeResourceUpdateTypeDef = None,
        serviceRole: str = None,
    ) -> UpdateComputeEnvironmentResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/batch.html#Batch.Client.update_compute_environment)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#update-compute-environment)
        """

    def update_job_queue(
        self,
        jobQueue: str,
        state: JQState = None,
        priority: int = None,
        computeEnvironmentOrder: List["ComputeEnvironmentOrderTypeDef"] = None,
    ) -> UpdateJobQueueResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/batch.html#Batch.Client.update_job_queue)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#update-job-queue)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_compute_environments"]
    ) -> DescribeComputeEnvironmentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/batch.html#Batch.Paginator.DescribeComputeEnvironments)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/paginators.html#describecomputeenvironmentspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_job_definitions"]
    ) -> DescribeJobDefinitionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/batch.html#Batch.Paginator.DescribeJobDefinitions)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/paginators.html#describejobdefinitionspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_job_queues"]
    ) -> DescribeJobQueuesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/batch.html#Batch.Paginator.DescribeJobQueues)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/paginators.html#describejobqueuespaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_jobs"]) -> ListJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/batch.html#Batch.Paginator.ListJobs)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/paginators.html#listjobspaginator)
        """
