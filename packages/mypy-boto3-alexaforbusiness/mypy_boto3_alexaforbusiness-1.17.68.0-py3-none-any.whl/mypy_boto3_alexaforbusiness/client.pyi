"""
Type annotations for alexaforbusiness service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html)

Usage::

    ```python
    import boto3
    from mypy_boto3_alexaforbusiness import AlexaForBusinessClient

    client: AlexaForBusinessClient = boto3.client("alexaforbusiness")
    ```
"""
import sys
from typing import Any, Dict, List, Type, overload

from botocore.client import ClientMeta

from mypy_boto3_alexaforbusiness.literals import (
    BusinessReportFormat,
    ConferenceProviderType,
    DeviceEventType,
    DistanceUnit,
    EnablementTypeFilter,
    Feature,
    NetworkSecurityType,
    SkillTypeFilter,
    TemperatureUnit,
    WakeWord,
)
from mypy_boto3_alexaforbusiness.paginator import (
    ListBusinessReportSchedulesPaginator,
    ListConferenceProvidersPaginator,
    ListDeviceEventsPaginator,
    ListSkillsPaginator,
    ListSkillsStoreCategoriesPaginator,
    ListSkillsStoreSkillsByCategoryPaginator,
    ListSmartHomeAppliancesPaginator,
    ListTagsPaginator,
    SearchDevicesPaginator,
    SearchProfilesPaginator,
    SearchRoomsPaginator,
    SearchSkillGroupsPaginator,
    SearchUsersPaginator,
)
from mypy_boto3_alexaforbusiness.type_defs import (
    BusinessReportContentRangeTypeDef,
    BusinessReportRecurrenceTypeDef,
    ConferencePreferenceTypeDef,
    ContentTypeDef,
    CreateAddressBookResponseTypeDef,
    CreateBusinessReportScheduleResponseTypeDef,
    CreateConferenceProviderResponseTypeDef,
    CreateContactResponseTypeDef,
    CreateGatewayGroupResponseTypeDef,
    CreateMeetingRoomConfigurationTypeDef,
    CreateNetworkProfileResponseTypeDef,
    CreateProfileResponseTypeDef,
    CreateRoomResponseTypeDef,
    CreateSkillGroupResponseTypeDef,
    CreateUserResponseTypeDef,
    FilterTypeDef,
    GetAddressBookResponseTypeDef,
    GetConferencePreferenceResponseTypeDef,
    GetConferenceProviderResponseTypeDef,
    GetContactResponseTypeDef,
    GetDeviceResponseTypeDef,
    GetGatewayGroupResponseTypeDef,
    GetGatewayResponseTypeDef,
    GetInvitationConfigurationResponseTypeDef,
    GetNetworkProfileResponseTypeDef,
    GetProfileResponseTypeDef,
    GetRoomResponseTypeDef,
    GetRoomSkillParameterResponseTypeDef,
    GetSkillGroupResponseTypeDef,
    IPDialInTypeDef,
    ListBusinessReportSchedulesResponseTypeDef,
    ListConferenceProvidersResponseTypeDef,
    ListDeviceEventsResponseTypeDef,
    ListGatewayGroupsResponseTypeDef,
    ListGatewaysResponseTypeDef,
    ListSkillsResponseTypeDef,
    ListSkillsStoreCategoriesResponseTypeDef,
    ListSkillsStoreSkillsByCategoryResponseTypeDef,
    ListSmartHomeAppliancesResponseTypeDef,
    ListTagsResponseTypeDef,
    MeetingSettingTypeDef,
    PhoneNumberTypeDef,
    PSTNDialInTypeDef,
    RegisterAVSDeviceResponseTypeDef,
    ResolveRoomResponseTypeDef,
    RoomSkillParameterTypeDef,
    SearchAddressBooksResponseTypeDef,
    SearchContactsResponseTypeDef,
    SearchDevicesResponseTypeDef,
    SearchNetworkProfilesResponseTypeDef,
    SearchProfilesResponseTypeDef,
    SearchRoomsResponseTypeDef,
    SearchSkillGroupsResponseTypeDef,
    SearchUsersResponseTypeDef,
    SendAnnouncementResponseTypeDef,
    SipAddressTypeDef,
    SortTypeDef,
    TagTypeDef,
    UpdateMeetingRoomConfigurationTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("AlexaForBusinessClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str
    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AlreadyExistsException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    DeviceNotRegisteredException: Type[BotocoreClientError]
    InvalidCertificateAuthorityException: Type[BotocoreClientError]
    InvalidDeviceException: Type[BotocoreClientError]
    InvalidSecretsManagerResourceException: Type[BotocoreClientError]
    InvalidServiceLinkedRoleStateException: Type[BotocoreClientError]
    InvalidUserStatusException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NameInUseException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ResourceAssociatedException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    SkillNotLinkedException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]

class AlexaForBusinessClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html)
    """

    meta: ClientMeta
    exceptions: Exceptions
    def approve_skill(self, SkillId: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.approve_skill)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#approve-skill)
        """
    def associate_contact_with_address_book(
        self, ContactArn: str, AddressBookArn: str
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.associate_contact_with_address_book)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#associate-contact-with-address-book)
        """
    def associate_device_with_network_profile(
        self, DeviceArn: str, NetworkProfileArn: str
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.associate_device_with_network_profile)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#associate-device-with-network-profile)
        """
    def associate_device_with_room(
        self, DeviceArn: str = None, RoomArn: str = None
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.associate_device_with_room)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#associate-device-with-room)
        """
    def associate_skill_group_with_room(
        self, SkillGroupArn: str = None, RoomArn: str = None
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.associate_skill_group_with_room)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#associate-skill-group-with-room)
        """
    def associate_skill_with_skill_group(
        self, SkillId: str, SkillGroupArn: str = None
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.associate_skill_with_skill_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#associate-skill-with-skill-group)
        """
    def associate_skill_with_users(self, SkillId: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.associate_skill_with_users)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#associate-skill-with-users)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#can-paginate)
        """
    def create_address_book(
        self,
        Name: str,
        Description: str = None,
        ClientRequestToken: str = None,
        Tags: List["TagTypeDef"] = None,
    ) -> CreateAddressBookResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.create_address_book)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#create-address-book)
        """
    def create_business_report_schedule(
        self,
        Format: BusinessReportFormat,
        ContentRange: "BusinessReportContentRangeTypeDef",
        ScheduleName: str = None,
        S3BucketName: str = None,
        S3KeyPrefix: str = None,
        Recurrence: "BusinessReportRecurrenceTypeDef" = None,
        ClientRequestToken: str = None,
        Tags: List["TagTypeDef"] = None,
    ) -> CreateBusinessReportScheduleResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.create_business_report_schedule)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#create-business-report-schedule)
        """
    def create_conference_provider(
        self,
        ConferenceProviderName: str,
        ConferenceProviderType: ConferenceProviderType,
        MeetingSetting: "MeetingSettingTypeDef",
        IPDialIn: "IPDialInTypeDef" = None,
        PSTNDialIn: "PSTNDialInTypeDef" = None,
        ClientRequestToken: str = None,
        Tags: List["TagTypeDef"] = None,
    ) -> CreateConferenceProviderResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.create_conference_provider)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#create-conference-provider)
        """
    def create_contact(
        self,
        FirstName: str,
        DisplayName: str = None,
        LastName: str = None,
        PhoneNumber: str = None,
        PhoneNumbers: List["PhoneNumberTypeDef"] = None,
        SipAddresses: List["SipAddressTypeDef"] = None,
        ClientRequestToken: str = None,
        Tags: List["TagTypeDef"] = None,
    ) -> CreateContactResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.create_contact)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#create-contact)
        """
    def create_gateway_group(
        self,
        Name: str,
        ClientRequestToken: str,
        Description: str = None,
        Tags: List["TagTypeDef"] = None,
    ) -> CreateGatewayGroupResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.create_gateway_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#create-gateway-group)
        """
    def create_network_profile(
        self,
        NetworkProfileName: str,
        Ssid: str,
        SecurityType: NetworkSecurityType,
        ClientRequestToken: str,
        Description: str = None,
        EapMethod: Literal["EAP_TLS"] = None,
        CurrentPassword: str = None,
        NextPassword: str = None,
        CertificateAuthorityArn: str = None,
        TrustAnchors: List[str] = None,
        Tags: List["TagTypeDef"] = None,
    ) -> CreateNetworkProfileResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.create_network_profile)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#create-network-profile)
        """
    def create_profile(
        self,
        ProfileName: str,
        Timezone: str,
        Address: str,
        DistanceUnit: DistanceUnit,
        TemperatureUnit: TemperatureUnit,
        WakeWord: WakeWord,
        Locale: str = None,
        ClientRequestToken: str = None,
        SetupModeDisabled: bool = None,
        MaxVolumeLimit: int = None,
        PSTNEnabled: bool = None,
        DataRetentionOptIn: bool = None,
        MeetingRoomConfiguration: CreateMeetingRoomConfigurationTypeDef = None,
        Tags: List["TagTypeDef"] = None,
    ) -> CreateProfileResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.create_profile)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#create-profile)
        """
    def create_room(
        self,
        RoomName: str,
        Description: str = None,
        ProfileArn: str = None,
        ProviderCalendarId: str = None,
        ClientRequestToken: str = None,
        Tags: List["TagTypeDef"] = None,
    ) -> CreateRoomResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.create_room)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#create-room)
        """
    def create_skill_group(
        self,
        SkillGroupName: str,
        Description: str = None,
        ClientRequestToken: str = None,
        Tags: List["TagTypeDef"] = None,
    ) -> CreateSkillGroupResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.create_skill_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#create-skill-group)
        """
    def create_user(
        self,
        UserId: str,
        FirstName: str = None,
        LastName: str = None,
        Email: str = None,
        ClientRequestToken: str = None,
        Tags: List["TagTypeDef"] = None,
    ) -> CreateUserResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.create_user)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#create-user)
        """
    def delete_address_book(self, AddressBookArn: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_address_book)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#delete-address-book)
        """
    def delete_business_report_schedule(self, ScheduleArn: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_business_report_schedule)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#delete-business-report-schedule)
        """
    def delete_conference_provider(self, ConferenceProviderArn: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_conference_provider)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#delete-conference-provider)
        """
    def delete_contact(self, ContactArn: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_contact)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#delete-contact)
        """
    def delete_device(self, DeviceArn: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_device)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#delete-device)
        """
    def delete_device_usage_data(
        self, DeviceArn: str, DeviceUsageType: Literal["VOICE"]
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_device_usage_data)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#delete-device-usage-data)
        """
    def delete_gateway_group(self, GatewayGroupArn: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_gateway_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#delete-gateway-group)
        """
    def delete_network_profile(self, NetworkProfileArn: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_network_profile)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#delete-network-profile)
        """
    def delete_profile(self, ProfileArn: str = None) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_profile)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#delete-profile)
        """
    def delete_room(self, RoomArn: str = None) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_room)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#delete-room)
        """
    def delete_room_skill_parameter(
        self, SkillId: str, ParameterKey: str, RoomArn: str = None
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_room_skill_parameter)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#delete-room-skill-parameter)
        """
    def delete_skill_authorization(self, SkillId: str, RoomArn: str = None) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_skill_authorization)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#delete-skill-authorization)
        """
    def delete_skill_group(self, SkillGroupArn: str = None) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_skill_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#delete-skill-group)
        """
    def delete_user(self, EnrollmentId: str, UserArn: str = None) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_user)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#delete-user)
        """
    def disassociate_contact_from_address_book(
        self, ContactArn: str, AddressBookArn: str
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.disassociate_contact_from_address_book)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#disassociate-contact-from-address-book)
        """
    def disassociate_device_from_room(self, DeviceArn: str = None) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.disassociate_device_from_room)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#disassociate-device-from-room)
        """
    def disassociate_skill_from_skill_group(
        self, SkillId: str, SkillGroupArn: str = None
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.disassociate_skill_from_skill_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#disassociate-skill-from-skill-group)
        """
    def disassociate_skill_from_users(self, SkillId: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.disassociate_skill_from_users)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#disassociate-skill-from-users)
        """
    def disassociate_skill_group_from_room(
        self, SkillGroupArn: str = None, RoomArn: str = None
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.disassociate_skill_group_from_room)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#disassociate-skill-group-from-room)
        """
    def forget_smart_home_appliances(self, RoomArn: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.forget_smart_home_appliances)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#forget-smart-home-appliances)
        """
    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#generate-presigned-url)
        """
    def get_address_book(self, AddressBookArn: str) -> GetAddressBookResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_address_book)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#get-address-book)
        """
    def get_conference_preference(self) -> GetConferencePreferenceResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_conference_preference)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#get-conference-preference)
        """
    def get_conference_provider(
        self, ConferenceProviderArn: str
    ) -> GetConferenceProviderResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_conference_provider)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#get-conference-provider)
        """
    def get_contact(self, ContactArn: str) -> GetContactResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_contact)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#get-contact)
        """
    def get_device(self, DeviceArn: str = None) -> GetDeviceResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_device)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#get-device)
        """
    def get_gateway(self, GatewayArn: str) -> GetGatewayResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_gateway)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#get-gateway)
        """
    def get_gateway_group(self, GatewayGroupArn: str) -> GetGatewayGroupResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_gateway_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#get-gateway-group)
        """
    def get_invitation_configuration(self) -> GetInvitationConfigurationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_invitation_configuration)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#get-invitation-configuration)
        """
    def get_network_profile(self, NetworkProfileArn: str) -> GetNetworkProfileResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_network_profile)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#get-network-profile)
        """
    def get_profile(self, ProfileArn: str = None) -> GetProfileResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_profile)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#get-profile)
        """
    def get_room(self, RoomArn: str = None) -> GetRoomResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_room)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#get-room)
        """
    def get_room_skill_parameter(
        self, SkillId: str, ParameterKey: str, RoomArn: str = None
    ) -> GetRoomSkillParameterResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_room_skill_parameter)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#get-room-skill-parameter)
        """
    def get_skill_group(self, SkillGroupArn: str = None) -> GetSkillGroupResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_skill_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#get-skill-group)
        """
    def list_business_report_schedules(
        self, NextToken: str = None, MaxResults: int = None
    ) -> ListBusinessReportSchedulesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.list_business_report_schedules)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#list-business-report-schedules)
        """
    def list_conference_providers(
        self, NextToken: str = None, MaxResults: int = None
    ) -> ListConferenceProvidersResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.list_conference_providers)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#list-conference-providers)
        """
    def list_device_events(
        self,
        DeviceArn: str,
        EventType: DeviceEventType = None,
        NextToken: str = None,
        MaxResults: int = None,
    ) -> ListDeviceEventsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.list_device_events)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#list-device-events)
        """
    def list_gateway_groups(
        self, NextToken: str = None, MaxResults: int = None
    ) -> ListGatewayGroupsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.list_gateway_groups)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#list-gateway-groups)
        """
    def list_gateways(
        self, GatewayGroupArn: str = None, NextToken: str = None, MaxResults: int = None
    ) -> ListGatewaysResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.list_gateways)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#list-gateways)
        """
    def list_skills(
        self,
        SkillGroupArn: str = None,
        EnablementType: EnablementTypeFilter = None,
        SkillType: SkillTypeFilter = None,
        NextToken: str = None,
        MaxResults: int = None,
    ) -> ListSkillsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.list_skills)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#list-skills)
        """
    def list_skills_store_categories(
        self, NextToken: str = None, MaxResults: int = None
    ) -> ListSkillsStoreCategoriesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.list_skills_store_categories)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#list-skills-store-categories)
        """
    def list_skills_store_skills_by_category(
        self, CategoryId: int, NextToken: str = None, MaxResults: int = None
    ) -> ListSkillsStoreSkillsByCategoryResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.list_skills_store_skills_by_category)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#list-skills-store-skills-by-category)
        """
    def list_smart_home_appliances(
        self, RoomArn: str, MaxResults: int = None, NextToken: str = None
    ) -> ListSmartHomeAppliancesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.list_smart_home_appliances)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#list-smart-home-appliances)
        """
    def list_tags(
        self, Arn: str, NextToken: str = None, MaxResults: int = None
    ) -> ListTagsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.list_tags)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#list-tags)
        """
    def put_conference_preference(
        self, ConferencePreference: "ConferencePreferenceTypeDef"
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.put_conference_preference)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#put-conference-preference)
        """
    def put_invitation_configuration(
        self, OrganizationName: str, ContactEmail: str = None, PrivateSkillIds: List[str] = None
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.put_invitation_configuration)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#put-invitation-configuration)
        """
    def put_room_skill_parameter(
        self, SkillId: str, RoomSkillParameter: "RoomSkillParameterTypeDef", RoomArn: str = None
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.put_room_skill_parameter)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#put-room-skill-parameter)
        """
    def put_skill_authorization(
        self, AuthorizationResult: Dict[str, str], SkillId: str, RoomArn: str = None
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.put_skill_authorization)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#put-skill-authorization)
        """
    def register_avs_device(
        self,
        ClientId: str,
        UserCode: str,
        ProductId: str,
        AmazonId: str,
        DeviceSerialNumber: str = None,
        RoomArn: str = None,
        Tags: List["TagTypeDef"] = None,
    ) -> RegisterAVSDeviceResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.register_avs_device)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#register-avs-device)
        """
    def reject_skill(self, SkillId: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.reject_skill)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#reject-skill)
        """
    def resolve_room(self, UserId: str, SkillId: str) -> ResolveRoomResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.resolve_room)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#resolve-room)
        """
    def revoke_invitation(self, UserArn: str = None, EnrollmentId: str = None) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.revoke_invitation)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#revoke-invitation)
        """
    def search_address_books(
        self,
        Filters: List[FilterTypeDef] = None,
        SortCriteria: List[SortTypeDef] = None,
        NextToken: str = None,
        MaxResults: int = None,
    ) -> SearchAddressBooksResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.search_address_books)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#search-address-books)
        """
    def search_contacts(
        self,
        Filters: List[FilterTypeDef] = None,
        SortCriteria: List[SortTypeDef] = None,
        NextToken: str = None,
        MaxResults: int = None,
    ) -> SearchContactsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.search_contacts)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#search-contacts)
        """
    def search_devices(
        self,
        NextToken: str = None,
        MaxResults: int = None,
        Filters: List[FilterTypeDef] = None,
        SortCriteria: List[SortTypeDef] = None,
    ) -> SearchDevicesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.search_devices)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#search-devices)
        """
    def search_network_profiles(
        self,
        NextToken: str = None,
        MaxResults: int = None,
        Filters: List[FilterTypeDef] = None,
        SortCriteria: List[SortTypeDef] = None,
    ) -> SearchNetworkProfilesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.search_network_profiles)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#search-network-profiles)
        """
    def search_profiles(
        self,
        NextToken: str = None,
        MaxResults: int = None,
        Filters: List[FilterTypeDef] = None,
        SortCriteria: List[SortTypeDef] = None,
    ) -> SearchProfilesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.search_profiles)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#search-profiles)
        """
    def search_rooms(
        self,
        NextToken: str = None,
        MaxResults: int = None,
        Filters: List[FilterTypeDef] = None,
        SortCriteria: List[SortTypeDef] = None,
    ) -> SearchRoomsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.search_rooms)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#search-rooms)
        """
    def search_skill_groups(
        self,
        NextToken: str = None,
        MaxResults: int = None,
        Filters: List[FilterTypeDef] = None,
        SortCriteria: List[SortTypeDef] = None,
    ) -> SearchSkillGroupsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.search_skill_groups)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#search-skill-groups)
        """
    def search_users(
        self,
        NextToken: str = None,
        MaxResults: int = None,
        Filters: List[FilterTypeDef] = None,
        SortCriteria: List[SortTypeDef] = None,
    ) -> SearchUsersResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.search_users)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#search-users)
        """
    def send_announcement(
        self,
        RoomFilters: List[FilterTypeDef],
        Content: ContentTypeDef,
        ClientRequestToken: str,
        TimeToLiveInSeconds: int = None,
    ) -> SendAnnouncementResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.send_announcement)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#send-announcement)
        """
    def send_invitation(self, UserArn: str = None) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.send_invitation)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#send-invitation)
        """
    def start_device_sync(
        self, Features: List[Feature], RoomArn: str = None, DeviceArn: str = None
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.start_device_sync)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#start-device-sync)
        """
    def start_smart_home_appliance_discovery(self, RoomArn: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.start_smart_home_appliance_discovery)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#start-smart-home-appliance-discovery)
        """
    def tag_resource(self, Arn: str, Tags: List["TagTypeDef"]) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.tag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#tag-resource)
        """
    def untag_resource(self, Arn: str, TagKeys: List[str]) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.untag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#untag-resource)
        """
    def update_address_book(
        self, AddressBookArn: str, Name: str = None, Description: str = None
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.update_address_book)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#update-address-book)
        """
    def update_business_report_schedule(
        self,
        ScheduleArn: str,
        S3BucketName: str = None,
        S3KeyPrefix: str = None,
        Format: BusinessReportFormat = None,
        ScheduleName: str = None,
        Recurrence: "BusinessReportRecurrenceTypeDef" = None,
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.update_business_report_schedule)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#update-business-report-schedule)
        """
    def update_conference_provider(
        self,
        ConferenceProviderArn: str,
        ConferenceProviderType: ConferenceProviderType,
        MeetingSetting: "MeetingSettingTypeDef",
        IPDialIn: "IPDialInTypeDef" = None,
        PSTNDialIn: "PSTNDialInTypeDef" = None,
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.update_conference_provider)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#update-conference-provider)
        """
    def update_contact(
        self,
        ContactArn: str,
        DisplayName: str = None,
        FirstName: str = None,
        LastName: str = None,
        PhoneNumber: str = None,
        PhoneNumbers: List["PhoneNumberTypeDef"] = None,
        SipAddresses: List["SipAddressTypeDef"] = None,
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.update_contact)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#update-contact)
        """
    def update_device(self, DeviceArn: str = None, DeviceName: str = None) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.update_device)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#update-device)
        """
    def update_gateway(
        self,
        GatewayArn: str,
        Name: str = None,
        Description: str = None,
        SoftwareVersion: str = None,
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.update_gateway)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#update-gateway)
        """
    def update_gateway_group(
        self, GatewayGroupArn: str, Name: str = None, Description: str = None
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.update_gateway_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#update-gateway-group)
        """
    def update_network_profile(
        self,
        NetworkProfileArn: str,
        NetworkProfileName: str = None,
        Description: str = None,
        CurrentPassword: str = None,
        NextPassword: str = None,
        CertificateAuthorityArn: str = None,
        TrustAnchors: List[str] = None,
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.update_network_profile)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#update-network-profile)
        """
    def update_profile(
        self,
        ProfileArn: str = None,
        ProfileName: str = None,
        IsDefault: bool = None,
        Timezone: str = None,
        Address: str = None,
        DistanceUnit: DistanceUnit = None,
        TemperatureUnit: TemperatureUnit = None,
        WakeWord: WakeWord = None,
        Locale: str = None,
        SetupModeDisabled: bool = None,
        MaxVolumeLimit: int = None,
        PSTNEnabled: bool = None,
        DataRetentionOptIn: bool = None,
        MeetingRoomConfiguration: UpdateMeetingRoomConfigurationTypeDef = None,
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.update_profile)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#update-profile)
        """
    def update_room(
        self,
        RoomArn: str = None,
        RoomName: str = None,
        Description: str = None,
        ProviderCalendarId: str = None,
        ProfileArn: str = None,
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.update_room)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#update-room)
        """
    def update_skill_group(
        self, SkillGroupArn: str = None, SkillGroupName: str = None, Description: str = None
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.update_skill_group)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/client.html#update-skill-group)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_business_report_schedules"]
    ) -> ListBusinessReportSchedulesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.ListBusinessReportSchedules)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/paginators.html#listbusinessreportschedulespaginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_conference_providers"]
    ) -> ListConferenceProvidersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.ListConferenceProviders)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/paginators.html#listconferenceproviderspaginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_device_events"]
    ) -> ListDeviceEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.ListDeviceEvents)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/paginators.html#listdeviceeventspaginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_skills"]) -> ListSkillsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.ListSkills)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/paginators.html#listskillspaginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_skills_store_categories"]
    ) -> ListSkillsStoreCategoriesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.ListSkillsStoreCategories)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/paginators.html#listskillsstorecategoriespaginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_skills_store_skills_by_category"]
    ) -> ListSkillsStoreSkillsByCategoryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.ListSkillsStoreSkillsByCategory)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/paginators.html#listskillsstoreskillsbycategorypaginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_smart_home_appliances"]
    ) -> ListSmartHomeAppliancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.ListSmartHomeAppliances)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/paginators.html#listsmarthomeappliancespaginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_tags"]) -> ListTagsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.ListTags)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/paginators.html#listtagspaginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["search_devices"]) -> SearchDevicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.SearchDevices)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/paginators.html#searchdevicespaginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["search_profiles"]) -> SearchProfilesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.SearchProfiles)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/paginators.html#searchprofilespaginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["search_rooms"]) -> SearchRoomsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.SearchRooms)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/paginators.html#searchroomspaginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["search_skill_groups"]
    ) -> SearchSkillGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.SearchSkillGroups)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/paginators.html#searchskillgroupspaginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["search_users"]) -> SearchUsersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.SearchUsers)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_alexaforbusiness/paginators.html#searchuserspaginator)
        """
