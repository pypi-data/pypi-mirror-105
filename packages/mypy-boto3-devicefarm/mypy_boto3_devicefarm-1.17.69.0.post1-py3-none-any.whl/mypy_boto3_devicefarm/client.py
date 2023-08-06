"""
Type annotations for devicefarm service client.

[Open documentation](./client.md)

Usage::

    ```python
    import boto3
    from mypy_boto3_devicefarm import DeviceFarmClient

    client: DeviceFarmClient = boto3.client("devicefarm")
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Type, overload

from botocore.client import ClientMeta

from mypy_boto3_devicefarm.paginator import (
    GetOfferingStatusPaginator,
    ListArtifactsPaginator,
    ListDeviceInstancesPaginator,
    ListDevicePoolsPaginator,
    ListDevicesPaginator,
    ListInstanceProfilesPaginator,
    ListJobsPaginator,
    ListNetworkProfilesPaginator,
    ListOfferingPromotionsPaginator,
    ListOfferingsPaginator,
    ListOfferingTransactionsPaginator,
    ListProjectsPaginator,
    ListRemoteAccessSessionsPaginator,
    ListRunsPaginator,
    ListSamplesPaginator,
    ListSuitesPaginator,
    ListTestsPaginator,
    ListUniqueProblemsPaginator,
    ListUploadsPaginator,
    ListVPCEConfigurationsPaginator,
)

from .literals import (
    ArtifactCategory,
    DevicePoolType,
    InteractionMode,
    NetworkProfileType,
    TestGridSessionArtifactCategory,
    TestGridSessionStatus,
    TestType,
    UploadType,
)
from .type_defs import (
    CreateDevicePoolResultTypeDef,
    CreateInstanceProfileResultTypeDef,
    CreateNetworkProfileResultTypeDef,
    CreateProjectResultTypeDef,
    CreateRemoteAccessSessionConfigurationTypeDef,
    CreateRemoteAccessSessionResultTypeDef,
    CreateTestGridProjectResultTypeDef,
    CreateTestGridUrlResultTypeDef,
    CreateUploadResultTypeDef,
    CreateVPCEConfigurationResultTypeDef,
    DeviceFilterTypeDef,
    DeviceSelectionConfigurationTypeDef,
    ExecutionConfigurationTypeDef,
    GetAccountSettingsResultTypeDef,
    GetDeviceInstanceResultTypeDef,
    GetDevicePoolCompatibilityResultTypeDef,
    GetDevicePoolResultTypeDef,
    GetDeviceResultTypeDef,
    GetInstanceProfileResultTypeDef,
    GetJobResultTypeDef,
    GetNetworkProfileResultTypeDef,
    GetOfferingStatusResultTypeDef,
    GetProjectResultTypeDef,
    GetRemoteAccessSessionResultTypeDef,
    GetRunResultTypeDef,
    GetSuiteResultTypeDef,
    GetTestGridProjectResultTypeDef,
    GetTestGridSessionResultTypeDef,
    GetTestResultTypeDef,
    GetUploadResultTypeDef,
    GetVPCEConfigurationResultTypeDef,
    InstallToRemoteAccessSessionResultTypeDef,
    ListArtifactsResultTypeDef,
    ListDeviceInstancesResultTypeDef,
    ListDevicePoolsResultTypeDef,
    ListDevicesResultTypeDef,
    ListInstanceProfilesResultTypeDef,
    ListJobsResultTypeDef,
    ListNetworkProfilesResultTypeDef,
    ListOfferingPromotionsResultTypeDef,
    ListOfferingsResultTypeDef,
    ListOfferingTransactionsResultTypeDef,
    ListProjectsResultTypeDef,
    ListRemoteAccessSessionsResultTypeDef,
    ListRunsResultTypeDef,
    ListSamplesResultTypeDef,
    ListSuitesResultTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTestGridProjectsResultTypeDef,
    ListTestGridSessionActionsResultTypeDef,
    ListTestGridSessionArtifactsResultTypeDef,
    ListTestGridSessionsResultTypeDef,
    ListTestsResultTypeDef,
    ListUniqueProblemsResultTypeDef,
    ListUploadsResultTypeDef,
    ListVPCEConfigurationsResultTypeDef,
    PurchaseOfferingResultTypeDef,
    RenewOfferingResultTypeDef,
    RuleTypeDef,
    ScheduleRunConfigurationTypeDef,
    ScheduleRunResultTypeDef,
    ScheduleRunTestTypeDef,
    StopJobResultTypeDef,
    StopRemoteAccessSessionResultTypeDef,
    StopRunResultTypeDef,
    TagTypeDef,
    UpdateDeviceInstanceResultTypeDef,
    UpdateDevicePoolResultTypeDef,
    UpdateInstanceProfileResultTypeDef,
    UpdateNetworkProfileResultTypeDef,
    UpdateProjectResultTypeDef,
    UpdateTestGridProjectResultTypeDef,
    UpdateUploadResultTypeDef,
    UpdateVPCEConfigurationResultTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("DeviceFarmClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ArgumentException: Type[BotocoreClientError]
    CannotDeleteException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    IdempotencyException: Type[BotocoreClientError]
    InternalServiceException: Type[BotocoreClientError]
    InvalidOperationException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotEligibleException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ServiceAccountException: Type[BotocoreClientError]
    TagOperationException: Type[BotocoreClientError]
    TagPolicyException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]


class DeviceFarmClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client)
    [Show boto3-stubs documentation](./client.md)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.can_paginate)
        [Show boto3-stubs documentation](./client.md#can-paginate)
        """

    def create_device_pool(
        self,
        projectArn: str,
        name: str,
        rules: List["RuleTypeDef"],
        description: str = None,
        maxDevices: int = None,
    ) -> CreateDevicePoolResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.create_device_pool)
        [Show boto3-stubs documentation](./client.md#create-device-pool)
        """

    def create_instance_profile(
        self,
        name: str,
        description: str = None,
        packageCleanup: bool = None,
        excludeAppPackagesFromCleanup: List[str] = None,
        rebootAfterUse: bool = None,
    ) -> CreateInstanceProfileResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.create_instance_profile)
        [Show boto3-stubs documentation](./client.md#create-instance-profile)
        """

    def create_network_profile(
        self,
        projectArn: str,
        name: str,
        description: str = None,
        type: NetworkProfileType = None,
        uplinkBandwidthBits: int = None,
        downlinkBandwidthBits: int = None,
        uplinkDelayMs: int = None,
        downlinkDelayMs: int = None,
        uplinkJitterMs: int = None,
        downlinkJitterMs: int = None,
        uplinkLossPercent: int = None,
        downlinkLossPercent: int = None,
    ) -> CreateNetworkProfileResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.create_network_profile)
        [Show boto3-stubs documentation](./client.md#create-network-profile)
        """

    def create_project(
        self, name: str, defaultJobTimeoutMinutes: int = None
    ) -> CreateProjectResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.create_project)
        [Show boto3-stubs documentation](./client.md#create-project)
        """

    def create_remote_access_session(
        self,
        projectArn: str,
        deviceArn: str,
        instanceArn: str = None,
        sshPublicKey: str = None,
        remoteDebugEnabled: bool = None,
        remoteRecordEnabled: bool = None,
        remoteRecordAppArn: str = None,
        name: str = None,
        clientId: str = None,
        configuration: CreateRemoteAccessSessionConfigurationTypeDef = None,
        interactionMode: InteractionMode = None,
        skipAppResign: bool = None,
    ) -> CreateRemoteAccessSessionResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.create_remote_access_session)
        [Show boto3-stubs documentation](./client.md#create-remote-access-session)
        """

    def create_test_grid_project(
        self, name: str, description: str = None
    ) -> CreateTestGridProjectResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.create_test_grid_project)
        [Show boto3-stubs documentation](./client.md#create-test-grid-project)
        """

    def create_test_grid_url(
        self, projectArn: str, expiresInSeconds: int
    ) -> CreateTestGridUrlResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.create_test_grid_url)
        [Show boto3-stubs documentation](./client.md#create-test-grid-url)
        """

    def create_upload(
        self, projectArn: str, name: str, type: UploadType, contentType: str = None
    ) -> CreateUploadResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.create_upload)
        [Show boto3-stubs documentation](./client.md#create-upload)
        """

    def create_vpce_configuration(
        self,
        vpceConfigurationName: str,
        vpceServiceName: str,
        serviceDnsName: str,
        vpceConfigurationDescription: str = None,
    ) -> CreateVPCEConfigurationResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.create_vpce_configuration)
        [Show boto3-stubs documentation](./client.md#create-vpce-configuration)
        """

    def delete_device_pool(self, arn: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.delete_device_pool)
        [Show boto3-stubs documentation](./client.md#delete-device-pool)
        """

    def delete_instance_profile(self, arn: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.delete_instance_profile)
        [Show boto3-stubs documentation](./client.md#delete-instance-profile)
        """

    def delete_network_profile(self, arn: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.delete_network_profile)
        [Show boto3-stubs documentation](./client.md#delete-network-profile)
        """

    def delete_project(self, arn: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.delete_project)
        [Show boto3-stubs documentation](./client.md#delete-project)
        """

    def delete_remote_access_session(self, arn: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.delete_remote_access_session)
        [Show boto3-stubs documentation](./client.md#delete-remote-access-session)
        """

    def delete_run(self, arn: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.delete_run)
        [Show boto3-stubs documentation](./client.md#delete-run)
        """

    def delete_test_grid_project(self, projectArn: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.delete_test_grid_project)
        [Show boto3-stubs documentation](./client.md#delete-test-grid-project)
        """

    def delete_upload(self, arn: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.delete_upload)
        [Show boto3-stubs documentation](./client.md#delete-upload)
        """

    def delete_vpce_configuration(self, arn: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.delete_vpce_configuration)
        [Show boto3-stubs documentation](./client.md#delete-vpce-configuration)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.generate_presigned_url)
        [Show boto3-stubs documentation](./client.md#generate-presigned-url)
        """

    def get_account_settings(self) -> GetAccountSettingsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.get_account_settings)
        [Show boto3-stubs documentation](./client.md#get-account-settings)
        """

    def get_device(self, arn: str) -> GetDeviceResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.get_device)
        [Show boto3-stubs documentation](./client.md#get-device)
        """

    def get_device_instance(self, arn: str) -> GetDeviceInstanceResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.get_device_instance)
        [Show boto3-stubs documentation](./client.md#get-device-instance)
        """

    def get_device_pool(self, arn: str) -> GetDevicePoolResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.get_device_pool)
        [Show boto3-stubs documentation](./client.md#get-device-pool)
        """

    def get_device_pool_compatibility(
        self,
        devicePoolArn: str,
        appArn: str = None,
        testType: TestType = None,
        test: ScheduleRunTestTypeDef = None,
        configuration: ScheduleRunConfigurationTypeDef = None,
    ) -> GetDevicePoolCompatibilityResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.get_device_pool_compatibility)
        [Show boto3-stubs documentation](./client.md#get-device-pool-compatibility)
        """

    def get_instance_profile(self, arn: str) -> GetInstanceProfileResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.get_instance_profile)
        [Show boto3-stubs documentation](./client.md#get-instance-profile)
        """

    def get_job(self, arn: str) -> GetJobResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.get_job)
        [Show boto3-stubs documentation](./client.md#get-job)
        """

    def get_network_profile(self, arn: str) -> GetNetworkProfileResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.get_network_profile)
        [Show boto3-stubs documentation](./client.md#get-network-profile)
        """

    def get_offering_status(self, nextToken: str = None) -> GetOfferingStatusResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.get_offering_status)
        [Show boto3-stubs documentation](./client.md#get-offering-status)
        """

    def get_project(self, arn: str) -> GetProjectResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.get_project)
        [Show boto3-stubs documentation](./client.md#get-project)
        """

    def get_remote_access_session(self, arn: str) -> GetRemoteAccessSessionResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.get_remote_access_session)
        [Show boto3-stubs documentation](./client.md#get-remote-access-session)
        """

    def get_run(self, arn: str) -> GetRunResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.get_run)
        [Show boto3-stubs documentation](./client.md#get-run)
        """

    def get_suite(self, arn: str) -> GetSuiteResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.get_suite)
        [Show boto3-stubs documentation](./client.md#get-suite)
        """

    def get_test(self, arn: str) -> GetTestResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.get_test)
        [Show boto3-stubs documentation](./client.md#get-test)
        """

    def get_test_grid_project(self, projectArn: str) -> GetTestGridProjectResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.get_test_grid_project)
        [Show boto3-stubs documentation](./client.md#get-test-grid-project)
        """

    def get_test_grid_session(
        self, projectArn: str = None, sessionId: str = None, sessionArn: str = None
    ) -> GetTestGridSessionResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.get_test_grid_session)
        [Show boto3-stubs documentation](./client.md#get-test-grid-session)
        """

    def get_upload(self, arn: str) -> GetUploadResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.get_upload)
        [Show boto3-stubs documentation](./client.md#get-upload)
        """

    def get_vpce_configuration(self, arn: str) -> GetVPCEConfigurationResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.get_vpce_configuration)
        [Show boto3-stubs documentation](./client.md#get-vpce-configuration)
        """

    def install_to_remote_access_session(
        self, remoteAccessSessionArn: str, appArn: str
    ) -> InstallToRemoteAccessSessionResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.install_to_remote_access_session)
        [Show boto3-stubs documentation](./client.md#install-to-remote-access-session)
        """

    def list_artifacts(
        self, arn: str, type: ArtifactCategory, nextToken: str = None
    ) -> ListArtifactsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.list_artifacts)
        [Show boto3-stubs documentation](./client.md#list-artifacts)
        """

    def list_device_instances(
        self, maxResults: int = None, nextToken: str = None
    ) -> ListDeviceInstancesResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.list_device_instances)
        [Show boto3-stubs documentation](./client.md#list-device-instances)
        """

    def list_device_pools(
        self, arn: str, type: DevicePoolType = None, nextToken: str = None
    ) -> ListDevicePoolsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.list_device_pools)
        [Show boto3-stubs documentation](./client.md#list-device-pools)
        """

    def list_devices(
        self, arn: str = None, nextToken: str = None, filters: List["DeviceFilterTypeDef"] = None
    ) -> ListDevicesResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.list_devices)
        [Show boto3-stubs documentation](./client.md#list-devices)
        """

    def list_instance_profiles(
        self, maxResults: int = None, nextToken: str = None
    ) -> ListInstanceProfilesResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.list_instance_profiles)
        [Show boto3-stubs documentation](./client.md#list-instance-profiles)
        """

    def list_jobs(self, arn: str, nextToken: str = None) -> ListJobsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.list_jobs)
        [Show boto3-stubs documentation](./client.md#list-jobs)
        """

    def list_network_profiles(
        self, arn: str, type: NetworkProfileType = None, nextToken: str = None
    ) -> ListNetworkProfilesResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.list_network_profiles)
        [Show boto3-stubs documentation](./client.md#list-network-profiles)
        """

    def list_offering_promotions(
        self, nextToken: str = None
    ) -> ListOfferingPromotionsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.list_offering_promotions)
        [Show boto3-stubs documentation](./client.md#list-offering-promotions)
        """

    def list_offering_transactions(
        self, nextToken: str = None
    ) -> ListOfferingTransactionsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.list_offering_transactions)
        [Show boto3-stubs documentation](./client.md#list-offering-transactions)
        """

    def list_offerings(self, nextToken: str = None) -> ListOfferingsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.list_offerings)
        [Show boto3-stubs documentation](./client.md#list-offerings)
        """

    def list_projects(self, arn: str = None, nextToken: str = None) -> ListProjectsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.list_projects)
        [Show boto3-stubs documentation](./client.md#list-projects)
        """

    def list_remote_access_sessions(
        self, arn: str, nextToken: str = None
    ) -> ListRemoteAccessSessionsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.list_remote_access_sessions)
        [Show boto3-stubs documentation](./client.md#list-remote-access-sessions)
        """

    def list_runs(self, arn: str, nextToken: str = None) -> ListRunsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.list_runs)
        [Show boto3-stubs documentation](./client.md#list-runs)
        """

    def list_samples(self, arn: str, nextToken: str = None) -> ListSamplesResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.list_samples)
        [Show boto3-stubs documentation](./client.md#list-samples)
        """

    def list_suites(self, arn: str, nextToken: str = None) -> ListSuitesResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.list_suites)
        [Show boto3-stubs documentation](./client.md#list-suites)
        """

    def list_tags_for_resource(self, ResourceARN: str) -> ListTagsForResourceResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](./client.md#list-tags-for-resource)
        """

    def list_test_grid_projects(
        self, maxResult: int = None, nextToken: str = None
    ) -> ListTestGridProjectsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.list_test_grid_projects)
        [Show boto3-stubs documentation](./client.md#list-test-grid-projects)
        """

    def list_test_grid_session_actions(
        self, sessionArn: str, maxResult: int = None, nextToken: str = None
    ) -> ListTestGridSessionActionsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.list_test_grid_session_actions)
        [Show boto3-stubs documentation](./client.md#list-test-grid-session-actions)
        """

    def list_test_grid_session_artifacts(
        self,
        sessionArn: str,
        type: TestGridSessionArtifactCategory = None,
        maxResult: int = None,
        nextToken: str = None,
    ) -> ListTestGridSessionArtifactsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.list_test_grid_session_artifacts)
        [Show boto3-stubs documentation](./client.md#list-test-grid-session-artifacts)
        """

    def list_test_grid_sessions(
        self,
        projectArn: str,
        status: TestGridSessionStatus = None,
        creationTimeAfter: datetime = None,
        creationTimeBefore: datetime = None,
        endTimeAfter: datetime = None,
        endTimeBefore: datetime = None,
        maxResult: int = None,
        nextToken: str = None,
    ) -> ListTestGridSessionsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.list_test_grid_sessions)
        [Show boto3-stubs documentation](./client.md#list-test-grid-sessions)
        """

    def list_tests(self, arn: str, nextToken: str = None) -> ListTestsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.list_tests)
        [Show boto3-stubs documentation](./client.md#list-tests)
        """

    def list_unique_problems(
        self, arn: str, nextToken: str = None
    ) -> ListUniqueProblemsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.list_unique_problems)
        [Show boto3-stubs documentation](./client.md#list-unique-problems)
        """

    def list_uploads(
        self, arn: str, type: UploadType = None, nextToken: str = None
    ) -> ListUploadsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.list_uploads)
        [Show boto3-stubs documentation](./client.md#list-uploads)
        """

    def list_vpce_configurations(
        self, maxResults: int = None, nextToken: str = None
    ) -> ListVPCEConfigurationsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.list_vpce_configurations)
        [Show boto3-stubs documentation](./client.md#list-vpce-configurations)
        """

    def purchase_offering(
        self, offeringId: str = None, quantity: int = None, offeringPromotionId: str = None
    ) -> PurchaseOfferingResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.purchase_offering)
        [Show boto3-stubs documentation](./client.md#purchase-offering)
        """

    def renew_offering(
        self, offeringId: str = None, quantity: int = None
    ) -> RenewOfferingResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.renew_offering)
        [Show boto3-stubs documentation](./client.md#renew-offering)
        """

    def schedule_run(
        self,
        projectArn: str,
        test: ScheduleRunTestTypeDef,
        appArn: str = None,
        devicePoolArn: str = None,
        deviceSelectionConfiguration: DeviceSelectionConfigurationTypeDef = None,
        name: str = None,
        configuration: ScheduleRunConfigurationTypeDef = None,
        executionConfiguration: ExecutionConfigurationTypeDef = None,
    ) -> ScheduleRunResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.schedule_run)
        [Show boto3-stubs documentation](./client.md#schedule-run)
        """

    def stop_job(self, arn: str) -> StopJobResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.stop_job)
        [Show boto3-stubs documentation](./client.md#stop-job)
        """

    def stop_remote_access_session(self, arn: str) -> StopRemoteAccessSessionResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.stop_remote_access_session)
        [Show boto3-stubs documentation](./client.md#stop-remote-access-session)
        """

    def stop_run(self, arn: str) -> StopRunResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.stop_run)
        [Show boto3-stubs documentation](./client.md#stop-run)
        """

    def tag_resource(self, ResourceARN: str, Tags: List["TagTypeDef"]) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.tag_resource)
        [Show boto3-stubs documentation](./client.md#tag-resource)
        """

    def untag_resource(self, ResourceARN: str, TagKeys: List[str]) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.untag_resource)
        [Show boto3-stubs documentation](./client.md#untag-resource)
        """

    def update_device_instance(
        self, arn: str, profileArn: str = None, labels: List[str] = None
    ) -> UpdateDeviceInstanceResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.update_device_instance)
        [Show boto3-stubs documentation](./client.md#update-device-instance)
        """

    def update_device_pool(
        self,
        arn: str,
        name: str = None,
        description: str = None,
        rules: List["RuleTypeDef"] = None,
        maxDevices: int = None,
        clearMaxDevices: bool = None,
    ) -> UpdateDevicePoolResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.update_device_pool)
        [Show boto3-stubs documentation](./client.md#update-device-pool)
        """

    def update_instance_profile(
        self,
        arn: str,
        name: str = None,
        description: str = None,
        packageCleanup: bool = None,
        excludeAppPackagesFromCleanup: List[str] = None,
        rebootAfterUse: bool = None,
    ) -> UpdateInstanceProfileResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.update_instance_profile)
        [Show boto3-stubs documentation](./client.md#update-instance-profile)
        """

    def update_network_profile(
        self,
        arn: str,
        name: str = None,
        description: str = None,
        type: NetworkProfileType = None,
        uplinkBandwidthBits: int = None,
        downlinkBandwidthBits: int = None,
        uplinkDelayMs: int = None,
        downlinkDelayMs: int = None,
        uplinkJitterMs: int = None,
        downlinkJitterMs: int = None,
        uplinkLossPercent: int = None,
        downlinkLossPercent: int = None,
    ) -> UpdateNetworkProfileResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.update_network_profile)
        [Show boto3-stubs documentation](./client.md#update-network-profile)
        """

    def update_project(
        self, arn: str, name: str = None, defaultJobTimeoutMinutes: int = None
    ) -> UpdateProjectResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.update_project)
        [Show boto3-stubs documentation](./client.md#update-project)
        """

    def update_test_grid_project(
        self, projectArn: str, name: str = None, description: str = None
    ) -> UpdateTestGridProjectResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.update_test_grid_project)
        [Show boto3-stubs documentation](./client.md#update-test-grid-project)
        """

    def update_upload(
        self, arn: str, name: str = None, contentType: str = None, editContent: bool = None
    ) -> UpdateUploadResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.update_upload)
        [Show boto3-stubs documentation](./client.md#update-upload)
        """

    def update_vpce_configuration(
        self,
        arn: str,
        vpceConfigurationName: str = None,
        vpceServiceName: str = None,
        serviceDnsName: str = None,
        vpceConfigurationDescription: str = None,
    ) -> UpdateVPCEConfigurationResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Client.update_vpce_configuration)
        [Show boto3-stubs documentation](./client.md#update-vpce-configuration)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_offering_status"]
    ) -> GetOfferingStatusPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Paginator.GetOfferingStatus)[Show boto3-stubs documentation](./paginators.md#getofferingstatuspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_artifacts"]) -> ListArtifactsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Paginator.ListArtifacts)[Show boto3-stubs documentation](./paginators.md#listartifactspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_device_instances"]
    ) -> ListDeviceInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Paginator.ListDeviceInstances)[Show boto3-stubs documentation](./paginators.md#listdeviceinstancespaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_device_pools"]
    ) -> ListDevicePoolsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Paginator.ListDevicePools)[Show boto3-stubs documentation](./paginators.md#listdevicepoolspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_devices"]) -> ListDevicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Paginator.ListDevices)[Show boto3-stubs documentation](./paginators.md#listdevicespaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_instance_profiles"]
    ) -> ListInstanceProfilesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Paginator.ListInstanceProfiles)[Show boto3-stubs documentation](./paginators.md#listinstanceprofilespaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_jobs"]) -> ListJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Paginator.ListJobs)[Show boto3-stubs documentation](./paginators.md#listjobspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_network_profiles"]
    ) -> ListNetworkProfilesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Paginator.ListNetworkProfiles)[Show boto3-stubs documentation](./paginators.md#listnetworkprofilespaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_offering_promotions"]
    ) -> ListOfferingPromotionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Paginator.ListOfferingPromotions)[Show boto3-stubs documentation](./paginators.md#listofferingpromotionspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_offering_transactions"]
    ) -> ListOfferingTransactionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Paginator.ListOfferingTransactions)[Show boto3-stubs documentation](./paginators.md#listofferingtransactionspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_offerings"]) -> ListOfferingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Paginator.ListOfferings)[Show boto3-stubs documentation](./paginators.md#listofferingspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_projects"]) -> ListProjectsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Paginator.ListProjects)[Show boto3-stubs documentation](./paginators.md#listprojectspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_remote_access_sessions"]
    ) -> ListRemoteAccessSessionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Paginator.ListRemoteAccessSessions)[Show boto3-stubs documentation](./paginators.md#listremoteaccesssessionspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_runs"]) -> ListRunsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Paginator.ListRuns)[Show boto3-stubs documentation](./paginators.md#listrunspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_samples"]) -> ListSamplesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Paginator.ListSamples)[Show boto3-stubs documentation](./paginators.md#listsamplespaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_suites"]) -> ListSuitesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Paginator.ListSuites)[Show boto3-stubs documentation](./paginators.md#listsuitespaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tests"]) -> ListTestsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Paginator.ListTests)[Show boto3-stubs documentation](./paginators.md#listtestspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_unique_problems"]
    ) -> ListUniqueProblemsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Paginator.ListUniqueProblems)[Show boto3-stubs documentation](./paginators.md#listuniqueproblemspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_uploads"]) -> ListUploadsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Paginator.ListUploads)[Show boto3-stubs documentation](./paginators.md#listuploadspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_vpce_configurations"]
    ) -> ListVPCEConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.69/reference/services/devicefarm.html#DeviceFarm.Paginator.ListVPCEConfigurations)[Show boto3-stubs documentation](./paginators.md#listvpceconfigurationspaginator)
        """
