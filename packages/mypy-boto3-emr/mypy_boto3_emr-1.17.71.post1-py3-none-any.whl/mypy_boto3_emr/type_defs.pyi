"""
Type annotations for emr service type definitions.

[Open documentation](./type_defs.md)

Usage::

    ```python
    from mypy_boto3_emr.type_defs import AddInstanceFleetOutputTypeDef

    data: AddInstanceFleetOutputTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List

from .literals import (
    ActionOnFailure,
    AdjustmentType,
    AuthMode,
    AutoScalingPolicyState,
    AutoScalingPolicyStateChangeReasonCode,
    CancelStepsRequestStatus,
    ClusterState,
    ClusterStateChangeReasonCode,
    ComparisonOperator,
    ComputeLimitsUnitType,
    IdentityType,
    InstanceCollectionType,
    InstanceFleetState,
    InstanceFleetStateChangeReasonCode,
    InstanceFleetType,
    InstanceGroupState,
    InstanceGroupStateChangeReasonCode,
    InstanceGroupType,
    InstanceRoleType,
    InstanceState,
    InstanceStateChangeReasonCode,
    JobFlowExecutionState,
    MarketType,
    NotebookExecutionStatus,
    OnDemandCapacityReservationPreference,
    PlacementGroupStrategy,
    RepoUpgradeOnBoot,
    ScaleDownBehavior,
    SpotProvisioningTimeoutAction,
    Statistic,
    StepExecutionState,
    StepState,
    Unit,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AddInstanceFleetOutputTypeDef",
    "AddInstanceGroupsOutputTypeDef",
    "AddJobFlowStepsOutputTypeDef",
    "ApplicationTypeDef",
    "AutoScalingPolicyDescriptionTypeDef",
    "AutoScalingPolicyStateChangeReasonTypeDef",
    "AutoScalingPolicyStatusTypeDef",
    "AutoScalingPolicyTypeDef",
    "BlockPublicAccessConfigurationMetadataTypeDef",
    "BlockPublicAccessConfigurationTypeDef",
    "BootstrapActionConfigTypeDef",
    "BootstrapActionDetailTypeDef",
    "CancelStepsInfoTypeDef",
    "CancelStepsOutputTypeDef",
    "CloudWatchAlarmDefinitionTypeDef",
    "ClusterStateChangeReasonTypeDef",
    "ClusterStatusTypeDef",
    "ClusterSummaryTypeDef",
    "ClusterTimelineTypeDef",
    "ClusterTypeDef",
    "CommandTypeDef",
    "ComputeLimitsTypeDef",
    "ConfigurationTypeDef",
    "CreateSecurityConfigurationOutputTypeDef",
    "CreateStudioOutputTypeDef",
    "DescribeClusterOutputTypeDef",
    "DescribeJobFlowsOutputTypeDef",
    "DescribeNotebookExecutionOutputTypeDef",
    "DescribeSecurityConfigurationOutputTypeDef",
    "DescribeStepOutputTypeDef",
    "DescribeStudioOutputTypeDef",
    "EbsBlockDeviceConfigTypeDef",
    "EbsBlockDeviceTypeDef",
    "EbsConfigurationTypeDef",
    "EbsVolumeTypeDef",
    "Ec2InstanceAttributesTypeDef",
    "ExecutionEngineConfigTypeDef",
    "FailureDetailsTypeDef",
    "GetBlockPublicAccessConfigurationOutputTypeDef",
    "GetManagedScalingPolicyOutputTypeDef",
    "GetStudioSessionMappingOutputTypeDef",
    "HadoopJarStepConfigTypeDef",
    "HadoopStepConfigTypeDef",
    "InstanceFleetConfigTypeDef",
    "InstanceFleetModifyConfigTypeDef",
    "InstanceFleetProvisioningSpecificationsTypeDef",
    "InstanceFleetStateChangeReasonTypeDef",
    "InstanceFleetStatusTypeDef",
    "InstanceFleetTimelineTypeDef",
    "InstanceFleetTypeDef",
    "InstanceGroupConfigTypeDef",
    "InstanceGroupDetailTypeDef",
    "InstanceGroupModifyConfigTypeDef",
    "InstanceGroupStateChangeReasonTypeDef",
    "InstanceGroupStatusTypeDef",
    "InstanceGroupTimelineTypeDef",
    "InstanceGroupTypeDef",
    "InstanceResizePolicyTypeDef",
    "InstanceStateChangeReasonTypeDef",
    "InstanceStatusTypeDef",
    "InstanceTimelineTypeDef",
    "InstanceTypeConfigTypeDef",
    "InstanceTypeDef",
    "InstanceTypeSpecificationTypeDef",
    "JobFlowDetailTypeDef",
    "JobFlowExecutionStatusDetailTypeDef",
    "JobFlowInstancesConfigTypeDef",
    "JobFlowInstancesDetailTypeDef",
    "KerberosAttributesTypeDef",
    "KeyValueTypeDef",
    "ListBootstrapActionsOutputTypeDef",
    "ListClustersOutputTypeDef",
    "ListInstanceFleetsOutputTypeDef",
    "ListInstanceGroupsOutputTypeDef",
    "ListInstancesOutputTypeDef",
    "ListNotebookExecutionsOutputTypeDef",
    "ListSecurityConfigurationsOutputTypeDef",
    "ListStepsOutputTypeDef",
    "ListStudioSessionMappingsOutputTypeDef",
    "ListStudiosOutputTypeDef",
    "ManagedScalingPolicyTypeDef",
    "MetricDimensionTypeDef",
    "ModifyClusterOutputTypeDef",
    "NotebookExecutionSummaryTypeDef",
    "NotebookExecutionTypeDef",
    "OnDemandCapacityReservationOptionsTypeDef",
    "OnDemandProvisioningSpecificationTypeDef",
    "PaginatorConfigTypeDef",
    "PlacementGroupConfigTypeDef",
    "PlacementTypeTypeDef",
    "PortRangeTypeDef",
    "PutAutoScalingPolicyOutputTypeDef",
    "ResponseMetadataTypeDef",
    "RunJobFlowOutputTypeDef",
    "ScalingActionTypeDef",
    "ScalingConstraintsTypeDef",
    "ScalingRuleTypeDef",
    "ScalingTriggerTypeDef",
    "ScriptBootstrapActionConfigTypeDef",
    "SecurityConfigurationSummaryTypeDef",
    "SessionMappingDetailTypeDef",
    "SessionMappingSummaryTypeDef",
    "ShrinkPolicyTypeDef",
    "SimpleScalingPolicyConfigurationTypeDef",
    "SpotProvisioningSpecificationTypeDef",
    "StartNotebookExecutionOutputTypeDef",
    "StepConfigTypeDef",
    "StepDetailTypeDef",
    "StepExecutionStatusDetailTypeDef",
    "StepStateChangeReasonTypeDef",
    "StepStatusTypeDef",
    "StepSummaryTypeDef",
    "StepTimelineTypeDef",
    "StepTypeDef",
    "StudioSummaryTypeDef",
    "StudioTypeDef",
    "SupportedProductConfigTypeDef",
    "TagTypeDef",
    "VolumeSpecificationTypeDef",
    "WaiterConfigTypeDef",
)

AddInstanceFleetOutputTypeDef = TypedDict(
    "AddInstanceFleetOutputTypeDef",
    {
        "ClusterId": str,
        "InstanceFleetId": str,
        "ClusterArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AddInstanceGroupsOutputTypeDef = TypedDict(
    "AddInstanceGroupsOutputTypeDef",
    {
        "JobFlowId": str,
        "InstanceGroupIds": List[str],
        "ClusterArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AddJobFlowStepsOutputTypeDef = TypedDict(
    "AddJobFlowStepsOutputTypeDef",
    {
        "StepIds": List[str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ApplicationTypeDef = TypedDict(
    "ApplicationTypeDef",
    {
        "Name": str,
        "Version": str,
        "Args": List[str],
        "AdditionalInfo": Dict[str, str],
    },
    total=False,
)

AutoScalingPolicyDescriptionTypeDef = TypedDict(
    "AutoScalingPolicyDescriptionTypeDef",
    {
        "Status": "AutoScalingPolicyStatusTypeDef",
        "Constraints": "ScalingConstraintsTypeDef",
        "Rules": List["ScalingRuleTypeDef"],
    },
    total=False,
)

AutoScalingPolicyStateChangeReasonTypeDef = TypedDict(
    "AutoScalingPolicyStateChangeReasonTypeDef",
    {
        "Code": AutoScalingPolicyStateChangeReasonCode,
        "Message": str,
    },
    total=False,
)

AutoScalingPolicyStatusTypeDef = TypedDict(
    "AutoScalingPolicyStatusTypeDef",
    {
        "State": AutoScalingPolicyState,
        "StateChangeReason": "AutoScalingPolicyStateChangeReasonTypeDef",
    },
    total=False,
)

AutoScalingPolicyTypeDef = TypedDict(
    "AutoScalingPolicyTypeDef",
    {
        "Constraints": "ScalingConstraintsTypeDef",
        "Rules": List["ScalingRuleTypeDef"],
    },
)

BlockPublicAccessConfigurationMetadataTypeDef = TypedDict(
    "BlockPublicAccessConfigurationMetadataTypeDef",
    {
        "CreationDateTime": datetime,
        "CreatedByArn": str,
    },
)

_RequiredBlockPublicAccessConfigurationTypeDef = TypedDict(
    "_RequiredBlockPublicAccessConfigurationTypeDef",
    {
        "BlockPublicSecurityGroupRules": bool,
    },
)
_OptionalBlockPublicAccessConfigurationTypeDef = TypedDict(
    "_OptionalBlockPublicAccessConfigurationTypeDef",
    {
        "PermittedPublicSecurityGroupRuleRanges": List["PortRangeTypeDef"],
    },
    total=False,
)

class BlockPublicAccessConfigurationTypeDef(
    _RequiredBlockPublicAccessConfigurationTypeDef, _OptionalBlockPublicAccessConfigurationTypeDef
):
    pass

BootstrapActionConfigTypeDef = TypedDict(
    "BootstrapActionConfigTypeDef",
    {
        "Name": str,
        "ScriptBootstrapAction": "ScriptBootstrapActionConfigTypeDef",
    },
)

BootstrapActionDetailTypeDef = TypedDict(
    "BootstrapActionDetailTypeDef",
    {
        "BootstrapActionConfig": "BootstrapActionConfigTypeDef",
    },
    total=False,
)

CancelStepsInfoTypeDef = TypedDict(
    "CancelStepsInfoTypeDef",
    {
        "StepId": str,
        "Status": CancelStepsRequestStatus,
        "Reason": str,
    },
    total=False,
)

CancelStepsOutputTypeDef = TypedDict(
    "CancelStepsOutputTypeDef",
    {
        "CancelStepsInfoList": List["CancelStepsInfoTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCloudWatchAlarmDefinitionTypeDef = TypedDict(
    "_RequiredCloudWatchAlarmDefinitionTypeDef",
    {
        "ComparisonOperator": ComparisonOperator,
        "MetricName": str,
        "Period": int,
        "Threshold": float,
    },
)
_OptionalCloudWatchAlarmDefinitionTypeDef = TypedDict(
    "_OptionalCloudWatchAlarmDefinitionTypeDef",
    {
        "EvaluationPeriods": int,
        "Namespace": str,
        "Statistic": Statistic,
        "Unit": Unit,
        "Dimensions": List["MetricDimensionTypeDef"],
    },
    total=False,
)

class CloudWatchAlarmDefinitionTypeDef(
    _RequiredCloudWatchAlarmDefinitionTypeDef, _OptionalCloudWatchAlarmDefinitionTypeDef
):
    pass

ClusterStateChangeReasonTypeDef = TypedDict(
    "ClusterStateChangeReasonTypeDef",
    {
        "Code": ClusterStateChangeReasonCode,
        "Message": str,
    },
    total=False,
)

ClusterStatusTypeDef = TypedDict(
    "ClusterStatusTypeDef",
    {
        "State": ClusterState,
        "StateChangeReason": "ClusterStateChangeReasonTypeDef",
        "Timeline": "ClusterTimelineTypeDef",
    },
    total=False,
)

ClusterSummaryTypeDef = TypedDict(
    "ClusterSummaryTypeDef",
    {
        "Id": str,
        "Name": str,
        "Status": "ClusterStatusTypeDef",
        "NormalizedInstanceHours": int,
        "ClusterArn": str,
        "OutpostArn": str,
    },
    total=False,
)

ClusterTimelineTypeDef = TypedDict(
    "ClusterTimelineTypeDef",
    {
        "CreationDateTime": datetime,
        "ReadyDateTime": datetime,
        "EndDateTime": datetime,
    },
    total=False,
)

ClusterTypeDef = TypedDict(
    "ClusterTypeDef",
    {
        "Id": str,
        "Name": str,
        "Status": "ClusterStatusTypeDef",
        "Ec2InstanceAttributes": "Ec2InstanceAttributesTypeDef",
        "InstanceCollectionType": InstanceCollectionType,
        "LogUri": str,
        "LogEncryptionKmsKeyId": str,
        "RequestedAmiVersion": str,
        "RunningAmiVersion": str,
        "ReleaseLabel": str,
        "AutoTerminate": bool,
        "TerminationProtected": bool,
        "VisibleToAllUsers": bool,
        "Applications": List["ApplicationTypeDef"],
        "Tags": List["TagTypeDef"],
        "ServiceRole": str,
        "NormalizedInstanceHours": int,
        "MasterPublicDnsName": str,
        "Configurations": List["ConfigurationTypeDef"],
        "SecurityConfiguration": str,
        "AutoScalingRole": str,
        "ScaleDownBehavior": ScaleDownBehavior,
        "CustomAmiId": str,
        "EbsRootVolumeSize": int,
        "RepoUpgradeOnBoot": RepoUpgradeOnBoot,
        "KerberosAttributes": "KerberosAttributesTypeDef",
        "ClusterArn": str,
        "OutpostArn": str,
        "StepConcurrencyLevel": int,
        "PlacementGroups": List["PlacementGroupConfigTypeDef"],
    },
    total=False,
)

CommandTypeDef = TypedDict(
    "CommandTypeDef",
    {
        "Name": str,
        "ScriptPath": str,
        "Args": List[str],
    },
    total=False,
)

_RequiredComputeLimitsTypeDef = TypedDict(
    "_RequiredComputeLimitsTypeDef",
    {
        "UnitType": ComputeLimitsUnitType,
        "MinimumCapacityUnits": int,
        "MaximumCapacityUnits": int,
    },
)
_OptionalComputeLimitsTypeDef = TypedDict(
    "_OptionalComputeLimitsTypeDef",
    {
        "MaximumOnDemandCapacityUnits": int,
        "MaximumCoreCapacityUnits": int,
    },
    total=False,
)

class ComputeLimitsTypeDef(_RequiredComputeLimitsTypeDef, _OptionalComputeLimitsTypeDef):
    pass

ConfigurationTypeDef = TypedDict(
    "ConfigurationTypeDef",
    {
        "Classification": str,
        "Configurations": List[Dict[str, Any]],
        "Properties": Dict[str, str],
    },
    total=False,
)

CreateSecurityConfigurationOutputTypeDef = TypedDict(
    "CreateSecurityConfigurationOutputTypeDef",
    {
        "Name": str,
        "CreationDateTime": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateStudioOutputTypeDef = TypedDict(
    "CreateStudioOutputTypeDef",
    {
        "StudioId": str,
        "Url": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeClusterOutputTypeDef = TypedDict(
    "DescribeClusterOutputTypeDef",
    {
        "Cluster": "ClusterTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeJobFlowsOutputTypeDef = TypedDict(
    "DescribeJobFlowsOutputTypeDef",
    {
        "JobFlows": List["JobFlowDetailTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeNotebookExecutionOutputTypeDef = TypedDict(
    "DescribeNotebookExecutionOutputTypeDef",
    {
        "NotebookExecution": "NotebookExecutionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeSecurityConfigurationOutputTypeDef = TypedDict(
    "DescribeSecurityConfigurationOutputTypeDef",
    {
        "Name": str,
        "SecurityConfiguration": str,
        "CreationDateTime": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeStepOutputTypeDef = TypedDict(
    "DescribeStepOutputTypeDef",
    {
        "Step": "StepTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeStudioOutputTypeDef = TypedDict(
    "DescribeStudioOutputTypeDef",
    {
        "Studio": "StudioTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredEbsBlockDeviceConfigTypeDef = TypedDict(
    "_RequiredEbsBlockDeviceConfigTypeDef",
    {
        "VolumeSpecification": "VolumeSpecificationTypeDef",
    },
)
_OptionalEbsBlockDeviceConfigTypeDef = TypedDict(
    "_OptionalEbsBlockDeviceConfigTypeDef",
    {
        "VolumesPerInstance": int,
    },
    total=False,
)

class EbsBlockDeviceConfigTypeDef(
    _RequiredEbsBlockDeviceConfigTypeDef, _OptionalEbsBlockDeviceConfigTypeDef
):
    pass

EbsBlockDeviceTypeDef = TypedDict(
    "EbsBlockDeviceTypeDef",
    {
        "VolumeSpecification": "VolumeSpecificationTypeDef",
        "Device": str,
    },
    total=False,
)

EbsConfigurationTypeDef = TypedDict(
    "EbsConfigurationTypeDef",
    {
        "EbsBlockDeviceConfigs": List["EbsBlockDeviceConfigTypeDef"],
        "EbsOptimized": bool,
    },
    total=False,
)

EbsVolumeTypeDef = TypedDict(
    "EbsVolumeTypeDef",
    {
        "Device": str,
        "VolumeId": str,
    },
    total=False,
)

Ec2InstanceAttributesTypeDef = TypedDict(
    "Ec2InstanceAttributesTypeDef",
    {
        "Ec2KeyName": str,
        "Ec2SubnetId": str,
        "RequestedEc2SubnetIds": List[str],
        "Ec2AvailabilityZone": str,
        "RequestedEc2AvailabilityZones": List[str],
        "IamInstanceProfile": str,
        "EmrManagedMasterSecurityGroup": str,
        "EmrManagedSlaveSecurityGroup": str,
        "ServiceAccessSecurityGroup": str,
        "AdditionalMasterSecurityGroups": List[str],
        "AdditionalSlaveSecurityGroups": List[str],
    },
    total=False,
)

_RequiredExecutionEngineConfigTypeDef = TypedDict(
    "_RequiredExecutionEngineConfigTypeDef",
    {
        "Id": str,
    },
)
_OptionalExecutionEngineConfigTypeDef = TypedDict(
    "_OptionalExecutionEngineConfigTypeDef",
    {
        "Type": Literal["EMR"],
        "MasterInstanceSecurityGroupId": str,
    },
    total=False,
)

class ExecutionEngineConfigTypeDef(
    _RequiredExecutionEngineConfigTypeDef, _OptionalExecutionEngineConfigTypeDef
):
    pass

FailureDetailsTypeDef = TypedDict(
    "FailureDetailsTypeDef",
    {
        "Reason": str,
        "Message": str,
        "LogFile": str,
    },
    total=False,
)

GetBlockPublicAccessConfigurationOutputTypeDef = TypedDict(
    "GetBlockPublicAccessConfigurationOutputTypeDef",
    {
        "BlockPublicAccessConfiguration": "BlockPublicAccessConfigurationTypeDef",
        "BlockPublicAccessConfigurationMetadata": "BlockPublicAccessConfigurationMetadataTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetManagedScalingPolicyOutputTypeDef = TypedDict(
    "GetManagedScalingPolicyOutputTypeDef",
    {
        "ManagedScalingPolicy": "ManagedScalingPolicyTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetStudioSessionMappingOutputTypeDef = TypedDict(
    "GetStudioSessionMappingOutputTypeDef",
    {
        "SessionMapping": "SessionMappingDetailTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredHadoopJarStepConfigTypeDef = TypedDict(
    "_RequiredHadoopJarStepConfigTypeDef",
    {
        "Jar": str,
    },
)
_OptionalHadoopJarStepConfigTypeDef = TypedDict(
    "_OptionalHadoopJarStepConfigTypeDef",
    {
        "Properties": List["KeyValueTypeDef"],
        "MainClass": str,
        "Args": List[str],
    },
    total=False,
)

class HadoopJarStepConfigTypeDef(
    _RequiredHadoopJarStepConfigTypeDef, _OptionalHadoopJarStepConfigTypeDef
):
    pass

HadoopStepConfigTypeDef = TypedDict(
    "HadoopStepConfigTypeDef",
    {
        "Jar": str,
        "Properties": Dict[str, str],
        "MainClass": str,
        "Args": List[str],
    },
    total=False,
)

_RequiredInstanceFleetConfigTypeDef = TypedDict(
    "_RequiredInstanceFleetConfigTypeDef",
    {
        "InstanceFleetType": InstanceFleetType,
    },
)
_OptionalInstanceFleetConfigTypeDef = TypedDict(
    "_OptionalInstanceFleetConfigTypeDef",
    {
        "Name": str,
        "TargetOnDemandCapacity": int,
        "TargetSpotCapacity": int,
        "InstanceTypeConfigs": List["InstanceTypeConfigTypeDef"],
        "LaunchSpecifications": "InstanceFleetProvisioningSpecificationsTypeDef",
    },
    total=False,
)

class InstanceFleetConfigTypeDef(
    _RequiredInstanceFleetConfigTypeDef, _OptionalInstanceFleetConfigTypeDef
):
    pass

_RequiredInstanceFleetModifyConfigTypeDef = TypedDict(
    "_RequiredInstanceFleetModifyConfigTypeDef",
    {
        "InstanceFleetId": str,
    },
)
_OptionalInstanceFleetModifyConfigTypeDef = TypedDict(
    "_OptionalInstanceFleetModifyConfigTypeDef",
    {
        "TargetOnDemandCapacity": int,
        "TargetSpotCapacity": int,
    },
    total=False,
)

class InstanceFleetModifyConfigTypeDef(
    _RequiredInstanceFleetModifyConfigTypeDef, _OptionalInstanceFleetModifyConfigTypeDef
):
    pass

InstanceFleetProvisioningSpecificationsTypeDef = TypedDict(
    "InstanceFleetProvisioningSpecificationsTypeDef",
    {
        "SpotSpecification": "SpotProvisioningSpecificationTypeDef",
        "OnDemandSpecification": "OnDemandProvisioningSpecificationTypeDef",
    },
    total=False,
)

InstanceFleetStateChangeReasonTypeDef = TypedDict(
    "InstanceFleetStateChangeReasonTypeDef",
    {
        "Code": InstanceFleetStateChangeReasonCode,
        "Message": str,
    },
    total=False,
)

InstanceFleetStatusTypeDef = TypedDict(
    "InstanceFleetStatusTypeDef",
    {
        "State": InstanceFleetState,
        "StateChangeReason": "InstanceFleetStateChangeReasonTypeDef",
        "Timeline": "InstanceFleetTimelineTypeDef",
    },
    total=False,
)

InstanceFleetTimelineTypeDef = TypedDict(
    "InstanceFleetTimelineTypeDef",
    {
        "CreationDateTime": datetime,
        "ReadyDateTime": datetime,
        "EndDateTime": datetime,
    },
    total=False,
)

InstanceFleetTypeDef = TypedDict(
    "InstanceFleetTypeDef",
    {
        "Id": str,
        "Name": str,
        "Status": "InstanceFleetStatusTypeDef",
        "InstanceFleetType": InstanceFleetType,
        "TargetOnDemandCapacity": int,
        "TargetSpotCapacity": int,
        "ProvisionedOnDemandCapacity": int,
        "ProvisionedSpotCapacity": int,
        "InstanceTypeSpecifications": List["InstanceTypeSpecificationTypeDef"],
        "LaunchSpecifications": "InstanceFleetProvisioningSpecificationsTypeDef",
    },
    total=False,
)

_RequiredInstanceGroupConfigTypeDef = TypedDict(
    "_RequiredInstanceGroupConfigTypeDef",
    {
        "InstanceRole": InstanceRoleType,
        "InstanceType": str,
        "InstanceCount": int,
    },
)
_OptionalInstanceGroupConfigTypeDef = TypedDict(
    "_OptionalInstanceGroupConfigTypeDef",
    {
        "Name": str,
        "Market": MarketType,
        "BidPrice": str,
        "Configurations": List["ConfigurationTypeDef"],
        "EbsConfiguration": "EbsConfigurationTypeDef",
        "AutoScalingPolicy": "AutoScalingPolicyTypeDef",
    },
    total=False,
)

class InstanceGroupConfigTypeDef(
    _RequiredInstanceGroupConfigTypeDef, _OptionalInstanceGroupConfigTypeDef
):
    pass

_RequiredInstanceGroupDetailTypeDef = TypedDict(
    "_RequiredInstanceGroupDetailTypeDef",
    {
        "Market": MarketType,
        "InstanceRole": InstanceRoleType,
        "InstanceType": str,
        "InstanceRequestCount": int,
        "InstanceRunningCount": int,
        "State": InstanceGroupState,
        "CreationDateTime": datetime,
    },
)
_OptionalInstanceGroupDetailTypeDef = TypedDict(
    "_OptionalInstanceGroupDetailTypeDef",
    {
        "InstanceGroupId": str,
        "Name": str,
        "BidPrice": str,
        "LastStateChangeReason": str,
        "StartDateTime": datetime,
        "ReadyDateTime": datetime,
        "EndDateTime": datetime,
    },
    total=False,
)

class InstanceGroupDetailTypeDef(
    _RequiredInstanceGroupDetailTypeDef, _OptionalInstanceGroupDetailTypeDef
):
    pass

_RequiredInstanceGroupModifyConfigTypeDef = TypedDict(
    "_RequiredInstanceGroupModifyConfigTypeDef",
    {
        "InstanceGroupId": str,
    },
)
_OptionalInstanceGroupModifyConfigTypeDef = TypedDict(
    "_OptionalInstanceGroupModifyConfigTypeDef",
    {
        "InstanceCount": int,
        "EC2InstanceIdsToTerminate": List[str],
        "ShrinkPolicy": "ShrinkPolicyTypeDef",
        "Configurations": List["ConfigurationTypeDef"],
    },
    total=False,
)

class InstanceGroupModifyConfigTypeDef(
    _RequiredInstanceGroupModifyConfigTypeDef, _OptionalInstanceGroupModifyConfigTypeDef
):
    pass

InstanceGroupStateChangeReasonTypeDef = TypedDict(
    "InstanceGroupStateChangeReasonTypeDef",
    {
        "Code": InstanceGroupStateChangeReasonCode,
        "Message": str,
    },
    total=False,
)

InstanceGroupStatusTypeDef = TypedDict(
    "InstanceGroupStatusTypeDef",
    {
        "State": InstanceGroupState,
        "StateChangeReason": "InstanceGroupStateChangeReasonTypeDef",
        "Timeline": "InstanceGroupTimelineTypeDef",
    },
    total=False,
)

InstanceGroupTimelineTypeDef = TypedDict(
    "InstanceGroupTimelineTypeDef",
    {
        "CreationDateTime": datetime,
        "ReadyDateTime": datetime,
        "EndDateTime": datetime,
    },
    total=False,
)

InstanceGroupTypeDef = TypedDict(
    "InstanceGroupTypeDef",
    {
        "Id": str,
        "Name": str,
        "Market": MarketType,
        "InstanceGroupType": InstanceGroupType,
        "BidPrice": str,
        "InstanceType": str,
        "RequestedInstanceCount": int,
        "RunningInstanceCount": int,
        "Status": "InstanceGroupStatusTypeDef",
        "Configurations": List["ConfigurationTypeDef"],
        "ConfigurationsVersion": int,
        "LastSuccessfullyAppliedConfigurations": List["ConfigurationTypeDef"],
        "LastSuccessfullyAppliedConfigurationsVersion": int,
        "EbsBlockDevices": List["EbsBlockDeviceTypeDef"],
        "EbsOptimized": bool,
        "ShrinkPolicy": "ShrinkPolicyTypeDef",
        "AutoScalingPolicy": "AutoScalingPolicyDescriptionTypeDef",
    },
    total=False,
)

InstanceResizePolicyTypeDef = TypedDict(
    "InstanceResizePolicyTypeDef",
    {
        "InstancesToTerminate": List[str],
        "InstancesToProtect": List[str],
        "InstanceTerminationTimeout": int,
    },
    total=False,
)

InstanceStateChangeReasonTypeDef = TypedDict(
    "InstanceStateChangeReasonTypeDef",
    {
        "Code": InstanceStateChangeReasonCode,
        "Message": str,
    },
    total=False,
)

InstanceStatusTypeDef = TypedDict(
    "InstanceStatusTypeDef",
    {
        "State": InstanceState,
        "StateChangeReason": "InstanceStateChangeReasonTypeDef",
        "Timeline": "InstanceTimelineTypeDef",
    },
    total=False,
)

InstanceTimelineTypeDef = TypedDict(
    "InstanceTimelineTypeDef",
    {
        "CreationDateTime": datetime,
        "ReadyDateTime": datetime,
        "EndDateTime": datetime,
    },
    total=False,
)

_RequiredInstanceTypeConfigTypeDef = TypedDict(
    "_RequiredInstanceTypeConfigTypeDef",
    {
        "InstanceType": str,
    },
)
_OptionalInstanceTypeConfigTypeDef = TypedDict(
    "_OptionalInstanceTypeConfigTypeDef",
    {
        "WeightedCapacity": int,
        "BidPrice": str,
        "BidPriceAsPercentageOfOnDemandPrice": float,
        "EbsConfiguration": "EbsConfigurationTypeDef",
        "Configurations": List["ConfigurationTypeDef"],
    },
    total=False,
)

class InstanceTypeConfigTypeDef(
    _RequiredInstanceTypeConfigTypeDef, _OptionalInstanceTypeConfigTypeDef
):
    pass

InstanceTypeDef = TypedDict(
    "InstanceTypeDef",
    {
        "Id": str,
        "Ec2InstanceId": str,
        "PublicDnsName": str,
        "PublicIpAddress": str,
        "PrivateDnsName": str,
        "PrivateIpAddress": str,
        "Status": "InstanceStatusTypeDef",
        "InstanceGroupId": str,
        "InstanceFleetId": str,
        "Market": MarketType,
        "InstanceType": str,
        "EbsVolumes": List["EbsVolumeTypeDef"],
    },
    total=False,
)

InstanceTypeSpecificationTypeDef = TypedDict(
    "InstanceTypeSpecificationTypeDef",
    {
        "InstanceType": str,
        "WeightedCapacity": int,
        "BidPrice": str,
        "BidPriceAsPercentageOfOnDemandPrice": float,
        "Configurations": List["ConfigurationTypeDef"],
        "EbsBlockDevices": List["EbsBlockDeviceTypeDef"],
        "EbsOptimized": bool,
    },
    total=False,
)

_RequiredJobFlowDetailTypeDef = TypedDict(
    "_RequiredJobFlowDetailTypeDef",
    {
        "JobFlowId": str,
        "Name": str,
        "ExecutionStatusDetail": "JobFlowExecutionStatusDetailTypeDef",
        "Instances": "JobFlowInstancesDetailTypeDef",
    },
)
_OptionalJobFlowDetailTypeDef = TypedDict(
    "_OptionalJobFlowDetailTypeDef",
    {
        "LogUri": str,
        "LogEncryptionKmsKeyId": str,
        "AmiVersion": str,
        "Steps": List["StepDetailTypeDef"],
        "BootstrapActions": List["BootstrapActionDetailTypeDef"],
        "SupportedProducts": List[str],
        "VisibleToAllUsers": bool,
        "JobFlowRole": str,
        "ServiceRole": str,
        "AutoScalingRole": str,
        "ScaleDownBehavior": ScaleDownBehavior,
    },
    total=False,
)

class JobFlowDetailTypeDef(_RequiredJobFlowDetailTypeDef, _OptionalJobFlowDetailTypeDef):
    pass

_RequiredJobFlowExecutionStatusDetailTypeDef = TypedDict(
    "_RequiredJobFlowExecutionStatusDetailTypeDef",
    {
        "State": JobFlowExecutionState,
        "CreationDateTime": datetime,
    },
)
_OptionalJobFlowExecutionStatusDetailTypeDef = TypedDict(
    "_OptionalJobFlowExecutionStatusDetailTypeDef",
    {
        "StartDateTime": datetime,
        "ReadyDateTime": datetime,
        "EndDateTime": datetime,
        "LastStateChangeReason": str,
    },
    total=False,
)

class JobFlowExecutionStatusDetailTypeDef(
    _RequiredJobFlowExecutionStatusDetailTypeDef, _OptionalJobFlowExecutionStatusDetailTypeDef
):
    pass

JobFlowInstancesConfigTypeDef = TypedDict(
    "JobFlowInstancesConfigTypeDef",
    {
        "MasterInstanceType": str,
        "SlaveInstanceType": str,
        "InstanceCount": int,
        "InstanceGroups": List["InstanceGroupConfigTypeDef"],
        "InstanceFleets": List["InstanceFleetConfigTypeDef"],
        "Ec2KeyName": str,
        "Placement": "PlacementTypeTypeDef",
        "KeepJobFlowAliveWhenNoSteps": bool,
        "TerminationProtected": bool,
        "HadoopVersion": str,
        "Ec2SubnetId": str,
        "Ec2SubnetIds": List[str],
        "EmrManagedMasterSecurityGroup": str,
        "EmrManagedSlaveSecurityGroup": str,
        "ServiceAccessSecurityGroup": str,
        "AdditionalMasterSecurityGroups": List[str],
        "AdditionalSlaveSecurityGroups": List[str],
    },
    total=False,
)

_RequiredJobFlowInstancesDetailTypeDef = TypedDict(
    "_RequiredJobFlowInstancesDetailTypeDef",
    {
        "MasterInstanceType": str,
        "SlaveInstanceType": str,
        "InstanceCount": int,
    },
)
_OptionalJobFlowInstancesDetailTypeDef = TypedDict(
    "_OptionalJobFlowInstancesDetailTypeDef",
    {
        "MasterPublicDnsName": str,
        "MasterInstanceId": str,
        "InstanceGroups": List["InstanceGroupDetailTypeDef"],
        "NormalizedInstanceHours": int,
        "Ec2KeyName": str,
        "Ec2SubnetId": str,
        "Placement": "PlacementTypeTypeDef",
        "KeepJobFlowAliveWhenNoSteps": bool,
        "TerminationProtected": bool,
        "HadoopVersion": str,
    },
    total=False,
)

class JobFlowInstancesDetailTypeDef(
    _RequiredJobFlowInstancesDetailTypeDef, _OptionalJobFlowInstancesDetailTypeDef
):
    pass

_RequiredKerberosAttributesTypeDef = TypedDict(
    "_RequiredKerberosAttributesTypeDef",
    {
        "Realm": str,
        "KdcAdminPassword": str,
    },
)
_OptionalKerberosAttributesTypeDef = TypedDict(
    "_OptionalKerberosAttributesTypeDef",
    {
        "CrossRealmTrustPrincipalPassword": str,
        "ADDomainJoinUser": str,
        "ADDomainJoinPassword": str,
    },
    total=False,
)

class KerberosAttributesTypeDef(
    _RequiredKerberosAttributesTypeDef, _OptionalKerberosAttributesTypeDef
):
    pass

KeyValueTypeDef = TypedDict(
    "KeyValueTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

ListBootstrapActionsOutputTypeDef = TypedDict(
    "ListBootstrapActionsOutputTypeDef",
    {
        "BootstrapActions": List["CommandTypeDef"],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListClustersOutputTypeDef = TypedDict(
    "ListClustersOutputTypeDef",
    {
        "Clusters": List["ClusterSummaryTypeDef"],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListInstanceFleetsOutputTypeDef = TypedDict(
    "ListInstanceFleetsOutputTypeDef",
    {
        "InstanceFleets": List["InstanceFleetTypeDef"],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListInstanceGroupsOutputTypeDef = TypedDict(
    "ListInstanceGroupsOutputTypeDef",
    {
        "InstanceGroups": List["InstanceGroupTypeDef"],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListInstancesOutputTypeDef = TypedDict(
    "ListInstancesOutputTypeDef",
    {
        "Instances": List["InstanceTypeDef"],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListNotebookExecutionsOutputTypeDef = TypedDict(
    "ListNotebookExecutionsOutputTypeDef",
    {
        "NotebookExecutions": List["NotebookExecutionSummaryTypeDef"],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListSecurityConfigurationsOutputTypeDef = TypedDict(
    "ListSecurityConfigurationsOutputTypeDef",
    {
        "SecurityConfigurations": List["SecurityConfigurationSummaryTypeDef"],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListStepsOutputTypeDef = TypedDict(
    "ListStepsOutputTypeDef",
    {
        "Steps": List["StepSummaryTypeDef"],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListStudioSessionMappingsOutputTypeDef = TypedDict(
    "ListStudioSessionMappingsOutputTypeDef",
    {
        "SessionMappings": List["SessionMappingSummaryTypeDef"],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListStudiosOutputTypeDef = TypedDict(
    "ListStudiosOutputTypeDef",
    {
        "Studios": List["StudioSummaryTypeDef"],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ManagedScalingPolicyTypeDef = TypedDict(
    "ManagedScalingPolicyTypeDef",
    {
        "ComputeLimits": "ComputeLimitsTypeDef",
    },
    total=False,
)

MetricDimensionTypeDef = TypedDict(
    "MetricDimensionTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

ModifyClusterOutputTypeDef = TypedDict(
    "ModifyClusterOutputTypeDef",
    {
        "StepConcurrencyLevel": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

NotebookExecutionSummaryTypeDef = TypedDict(
    "NotebookExecutionSummaryTypeDef",
    {
        "NotebookExecutionId": str,
        "EditorId": str,
        "NotebookExecutionName": str,
        "Status": NotebookExecutionStatus,
        "StartTime": datetime,
        "EndTime": datetime,
    },
    total=False,
)

NotebookExecutionTypeDef = TypedDict(
    "NotebookExecutionTypeDef",
    {
        "NotebookExecutionId": str,
        "EditorId": str,
        "ExecutionEngine": "ExecutionEngineConfigTypeDef",
        "NotebookExecutionName": str,
        "NotebookParams": str,
        "Status": NotebookExecutionStatus,
        "StartTime": datetime,
        "EndTime": datetime,
        "Arn": str,
        "OutputNotebookURI": str,
        "LastStateChangeReason": str,
        "NotebookInstanceSecurityGroupId": str,
        "Tags": List["TagTypeDef"],
    },
    total=False,
)

OnDemandCapacityReservationOptionsTypeDef = TypedDict(
    "OnDemandCapacityReservationOptionsTypeDef",
    {
        "UsageStrategy": Literal["use-capacity-reservations-first"],
        "CapacityReservationPreference": OnDemandCapacityReservationPreference,
        "CapacityReservationResourceGroupArn": str,
    },
    total=False,
)

_RequiredOnDemandProvisioningSpecificationTypeDef = TypedDict(
    "_RequiredOnDemandProvisioningSpecificationTypeDef",
    {
        "AllocationStrategy": Literal["lowest-price"],
    },
)
_OptionalOnDemandProvisioningSpecificationTypeDef = TypedDict(
    "_OptionalOnDemandProvisioningSpecificationTypeDef",
    {
        "CapacityReservationOptions": "OnDemandCapacityReservationOptionsTypeDef",
    },
    total=False,
)

class OnDemandProvisioningSpecificationTypeDef(
    _RequiredOnDemandProvisioningSpecificationTypeDef,
    _OptionalOnDemandProvisioningSpecificationTypeDef,
):
    pass

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredPlacementGroupConfigTypeDef = TypedDict(
    "_RequiredPlacementGroupConfigTypeDef",
    {
        "InstanceRole": InstanceRoleType,
    },
)
_OptionalPlacementGroupConfigTypeDef = TypedDict(
    "_OptionalPlacementGroupConfigTypeDef",
    {
        "PlacementStrategy": PlacementGroupStrategy,
    },
    total=False,
)

class PlacementGroupConfigTypeDef(
    _RequiredPlacementGroupConfigTypeDef, _OptionalPlacementGroupConfigTypeDef
):
    pass

PlacementTypeTypeDef = TypedDict(
    "PlacementTypeTypeDef",
    {
        "AvailabilityZone": str,
        "AvailabilityZones": List[str],
    },
    total=False,
)

_RequiredPortRangeTypeDef = TypedDict(
    "_RequiredPortRangeTypeDef",
    {
        "MinRange": int,
    },
)
_OptionalPortRangeTypeDef = TypedDict(
    "_OptionalPortRangeTypeDef",
    {
        "MaxRange": int,
    },
    total=False,
)

class PortRangeTypeDef(_RequiredPortRangeTypeDef, _OptionalPortRangeTypeDef):
    pass

PutAutoScalingPolicyOutputTypeDef = TypedDict(
    "PutAutoScalingPolicyOutputTypeDef",
    {
        "ClusterId": str,
        "InstanceGroupId": str,
        "AutoScalingPolicy": "AutoScalingPolicyDescriptionTypeDef",
        "ClusterArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, Any],
        "RetryAttempts": int,
    },
)

RunJobFlowOutputTypeDef = TypedDict(
    "RunJobFlowOutputTypeDef",
    {
        "JobFlowId": str,
        "ClusterArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredScalingActionTypeDef = TypedDict(
    "_RequiredScalingActionTypeDef",
    {
        "SimpleScalingPolicyConfiguration": "SimpleScalingPolicyConfigurationTypeDef",
    },
)
_OptionalScalingActionTypeDef = TypedDict(
    "_OptionalScalingActionTypeDef",
    {
        "Market": MarketType,
    },
    total=False,
)

class ScalingActionTypeDef(_RequiredScalingActionTypeDef, _OptionalScalingActionTypeDef):
    pass

ScalingConstraintsTypeDef = TypedDict(
    "ScalingConstraintsTypeDef",
    {
        "MinCapacity": int,
        "MaxCapacity": int,
    },
)

_RequiredScalingRuleTypeDef = TypedDict(
    "_RequiredScalingRuleTypeDef",
    {
        "Name": str,
        "Action": "ScalingActionTypeDef",
        "Trigger": "ScalingTriggerTypeDef",
    },
)
_OptionalScalingRuleTypeDef = TypedDict(
    "_OptionalScalingRuleTypeDef",
    {
        "Description": str,
    },
    total=False,
)

class ScalingRuleTypeDef(_RequiredScalingRuleTypeDef, _OptionalScalingRuleTypeDef):
    pass

ScalingTriggerTypeDef = TypedDict(
    "ScalingTriggerTypeDef",
    {
        "CloudWatchAlarmDefinition": "CloudWatchAlarmDefinitionTypeDef",
    },
)

_RequiredScriptBootstrapActionConfigTypeDef = TypedDict(
    "_RequiredScriptBootstrapActionConfigTypeDef",
    {
        "Path": str,
    },
)
_OptionalScriptBootstrapActionConfigTypeDef = TypedDict(
    "_OptionalScriptBootstrapActionConfigTypeDef",
    {
        "Args": List[str],
    },
    total=False,
)

class ScriptBootstrapActionConfigTypeDef(
    _RequiredScriptBootstrapActionConfigTypeDef, _OptionalScriptBootstrapActionConfigTypeDef
):
    pass

SecurityConfigurationSummaryTypeDef = TypedDict(
    "SecurityConfigurationSummaryTypeDef",
    {
        "Name": str,
        "CreationDateTime": datetime,
    },
    total=False,
)

SessionMappingDetailTypeDef = TypedDict(
    "SessionMappingDetailTypeDef",
    {
        "StudioId": str,
        "IdentityId": str,
        "IdentityName": str,
        "IdentityType": IdentityType,
        "SessionPolicyArn": str,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
    total=False,
)

SessionMappingSummaryTypeDef = TypedDict(
    "SessionMappingSummaryTypeDef",
    {
        "StudioId": str,
        "IdentityId": str,
        "IdentityName": str,
        "IdentityType": IdentityType,
        "SessionPolicyArn": str,
        "CreationTime": datetime,
    },
    total=False,
)

ShrinkPolicyTypeDef = TypedDict(
    "ShrinkPolicyTypeDef",
    {
        "DecommissionTimeout": int,
        "InstanceResizePolicy": "InstanceResizePolicyTypeDef",
    },
    total=False,
)

_RequiredSimpleScalingPolicyConfigurationTypeDef = TypedDict(
    "_RequiredSimpleScalingPolicyConfigurationTypeDef",
    {
        "ScalingAdjustment": int,
    },
)
_OptionalSimpleScalingPolicyConfigurationTypeDef = TypedDict(
    "_OptionalSimpleScalingPolicyConfigurationTypeDef",
    {
        "AdjustmentType": AdjustmentType,
        "CoolDown": int,
    },
    total=False,
)

class SimpleScalingPolicyConfigurationTypeDef(
    _RequiredSimpleScalingPolicyConfigurationTypeDef,
    _OptionalSimpleScalingPolicyConfigurationTypeDef,
):
    pass

_RequiredSpotProvisioningSpecificationTypeDef = TypedDict(
    "_RequiredSpotProvisioningSpecificationTypeDef",
    {
        "TimeoutDurationMinutes": int,
        "TimeoutAction": SpotProvisioningTimeoutAction,
    },
)
_OptionalSpotProvisioningSpecificationTypeDef = TypedDict(
    "_OptionalSpotProvisioningSpecificationTypeDef",
    {
        "BlockDurationMinutes": int,
        "AllocationStrategy": Literal["capacity-optimized"],
    },
    total=False,
)

class SpotProvisioningSpecificationTypeDef(
    _RequiredSpotProvisioningSpecificationTypeDef, _OptionalSpotProvisioningSpecificationTypeDef
):
    pass

StartNotebookExecutionOutputTypeDef = TypedDict(
    "StartNotebookExecutionOutputTypeDef",
    {
        "NotebookExecutionId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredStepConfigTypeDef = TypedDict(
    "_RequiredStepConfigTypeDef",
    {
        "Name": str,
        "HadoopJarStep": "HadoopJarStepConfigTypeDef",
    },
)
_OptionalStepConfigTypeDef = TypedDict(
    "_OptionalStepConfigTypeDef",
    {
        "ActionOnFailure": ActionOnFailure,
    },
    total=False,
)

class StepConfigTypeDef(_RequiredStepConfigTypeDef, _OptionalStepConfigTypeDef):
    pass

StepDetailTypeDef = TypedDict(
    "StepDetailTypeDef",
    {
        "StepConfig": "StepConfigTypeDef",
        "ExecutionStatusDetail": "StepExecutionStatusDetailTypeDef",
    },
)

_RequiredStepExecutionStatusDetailTypeDef = TypedDict(
    "_RequiredStepExecutionStatusDetailTypeDef",
    {
        "State": StepExecutionState,
        "CreationDateTime": datetime,
    },
)
_OptionalStepExecutionStatusDetailTypeDef = TypedDict(
    "_OptionalStepExecutionStatusDetailTypeDef",
    {
        "StartDateTime": datetime,
        "EndDateTime": datetime,
        "LastStateChangeReason": str,
    },
    total=False,
)

class StepExecutionStatusDetailTypeDef(
    _RequiredStepExecutionStatusDetailTypeDef, _OptionalStepExecutionStatusDetailTypeDef
):
    pass

StepStateChangeReasonTypeDef = TypedDict(
    "StepStateChangeReasonTypeDef",
    {
        "Code": Literal["NONE"],
        "Message": str,
    },
    total=False,
)

StepStatusTypeDef = TypedDict(
    "StepStatusTypeDef",
    {
        "State": StepState,
        "StateChangeReason": "StepStateChangeReasonTypeDef",
        "FailureDetails": "FailureDetailsTypeDef",
        "Timeline": "StepTimelineTypeDef",
    },
    total=False,
)

StepSummaryTypeDef = TypedDict(
    "StepSummaryTypeDef",
    {
        "Id": str,
        "Name": str,
        "Config": "HadoopStepConfigTypeDef",
        "ActionOnFailure": ActionOnFailure,
        "Status": "StepStatusTypeDef",
    },
    total=False,
)

StepTimelineTypeDef = TypedDict(
    "StepTimelineTypeDef",
    {
        "CreationDateTime": datetime,
        "StartDateTime": datetime,
        "EndDateTime": datetime,
    },
    total=False,
)

StepTypeDef = TypedDict(
    "StepTypeDef",
    {
        "Id": str,
        "Name": str,
        "Config": "HadoopStepConfigTypeDef",
        "ActionOnFailure": ActionOnFailure,
        "Status": "StepStatusTypeDef",
    },
    total=False,
)

StudioSummaryTypeDef = TypedDict(
    "StudioSummaryTypeDef",
    {
        "StudioId": str,
        "Name": str,
        "VpcId": str,
        "Description": str,
        "Url": str,
        "CreationTime": datetime,
    },
    total=False,
)

StudioTypeDef = TypedDict(
    "StudioTypeDef",
    {
        "StudioId": str,
        "StudioArn": str,
        "Name": str,
        "Description": str,
        "AuthMode": AuthMode,
        "VpcId": str,
        "SubnetIds": List[str],
        "ServiceRole": str,
        "UserRole": str,
        "WorkspaceSecurityGroupId": str,
        "EngineSecurityGroupId": str,
        "Url": str,
        "CreationTime": datetime,
        "DefaultS3Location": str,
        "Tags": List["TagTypeDef"],
    },
    total=False,
)

SupportedProductConfigTypeDef = TypedDict(
    "SupportedProductConfigTypeDef",
    {
        "Name": str,
        "Args": List[str],
    },
    total=False,
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

_RequiredVolumeSpecificationTypeDef = TypedDict(
    "_RequiredVolumeSpecificationTypeDef",
    {
        "VolumeType": str,
        "SizeInGB": int,
    },
)
_OptionalVolumeSpecificationTypeDef = TypedDict(
    "_OptionalVolumeSpecificationTypeDef",
    {
        "Iops": int,
    },
    total=False,
)

class VolumeSpecificationTypeDef(
    _RequiredVolumeSpecificationTypeDef, _OptionalVolumeSpecificationTypeDef
):
    pass

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)
