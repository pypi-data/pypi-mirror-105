"""
Type annotations for devicefarm service literal definitions.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_devicefarm/literals.html)

Usage::

    ```python
    from mypy_boto3_devicefarm.literals import ArtifactCategory

    data: ArtifactCategory = "FILE"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "ArtifactCategory",
    "ArtifactType",
    "BillingMethod",
    "CurrencyCode",
    "DeviceAttribute",
    "DeviceAvailability",
    "DeviceFilterAttribute",
    "DeviceFormFactor",
    "DevicePlatform",
    "DevicePoolType",
    "ExecutionResult",
    "ExecutionResultCode",
    "ExecutionStatus",
    "GetOfferingStatusPaginatorName",
    "InstanceStatus",
    "InteractionMode",
    "ListArtifactsPaginatorName",
    "ListDeviceInstancesPaginatorName",
    "ListDevicePoolsPaginatorName",
    "ListDevicesPaginatorName",
    "ListInstanceProfilesPaginatorName",
    "ListJobsPaginatorName",
    "ListNetworkProfilesPaginatorName",
    "ListOfferingPromotionsPaginatorName",
    "ListOfferingTransactionsPaginatorName",
    "ListOfferingsPaginatorName",
    "ListProjectsPaginatorName",
    "ListRemoteAccessSessionsPaginatorName",
    "ListRunsPaginatorName",
    "ListSamplesPaginatorName",
    "ListSuitesPaginatorName",
    "ListTestsPaginatorName",
    "ListUniqueProblemsPaginatorName",
    "ListUploadsPaginatorName",
    "ListVPCEConfigurationsPaginatorName",
    "NetworkProfileType",
    "OfferingTransactionType",
    "OfferingType",
    "RecurringChargeFrequency",
    "RuleOperator",
    "SampleType",
    "TestGridSessionArtifactCategory",
    "TestGridSessionArtifactType",
    "TestGridSessionStatus",
    "TestType",
    "UploadCategory",
    "UploadStatus",
    "UploadType",
)


ArtifactCategory = Literal["FILE", "LOG", "SCREENSHOT"]
ArtifactType = Literal[
    "APPIUM_JAVA_OUTPUT",
    "APPIUM_JAVA_XML_OUTPUT",
    "APPIUM_PYTHON_OUTPUT",
    "APPIUM_PYTHON_XML_OUTPUT",
    "APPIUM_SERVER_OUTPUT",
    "APPLICATION_CRASH_REPORT",
    "AUTOMATION_OUTPUT",
    "CALABASH_JAVA_XML_OUTPUT",
    "CALABASH_JSON_OUTPUT",
    "CALABASH_PRETTY_OUTPUT",
    "CALABASH_STANDARD_OUTPUT",
    "CUSTOMER_ARTIFACT",
    "CUSTOMER_ARTIFACT_LOG",
    "DEVICE_LOG",
    "EXERCISER_MONKEY_OUTPUT",
    "EXPLORER_EVENT_LOG",
    "EXPLORER_SUMMARY_LOG",
    "INSTRUMENTATION_OUTPUT",
    "MESSAGE_LOG",
    "RESULT_LOG",
    "SCREENSHOT",
    "SERVICE_LOG",
    "TESTSPEC_OUTPUT",
    "UNKNOWN",
    "VIDEO",
    "VIDEO_LOG",
    "WEBKIT_LOG",
    "XCTEST_LOG",
]
BillingMethod = Literal["METERED", "UNMETERED"]
CurrencyCode = Literal["USD"]
DeviceAttribute = Literal[
    "APPIUM_VERSION",
    "ARN",
    "AVAILABILITY",
    "FLEET_TYPE",
    "FORM_FACTOR",
    "INSTANCE_ARN",
    "INSTANCE_LABELS",
    "MANUFACTURER",
    "MODEL",
    "OS_VERSION",
    "PLATFORM",
    "REMOTE_ACCESS_ENABLED",
    "REMOTE_DEBUG_ENABLED",
]
DeviceAvailability = Literal["AVAILABLE", "BUSY", "HIGHLY_AVAILABLE", "TEMPORARY_NOT_AVAILABLE"]
DeviceFilterAttribute = Literal[
    "ARN",
    "AVAILABILITY",
    "FLEET_TYPE",
    "FORM_FACTOR",
    "INSTANCE_ARN",
    "INSTANCE_LABELS",
    "MANUFACTURER",
    "MODEL",
    "OS_VERSION",
    "PLATFORM",
    "REMOTE_ACCESS_ENABLED",
    "REMOTE_DEBUG_ENABLED",
]
DeviceFormFactor = Literal["PHONE", "TABLET"]
DevicePlatform = Literal["ANDROID", "IOS"]
DevicePoolType = Literal["CURATED", "PRIVATE"]
ExecutionResult = Literal["ERRORED", "FAILED", "PASSED", "PENDING", "SKIPPED", "STOPPED", "WARNED"]
ExecutionResultCode = Literal["PARSING_FAILED", "VPC_ENDPOINT_SETUP_FAILED"]
ExecutionStatus = Literal[
    "COMPLETED",
    "PENDING",
    "PENDING_CONCURRENCY",
    "PENDING_DEVICE",
    "PREPARING",
    "PROCESSING",
    "RUNNING",
    "SCHEDULING",
    "STOPPING",
]
GetOfferingStatusPaginatorName = Literal["get_offering_status"]
InstanceStatus = Literal["AVAILABLE", "IN_USE", "NOT_AVAILABLE", "PREPARING"]
InteractionMode = Literal["INTERACTIVE", "NO_VIDEO", "VIDEO_ONLY"]
ListArtifactsPaginatorName = Literal["list_artifacts"]
ListDeviceInstancesPaginatorName = Literal["list_device_instances"]
ListDevicePoolsPaginatorName = Literal["list_device_pools"]
ListDevicesPaginatorName = Literal["list_devices"]
ListInstanceProfilesPaginatorName = Literal["list_instance_profiles"]
ListJobsPaginatorName = Literal["list_jobs"]
ListNetworkProfilesPaginatorName = Literal["list_network_profiles"]
ListOfferingPromotionsPaginatorName = Literal["list_offering_promotions"]
ListOfferingTransactionsPaginatorName = Literal["list_offering_transactions"]
ListOfferingsPaginatorName = Literal["list_offerings"]
ListProjectsPaginatorName = Literal["list_projects"]
ListRemoteAccessSessionsPaginatorName = Literal["list_remote_access_sessions"]
ListRunsPaginatorName = Literal["list_runs"]
ListSamplesPaginatorName = Literal["list_samples"]
ListSuitesPaginatorName = Literal["list_suites"]
ListTestsPaginatorName = Literal["list_tests"]
ListUniqueProblemsPaginatorName = Literal["list_unique_problems"]
ListUploadsPaginatorName = Literal["list_uploads"]
ListVPCEConfigurationsPaginatorName = Literal["list_vpce_configurations"]
NetworkProfileType = Literal["CURATED", "PRIVATE"]
OfferingTransactionType = Literal["PURCHASE", "RENEW", "SYSTEM"]
OfferingType = Literal["RECURRING"]
RecurringChargeFrequency = Literal["MONTHLY"]
RuleOperator = Literal[
    "CONTAINS",
    "EQUALS",
    "GREATER_THAN",
    "GREATER_THAN_OR_EQUALS",
    "IN",
    "LESS_THAN",
    "LESS_THAN_OR_EQUALS",
    "NOT_IN",
]
SampleType = Literal[
    "CPU",
    "MEMORY",
    "NATIVE_AVG_DRAWTIME",
    "NATIVE_FPS",
    "NATIVE_FRAMES",
    "NATIVE_MAX_DRAWTIME",
    "NATIVE_MIN_DRAWTIME",
    "OPENGL_AVG_DRAWTIME",
    "OPENGL_FPS",
    "OPENGL_FRAMES",
    "OPENGL_MAX_DRAWTIME",
    "OPENGL_MIN_DRAWTIME",
    "RX",
    "RX_RATE",
    "THREADS",
    "TX",
    "TX_RATE",
]
TestGridSessionArtifactCategory = Literal["LOG", "VIDEO"]
TestGridSessionArtifactType = Literal["SELENIUM_LOG", "UNKNOWN", "VIDEO"]
TestGridSessionStatus = Literal["ACTIVE", "CLOSED", "ERRORED"]
TestType = Literal[
    "APPIUM_JAVA_JUNIT",
    "APPIUM_JAVA_TESTNG",
    "APPIUM_NODE",
    "APPIUM_PYTHON",
    "APPIUM_RUBY",
    "APPIUM_WEB_JAVA_JUNIT",
    "APPIUM_WEB_JAVA_TESTNG",
    "APPIUM_WEB_NODE",
    "APPIUM_WEB_PYTHON",
    "APPIUM_WEB_RUBY",
    "BUILTIN_EXPLORER",
    "BUILTIN_FUZZ",
    "CALABASH",
    "INSTRUMENTATION",
    "REMOTE_ACCESS_RECORD",
    "REMOTE_ACCESS_REPLAY",
    "UIAUTOMATION",
    "UIAUTOMATOR",
    "WEB_PERFORMANCE_PROFILE",
    "XCTEST",
    "XCTEST_UI",
]
UploadCategory = Literal["CURATED", "PRIVATE"]
UploadStatus = Literal["FAILED", "INITIALIZED", "PROCESSING", "SUCCEEDED"]
UploadType = Literal[
    "ANDROID_APP",
    "APPIUM_JAVA_JUNIT_TEST_PACKAGE",
    "APPIUM_JAVA_JUNIT_TEST_SPEC",
    "APPIUM_JAVA_TESTNG_TEST_PACKAGE",
    "APPIUM_JAVA_TESTNG_TEST_SPEC",
    "APPIUM_NODE_TEST_PACKAGE",
    "APPIUM_NODE_TEST_SPEC",
    "APPIUM_PYTHON_TEST_PACKAGE",
    "APPIUM_PYTHON_TEST_SPEC",
    "APPIUM_RUBY_TEST_PACKAGE",
    "APPIUM_RUBY_TEST_SPEC",
    "APPIUM_WEB_JAVA_JUNIT_TEST_PACKAGE",
    "APPIUM_WEB_JAVA_JUNIT_TEST_SPEC",
    "APPIUM_WEB_JAVA_TESTNG_TEST_PACKAGE",
    "APPIUM_WEB_JAVA_TESTNG_TEST_SPEC",
    "APPIUM_WEB_NODE_TEST_PACKAGE",
    "APPIUM_WEB_NODE_TEST_SPEC",
    "APPIUM_WEB_PYTHON_TEST_PACKAGE",
    "APPIUM_WEB_PYTHON_TEST_SPEC",
    "APPIUM_WEB_RUBY_TEST_PACKAGE",
    "APPIUM_WEB_RUBY_TEST_SPEC",
    "CALABASH_TEST_PACKAGE",
    "EXTERNAL_DATA",
    "INSTRUMENTATION_TEST_PACKAGE",
    "INSTRUMENTATION_TEST_SPEC",
    "IOS_APP",
    "UIAUTOMATION_TEST_PACKAGE",
    "UIAUTOMATOR_TEST_PACKAGE",
    "WEB_APP",
    "XCTEST_TEST_PACKAGE",
    "XCTEST_UI_TEST_PACKAGE",
    "XCTEST_UI_TEST_SPEC",
]
