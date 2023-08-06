"""
Type annotations for robomaker service client.

[Open documentation](./client.md)

Usage::

    ```python
    import boto3
    from mypy_boto3_robomaker import RoboMakerClient

    client: RoboMakerClient = boto3.client("robomaker")
    ```
"""
import sys
from typing import Any, Dict, List, Type, overload

from botocore.client import ClientMeta

from mypy_boto3_robomaker.paginator import (
    ListDeploymentJobsPaginator,
    ListFleetsPaginator,
    ListRobotApplicationsPaginator,
    ListRobotsPaginator,
    ListSimulationApplicationsPaginator,
    ListSimulationJobBatchesPaginator,
    ListSimulationJobsPaginator,
    ListWorldExportJobsPaginator,
    ListWorldGenerationJobsPaginator,
    ListWorldsPaginator,
    ListWorldTemplatesPaginator,
)

from .literals import Architecture, FailureBehavior
from .type_defs import (
    BatchDeleteWorldsResponseTypeDef,
    BatchDescribeSimulationJobResponseTypeDef,
    BatchPolicyTypeDef,
    ComputeTypeDef,
    CreateDeploymentJobResponseTypeDef,
    CreateFleetResponseTypeDef,
    CreateRobotApplicationResponseTypeDef,
    CreateRobotApplicationVersionResponseTypeDef,
    CreateRobotResponseTypeDef,
    CreateSimulationApplicationResponseTypeDef,
    CreateSimulationApplicationVersionResponseTypeDef,
    CreateSimulationJobResponseTypeDef,
    CreateWorldExportJobResponseTypeDef,
    CreateWorldGenerationJobResponseTypeDef,
    CreateWorldTemplateResponseTypeDef,
    DataSourceConfigTypeDef,
    DeploymentApplicationConfigTypeDef,
    DeploymentConfigTypeDef,
    DeregisterRobotResponseTypeDef,
    DescribeDeploymentJobResponseTypeDef,
    DescribeFleetResponseTypeDef,
    DescribeRobotApplicationResponseTypeDef,
    DescribeRobotResponseTypeDef,
    DescribeSimulationApplicationResponseTypeDef,
    DescribeSimulationJobBatchResponseTypeDef,
    DescribeSimulationJobResponseTypeDef,
    DescribeWorldExportJobResponseTypeDef,
    DescribeWorldGenerationJobResponseTypeDef,
    DescribeWorldResponseTypeDef,
    DescribeWorldTemplateResponseTypeDef,
    FilterTypeDef,
    GetWorldTemplateBodyResponseTypeDef,
    ListDeploymentJobsResponseTypeDef,
    ListFleetsResponseTypeDef,
    ListRobotApplicationsResponseTypeDef,
    ListRobotsResponseTypeDef,
    ListSimulationApplicationsResponseTypeDef,
    ListSimulationJobBatchesResponseTypeDef,
    ListSimulationJobsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWorldExportJobsResponseTypeDef,
    ListWorldGenerationJobsResponseTypeDef,
    ListWorldsResponseTypeDef,
    ListWorldTemplatesResponseTypeDef,
    LoggingConfigTypeDef,
    OutputLocationTypeDef,
    RegisterRobotResponseTypeDef,
    RenderingEngineTypeDef,
    RobotApplicationConfigTypeDef,
    RobotSoftwareSuiteTypeDef,
    SimulationApplicationConfigTypeDef,
    SimulationJobRequestTypeDef,
    SimulationSoftwareSuiteTypeDef,
    SourceConfigTypeDef,
    StartSimulationJobBatchResponseTypeDef,
    SyncDeploymentJobResponseTypeDef,
    TemplateLocationTypeDef,
    UpdateRobotApplicationResponseTypeDef,
    UpdateSimulationApplicationResponseTypeDef,
    UpdateWorldTemplateResponseTypeDef,
    VPCConfigTypeDef,
    WorldCountTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("RoboMakerClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentDeploymentException: Type[BotocoreClientError]
    IdempotentParameterMismatchException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]


class RoboMakerClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client)
    [Show boto3-stubs documentation](./client.md)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def batch_delete_worlds(self, worlds: List[str]) -> BatchDeleteWorldsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.batch_delete_worlds)
        [Show boto3-stubs documentation](./client.md#batch-delete-worlds)
        """

    def batch_describe_simulation_job(
        self, jobs: List[str]
    ) -> BatchDescribeSimulationJobResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.batch_describe_simulation_job)
        [Show boto3-stubs documentation](./client.md#batch-describe-simulation-job)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.can_paginate)
        [Show boto3-stubs documentation](./client.md#can-paginate)
        """

    def cancel_deployment_job(self, job: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.cancel_deployment_job)
        [Show boto3-stubs documentation](./client.md#cancel-deployment-job)
        """

    def cancel_simulation_job(self, job: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.cancel_simulation_job)
        [Show boto3-stubs documentation](./client.md#cancel-simulation-job)
        """

    def cancel_simulation_job_batch(self, batch: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.cancel_simulation_job_batch)
        [Show boto3-stubs documentation](./client.md#cancel-simulation-job-batch)
        """

    def cancel_world_export_job(self, job: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.cancel_world_export_job)
        [Show boto3-stubs documentation](./client.md#cancel-world-export-job)
        """

    def cancel_world_generation_job(self, job: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.cancel_world_generation_job)
        [Show boto3-stubs documentation](./client.md#cancel-world-generation-job)
        """

    def create_deployment_job(
        self,
        clientRequestToken: str,
        fleet: str,
        deploymentApplicationConfigs: List["DeploymentApplicationConfigTypeDef"],
        deploymentConfig: "DeploymentConfigTypeDef" = None,
        tags: Dict[str, str] = None,
    ) -> CreateDeploymentJobResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.create_deployment_job)
        [Show boto3-stubs documentation](./client.md#create-deployment-job)
        """

    def create_fleet(self, name: str, tags: Dict[str, str] = None) -> CreateFleetResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.create_fleet)
        [Show boto3-stubs documentation](./client.md#create-fleet)
        """

    def create_robot(
        self,
        name: str,
        architecture: Architecture,
        greengrassGroupId: str,
        tags: Dict[str, str] = None,
    ) -> CreateRobotResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.create_robot)
        [Show boto3-stubs documentation](./client.md#create-robot)
        """

    def create_robot_application(
        self,
        name: str,
        sources: List[SourceConfigTypeDef],
        robotSoftwareSuite: "RobotSoftwareSuiteTypeDef",
        tags: Dict[str, str] = None,
    ) -> CreateRobotApplicationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.create_robot_application)
        [Show boto3-stubs documentation](./client.md#create-robot-application)
        """

    def create_robot_application_version(
        self, application: str, currentRevisionId: str = None
    ) -> CreateRobotApplicationVersionResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.create_robot_application_version)
        [Show boto3-stubs documentation](./client.md#create-robot-application-version)
        """

    def create_simulation_application(
        self,
        name: str,
        sources: List[SourceConfigTypeDef],
        simulationSoftwareSuite: "SimulationSoftwareSuiteTypeDef",
        robotSoftwareSuite: "RobotSoftwareSuiteTypeDef",
        renderingEngine: "RenderingEngineTypeDef" = None,
        tags: Dict[str, str] = None,
    ) -> CreateSimulationApplicationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.create_simulation_application)
        [Show boto3-stubs documentation](./client.md#create-simulation-application)
        """

    def create_simulation_application_version(
        self, application: str, currentRevisionId: str = None
    ) -> CreateSimulationApplicationVersionResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.create_simulation_application_version)
        [Show boto3-stubs documentation](./client.md#create-simulation-application-version)
        """

    def create_simulation_job(
        self,
        maxJobDurationInSeconds: int,
        iamRole: str,
        clientRequestToken: str = None,
        outputLocation: "OutputLocationTypeDef" = None,
        loggingConfig: "LoggingConfigTypeDef" = None,
        failureBehavior: FailureBehavior = None,
        robotApplications: List["RobotApplicationConfigTypeDef"] = None,
        simulationApplications: List["SimulationApplicationConfigTypeDef"] = None,
        dataSources: List["DataSourceConfigTypeDef"] = None,
        tags: Dict[str, str] = None,
        vpcConfig: "VPCConfigTypeDef" = None,
        compute: "ComputeTypeDef" = None,
    ) -> CreateSimulationJobResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.create_simulation_job)
        [Show boto3-stubs documentation](./client.md#create-simulation-job)
        """

    def create_world_export_job(
        self,
        worlds: List[str],
        outputLocation: "OutputLocationTypeDef",
        iamRole: str,
        clientRequestToken: str = None,
        tags: Dict[str, str] = None,
    ) -> CreateWorldExportJobResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.create_world_export_job)
        [Show boto3-stubs documentation](./client.md#create-world-export-job)
        """

    def create_world_generation_job(
        self,
        template: str,
        worldCount: "WorldCountTypeDef",
        clientRequestToken: str = None,
        tags: Dict[str, str] = None,
        worldTags: Dict[str, str] = None,
    ) -> CreateWorldGenerationJobResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.create_world_generation_job)
        [Show boto3-stubs documentation](./client.md#create-world-generation-job)
        """

    def create_world_template(
        self,
        clientRequestToken: str = None,
        name: str = None,
        templateBody: str = None,
        templateLocation: TemplateLocationTypeDef = None,
        tags: Dict[str, str] = None,
    ) -> CreateWorldTemplateResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.create_world_template)
        [Show boto3-stubs documentation](./client.md#create-world-template)
        """

    def delete_fleet(self, fleet: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.delete_fleet)
        [Show boto3-stubs documentation](./client.md#delete-fleet)
        """

    def delete_robot(self, robot: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.delete_robot)
        [Show boto3-stubs documentation](./client.md#delete-robot)
        """

    def delete_robot_application(
        self, application: str, applicationVersion: str = None
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.delete_robot_application)
        [Show boto3-stubs documentation](./client.md#delete-robot-application)
        """

    def delete_simulation_application(
        self, application: str, applicationVersion: str = None
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.delete_simulation_application)
        [Show boto3-stubs documentation](./client.md#delete-simulation-application)
        """

    def delete_world_template(self, template: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.delete_world_template)
        [Show boto3-stubs documentation](./client.md#delete-world-template)
        """

    def deregister_robot(self, fleet: str, robot: str) -> DeregisterRobotResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.deregister_robot)
        [Show boto3-stubs documentation](./client.md#deregister-robot)
        """

    def describe_deployment_job(self, job: str) -> DescribeDeploymentJobResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.describe_deployment_job)
        [Show boto3-stubs documentation](./client.md#describe-deployment-job)
        """

    def describe_fleet(self, fleet: str) -> DescribeFleetResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.describe_fleet)
        [Show boto3-stubs documentation](./client.md#describe-fleet)
        """

    def describe_robot(self, robot: str) -> DescribeRobotResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.describe_robot)
        [Show boto3-stubs documentation](./client.md#describe-robot)
        """

    def describe_robot_application(
        self, application: str, applicationVersion: str = None
    ) -> DescribeRobotApplicationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.describe_robot_application)
        [Show boto3-stubs documentation](./client.md#describe-robot-application)
        """

    def describe_simulation_application(
        self, application: str, applicationVersion: str = None
    ) -> DescribeSimulationApplicationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.describe_simulation_application)
        [Show boto3-stubs documentation](./client.md#describe-simulation-application)
        """

    def describe_simulation_job(self, job: str) -> DescribeSimulationJobResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.describe_simulation_job)
        [Show boto3-stubs documentation](./client.md#describe-simulation-job)
        """

    def describe_simulation_job_batch(
        self, batch: str
    ) -> DescribeSimulationJobBatchResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.describe_simulation_job_batch)
        [Show boto3-stubs documentation](./client.md#describe-simulation-job-batch)
        """

    def describe_world(self, world: str) -> DescribeWorldResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.describe_world)
        [Show boto3-stubs documentation](./client.md#describe-world)
        """

    def describe_world_export_job(self, job: str) -> DescribeWorldExportJobResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.describe_world_export_job)
        [Show boto3-stubs documentation](./client.md#describe-world-export-job)
        """

    def describe_world_generation_job(self, job: str) -> DescribeWorldGenerationJobResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.describe_world_generation_job)
        [Show boto3-stubs documentation](./client.md#describe-world-generation-job)
        """

    def describe_world_template(self, template: str) -> DescribeWorldTemplateResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.describe_world_template)
        [Show boto3-stubs documentation](./client.md#describe-world-template)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.generate_presigned_url)
        [Show boto3-stubs documentation](./client.md#generate-presigned-url)
        """

    def get_world_template_body(
        self, template: str = None, generationJob: str = None
    ) -> GetWorldTemplateBodyResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.get_world_template_body)
        [Show boto3-stubs documentation](./client.md#get-world-template-body)
        """

    def list_deployment_jobs(
        self, filters: List[FilterTypeDef] = None, nextToken: str = None, maxResults: int = None
    ) -> ListDeploymentJobsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.list_deployment_jobs)
        [Show boto3-stubs documentation](./client.md#list-deployment-jobs)
        """

    def list_fleets(
        self, nextToken: str = None, maxResults: int = None, filters: List[FilterTypeDef] = None
    ) -> ListFleetsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.list_fleets)
        [Show boto3-stubs documentation](./client.md#list-fleets)
        """

    def list_robot_applications(
        self,
        versionQualifier: str = None,
        nextToken: str = None,
        maxResults: int = None,
        filters: List[FilterTypeDef] = None,
    ) -> ListRobotApplicationsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.list_robot_applications)
        [Show boto3-stubs documentation](./client.md#list-robot-applications)
        """

    def list_robots(
        self, nextToken: str = None, maxResults: int = None, filters: List[FilterTypeDef] = None
    ) -> ListRobotsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.list_robots)
        [Show boto3-stubs documentation](./client.md#list-robots)
        """

    def list_simulation_applications(
        self,
        versionQualifier: str = None,
        nextToken: str = None,
        maxResults: int = None,
        filters: List[FilterTypeDef] = None,
    ) -> ListSimulationApplicationsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.list_simulation_applications)
        [Show boto3-stubs documentation](./client.md#list-simulation-applications)
        """

    def list_simulation_job_batches(
        self, nextToken: str = None, maxResults: int = None, filters: List[FilterTypeDef] = None
    ) -> ListSimulationJobBatchesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.list_simulation_job_batches)
        [Show boto3-stubs documentation](./client.md#list-simulation-job-batches)
        """

    def list_simulation_jobs(
        self, nextToken: str = None, maxResults: int = None, filters: List[FilterTypeDef] = None
    ) -> ListSimulationJobsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.list_simulation_jobs)
        [Show boto3-stubs documentation](./client.md#list-simulation-jobs)
        """

    def list_tags_for_resource(self, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](./client.md#list-tags-for-resource)
        """

    def list_world_export_jobs(
        self, nextToken: str = None, maxResults: int = None, filters: List[FilterTypeDef] = None
    ) -> ListWorldExportJobsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.list_world_export_jobs)
        [Show boto3-stubs documentation](./client.md#list-world-export-jobs)
        """

    def list_world_generation_jobs(
        self, nextToken: str = None, maxResults: int = None, filters: List[FilterTypeDef] = None
    ) -> ListWorldGenerationJobsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.list_world_generation_jobs)
        [Show boto3-stubs documentation](./client.md#list-world-generation-jobs)
        """

    def list_world_templates(
        self, nextToken: str = None, maxResults: int = None
    ) -> ListWorldTemplatesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.list_world_templates)
        [Show boto3-stubs documentation](./client.md#list-world-templates)
        """

    def list_worlds(
        self, nextToken: str = None, maxResults: int = None, filters: List[FilterTypeDef] = None
    ) -> ListWorldsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.list_worlds)
        [Show boto3-stubs documentation](./client.md#list-worlds)
        """

    def register_robot(self, fleet: str, robot: str) -> RegisterRobotResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.register_robot)
        [Show boto3-stubs documentation](./client.md#register-robot)
        """

    def restart_simulation_job(self, job: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.restart_simulation_job)
        [Show boto3-stubs documentation](./client.md#restart-simulation-job)
        """

    def start_simulation_job_batch(
        self,
        createSimulationJobRequests: List["SimulationJobRequestTypeDef"],
        clientRequestToken: str = None,
        batchPolicy: "BatchPolicyTypeDef" = None,
        tags: Dict[str, str] = None,
    ) -> StartSimulationJobBatchResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.start_simulation_job_batch)
        [Show boto3-stubs documentation](./client.md#start-simulation-job-batch)
        """

    def sync_deployment_job(
        self, clientRequestToken: str, fleet: str
    ) -> SyncDeploymentJobResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.sync_deployment_job)
        [Show boto3-stubs documentation](./client.md#sync-deployment-job)
        """

    def tag_resource(self, resourceArn: str, tags: Dict[str, str]) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.tag_resource)
        [Show boto3-stubs documentation](./client.md#tag-resource)
        """

    def untag_resource(self, resourceArn: str, tagKeys: List[str]) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.untag_resource)
        [Show boto3-stubs documentation](./client.md#untag-resource)
        """

    def update_robot_application(
        self,
        application: str,
        sources: List[SourceConfigTypeDef],
        robotSoftwareSuite: "RobotSoftwareSuiteTypeDef",
        currentRevisionId: str = None,
    ) -> UpdateRobotApplicationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.update_robot_application)
        [Show boto3-stubs documentation](./client.md#update-robot-application)
        """

    def update_simulation_application(
        self,
        application: str,
        sources: List[SourceConfigTypeDef],
        simulationSoftwareSuite: "SimulationSoftwareSuiteTypeDef",
        robotSoftwareSuite: "RobotSoftwareSuiteTypeDef",
        renderingEngine: "RenderingEngineTypeDef" = None,
        currentRevisionId: str = None,
    ) -> UpdateSimulationApplicationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.update_simulation_application)
        [Show boto3-stubs documentation](./client.md#update-simulation-application)
        """

    def update_world_template(
        self,
        template: str,
        name: str = None,
        templateBody: str = None,
        templateLocation: TemplateLocationTypeDef = None,
    ) -> UpdateWorldTemplateResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Client.update_world_template)
        [Show boto3-stubs documentation](./client.md#update-world-template)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_deployment_jobs"]
    ) -> ListDeploymentJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Paginator.ListDeploymentJobs)[Show boto3-stubs documentation](./paginators.md#listdeploymentjobspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_fleets"]) -> ListFleetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Paginator.ListFleets)[Show boto3-stubs documentation](./paginators.md#listfleetspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_robot_applications"]
    ) -> ListRobotApplicationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Paginator.ListRobotApplications)[Show boto3-stubs documentation](./paginators.md#listrobotapplicationspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_robots"]) -> ListRobotsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Paginator.ListRobots)[Show boto3-stubs documentation](./paginators.md#listrobotspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_simulation_applications"]
    ) -> ListSimulationApplicationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Paginator.ListSimulationApplications)[Show boto3-stubs documentation](./paginators.md#listsimulationapplicationspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_simulation_job_batches"]
    ) -> ListSimulationJobBatchesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Paginator.ListSimulationJobBatches)[Show boto3-stubs documentation](./paginators.md#listsimulationjobbatchespaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_simulation_jobs"]
    ) -> ListSimulationJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Paginator.ListSimulationJobs)[Show boto3-stubs documentation](./paginators.md#listsimulationjobspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_world_export_jobs"]
    ) -> ListWorldExportJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Paginator.ListWorldExportJobs)[Show boto3-stubs documentation](./paginators.md#listworldexportjobspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_world_generation_jobs"]
    ) -> ListWorldGenerationJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Paginator.ListWorldGenerationJobs)[Show boto3-stubs documentation](./paginators.md#listworldgenerationjobspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_world_templates"]
    ) -> ListWorldTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Paginator.ListWorldTemplates)[Show boto3-stubs documentation](./paginators.md#listworldtemplatespaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_worlds"]) -> ListWorldsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/robomaker.html#RoboMaker.Paginator.ListWorlds)[Show boto3-stubs documentation](./paginators.md#listworldspaginator)
        """
