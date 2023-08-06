"""
Type annotations for lightsail service client.

[Open documentation](./client.md)

Usage::

    ```python
    import boto3
    from mypy_boto3_lightsail import LightsailClient

    client: LightsailClient = boto3.client("lightsail")
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Type, overload

from botocore.client import ClientMeta

from mypy_boto3_lightsail.paginator import (
    GetActiveNamesPaginator,
    GetBlueprintsPaginator,
    GetBundlesPaginator,
    GetCloudFormationStackRecordsPaginator,
    GetDiskSnapshotsPaginator,
    GetDisksPaginator,
    GetDomainsPaginator,
    GetExportSnapshotRecordsPaginator,
    GetInstanceSnapshotsPaginator,
    GetInstancesPaginator,
    GetKeyPairsPaginator,
    GetLoadBalancersPaginator,
    GetOperationsPaginator,
    GetRelationalDatabaseBlueprintsPaginator,
    GetRelationalDatabaseBundlesPaginator,
    GetRelationalDatabaseEventsPaginator,
    GetRelationalDatabaseParametersPaginator,
    GetRelationalDatabaseSnapshotsPaginator,
    GetRelationalDatabasesPaginator,
    GetStaticIpsPaginator,
)

from .literals import (
    AlarmState,
    CertificateStatus,
    ComparisonOperator,
    ContactProtocol,
    ContainerServiceMetricName,
    ContainerServicePowerName,
    DistributionMetricName,
    InstanceAccessProtocol,
    InstanceMetricName,
    IpAddressType,
    LoadBalancerAttributeName,
    LoadBalancerMetricName,
    MetricName,
    MetricStatistic,
    MetricUnit,
    RegionName,
    RelationalDatabaseMetricName,
    RelationalDatabasePasswordVersion,
    ResourceType,
    TreatMissingData,
)
from .type_defs import (
    AddOnRequestTypeDef,
    AllocateStaticIpResultTypeDef,
    AttachCertificateToDistributionResultTypeDef,
    AttachDiskResultTypeDef,
    AttachInstancesToLoadBalancerResultTypeDef,
    AttachLoadBalancerTlsCertificateResultTypeDef,
    AttachStaticIpResultTypeDef,
    CacheBehaviorPerPathTypeDef,
    CacheBehaviorTypeDef,
    CacheSettingsTypeDef,
    CloseInstancePublicPortsResultTypeDef,
    ContainerServiceDeploymentRequestTypeDef,
    ContainerServicesListResultTypeDef,
    ContainerTypeDef,
    CopySnapshotResultTypeDef,
    CreateCertificateResultTypeDef,
    CreateCloudFormationStackResultTypeDef,
    CreateContactMethodResultTypeDef,
    CreateContainerServiceDeploymentResultTypeDef,
    CreateContainerServiceRegistryLoginResultTypeDef,
    CreateContainerServiceResultTypeDef,
    CreateDiskFromSnapshotResultTypeDef,
    CreateDiskResultTypeDef,
    CreateDiskSnapshotResultTypeDef,
    CreateDistributionResultTypeDef,
    CreateDomainEntryResultTypeDef,
    CreateDomainResultTypeDef,
    CreateInstancesFromSnapshotResultTypeDef,
    CreateInstanceSnapshotResultTypeDef,
    CreateInstancesResultTypeDef,
    CreateKeyPairResultTypeDef,
    CreateLoadBalancerResultTypeDef,
    CreateLoadBalancerTlsCertificateResultTypeDef,
    CreateRelationalDatabaseFromSnapshotResultTypeDef,
    CreateRelationalDatabaseResultTypeDef,
    CreateRelationalDatabaseSnapshotResultTypeDef,
    DeleteAlarmResultTypeDef,
    DeleteAutoSnapshotResultTypeDef,
    DeleteCertificateResultTypeDef,
    DeleteContactMethodResultTypeDef,
    DeleteDiskResultTypeDef,
    DeleteDiskSnapshotResultTypeDef,
    DeleteDistributionResultTypeDef,
    DeleteDomainEntryResultTypeDef,
    DeleteDomainResultTypeDef,
    DeleteInstanceResultTypeDef,
    DeleteInstanceSnapshotResultTypeDef,
    DeleteKeyPairResultTypeDef,
    DeleteKnownHostKeysResultTypeDef,
    DeleteLoadBalancerResultTypeDef,
    DeleteLoadBalancerTlsCertificateResultTypeDef,
    DeleteRelationalDatabaseResultTypeDef,
    DeleteRelationalDatabaseSnapshotResultTypeDef,
    DetachCertificateFromDistributionResultTypeDef,
    DetachDiskResultTypeDef,
    DetachInstancesFromLoadBalancerResultTypeDef,
    DetachStaticIpResultTypeDef,
    DisableAddOnResultTypeDef,
    DiskMapTypeDef,
    DomainEntryTypeDef,
    DownloadDefaultKeyPairResultTypeDef,
    EnableAddOnResultTypeDef,
    EndpointRequestTypeDef,
    ExportSnapshotResultTypeDef,
    GetActiveNamesResultTypeDef,
    GetAlarmsResultTypeDef,
    GetAutoSnapshotsResultTypeDef,
    GetBlueprintsResultTypeDef,
    GetBundlesResultTypeDef,
    GetCertificatesResultTypeDef,
    GetCloudFormationStackRecordsResultTypeDef,
    GetContactMethodsResultTypeDef,
    GetContainerAPIMetadataResultTypeDef,
    GetContainerImagesResultTypeDef,
    GetContainerLogResultTypeDef,
    GetContainerServiceDeploymentsResultTypeDef,
    GetContainerServiceMetricDataResultTypeDef,
    GetContainerServicePowersResultTypeDef,
    GetDiskResultTypeDef,
    GetDiskSnapshotResultTypeDef,
    GetDiskSnapshotsResultTypeDef,
    GetDisksResultTypeDef,
    GetDistributionBundlesResultTypeDef,
    GetDistributionLatestCacheResetResultTypeDef,
    GetDistributionMetricDataResultTypeDef,
    GetDistributionsResultTypeDef,
    GetDomainResultTypeDef,
    GetDomainsResultTypeDef,
    GetExportSnapshotRecordsResultTypeDef,
    GetInstanceAccessDetailsResultTypeDef,
    GetInstanceMetricDataResultTypeDef,
    GetInstancePortStatesResultTypeDef,
    GetInstanceResultTypeDef,
    GetInstanceSnapshotResultTypeDef,
    GetInstanceSnapshotsResultTypeDef,
    GetInstancesResultTypeDef,
    GetInstanceStateResultTypeDef,
    GetKeyPairResultTypeDef,
    GetKeyPairsResultTypeDef,
    GetLoadBalancerMetricDataResultTypeDef,
    GetLoadBalancerResultTypeDef,
    GetLoadBalancersResultTypeDef,
    GetLoadBalancerTlsCertificatesResultTypeDef,
    GetOperationResultTypeDef,
    GetOperationsForResourceResultTypeDef,
    GetOperationsResultTypeDef,
    GetRegionsResultTypeDef,
    GetRelationalDatabaseBlueprintsResultTypeDef,
    GetRelationalDatabaseBundlesResultTypeDef,
    GetRelationalDatabaseEventsResultTypeDef,
    GetRelationalDatabaseLogEventsResultTypeDef,
    GetRelationalDatabaseLogStreamsResultTypeDef,
    GetRelationalDatabaseMasterUserPasswordResultTypeDef,
    GetRelationalDatabaseMetricDataResultTypeDef,
    GetRelationalDatabaseParametersResultTypeDef,
    GetRelationalDatabaseResultTypeDef,
    GetRelationalDatabaseSnapshotResultTypeDef,
    GetRelationalDatabaseSnapshotsResultTypeDef,
    GetRelationalDatabasesResultTypeDef,
    GetStaticIpResultTypeDef,
    GetStaticIpsResultTypeDef,
    ImportKeyPairResultTypeDef,
    InputOriginTypeDef,
    InstanceEntryTypeDef,
    IsVpcPeeredResultTypeDef,
    OpenInstancePublicPortsResultTypeDef,
    PeerVpcResultTypeDef,
    PortInfoTypeDef,
    PutAlarmResultTypeDef,
    PutInstancePublicPortsResultTypeDef,
    RebootInstanceResultTypeDef,
    RebootRelationalDatabaseResultTypeDef,
    RegisterContainerImageResultTypeDef,
    RelationalDatabaseParameterTypeDef,
    ReleaseStaticIpResultTypeDef,
    ResetDistributionCacheResultTypeDef,
    SendContactMethodVerificationResultTypeDef,
    SetIpAddressTypeResultTypeDef,
    StartInstanceResultTypeDef,
    StartRelationalDatabaseResultTypeDef,
    StopInstanceResultTypeDef,
    StopRelationalDatabaseResultTypeDef,
    TagResourceResultTypeDef,
    TagTypeDef,
    TestAlarmResultTypeDef,
    UnpeerVpcResultTypeDef,
    UntagResourceResultTypeDef,
    UpdateContainerServiceResultTypeDef,
    UpdateDistributionBundleResultTypeDef,
    UpdateDistributionResultTypeDef,
    UpdateDomainEntryResultTypeDef,
    UpdateLoadBalancerAttributeResultTypeDef,
    UpdateRelationalDatabaseParametersResultTypeDef,
    UpdateRelationalDatabaseResultTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("LightsailClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    AccountSetupInProgressException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    OperationFailureException: Type[BotocoreClientError]
    ServiceException: Type[BotocoreClientError]
    UnauthenticatedException: Type[BotocoreClientError]


class LightsailClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client)
    [Show boto3-stubs documentation](./client.md)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def allocate_static_ip(self, staticIpName: str) -> AllocateStaticIpResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.allocate_static_ip)
        [Show boto3-stubs documentation](./client.md#allocate-static-ip)
        """

    def attach_certificate_to_distribution(
        self, distributionName: str, certificateName: str
    ) -> AttachCertificateToDistributionResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.attach_certificate_to_distribution)
        [Show boto3-stubs documentation](./client.md#attach-certificate-to-distribution)
        """

    def attach_disk(
        self, diskName: str, instanceName: str, diskPath: str
    ) -> AttachDiskResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.attach_disk)
        [Show boto3-stubs documentation](./client.md#attach-disk)
        """

    def attach_instances_to_load_balancer(
        self, loadBalancerName: str, instanceNames: List[str]
    ) -> AttachInstancesToLoadBalancerResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.attach_instances_to_load_balancer)
        [Show boto3-stubs documentation](./client.md#attach-instances-to-load-balancer)
        """

    def attach_load_balancer_tls_certificate(
        self, loadBalancerName: str, certificateName: str
    ) -> AttachLoadBalancerTlsCertificateResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.attach_load_balancer_tls_certificate)
        [Show boto3-stubs documentation](./client.md#attach-load-balancer-tls-certificate)
        """

    def attach_static_ip(self, staticIpName: str, instanceName: str) -> AttachStaticIpResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.attach_static_ip)
        [Show boto3-stubs documentation](./client.md#attach-static-ip)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.can_paginate)
        [Show boto3-stubs documentation](./client.md#can-paginate)
        """

    def close_instance_public_ports(
        self, portInfo: PortInfoTypeDef, instanceName: str
    ) -> CloseInstancePublicPortsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.close_instance_public_ports)
        [Show boto3-stubs documentation](./client.md#close-instance-public-ports)
        """

    def copy_snapshot(
        self,
        targetSnapshotName: str,
        sourceRegion: RegionName,
        sourceSnapshotName: str = None,
        sourceResourceName: str = None,
        restoreDate: str = None,
        useLatestRestorableAutoSnapshot: bool = None,
    ) -> CopySnapshotResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.copy_snapshot)
        [Show boto3-stubs documentation](./client.md#copy-snapshot)
        """

    def create_certificate(
        self,
        certificateName: str,
        domainName: str,
        subjectAlternativeNames: List[str] = None,
        tags: List["TagTypeDef"] = None,
    ) -> CreateCertificateResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.create_certificate)
        [Show boto3-stubs documentation](./client.md#create-certificate)
        """

    def create_cloud_formation_stack(
        self, instances: List[InstanceEntryTypeDef]
    ) -> CreateCloudFormationStackResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.create_cloud_formation_stack)
        [Show boto3-stubs documentation](./client.md#create-cloud-formation-stack)
        """

    def create_contact_method(
        self, protocol: ContactProtocol, contactEndpoint: str
    ) -> CreateContactMethodResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.create_contact_method)
        [Show boto3-stubs documentation](./client.md#create-contact-method)
        """

    def create_container_service(
        self,
        serviceName: str,
        power: ContainerServicePowerName,
        scale: int,
        tags: List["TagTypeDef"] = None,
        publicDomainNames: Dict[str, List[str]] = None,
        deployment: ContainerServiceDeploymentRequestTypeDef = None,
    ) -> CreateContainerServiceResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.create_container_service)
        [Show boto3-stubs documentation](./client.md#create-container-service)
        """

    def create_container_service_deployment(
        self,
        serviceName: str,
        containers: Dict[str, "ContainerTypeDef"] = None,
        publicEndpoint: "EndpointRequestTypeDef" = None,
    ) -> CreateContainerServiceDeploymentResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.create_container_service_deployment)
        [Show boto3-stubs documentation](./client.md#create-container-service-deployment)
        """

    def create_container_service_registry_login(
        self,
    ) -> CreateContainerServiceRegistryLoginResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.create_container_service_registry_login)
        [Show boto3-stubs documentation](./client.md#create-container-service-registry-login)
        """

    def create_disk(
        self,
        diskName: str,
        availabilityZone: str,
        sizeInGb: int,
        tags: List["TagTypeDef"] = None,
        addOns: List[AddOnRequestTypeDef] = None,
    ) -> CreateDiskResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.create_disk)
        [Show boto3-stubs documentation](./client.md#create-disk)
        """

    def create_disk_from_snapshot(
        self,
        diskName: str,
        availabilityZone: str,
        sizeInGb: int,
        diskSnapshotName: str = None,
        tags: List["TagTypeDef"] = None,
        addOns: List[AddOnRequestTypeDef] = None,
        sourceDiskName: str = None,
        restoreDate: str = None,
        useLatestRestorableAutoSnapshot: bool = None,
    ) -> CreateDiskFromSnapshotResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.create_disk_from_snapshot)
        [Show boto3-stubs documentation](./client.md#create-disk-from-snapshot)
        """

    def create_disk_snapshot(
        self,
        diskSnapshotName: str,
        diskName: str = None,
        instanceName: str = None,
        tags: List["TagTypeDef"] = None,
    ) -> CreateDiskSnapshotResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.create_disk_snapshot)
        [Show boto3-stubs documentation](./client.md#create-disk-snapshot)
        """

    def create_distribution(
        self,
        distributionName: str,
        origin: InputOriginTypeDef,
        defaultCacheBehavior: "CacheBehaviorTypeDef",
        bundleId: str,
        cacheBehaviorSettings: "CacheSettingsTypeDef" = None,
        cacheBehaviors: List["CacheBehaviorPerPathTypeDef"] = None,
        ipAddressType: IpAddressType = None,
        tags: List["TagTypeDef"] = None,
    ) -> CreateDistributionResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.create_distribution)
        [Show boto3-stubs documentation](./client.md#create-distribution)
        """

    def create_domain(
        self, domainName: str, tags: List["TagTypeDef"] = None
    ) -> CreateDomainResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.create_domain)
        [Show boto3-stubs documentation](./client.md#create-domain)
        """

    def create_domain_entry(
        self, domainName: str, domainEntry: "DomainEntryTypeDef"
    ) -> CreateDomainEntryResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.create_domain_entry)
        [Show boto3-stubs documentation](./client.md#create-domain-entry)
        """

    def create_instance_snapshot(
        self, instanceSnapshotName: str, instanceName: str, tags: List["TagTypeDef"] = None
    ) -> CreateInstanceSnapshotResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.create_instance_snapshot)
        [Show boto3-stubs documentation](./client.md#create-instance-snapshot)
        """

    def create_instances(
        self,
        instanceNames: List[str],
        availabilityZone: str,
        blueprintId: str,
        bundleId: str,
        customImageName: str = None,
        userData: str = None,
        keyPairName: str = None,
        tags: List["TagTypeDef"] = None,
        addOns: List[AddOnRequestTypeDef] = None,
        ipAddressType: IpAddressType = None,
    ) -> CreateInstancesResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.create_instances)
        [Show boto3-stubs documentation](./client.md#create-instances)
        """

    def create_instances_from_snapshot(
        self,
        instanceNames: List[str],
        availabilityZone: str,
        bundleId: str,
        attachedDiskMapping: Dict[str, List[DiskMapTypeDef]] = None,
        instanceSnapshotName: str = None,
        userData: str = None,
        keyPairName: str = None,
        tags: List["TagTypeDef"] = None,
        addOns: List[AddOnRequestTypeDef] = None,
        ipAddressType: IpAddressType = None,
        sourceInstanceName: str = None,
        restoreDate: str = None,
        useLatestRestorableAutoSnapshot: bool = None,
    ) -> CreateInstancesFromSnapshotResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.create_instances_from_snapshot)
        [Show boto3-stubs documentation](./client.md#create-instances-from-snapshot)
        """

    def create_key_pair(
        self, keyPairName: str, tags: List["TagTypeDef"] = None
    ) -> CreateKeyPairResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.create_key_pair)
        [Show boto3-stubs documentation](./client.md#create-key-pair)
        """

    def create_load_balancer(
        self,
        loadBalancerName: str,
        instancePort: int,
        healthCheckPath: str = None,
        certificateName: str = None,
        certificateDomainName: str = None,
        certificateAlternativeNames: List[str] = None,
        tags: List["TagTypeDef"] = None,
        ipAddressType: IpAddressType = None,
    ) -> CreateLoadBalancerResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.create_load_balancer)
        [Show boto3-stubs documentation](./client.md#create-load-balancer)
        """

    def create_load_balancer_tls_certificate(
        self,
        loadBalancerName: str,
        certificateName: str,
        certificateDomainName: str,
        certificateAlternativeNames: List[str] = None,
        tags: List["TagTypeDef"] = None,
    ) -> CreateLoadBalancerTlsCertificateResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.create_load_balancer_tls_certificate)
        [Show boto3-stubs documentation](./client.md#create-load-balancer-tls-certificate)
        """

    def create_relational_database(
        self,
        relationalDatabaseName: str,
        relationalDatabaseBlueprintId: str,
        relationalDatabaseBundleId: str,
        masterDatabaseName: str,
        masterUsername: str,
        availabilityZone: str = None,
        masterUserPassword: str = None,
        preferredBackupWindow: str = None,
        preferredMaintenanceWindow: str = None,
        publiclyAccessible: bool = None,
        tags: List["TagTypeDef"] = None,
    ) -> CreateRelationalDatabaseResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.create_relational_database)
        [Show boto3-stubs documentation](./client.md#create-relational-database)
        """

    def create_relational_database_from_snapshot(
        self,
        relationalDatabaseName: str,
        availabilityZone: str = None,
        publiclyAccessible: bool = None,
        relationalDatabaseSnapshotName: str = None,
        relationalDatabaseBundleId: str = None,
        sourceRelationalDatabaseName: str = None,
        restoreTime: datetime = None,
        useLatestRestorableTime: bool = None,
        tags: List["TagTypeDef"] = None,
    ) -> CreateRelationalDatabaseFromSnapshotResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.create_relational_database_from_snapshot)
        [Show boto3-stubs documentation](./client.md#create-relational-database-from-snapshot)
        """

    def create_relational_database_snapshot(
        self,
        relationalDatabaseName: str,
        relationalDatabaseSnapshotName: str,
        tags: List["TagTypeDef"] = None,
    ) -> CreateRelationalDatabaseSnapshotResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.create_relational_database_snapshot)
        [Show boto3-stubs documentation](./client.md#create-relational-database-snapshot)
        """

    def delete_alarm(self, alarmName: str) -> DeleteAlarmResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.delete_alarm)
        [Show boto3-stubs documentation](./client.md#delete-alarm)
        """

    def delete_auto_snapshot(self, resourceName: str, date: str) -> DeleteAutoSnapshotResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.delete_auto_snapshot)
        [Show boto3-stubs documentation](./client.md#delete-auto-snapshot)
        """

    def delete_certificate(self, certificateName: str) -> DeleteCertificateResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.delete_certificate)
        [Show boto3-stubs documentation](./client.md#delete-certificate)
        """

    def delete_contact_method(self, protocol: ContactProtocol) -> DeleteContactMethodResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.delete_contact_method)
        [Show boto3-stubs documentation](./client.md#delete-contact-method)
        """

    def delete_container_image(self, serviceName: str, image: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.delete_container_image)
        [Show boto3-stubs documentation](./client.md#delete-container-image)
        """

    def delete_container_service(self, serviceName: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.delete_container_service)
        [Show boto3-stubs documentation](./client.md#delete-container-service)
        """

    def delete_disk(self, diskName: str, forceDeleteAddOns: bool = None) -> DeleteDiskResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.delete_disk)
        [Show boto3-stubs documentation](./client.md#delete-disk)
        """

    def delete_disk_snapshot(self, diskSnapshotName: str) -> DeleteDiskSnapshotResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.delete_disk_snapshot)
        [Show boto3-stubs documentation](./client.md#delete-disk-snapshot)
        """

    def delete_distribution(self, distributionName: str = None) -> DeleteDistributionResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.delete_distribution)
        [Show boto3-stubs documentation](./client.md#delete-distribution)
        """

    def delete_domain(self, domainName: str) -> DeleteDomainResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.delete_domain)
        [Show boto3-stubs documentation](./client.md#delete-domain)
        """

    def delete_domain_entry(
        self, domainName: str, domainEntry: "DomainEntryTypeDef"
    ) -> DeleteDomainEntryResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.delete_domain_entry)
        [Show boto3-stubs documentation](./client.md#delete-domain-entry)
        """

    def delete_instance(
        self, instanceName: str, forceDeleteAddOns: bool = None
    ) -> DeleteInstanceResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.delete_instance)
        [Show boto3-stubs documentation](./client.md#delete-instance)
        """

    def delete_instance_snapshot(
        self, instanceSnapshotName: str
    ) -> DeleteInstanceSnapshotResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.delete_instance_snapshot)
        [Show boto3-stubs documentation](./client.md#delete-instance-snapshot)
        """

    def delete_key_pair(self, keyPairName: str) -> DeleteKeyPairResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.delete_key_pair)
        [Show boto3-stubs documentation](./client.md#delete-key-pair)
        """

    def delete_known_host_keys(self, instanceName: str) -> DeleteKnownHostKeysResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.delete_known_host_keys)
        [Show boto3-stubs documentation](./client.md#delete-known-host-keys)
        """

    def delete_load_balancer(self, loadBalancerName: str) -> DeleteLoadBalancerResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.delete_load_balancer)
        [Show boto3-stubs documentation](./client.md#delete-load-balancer)
        """

    def delete_load_balancer_tls_certificate(
        self, loadBalancerName: str, certificateName: str, force: bool = None
    ) -> DeleteLoadBalancerTlsCertificateResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.delete_load_balancer_tls_certificate)
        [Show boto3-stubs documentation](./client.md#delete-load-balancer-tls-certificate)
        """

    def delete_relational_database(
        self,
        relationalDatabaseName: str,
        skipFinalSnapshot: bool = None,
        finalRelationalDatabaseSnapshotName: str = None,
    ) -> DeleteRelationalDatabaseResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.delete_relational_database)
        [Show boto3-stubs documentation](./client.md#delete-relational-database)
        """

    def delete_relational_database_snapshot(
        self, relationalDatabaseSnapshotName: str
    ) -> DeleteRelationalDatabaseSnapshotResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.delete_relational_database_snapshot)
        [Show boto3-stubs documentation](./client.md#delete-relational-database-snapshot)
        """

    def detach_certificate_from_distribution(
        self, distributionName: str
    ) -> DetachCertificateFromDistributionResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.detach_certificate_from_distribution)
        [Show boto3-stubs documentation](./client.md#detach-certificate-from-distribution)
        """

    def detach_disk(self, diskName: str) -> DetachDiskResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.detach_disk)
        [Show boto3-stubs documentation](./client.md#detach-disk)
        """

    def detach_instances_from_load_balancer(
        self, loadBalancerName: str, instanceNames: List[str]
    ) -> DetachInstancesFromLoadBalancerResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.detach_instances_from_load_balancer)
        [Show boto3-stubs documentation](./client.md#detach-instances-from-load-balancer)
        """

    def detach_static_ip(self, staticIpName: str) -> DetachStaticIpResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.detach_static_ip)
        [Show boto3-stubs documentation](./client.md#detach-static-ip)
        """

    def disable_add_on(
        self, addOnType: Literal["AutoSnapshot"], resourceName: str
    ) -> DisableAddOnResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.disable_add_on)
        [Show boto3-stubs documentation](./client.md#disable-add-on)
        """

    def download_default_key_pair(self) -> DownloadDefaultKeyPairResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.download_default_key_pair)
        [Show boto3-stubs documentation](./client.md#download-default-key-pair)
        """

    def enable_add_on(
        self, resourceName: str, addOnRequest: AddOnRequestTypeDef
    ) -> EnableAddOnResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.enable_add_on)
        [Show boto3-stubs documentation](./client.md#enable-add-on)
        """

    def export_snapshot(self, sourceSnapshotName: str) -> ExportSnapshotResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.export_snapshot)
        [Show boto3-stubs documentation](./client.md#export-snapshot)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.generate_presigned_url)
        [Show boto3-stubs documentation](./client.md#generate-presigned-url)
        """

    def get_active_names(self, pageToken: str = None) -> GetActiveNamesResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_active_names)
        [Show boto3-stubs documentation](./client.md#get-active-names)
        """

    def get_alarms(
        self, alarmName: str = None, pageToken: str = None, monitoredResourceName: str = None
    ) -> GetAlarmsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_alarms)
        [Show boto3-stubs documentation](./client.md#get-alarms)
        """

    def get_auto_snapshots(self, resourceName: str) -> GetAutoSnapshotsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_auto_snapshots)
        [Show boto3-stubs documentation](./client.md#get-auto-snapshots)
        """

    def get_blueprints(
        self, includeInactive: bool = None, pageToken: str = None
    ) -> GetBlueprintsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_blueprints)
        [Show boto3-stubs documentation](./client.md#get-blueprints)
        """

    def get_bundles(
        self, includeInactive: bool = None, pageToken: str = None
    ) -> GetBundlesResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_bundles)
        [Show boto3-stubs documentation](./client.md#get-bundles)
        """

    def get_certificates(
        self,
        certificateStatuses: List[CertificateStatus] = None,
        includeCertificateDetails: bool = None,
        certificateName: str = None,
    ) -> GetCertificatesResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_certificates)
        [Show boto3-stubs documentation](./client.md#get-certificates)
        """

    def get_cloud_formation_stack_records(
        self, pageToken: str = None
    ) -> GetCloudFormationStackRecordsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_cloud_formation_stack_records)
        [Show boto3-stubs documentation](./client.md#get-cloud-formation-stack-records)
        """

    def get_contact_methods(
        self, protocols: List[ContactProtocol] = None
    ) -> GetContactMethodsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_contact_methods)
        [Show boto3-stubs documentation](./client.md#get-contact-methods)
        """

    def get_container_api_metadata(self) -> GetContainerAPIMetadataResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_container_api_metadata)
        [Show boto3-stubs documentation](./client.md#get-container-api-metadata)
        """

    def get_container_images(self, serviceName: str) -> GetContainerImagesResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_container_images)
        [Show boto3-stubs documentation](./client.md#get-container-images)
        """

    def get_container_log(
        self,
        serviceName: str,
        containerName: str,
        startTime: datetime = None,
        endTime: datetime = None,
        filterPattern: str = None,
        pageToken: str = None,
    ) -> GetContainerLogResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_container_log)
        [Show boto3-stubs documentation](./client.md#get-container-log)
        """

    def get_container_service_deployments(
        self, serviceName: str
    ) -> GetContainerServiceDeploymentsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_container_service_deployments)
        [Show boto3-stubs documentation](./client.md#get-container-service-deployments)
        """

    def get_container_service_metric_data(
        self,
        serviceName: str,
        metricName: ContainerServiceMetricName,
        startTime: datetime,
        endTime: datetime,
        period: int,
        statistics: List[MetricStatistic],
    ) -> GetContainerServiceMetricDataResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_container_service_metric_data)
        [Show boto3-stubs documentation](./client.md#get-container-service-metric-data)
        """

    def get_container_service_powers(self) -> GetContainerServicePowersResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_container_service_powers)
        [Show boto3-stubs documentation](./client.md#get-container-service-powers)
        """

    def get_container_services(self, serviceName: str = None) -> ContainerServicesListResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_container_services)
        [Show boto3-stubs documentation](./client.md#get-container-services)
        """

    def get_disk(self, diskName: str) -> GetDiskResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_disk)
        [Show boto3-stubs documentation](./client.md#get-disk)
        """

    def get_disk_snapshot(self, diskSnapshotName: str) -> GetDiskSnapshotResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_disk_snapshot)
        [Show boto3-stubs documentation](./client.md#get-disk-snapshot)
        """

    def get_disk_snapshots(self, pageToken: str = None) -> GetDiskSnapshotsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_disk_snapshots)
        [Show boto3-stubs documentation](./client.md#get-disk-snapshots)
        """

    def get_disks(self, pageToken: str = None) -> GetDisksResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_disks)
        [Show boto3-stubs documentation](./client.md#get-disks)
        """

    def get_distribution_bundles(self) -> GetDistributionBundlesResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_distribution_bundles)
        [Show boto3-stubs documentation](./client.md#get-distribution-bundles)
        """

    def get_distribution_latest_cache_reset(
        self, distributionName: str = None
    ) -> GetDistributionLatestCacheResetResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_distribution_latest_cache_reset)
        [Show boto3-stubs documentation](./client.md#get-distribution-latest-cache-reset)
        """

    def get_distribution_metric_data(
        self,
        distributionName: str,
        metricName: DistributionMetricName,
        startTime: datetime,
        endTime: datetime,
        period: int,
        unit: MetricUnit,
        statistics: List[MetricStatistic],
    ) -> GetDistributionMetricDataResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_distribution_metric_data)
        [Show boto3-stubs documentation](./client.md#get-distribution-metric-data)
        """

    def get_distributions(
        self, distributionName: str = None, pageToken: str = None
    ) -> GetDistributionsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_distributions)
        [Show boto3-stubs documentation](./client.md#get-distributions)
        """

    def get_domain(self, domainName: str) -> GetDomainResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_domain)
        [Show boto3-stubs documentation](./client.md#get-domain)
        """

    def get_domains(self, pageToken: str = None) -> GetDomainsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_domains)
        [Show boto3-stubs documentation](./client.md#get-domains)
        """

    def get_export_snapshot_records(
        self, pageToken: str = None
    ) -> GetExportSnapshotRecordsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_export_snapshot_records)
        [Show boto3-stubs documentation](./client.md#get-export-snapshot-records)
        """

    def get_instance(self, instanceName: str) -> GetInstanceResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_instance)
        [Show boto3-stubs documentation](./client.md#get-instance)
        """

    def get_instance_access_details(
        self, instanceName: str, protocol: InstanceAccessProtocol = None
    ) -> GetInstanceAccessDetailsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_instance_access_details)
        [Show boto3-stubs documentation](./client.md#get-instance-access-details)
        """

    def get_instance_metric_data(
        self,
        instanceName: str,
        metricName: InstanceMetricName,
        period: int,
        startTime: datetime,
        endTime: datetime,
        unit: MetricUnit,
        statistics: List[MetricStatistic],
    ) -> GetInstanceMetricDataResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_instance_metric_data)
        [Show boto3-stubs documentation](./client.md#get-instance-metric-data)
        """

    def get_instance_port_states(self, instanceName: str) -> GetInstancePortStatesResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_instance_port_states)
        [Show boto3-stubs documentation](./client.md#get-instance-port-states)
        """

    def get_instance_snapshot(self, instanceSnapshotName: str) -> GetInstanceSnapshotResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_instance_snapshot)
        [Show boto3-stubs documentation](./client.md#get-instance-snapshot)
        """

    def get_instance_snapshots(self, pageToken: str = None) -> GetInstanceSnapshotsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_instance_snapshots)
        [Show boto3-stubs documentation](./client.md#get-instance-snapshots)
        """

    def get_instance_state(self, instanceName: str) -> GetInstanceStateResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_instance_state)
        [Show boto3-stubs documentation](./client.md#get-instance-state)
        """

    def get_instances(self, pageToken: str = None) -> GetInstancesResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_instances)
        [Show boto3-stubs documentation](./client.md#get-instances)
        """

    def get_key_pair(self, keyPairName: str) -> GetKeyPairResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_key_pair)
        [Show boto3-stubs documentation](./client.md#get-key-pair)
        """

    def get_key_pairs(self, pageToken: str = None) -> GetKeyPairsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_key_pairs)
        [Show boto3-stubs documentation](./client.md#get-key-pairs)
        """

    def get_load_balancer(self, loadBalancerName: str) -> GetLoadBalancerResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_load_balancer)
        [Show boto3-stubs documentation](./client.md#get-load-balancer)
        """

    def get_load_balancer_metric_data(
        self,
        loadBalancerName: str,
        metricName: LoadBalancerMetricName,
        period: int,
        startTime: datetime,
        endTime: datetime,
        unit: MetricUnit,
        statistics: List[MetricStatistic],
    ) -> GetLoadBalancerMetricDataResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_load_balancer_metric_data)
        [Show boto3-stubs documentation](./client.md#get-load-balancer-metric-data)
        """

    def get_load_balancer_tls_certificates(
        self, loadBalancerName: str
    ) -> GetLoadBalancerTlsCertificatesResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_load_balancer_tls_certificates)
        [Show boto3-stubs documentation](./client.md#get-load-balancer-tls-certificates)
        """

    def get_load_balancers(self, pageToken: str = None) -> GetLoadBalancersResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_load_balancers)
        [Show boto3-stubs documentation](./client.md#get-load-balancers)
        """

    def get_operation(self, operationId: str) -> GetOperationResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_operation)
        [Show boto3-stubs documentation](./client.md#get-operation)
        """

    def get_operations(self, pageToken: str = None) -> GetOperationsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_operations)
        [Show boto3-stubs documentation](./client.md#get-operations)
        """

    def get_operations_for_resource(
        self, resourceName: str, pageToken: str = None
    ) -> GetOperationsForResourceResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_operations_for_resource)
        [Show boto3-stubs documentation](./client.md#get-operations-for-resource)
        """

    def get_regions(
        self,
        includeAvailabilityZones: bool = None,
        includeRelationalDatabaseAvailabilityZones: bool = None,
    ) -> GetRegionsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_regions)
        [Show boto3-stubs documentation](./client.md#get-regions)
        """

    def get_relational_database(
        self, relationalDatabaseName: str
    ) -> GetRelationalDatabaseResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_relational_database)
        [Show boto3-stubs documentation](./client.md#get-relational-database)
        """

    def get_relational_database_blueprints(
        self, pageToken: str = None
    ) -> GetRelationalDatabaseBlueprintsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_relational_database_blueprints)
        [Show boto3-stubs documentation](./client.md#get-relational-database-blueprints)
        """

    def get_relational_database_bundles(
        self, pageToken: str = None
    ) -> GetRelationalDatabaseBundlesResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_relational_database_bundles)
        [Show boto3-stubs documentation](./client.md#get-relational-database-bundles)
        """

    def get_relational_database_events(
        self, relationalDatabaseName: str, durationInMinutes: int = None, pageToken: str = None
    ) -> GetRelationalDatabaseEventsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_relational_database_events)
        [Show boto3-stubs documentation](./client.md#get-relational-database-events)
        """

    def get_relational_database_log_events(
        self,
        relationalDatabaseName: str,
        logStreamName: str,
        startTime: datetime = None,
        endTime: datetime = None,
        startFromHead: bool = None,
        pageToken: str = None,
    ) -> GetRelationalDatabaseLogEventsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_relational_database_log_events)
        [Show boto3-stubs documentation](./client.md#get-relational-database-log-events)
        """

    def get_relational_database_log_streams(
        self, relationalDatabaseName: str
    ) -> GetRelationalDatabaseLogStreamsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_relational_database_log_streams)
        [Show boto3-stubs documentation](./client.md#get-relational-database-log-streams)
        """

    def get_relational_database_master_user_password(
        self, relationalDatabaseName: str, passwordVersion: RelationalDatabasePasswordVersion = None
    ) -> GetRelationalDatabaseMasterUserPasswordResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_relational_database_master_user_password)
        [Show boto3-stubs documentation](./client.md#get-relational-database-master-user-password)
        """

    def get_relational_database_metric_data(
        self,
        relationalDatabaseName: str,
        metricName: RelationalDatabaseMetricName,
        period: int,
        startTime: datetime,
        endTime: datetime,
        unit: MetricUnit,
        statistics: List[MetricStatistic],
    ) -> GetRelationalDatabaseMetricDataResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_relational_database_metric_data)
        [Show boto3-stubs documentation](./client.md#get-relational-database-metric-data)
        """

    def get_relational_database_parameters(
        self, relationalDatabaseName: str, pageToken: str = None
    ) -> GetRelationalDatabaseParametersResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_relational_database_parameters)
        [Show boto3-stubs documentation](./client.md#get-relational-database-parameters)
        """

    def get_relational_database_snapshot(
        self, relationalDatabaseSnapshotName: str
    ) -> GetRelationalDatabaseSnapshotResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_relational_database_snapshot)
        [Show boto3-stubs documentation](./client.md#get-relational-database-snapshot)
        """

    def get_relational_database_snapshots(
        self, pageToken: str = None
    ) -> GetRelationalDatabaseSnapshotsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_relational_database_snapshots)
        [Show boto3-stubs documentation](./client.md#get-relational-database-snapshots)
        """

    def get_relational_databases(
        self, pageToken: str = None
    ) -> GetRelationalDatabasesResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_relational_databases)
        [Show boto3-stubs documentation](./client.md#get-relational-databases)
        """

    def get_static_ip(self, staticIpName: str) -> GetStaticIpResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_static_ip)
        [Show boto3-stubs documentation](./client.md#get-static-ip)
        """

    def get_static_ips(self, pageToken: str = None) -> GetStaticIpsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.get_static_ips)
        [Show boto3-stubs documentation](./client.md#get-static-ips)
        """

    def import_key_pair(self, keyPairName: str, publicKeyBase64: str) -> ImportKeyPairResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.import_key_pair)
        [Show boto3-stubs documentation](./client.md#import-key-pair)
        """

    def is_vpc_peered(self) -> IsVpcPeeredResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.is_vpc_peered)
        [Show boto3-stubs documentation](./client.md#is-vpc-peered)
        """

    def open_instance_public_ports(
        self, portInfo: PortInfoTypeDef, instanceName: str
    ) -> OpenInstancePublicPortsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.open_instance_public_ports)
        [Show boto3-stubs documentation](./client.md#open-instance-public-ports)
        """

    def peer_vpc(self) -> PeerVpcResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.peer_vpc)
        [Show boto3-stubs documentation](./client.md#peer-vpc)
        """

    def put_alarm(
        self,
        alarmName: str,
        metricName: MetricName,
        monitoredResourceName: str,
        comparisonOperator: ComparisonOperator,
        threshold: float,
        evaluationPeriods: int,
        datapointsToAlarm: int = None,
        treatMissingData: TreatMissingData = None,
        contactProtocols: List[ContactProtocol] = None,
        notificationTriggers: List[AlarmState] = None,
        notificationEnabled: bool = None,
    ) -> PutAlarmResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.put_alarm)
        [Show boto3-stubs documentation](./client.md#put-alarm)
        """

    def put_instance_public_ports(
        self, portInfos: List[PortInfoTypeDef], instanceName: str
    ) -> PutInstancePublicPortsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.put_instance_public_ports)
        [Show boto3-stubs documentation](./client.md#put-instance-public-ports)
        """

    def reboot_instance(self, instanceName: str) -> RebootInstanceResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.reboot_instance)
        [Show boto3-stubs documentation](./client.md#reboot-instance)
        """

    def reboot_relational_database(
        self, relationalDatabaseName: str
    ) -> RebootRelationalDatabaseResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.reboot_relational_database)
        [Show boto3-stubs documentation](./client.md#reboot-relational-database)
        """

    def register_container_image(
        self, serviceName: str, label: str, digest: str
    ) -> RegisterContainerImageResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.register_container_image)
        [Show boto3-stubs documentation](./client.md#register-container-image)
        """

    def release_static_ip(self, staticIpName: str) -> ReleaseStaticIpResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.release_static_ip)
        [Show boto3-stubs documentation](./client.md#release-static-ip)
        """

    def reset_distribution_cache(
        self, distributionName: str = None
    ) -> ResetDistributionCacheResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.reset_distribution_cache)
        [Show boto3-stubs documentation](./client.md#reset-distribution-cache)
        """

    def send_contact_method_verification(
        self, protocol: Literal["Email"]
    ) -> SendContactMethodVerificationResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.send_contact_method_verification)
        [Show boto3-stubs documentation](./client.md#send-contact-method-verification)
        """

    def set_ip_address_type(
        self, resourceType: ResourceType, resourceName: str, ipAddressType: IpAddressType
    ) -> SetIpAddressTypeResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.set_ip_address_type)
        [Show boto3-stubs documentation](./client.md#set-ip-address-type)
        """

    def start_instance(self, instanceName: str) -> StartInstanceResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.start_instance)
        [Show boto3-stubs documentation](./client.md#start-instance)
        """

    def start_relational_database(
        self, relationalDatabaseName: str
    ) -> StartRelationalDatabaseResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.start_relational_database)
        [Show boto3-stubs documentation](./client.md#start-relational-database)
        """

    def stop_instance(self, instanceName: str, force: bool = None) -> StopInstanceResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.stop_instance)
        [Show boto3-stubs documentation](./client.md#stop-instance)
        """

    def stop_relational_database(
        self, relationalDatabaseName: str, relationalDatabaseSnapshotName: str = None
    ) -> StopRelationalDatabaseResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.stop_relational_database)
        [Show boto3-stubs documentation](./client.md#stop-relational-database)
        """

    def tag_resource(
        self, resourceName: str, tags: List["TagTypeDef"], resourceArn: str = None
    ) -> TagResourceResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.tag_resource)
        [Show boto3-stubs documentation](./client.md#tag-resource)
        """

    def test_alarm(self, alarmName: str, state: AlarmState) -> TestAlarmResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.test_alarm)
        [Show boto3-stubs documentation](./client.md#test-alarm)
        """

    def unpeer_vpc(self) -> UnpeerVpcResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.unpeer_vpc)
        [Show boto3-stubs documentation](./client.md#unpeer-vpc)
        """

    def untag_resource(
        self, resourceName: str, tagKeys: List[str], resourceArn: str = None
    ) -> UntagResourceResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.untag_resource)
        [Show boto3-stubs documentation](./client.md#untag-resource)
        """

    def update_container_service(
        self,
        serviceName: str,
        power: ContainerServicePowerName = None,
        scale: int = None,
        isDisabled: bool = None,
        publicDomainNames: Dict[str, List[str]] = None,
    ) -> UpdateContainerServiceResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.update_container_service)
        [Show boto3-stubs documentation](./client.md#update-container-service)
        """

    def update_distribution(
        self,
        distributionName: str,
        origin: InputOriginTypeDef = None,
        defaultCacheBehavior: "CacheBehaviorTypeDef" = None,
        cacheBehaviorSettings: "CacheSettingsTypeDef" = None,
        cacheBehaviors: List["CacheBehaviorPerPathTypeDef"] = None,
        isEnabled: bool = None,
    ) -> UpdateDistributionResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.update_distribution)
        [Show boto3-stubs documentation](./client.md#update-distribution)
        """

    def update_distribution_bundle(
        self, distributionName: str = None, bundleId: str = None
    ) -> UpdateDistributionBundleResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.update_distribution_bundle)
        [Show boto3-stubs documentation](./client.md#update-distribution-bundle)
        """

    def update_domain_entry(
        self, domainName: str, domainEntry: "DomainEntryTypeDef"
    ) -> UpdateDomainEntryResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.update_domain_entry)
        [Show boto3-stubs documentation](./client.md#update-domain-entry)
        """

    def update_load_balancer_attribute(
        self, loadBalancerName: str, attributeName: LoadBalancerAttributeName, attributeValue: str
    ) -> UpdateLoadBalancerAttributeResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.update_load_balancer_attribute)
        [Show boto3-stubs documentation](./client.md#update-load-balancer-attribute)
        """

    def update_relational_database(
        self,
        relationalDatabaseName: str,
        masterUserPassword: str = None,
        rotateMasterUserPassword: bool = None,
        preferredBackupWindow: str = None,
        preferredMaintenanceWindow: str = None,
        enableBackupRetention: bool = None,
        disableBackupRetention: bool = None,
        publiclyAccessible: bool = None,
        applyImmediately: bool = None,
        caCertificateIdentifier: str = None,
    ) -> UpdateRelationalDatabaseResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.update_relational_database)
        [Show boto3-stubs documentation](./client.md#update-relational-database)
        """

    def update_relational_database_parameters(
        self, relationalDatabaseName: str, parameters: List["RelationalDatabaseParameterTypeDef"]
    ) -> UpdateRelationalDatabaseParametersResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Client.update_relational_database_parameters)
        [Show boto3-stubs documentation](./client.md#update-relational-database-parameters)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_active_names"]) -> GetActiveNamesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Paginator.GetActiveNames)[Show boto3-stubs documentation](./paginators.md#getactivenamespaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_blueprints"]) -> GetBlueprintsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Paginator.GetBlueprints)[Show boto3-stubs documentation](./paginators.md#getblueprintspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_bundles"]) -> GetBundlesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Paginator.GetBundles)[Show boto3-stubs documentation](./paginators.md#getbundlespaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_cloud_formation_stack_records"]
    ) -> GetCloudFormationStackRecordsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Paginator.GetCloudFormationStackRecords)[Show boto3-stubs documentation](./paginators.md#getcloudformationstackrecordspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_disk_snapshots"]
    ) -> GetDiskSnapshotsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Paginator.GetDiskSnapshots)[Show boto3-stubs documentation](./paginators.md#getdisksnapshotspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_disks"]) -> GetDisksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Paginator.GetDisks)[Show boto3-stubs documentation](./paginators.md#getdiskspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_domains"]) -> GetDomainsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Paginator.GetDomains)[Show boto3-stubs documentation](./paginators.md#getdomainspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_export_snapshot_records"]
    ) -> GetExportSnapshotRecordsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Paginator.GetExportSnapshotRecords)[Show boto3-stubs documentation](./paginators.md#getexportsnapshotrecordspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_instance_snapshots"]
    ) -> GetInstanceSnapshotsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Paginator.GetInstanceSnapshots)[Show boto3-stubs documentation](./paginators.md#getinstancesnapshotspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_instances"]) -> GetInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Paginator.GetInstances)[Show boto3-stubs documentation](./paginators.md#getinstancespaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_key_pairs"]) -> GetKeyPairsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Paginator.GetKeyPairs)[Show boto3-stubs documentation](./paginators.md#getkeypairspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_load_balancers"]
    ) -> GetLoadBalancersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Paginator.GetLoadBalancers)[Show boto3-stubs documentation](./paginators.md#getloadbalancerspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_operations"]) -> GetOperationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Paginator.GetOperations)[Show boto3-stubs documentation](./paginators.md#getoperationspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_relational_database_blueprints"]
    ) -> GetRelationalDatabaseBlueprintsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Paginator.GetRelationalDatabaseBlueprints)[Show boto3-stubs documentation](./paginators.md#getrelationaldatabaseblueprintspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_relational_database_bundles"]
    ) -> GetRelationalDatabaseBundlesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Paginator.GetRelationalDatabaseBundles)[Show boto3-stubs documentation](./paginators.md#getrelationaldatabasebundlespaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_relational_database_events"]
    ) -> GetRelationalDatabaseEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Paginator.GetRelationalDatabaseEvents)[Show boto3-stubs documentation](./paginators.md#getrelationaldatabaseeventspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_relational_database_parameters"]
    ) -> GetRelationalDatabaseParametersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Paginator.GetRelationalDatabaseParameters)[Show boto3-stubs documentation](./paginators.md#getrelationaldatabaseparameterspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_relational_database_snapshots"]
    ) -> GetRelationalDatabaseSnapshotsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Paginator.GetRelationalDatabaseSnapshots)[Show boto3-stubs documentation](./paginators.md#getrelationaldatabasesnapshotspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_relational_databases"]
    ) -> GetRelationalDatabasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Paginator.GetRelationalDatabases)[Show boto3-stubs documentation](./paginators.md#getrelationaldatabasespaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_static_ips"]) -> GetStaticIpsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/lightsail.html#Lightsail.Paginator.GetStaticIps)[Show boto3-stubs documentation](./paginators.md#getstaticipspaginator)
        """
