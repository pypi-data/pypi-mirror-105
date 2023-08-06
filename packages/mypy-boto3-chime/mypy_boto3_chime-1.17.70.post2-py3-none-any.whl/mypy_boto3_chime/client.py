"""
Type annotations for chime service client.

[Open documentation](./client.md)

Usage::

    ```python
    import boto3
    from mypy_boto3_chime import ChimeClient

    client: ChimeClient = boto3.client("chime")
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Type, overload

from botocore.client import ClientMeta

from mypy_boto3_chime.paginator import ListAccountsPaginator, ListUsersPaginator

from .literals import (
    Capability,
    ChannelMembershipType,
    ChannelMessagePersistenceType,
    ChannelMessageType,
    ChannelMode,
    ChannelPrivacy,
    GeoMatchLevel,
    License,
    NumberSelectionBehavior,
    PhoneNumberAssociationName,
    PhoneNumberProductType,
    PhoneNumberStatus,
    PhoneNumberType,
    ProxySessionStatus,
    RoomMembershipRole,
    SipRuleTriggerType,
    SortOrder,
    UserType,
    VoiceConnectorAwsRegion,
)
from .type_defs import (
    AccountSettingsTypeDef,
    AlexaForBusinessMetadataTypeDef,
    AppInstanceRetentionSettingsTypeDef,
    AppInstanceStreamingConfigurationTypeDef,
    AssociatePhoneNumbersWithVoiceConnectorGroupResponseTypeDef,
    AssociatePhoneNumbersWithVoiceConnectorResponseTypeDef,
    BatchCreateAttendeeResponseTypeDef,
    BatchCreateChannelMembershipResponseTypeDef,
    BatchCreateRoomMembershipResponseTypeDef,
    BatchDeletePhoneNumberResponseTypeDef,
    BatchSuspendUserResponseTypeDef,
    BatchUnsuspendUserResponseTypeDef,
    BatchUpdatePhoneNumberResponseTypeDef,
    BatchUpdateUserResponseTypeDef,
    BusinessCallingSettingsTypeDef,
    CreateAccountResponseTypeDef,
    CreateAppInstanceAdminResponseTypeDef,
    CreateAppInstanceResponseTypeDef,
    CreateAppInstanceUserResponseTypeDef,
    CreateAttendeeRequestItemTypeDef,
    CreateAttendeeResponseTypeDef,
    CreateBotResponseTypeDef,
    CreateChannelBanResponseTypeDef,
    CreateChannelMembershipResponseTypeDef,
    CreateChannelModeratorResponseTypeDef,
    CreateChannelResponseTypeDef,
    CreateMeetingDialOutResponseTypeDef,
    CreateMeetingResponseTypeDef,
    CreateMeetingWithAttendeesResponseTypeDef,
    CreatePhoneNumberOrderResponseTypeDef,
    CreateProxySessionResponseTypeDef,
    CreateRoomMembershipResponseTypeDef,
    CreateRoomResponseTypeDef,
    CreateSipMediaApplicationCallResponseTypeDef,
    CreateSipMediaApplicationResponseTypeDef,
    CreateSipRuleResponseTypeDef,
    CreateUserResponseTypeDef,
    CreateVoiceConnectorGroupResponseTypeDef,
    CreateVoiceConnectorResponseTypeDef,
    CredentialTypeDef,
    DescribeAppInstanceAdminResponseTypeDef,
    DescribeAppInstanceResponseTypeDef,
    DescribeAppInstanceUserResponseTypeDef,
    DescribeChannelBanResponseTypeDef,
    DescribeChannelMembershipForAppInstanceUserResponseTypeDef,
    DescribeChannelMembershipResponseTypeDef,
    DescribeChannelModeratedByAppInstanceUserResponseTypeDef,
    DescribeChannelModeratorResponseTypeDef,
    DescribeChannelResponseTypeDef,
    DisassociatePhoneNumbersFromVoiceConnectorGroupResponseTypeDef,
    DisassociatePhoneNumbersFromVoiceConnectorResponseTypeDef,
    EmergencyCallingConfigurationTypeDef,
    GeoMatchParamsTypeDef,
    GetAccountResponseTypeDef,
    GetAccountSettingsResponseTypeDef,
    GetAppInstanceRetentionSettingsResponseTypeDef,
    GetAppInstanceStreamingConfigurationsResponseTypeDef,
    GetAttendeeResponseTypeDef,
    GetBotResponseTypeDef,
    GetChannelMessageResponseTypeDef,
    GetEventsConfigurationResponseTypeDef,
    GetGlobalSettingsResponseTypeDef,
    GetMeetingResponseTypeDef,
    GetMessagingSessionEndpointResponseTypeDef,
    GetPhoneNumberOrderResponseTypeDef,
    GetPhoneNumberResponseTypeDef,
    GetPhoneNumberSettingsResponseTypeDef,
    GetProxySessionResponseTypeDef,
    GetRetentionSettingsResponseTypeDef,
    GetRoomResponseTypeDef,
    GetSipMediaApplicationLoggingConfigurationResponseTypeDef,
    GetSipMediaApplicationResponseTypeDef,
    GetSipRuleResponseTypeDef,
    GetUserResponseTypeDef,
    GetUserSettingsResponseTypeDef,
    GetVoiceConnectorEmergencyCallingConfigurationResponseTypeDef,
    GetVoiceConnectorGroupResponseTypeDef,
    GetVoiceConnectorLoggingConfigurationResponseTypeDef,
    GetVoiceConnectorOriginationResponseTypeDef,
    GetVoiceConnectorProxyResponseTypeDef,
    GetVoiceConnectorResponseTypeDef,
    GetVoiceConnectorStreamingConfigurationResponseTypeDef,
    GetVoiceConnectorTerminationHealthResponseTypeDef,
    GetVoiceConnectorTerminationResponseTypeDef,
    InviteUsersResponseTypeDef,
    ListAccountsResponseTypeDef,
    ListAppInstanceAdminsResponseTypeDef,
    ListAppInstancesResponseTypeDef,
    ListAppInstanceUsersResponseTypeDef,
    ListAttendeesResponseTypeDef,
    ListAttendeeTagsResponseTypeDef,
    ListBotsResponseTypeDef,
    ListChannelBansResponseTypeDef,
    ListChannelMembershipsForAppInstanceUserResponseTypeDef,
    ListChannelMembershipsResponseTypeDef,
    ListChannelMessagesResponseTypeDef,
    ListChannelModeratorsResponseTypeDef,
    ListChannelsModeratedByAppInstanceUserResponseTypeDef,
    ListChannelsResponseTypeDef,
    ListMeetingsResponseTypeDef,
    ListMeetingTagsResponseTypeDef,
    ListPhoneNumberOrdersResponseTypeDef,
    ListPhoneNumbersResponseTypeDef,
    ListProxySessionsResponseTypeDef,
    ListRoomMembershipsResponseTypeDef,
    ListRoomsResponseTypeDef,
    ListSipMediaApplicationsResponseTypeDef,
    ListSipRulesResponseTypeDef,
    ListSupportedPhoneNumberCountriesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListUsersResponseTypeDef,
    ListVoiceConnectorGroupsResponseTypeDef,
    ListVoiceConnectorsResponseTypeDef,
    ListVoiceConnectorTerminationCredentialsResponseTypeDef,
    LoggingConfigurationTypeDef,
    MeetingNotificationConfigurationTypeDef,
    MembershipItemTypeDef,
    OriginationTypeDef,
    PutAppInstanceRetentionSettingsResponseTypeDef,
    PutAppInstanceStreamingConfigurationsResponseTypeDef,
    PutEventsConfigurationResponseTypeDef,
    PutRetentionSettingsResponseTypeDef,
    PutSipMediaApplicationLoggingConfigurationResponseTypeDef,
    PutVoiceConnectorEmergencyCallingConfigurationResponseTypeDef,
    PutVoiceConnectorLoggingConfigurationResponseTypeDef,
    PutVoiceConnectorOriginationResponseTypeDef,
    PutVoiceConnectorProxyResponseTypeDef,
    PutVoiceConnectorStreamingConfigurationResponseTypeDef,
    PutVoiceConnectorTerminationResponseTypeDef,
    RedactChannelMessageResponseTypeDef,
    RegenerateSecurityTokenResponseTypeDef,
    ResetPersonalPINResponseTypeDef,
    RestorePhoneNumberResponseTypeDef,
    RetentionSettingsTypeDef,
    SearchAvailablePhoneNumbersResponseTypeDef,
    SendChannelMessageResponseTypeDef,
    SigninDelegateGroupTypeDef,
    SipMediaApplicationEndpointTypeDef,
    SipMediaApplicationLoggingConfigurationTypeDef,
    SipRuleTargetApplicationTypeDef,
    StreamingConfigurationTypeDef,
    TagTypeDef,
    TerminationTypeDef,
    UpdateAccountResponseTypeDef,
    UpdateAppInstanceResponseTypeDef,
    UpdateAppInstanceUserResponseTypeDef,
    UpdateBotResponseTypeDef,
    UpdateChannelMessageResponseTypeDef,
    UpdateChannelReadMarkerResponseTypeDef,
    UpdateChannelResponseTypeDef,
    UpdatePhoneNumberRequestItemTypeDef,
    UpdatePhoneNumberResponseTypeDef,
    UpdateProxySessionResponseTypeDef,
    UpdateRoomMembershipResponseTypeDef,
    UpdateRoomResponseTypeDef,
    UpdateSipMediaApplicationResponseTypeDef,
    UpdateSipRuleResponseTypeDef,
    UpdateUserRequestItemTypeDef,
    UpdateUserResponseTypeDef,
    UpdateVoiceConnectorGroupResponseTypeDef,
    UpdateVoiceConnectorResponseTypeDef,
    UserSettingsTypeDef,
    VoiceConnectorItemTypeDef,
    VoiceConnectorSettingsTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ChimeClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ResourceLimitExceededException: Type[BotocoreClientError]
    ServiceFailureException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottledClientException: Type[BotocoreClientError]
    UnauthorizedClientException: Type[BotocoreClientError]
    UnprocessableEntityException: Type[BotocoreClientError]


class ChimeClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client)
    [Show boto3-stubs documentation](./client.md)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def associate_phone_number_with_user(
        self, AccountId: str, UserId: str, E164PhoneNumber: str
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.associate_phone_number_with_user)
        [Show boto3-stubs documentation](./client.md#associate-phone-number-with-user)
        """

    def associate_phone_numbers_with_voice_connector(
        self, VoiceConnectorId: str, E164PhoneNumbers: List[str], ForceAssociate: bool = None
    ) -> AssociatePhoneNumbersWithVoiceConnectorResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.associate_phone_numbers_with_voice_connector)
        [Show boto3-stubs documentation](./client.md#associate-phone-numbers-with-voice-connector)
        """

    def associate_phone_numbers_with_voice_connector_group(
        self, VoiceConnectorGroupId: str, E164PhoneNumbers: List[str], ForceAssociate: bool = None
    ) -> AssociatePhoneNumbersWithVoiceConnectorGroupResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.associate_phone_numbers_with_voice_connector_group)
        [Show boto3-stubs documentation](./client.md#associate-phone-numbers-with-voice-connector-group)
        """

    def associate_signin_delegate_groups_with_account(
        self, AccountId: str, SigninDelegateGroups: List["SigninDelegateGroupTypeDef"]
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.associate_signin_delegate_groups_with_account)
        [Show boto3-stubs documentation](./client.md#associate-signin-delegate-groups-with-account)
        """

    def batch_create_attendee(
        self, MeetingId: str, Attendees: List[CreateAttendeeRequestItemTypeDef]
    ) -> BatchCreateAttendeeResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.batch_create_attendee)
        [Show boto3-stubs documentation](./client.md#batch-create-attendee)
        """

    def batch_create_channel_membership(
        self,
        ChannelArn: str,
        MemberArns: List[str],
        Type: ChannelMembershipType = None,
        ChimeBearer: str = None,
    ) -> BatchCreateChannelMembershipResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.batch_create_channel_membership)
        [Show boto3-stubs documentation](./client.md#batch-create-channel-membership)
        """

    def batch_create_room_membership(
        self, AccountId: str, RoomId: str, MembershipItemList: List[MembershipItemTypeDef]
    ) -> BatchCreateRoomMembershipResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.batch_create_room_membership)
        [Show boto3-stubs documentation](./client.md#batch-create-room-membership)
        """

    def batch_delete_phone_number(
        self, PhoneNumberIds: List[str]
    ) -> BatchDeletePhoneNumberResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.batch_delete_phone_number)
        [Show boto3-stubs documentation](./client.md#batch-delete-phone-number)
        """

    def batch_suspend_user(
        self, AccountId: str, UserIdList: List[str]
    ) -> BatchSuspendUserResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.batch_suspend_user)
        [Show boto3-stubs documentation](./client.md#batch-suspend-user)
        """

    def batch_unsuspend_user(
        self, AccountId: str, UserIdList: List[str]
    ) -> BatchUnsuspendUserResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.batch_unsuspend_user)
        [Show boto3-stubs documentation](./client.md#batch-unsuspend-user)
        """

    def batch_update_phone_number(
        self, UpdatePhoneNumberRequestItems: List[UpdatePhoneNumberRequestItemTypeDef]
    ) -> BatchUpdatePhoneNumberResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.batch_update_phone_number)
        [Show boto3-stubs documentation](./client.md#batch-update-phone-number)
        """

    def batch_update_user(
        self, AccountId: str, UpdateUserRequestItems: List[UpdateUserRequestItemTypeDef]
    ) -> BatchUpdateUserResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.batch_update_user)
        [Show boto3-stubs documentation](./client.md#batch-update-user)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.can_paginate)
        [Show boto3-stubs documentation](./client.md#can-paginate)
        """

    def create_account(self, Name: str) -> CreateAccountResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.create_account)
        [Show boto3-stubs documentation](./client.md#create-account)
        """

    def create_app_instance(
        self,
        Name: str,
        ClientRequestToken: str,
        Metadata: str = None,
        Tags: List["TagTypeDef"] = None,
    ) -> CreateAppInstanceResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.create_app_instance)
        [Show boto3-stubs documentation](./client.md#create-app-instance)
        """

    def create_app_instance_admin(
        self, AppInstanceAdminArn: str, AppInstanceArn: str
    ) -> CreateAppInstanceAdminResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.create_app_instance_admin)
        [Show boto3-stubs documentation](./client.md#create-app-instance-admin)
        """

    def create_app_instance_user(
        self,
        AppInstanceArn: str,
        AppInstanceUserId: str,
        Name: str,
        ClientRequestToken: str,
        Metadata: str = None,
        Tags: List["TagTypeDef"] = None,
    ) -> CreateAppInstanceUserResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.create_app_instance_user)
        [Show boto3-stubs documentation](./client.md#create-app-instance-user)
        """

    def create_attendee(
        self, MeetingId: str, ExternalUserId: str, Tags: List["TagTypeDef"] = None
    ) -> CreateAttendeeResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.create_attendee)
        [Show boto3-stubs documentation](./client.md#create-attendee)
        """

    def create_bot(
        self, AccountId: str, DisplayName: str, Domain: str = None
    ) -> CreateBotResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.create_bot)
        [Show boto3-stubs documentation](./client.md#create-bot)
        """

    def create_channel(
        self,
        AppInstanceArn: str,
        Name: str,
        ClientRequestToken: str,
        Mode: ChannelMode = None,
        Privacy: ChannelPrivacy = None,
        Metadata: str = None,
        Tags: List["TagTypeDef"] = None,
        ChimeBearer: str = None,
    ) -> CreateChannelResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.create_channel)
        [Show boto3-stubs documentation](./client.md#create-channel)
        """

    def create_channel_ban(
        self, ChannelArn: str, MemberArn: str, ChimeBearer: str = None
    ) -> CreateChannelBanResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.create_channel_ban)
        [Show boto3-stubs documentation](./client.md#create-channel-ban)
        """

    def create_channel_membership(
        self, ChannelArn: str, MemberArn: str, Type: ChannelMembershipType, ChimeBearer: str = None
    ) -> CreateChannelMembershipResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.create_channel_membership)
        [Show boto3-stubs documentation](./client.md#create-channel-membership)
        """

    def create_channel_moderator(
        self, ChannelArn: str, ChannelModeratorArn: str, ChimeBearer: str = None
    ) -> CreateChannelModeratorResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.create_channel_moderator)
        [Show boto3-stubs documentation](./client.md#create-channel-moderator)
        """

    def create_meeting(
        self,
        ClientRequestToken: str,
        ExternalMeetingId: str = None,
        MeetingHostId: str = None,
        MediaRegion: str = None,
        Tags: List["TagTypeDef"] = None,
        NotificationsConfiguration: MeetingNotificationConfigurationTypeDef = None,
    ) -> CreateMeetingResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.create_meeting)
        [Show boto3-stubs documentation](./client.md#create-meeting)
        """

    def create_meeting_dial_out(
        self, MeetingId: str, FromPhoneNumber: str, ToPhoneNumber: str, JoinToken: str
    ) -> CreateMeetingDialOutResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.create_meeting_dial_out)
        [Show boto3-stubs documentation](./client.md#create-meeting-dial-out)
        """

    def create_meeting_with_attendees(
        self,
        ClientRequestToken: str,
        ExternalMeetingId: str = None,
        MeetingHostId: str = None,
        MediaRegion: str = None,
        Tags: List["TagTypeDef"] = None,
        NotificationsConfiguration: MeetingNotificationConfigurationTypeDef = None,
        Attendees: List[CreateAttendeeRequestItemTypeDef] = None,
    ) -> CreateMeetingWithAttendeesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.create_meeting_with_attendees)
        [Show boto3-stubs documentation](./client.md#create-meeting-with-attendees)
        """

    def create_phone_number_order(
        self, ProductType: PhoneNumberProductType, E164PhoneNumbers: List[str]
    ) -> CreatePhoneNumberOrderResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.create_phone_number_order)
        [Show boto3-stubs documentation](./client.md#create-phone-number-order)
        """

    def create_proxy_session(
        self,
        VoiceConnectorId: str,
        ParticipantPhoneNumbers: List[str],
        Capabilities: List[Capability],
        Name: str = None,
        ExpiryMinutes: int = None,
        NumberSelectionBehavior: NumberSelectionBehavior = None,
        GeoMatchLevel: GeoMatchLevel = None,
        GeoMatchParams: "GeoMatchParamsTypeDef" = None,
    ) -> CreateProxySessionResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.create_proxy_session)
        [Show boto3-stubs documentation](./client.md#create-proxy-session)
        """

    def create_room(
        self, AccountId: str, Name: str, ClientRequestToken: str = None
    ) -> CreateRoomResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.create_room)
        [Show boto3-stubs documentation](./client.md#create-room)
        """

    def create_room_membership(
        self, AccountId: str, RoomId: str, MemberId: str, Role: RoomMembershipRole = None
    ) -> CreateRoomMembershipResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.create_room_membership)
        [Show boto3-stubs documentation](./client.md#create-room-membership)
        """

    def create_sip_media_application(
        self, AwsRegion: str, Name: str, Endpoints: List["SipMediaApplicationEndpointTypeDef"]
    ) -> CreateSipMediaApplicationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.create_sip_media_application)
        [Show boto3-stubs documentation](./client.md#create-sip-media-application)
        """

    def create_sip_media_application_call(
        self, FromPhoneNumber: str, ToPhoneNumber: str, SipMediaApplicationId: str
    ) -> CreateSipMediaApplicationCallResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.create_sip_media_application_call)
        [Show boto3-stubs documentation](./client.md#create-sip-media-application-call)
        """

    def create_sip_rule(
        self,
        Name: str,
        TriggerType: SipRuleTriggerType,
        TriggerValue: str,
        TargetApplications: List["SipRuleTargetApplicationTypeDef"],
        Disabled: bool = None,
    ) -> CreateSipRuleResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.create_sip_rule)
        [Show boto3-stubs documentation](./client.md#create-sip-rule)
        """

    def create_user(
        self, AccountId: str, Username: str = None, Email: str = None, UserType: UserType = None
    ) -> CreateUserResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.create_user)
        [Show boto3-stubs documentation](./client.md#create-user)
        """

    def create_voice_connector(
        self, Name: str, RequireEncryption: bool, AwsRegion: VoiceConnectorAwsRegion = None
    ) -> CreateVoiceConnectorResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.create_voice_connector)
        [Show boto3-stubs documentation](./client.md#create-voice-connector)
        """

    def create_voice_connector_group(
        self, Name: str, VoiceConnectorItems: List["VoiceConnectorItemTypeDef"] = None
    ) -> CreateVoiceConnectorGroupResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.create_voice_connector_group)
        [Show boto3-stubs documentation](./client.md#create-voice-connector-group)
        """

    def delete_account(self, AccountId: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.delete_account)
        [Show boto3-stubs documentation](./client.md#delete-account)
        """

    def delete_app_instance(self, AppInstanceArn: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.delete_app_instance)
        [Show boto3-stubs documentation](./client.md#delete-app-instance)
        """

    def delete_app_instance_admin(self, AppInstanceAdminArn: str, AppInstanceArn: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.delete_app_instance_admin)
        [Show boto3-stubs documentation](./client.md#delete-app-instance-admin)
        """

    def delete_app_instance_streaming_configurations(self, AppInstanceArn: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.delete_app_instance_streaming_configurations)
        [Show boto3-stubs documentation](./client.md#delete-app-instance-streaming-configurations)
        """

    def delete_app_instance_user(self, AppInstanceUserArn: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.delete_app_instance_user)
        [Show boto3-stubs documentation](./client.md#delete-app-instance-user)
        """

    def delete_attendee(self, MeetingId: str, AttendeeId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.delete_attendee)
        [Show boto3-stubs documentation](./client.md#delete-attendee)
        """

    def delete_channel(self, ChannelArn: str, ChimeBearer: str = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.delete_channel)
        [Show boto3-stubs documentation](./client.md#delete-channel)
        """

    def delete_channel_ban(self, ChannelArn: str, MemberArn: str, ChimeBearer: str = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.delete_channel_ban)
        [Show boto3-stubs documentation](./client.md#delete-channel-ban)
        """

    def delete_channel_membership(
        self, ChannelArn: str, MemberArn: str, ChimeBearer: str = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.delete_channel_membership)
        [Show boto3-stubs documentation](./client.md#delete-channel-membership)
        """

    def delete_channel_message(
        self, ChannelArn: str, MessageId: str, ChimeBearer: str = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.delete_channel_message)
        [Show boto3-stubs documentation](./client.md#delete-channel-message)
        """

    def delete_channel_moderator(
        self, ChannelArn: str, ChannelModeratorArn: str, ChimeBearer: str = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.delete_channel_moderator)
        [Show boto3-stubs documentation](./client.md#delete-channel-moderator)
        """

    def delete_events_configuration(self, AccountId: str, BotId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.delete_events_configuration)
        [Show boto3-stubs documentation](./client.md#delete-events-configuration)
        """

    def delete_meeting(self, MeetingId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.delete_meeting)
        [Show boto3-stubs documentation](./client.md#delete-meeting)
        """

    def delete_phone_number(self, PhoneNumberId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.delete_phone_number)
        [Show boto3-stubs documentation](./client.md#delete-phone-number)
        """

    def delete_proxy_session(self, VoiceConnectorId: str, ProxySessionId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.delete_proxy_session)
        [Show boto3-stubs documentation](./client.md#delete-proxy-session)
        """

    def delete_room(self, AccountId: str, RoomId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.delete_room)
        [Show boto3-stubs documentation](./client.md#delete-room)
        """

    def delete_room_membership(self, AccountId: str, RoomId: str, MemberId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.delete_room_membership)
        [Show boto3-stubs documentation](./client.md#delete-room-membership)
        """

    def delete_sip_media_application(self, SipMediaApplicationId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.delete_sip_media_application)
        [Show boto3-stubs documentation](./client.md#delete-sip-media-application)
        """

    def delete_sip_rule(self, SipRuleId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.delete_sip_rule)
        [Show boto3-stubs documentation](./client.md#delete-sip-rule)
        """

    def delete_voice_connector(self, VoiceConnectorId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.delete_voice_connector)
        [Show boto3-stubs documentation](./client.md#delete-voice-connector)
        """

    def delete_voice_connector_emergency_calling_configuration(self, VoiceConnectorId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.delete_voice_connector_emergency_calling_configuration)
        [Show boto3-stubs documentation](./client.md#delete-voice-connector-emergency-calling-configuration)
        """

    def delete_voice_connector_group(self, VoiceConnectorGroupId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.delete_voice_connector_group)
        [Show boto3-stubs documentation](./client.md#delete-voice-connector-group)
        """

    def delete_voice_connector_origination(self, VoiceConnectorId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.delete_voice_connector_origination)
        [Show boto3-stubs documentation](./client.md#delete-voice-connector-origination)
        """

    def delete_voice_connector_proxy(self, VoiceConnectorId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.delete_voice_connector_proxy)
        [Show boto3-stubs documentation](./client.md#delete-voice-connector-proxy)
        """

    def delete_voice_connector_streaming_configuration(self, VoiceConnectorId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.delete_voice_connector_streaming_configuration)
        [Show boto3-stubs documentation](./client.md#delete-voice-connector-streaming-configuration)
        """

    def delete_voice_connector_termination(self, VoiceConnectorId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.delete_voice_connector_termination)
        [Show boto3-stubs documentation](./client.md#delete-voice-connector-termination)
        """

    def delete_voice_connector_termination_credentials(
        self, VoiceConnectorId: str, Usernames: List[str]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.delete_voice_connector_termination_credentials)
        [Show boto3-stubs documentation](./client.md#delete-voice-connector-termination-credentials)
        """

    def describe_app_instance(self, AppInstanceArn: str) -> DescribeAppInstanceResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.describe_app_instance)
        [Show boto3-stubs documentation](./client.md#describe-app-instance)
        """

    def describe_app_instance_admin(
        self, AppInstanceAdminArn: str, AppInstanceArn: str
    ) -> DescribeAppInstanceAdminResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.describe_app_instance_admin)
        [Show boto3-stubs documentation](./client.md#describe-app-instance-admin)
        """

    def describe_app_instance_user(
        self, AppInstanceUserArn: str
    ) -> DescribeAppInstanceUserResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.describe_app_instance_user)
        [Show boto3-stubs documentation](./client.md#describe-app-instance-user)
        """

    def describe_channel(
        self, ChannelArn: str, ChimeBearer: str = None
    ) -> DescribeChannelResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.describe_channel)
        [Show boto3-stubs documentation](./client.md#describe-channel)
        """

    def describe_channel_ban(
        self, ChannelArn: str, MemberArn: str, ChimeBearer: str = None
    ) -> DescribeChannelBanResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.describe_channel_ban)
        [Show boto3-stubs documentation](./client.md#describe-channel-ban)
        """

    def describe_channel_membership(
        self, ChannelArn: str, MemberArn: str, ChimeBearer: str = None
    ) -> DescribeChannelMembershipResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.describe_channel_membership)
        [Show boto3-stubs documentation](./client.md#describe-channel-membership)
        """

    def describe_channel_membership_for_app_instance_user(
        self, ChannelArn: str, AppInstanceUserArn: str, ChimeBearer: str = None
    ) -> DescribeChannelMembershipForAppInstanceUserResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.describe_channel_membership_for_app_instance_user)
        [Show boto3-stubs documentation](./client.md#describe-channel-membership-for-app-instance-user)
        """

    def describe_channel_moderated_by_app_instance_user(
        self, ChannelArn: str, AppInstanceUserArn: str, ChimeBearer: str = None
    ) -> DescribeChannelModeratedByAppInstanceUserResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.describe_channel_moderated_by_app_instance_user)
        [Show boto3-stubs documentation](./client.md#describe-channel-moderated-by-app-instance-user)
        """

    def describe_channel_moderator(
        self, ChannelArn: str, ChannelModeratorArn: str, ChimeBearer: str = None
    ) -> DescribeChannelModeratorResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.describe_channel_moderator)
        [Show boto3-stubs documentation](./client.md#describe-channel-moderator)
        """

    def disassociate_phone_number_from_user(self, AccountId: str, UserId: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.disassociate_phone_number_from_user)
        [Show boto3-stubs documentation](./client.md#disassociate-phone-number-from-user)
        """

    def disassociate_phone_numbers_from_voice_connector(
        self, VoiceConnectorId: str, E164PhoneNumbers: List[str]
    ) -> DisassociatePhoneNumbersFromVoiceConnectorResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.disassociate_phone_numbers_from_voice_connector)
        [Show boto3-stubs documentation](./client.md#disassociate-phone-numbers-from-voice-connector)
        """

    def disassociate_phone_numbers_from_voice_connector_group(
        self, VoiceConnectorGroupId: str, E164PhoneNumbers: List[str]
    ) -> DisassociatePhoneNumbersFromVoiceConnectorGroupResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.disassociate_phone_numbers_from_voice_connector_group)
        [Show boto3-stubs documentation](./client.md#disassociate-phone-numbers-from-voice-connector-group)
        """

    def disassociate_signin_delegate_groups_from_account(
        self, AccountId: str, GroupNames: List[str]
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.disassociate_signin_delegate_groups_from_account)
        [Show boto3-stubs documentation](./client.md#disassociate-signin-delegate-groups-from-account)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.generate_presigned_url)
        [Show boto3-stubs documentation](./client.md#generate-presigned-url)
        """

    def get_account(self, AccountId: str) -> GetAccountResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_account)
        [Show boto3-stubs documentation](./client.md#get-account)
        """

    def get_account_settings(self, AccountId: str) -> GetAccountSettingsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_account_settings)
        [Show boto3-stubs documentation](./client.md#get-account-settings)
        """

    def get_app_instance_retention_settings(
        self, AppInstanceArn: str
    ) -> GetAppInstanceRetentionSettingsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_app_instance_retention_settings)
        [Show boto3-stubs documentation](./client.md#get-app-instance-retention-settings)
        """

    def get_app_instance_streaming_configurations(
        self, AppInstanceArn: str
    ) -> GetAppInstanceStreamingConfigurationsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_app_instance_streaming_configurations)
        [Show boto3-stubs documentation](./client.md#get-app-instance-streaming-configurations)
        """

    def get_attendee(self, MeetingId: str, AttendeeId: str) -> GetAttendeeResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_attendee)
        [Show boto3-stubs documentation](./client.md#get-attendee)
        """

    def get_bot(self, AccountId: str, BotId: str) -> GetBotResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_bot)
        [Show boto3-stubs documentation](./client.md#get-bot)
        """

    def get_channel_message(
        self, ChannelArn: str, MessageId: str, ChimeBearer: str = None
    ) -> GetChannelMessageResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_channel_message)
        [Show boto3-stubs documentation](./client.md#get-channel-message)
        """

    def get_events_configuration(
        self, AccountId: str, BotId: str
    ) -> GetEventsConfigurationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_events_configuration)
        [Show boto3-stubs documentation](./client.md#get-events-configuration)
        """

    def get_global_settings(self) -> GetGlobalSettingsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_global_settings)
        [Show boto3-stubs documentation](./client.md#get-global-settings)
        """

    def get_meeting(self, MeetingId: str) -> GetMeetingResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_meeting)
        [Show boto3-stubs documentation](./client.md#get-meeting)
        """

    def get_messaging_session_endpoint(self) -> GetMessagingSessionEndpointResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_messaging_session_endpoint)
        [Show boto3-stubs documentation](./client.md#get-messaging-session-endpoint)
        """

    def get_phone_number(self, PhoneNumberId: str) -> GetPhoneNumberResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_phone_number)
        [Show boto3-stubs documentation](./client.md#get-phone-number)
        """

    def get_phone_number_order(self, PhoneNumberOrderId: str) -> GetPhoneNumberOrderResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_phone_number_order)
        [Show boto3-stubs documentation](./client.md#get-phone-number-order)
        """

    def get_phone_number_settings(self) -> GetPhoneNumberSettingsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_phone_number_settings)
        [Show boto3-stubs documentation](./client.md#get-phone-number-settings)
        """

    def get_proxy_session(
        self, VoiceConnectorId: str, ProxySessionId: str
    ) -> GetProxySessionResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_proxy_session)
        [Show boto3-stubs documentation](./client.md#get-proxy-session)
        """

    def get_retention_settings(self, AccountId: str) -> GetRetentionSettingsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_retention_settings)
        [Show boto3-stubs documentation](./client.md#get-retention-settings)
        """

    def get_room(self, AccountId: str, RoomId: str) -> GetRoomResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_room)
        [Show boto3-stubs documentation](./client.md#get-room)
        """

    def get_sip_media_application(
        self, SipMediaApplicationId: str
    ) -> GetSipMediaApplicationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_sip_media_application)
        [Show boto3-stubs documentation](./client.md#get-sip-media-application)
        """

    def get_sip_media_application_logging_configuration(
        self, SipMediaApplicationId: str
    ) -> GetSipMediaApplicationLoggingConfigurationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_sip_media_application_logging_configuration)
        [Show boto3-stubs documentation](./client.md#get-sip-media-application-logging-configuration)
        """

    def get_sip_rule(self, SipRuleId: str) -> GetSipRuleResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_sip_rule)
        [Show boto3-stubs documentation](./client.md#get-sip-rule)
        """

    def get_user(self, AccountId: str, UserId: str) -> GetUserResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_user)
        [Show boto3-stubs documentation](./client.md#get-user)
        """

    def get_user_settings(self, AccountId: str, UserId: str) -> GetUserSettingsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_user_settings)
        [Show boto3-stubs documentation](./client.md#get-user-settings)
        """

    def get_voice_connector(self, VoiceConnectorId: str) -> GetVoiceConnectorResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_voice_connector)
        [Show boto3-stubs documentation](./client.md#get-voice-connector)
        """

    def get_voice_connector_emergency_calling_configuration(
        self, VoiceConnectorId: str
    ) -> GetVoiceConnectorEmergencyCallingConfigurationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_voice_connector_emergency_calling_configuration)
        [Show boto3-stubs documentation](./client.md#get-voice-connector-emergency-calling-configuration)
        """

    def get_voice_connector_group(
        self, VoiceConnectorGroupId: str
    ) -> GetVoiceConnectorGroupResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_voice_connector_group)
        [Show boto3-stubs documentation](./client.md#get-voice-connector-group)
        """

    def get_voice_connector_logging_configuration(
        self, VoiceConnectorId: str
    ) -> GetVoiceConnectorLoggingConfigurationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_voice_connector_logging_configuration)
        [Show boto3-stubs documentation](./client.md#get-voice-connector-logging-configuration)
        """

    def get_voice_connector_origination(
        self, VoiceConnectorId: str
    ) -> GetVoiceConnectorOriginationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_voice_connector_origination)
        [Show boto3-stubs documentation](./client.md#get-voice-connector-origination)
        """

    def get_voice_connector_proxy(
        self, VoiceConnectorId: str
    ) -> GetVoiceConnectorProxyResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_voice_connector_proxy)
        [Show boto3-stubs documentation](./client.md#get-voice-connector-proxy)
        """

    def get_voice_connector_streaming_configuration(
        self, VoiceConnectorId: str
    ) -> GetVoiceConnectorStreamingConfigurationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_voice_connector_streaming_configuration)
        [Show boto3-stubs documentation](./client.md#get-voice-connector-streaming-configuration)
        """

    def get_voice_connector_termination(
        self, VoiceConnectorId: str
    ) -> GetVoiceConnectorTerminationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_voice_connector_termination)
        [Show boto3-stubs documentation](./client.md#get-voice-connector-termination)
        """

    def get_voice_connector_termination_health(
        self, VoiceConnectorId: str
    ) -> GetVoiceConnectorTerminationHealthResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.get_voice_connector_termination_health)
        [Show boto3-stubs documentation](./client.md#get-voice-connector-termination-health)
        """

    def invite_users(
        self, AccountId: str, UserEmailList: List[str], UserType: UserType = None
    ) -> InviteUsersResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.invite_users)
        [Show boto3-stubs documentation](./client.md#invite-users)
        """

    def list_accounts(
        self, Name: str = None, UserEmail: str = None, NextToken: str = None, MaxResults: int = None
    ) -> ListAccountsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_accounts)
        [Show boto3-stubs documentation](./client.md#list-accounts)
        """

    def list_app_instance_admins(
        self, AppInstanceArn: str, MaxResults: int = None, NextToken: str = None
    ) -> ListAppInstanceAdminsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_app_instance_admins)
        [Show boto3-stubs documentation](./client.md#list-app-instance-admins)
        """

    def list_app_instance_users(
        self, AppInstanceArn: str, MaxResults: int = None, NextToken: str = None
    ) -> ListAppInstanceUsersResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_app_instance_users)
        [Show boto3-stubs documentation](./client.md#list-app-instance-users)
        """

    def list_app_instances(
        self, MaxResults: int = None, NextToken: str = None
    ) -> ListAppInstancesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_app_instances)
        [Show boto3-stubs documentation](./client.md#list-app-instances)
        """

    def list_attendee_tags(
        self, MeetingId: str, AttendeeId: str
    ) -> ListAttendeeTagsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_attendee_tags)
        [Show boto3-stubs documentation](./client.md#list-attendee-tags)
        """

    def list_attendees(
        self, MeetingId: str, NextToken: str = None, MaxResults: int = None
    ) -> ListAttendeesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_attendees)
        [Show boto3-stubs documentation](./client.md#list-attendees)
        """

    def list_bots(
        self, AccountId: str, MaxResults: int = None, NextToken: str = None
    ) -> ListBotsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_bots)
        [Show boto3-stubs documentation](./client.md#list-bots)
        """

    def list_channel_bans(
        self,
        ChannelArn: str,
        MaxResults: int = None,
        NextToken: str = None,
        ChimeBearer: str = None,
    ) -> ListChannelBansResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_channel_bans)
        [Show boto3-stubs documentation](./client.md#list-channel-bans)
        """

    def list_channel_memberships(
        self,
        ChannelArn: str,
        Type: ChannelMembershipType = None,
        MaxResults: int = None,
        NextToken: str = None,
        ChimeBearer: str = None,
    ) -> ListChannelMembershipsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_channel_memberships)
        [Show boto3-stubs documentation](./client.md#list-channel-memberships)
        """

    def list_channel_memberships_for_app_instance_user(
        self,
        AppInstanceUserArn: str = None,
        MaxResults: int = None,
        NextToken: str = None,
        ChimeBearer: str = None,
    ) -> ListChannelMembershipsForAppInstanceUserResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_channel_memberships_for_app_instance_user)
        [Show boto3-stubs documentation](./client.md#list-channel-memberships-for-app-instance-user)
        """

    def list_channel_messages(
        self,
        ChannelArn: str,
        SortOrder: SortOrder = None,
        NotBefore: datetime = None,
        NotAfter: datetime = None,
        MaxResults: int = None,
        NextToken: str = None,
        ChimeBearer: str = None,
    ) -> ListChannelMessagesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_channel_messages)
        [Show boto3-stubs documentation](./client.md#list-channel-messages)
        """

    def list_channel_moderators(
        self,
        ChannelArn: str,
        MaxResults: int = None,
        NextToken: str = None,
        ChimeBearer: str = None,
    ) -> ListChannelModeratorsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_channel_moderators)
        [Show boto3-stubs documentation](./client.md#list-channel-moderators)
        """

    def list_channels(
        self,
        AppInstanceArn: str,
        Privacy: ChannelPrivacy = None,
        MaxResults: int = None,
        NextToken: str = None,
        ChimeBearer: str = None,
    ) -> ListChannelsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_channels)
        [Show boto3-stubs documentation](./client.md#list-channels)
        """

    def list_channels_moderated_by_app_instance_user(
        self,
        AppInstanceUserArn: str = None,
        MaxResults: int = None,
        NextToken: str = None,
        ChimeBearer: str = None,
    ) -> ListChannelsModeratedByAppInstanceUserResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_channels_moderated_by_app_instance_user)
        [Show boto3-stubs documentation](./client.md#list-channels-moderated-by-app-instance-user)
        """

    def list_meeting_tags(self, MeetingId: str) -> ListMeetingTagsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_meeting_tags)
        [Show boto3-stubs documentation](./client.md#list-meeting-tags)
        """

    def list_meetings(
        self, NextToken: str = None, MaxResults: int = None
    ) -> ListMeetingsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_meetings)
        [Show boto3-stubs documentation](./client.md#list-meetings)
        """

    def list_phone_number_orders(
        self, NextToken: str = None, MaxResults: int = None
    ) -> ListPhoneNumberOrdersResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_phone_number_orders)
        [Show boto3-stubs documentation](./client.md#list-phone-number-orders)
        """

    def list_phone_numbers(
        self,
        Status: PhoneNumberStatus = None,
        ProductType: PhoneNumberProductType = None,
        FilterName: PhoneNumberAssociationName = None,
        FilterValue: str = None,
        MaxResults: int = None,
        NextToken: str = None,
    ) -> ListPhoneNumbersResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_phone_numbers)
        [Show boto3-stubs documentation](./client.md#list-phone-numbers)
        """

    def list_proxy_sessions(
        self,
        VoiceConnectorId: str,
        Status: ProxySessionStatus = None,
        NextToken: str = None,
        MaxResults: int = None,
    ) -> ListProxySessionsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_proxy_sessions)
        [Show boto3-stubs documentation](./client.md#list-proxy-sessions)
        """

    def list_room_memberships(
        self, AccountId: str, RoomId: str, MaxResults: int = None, NextToken: str = None
    ) -> ListRoomMembershipsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_room_memberships)
        [Show boto3-stubs documentation](./client.md#list-room-memberships)
        """

    def list_rooms(
        self, AccountId: str, MemberId: str = None, MaxResults: int = None, NextToken: str = None
    ) -> ListRoomsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_rooms)
        [Show boto3-stubs documentation](./client.md#list-rooms)
        """

    def list_sip_media_applications(
        self, MaxResults: int = None, NextToken: str = None
    ) -> ListSipMediaApplicationsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_sip_media_applications)
        [Show boto3-stubs documentation](./client.md#list-sip-media-applications)
        """

    def list_sip_rules(
        self, SipMediaApplicationId: str = None, MaxResults: int = None, NextToken: str = None
    ) -> ListSipRulesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_sip_rules)
        [Show boto3-stubs documentation](./client.md#list-sip-rules)
        """

    def list_supported_phone_number_countries(
        self, ProductType: PhoneNumberProductType
    ) -> ListSupportedPhoneNumberCountriesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_supported_phone_number_countries)
        [Show boto3-stubs documentation](./client.md#list-supported-phone-number-countries)
        """

    def list_tags_for_resource(self, ResourceARN: str) -> ListTagsForResourceResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](./client.md#list-tags-for-resource)
        """

    def list_users(
        self,
        AccountId: str,
        UserEmail: str = None,
        UserType: UserType = None,
        MaxResults: int = None,
        NextToken: str = None,
    ) -> ListUsersResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_users)
        [Show boto3-stubs documentation](./client.md#list-users)
        """

    def list_voice_connector_groups(
        self, NextToken: str = None, MaxResults: int = None
    ) -> ListVoiceConnectorGroupsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_voice_connector_groups)
        [Show boto3-stubs documentation](./client.md#list-voice-connector-groups)
        """

    def list_voice_connector_termination_credentials(
        self, VoiceConnectorId: str
    ) -> ListVoiceConnectorTerminationCredentialsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_voice_connector_termination_credentials)
        [Show boto3-stubs documentation](./client.md#list-voice-connector-termination-credentials)
        """

    def list_voice_connectors(
        self, NextToken: str = None, MaxResults: int = None
    ) -> ListVoiceConnectorsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.list_voice_connectors)
        [Show boto3-stubs documentation](./client.md#list-voice-connectors)
        """

    def logout_user(self, AccountId: str, UserId: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.logout_user)
        [Show boto3-stubs documentation](./client.md#logout-user)
        """

    def put_app_instance_retention_settings(
        self,
        AppInstanceArn: str,
        AppInstanceRetentionSettings: "AppInstanceRetentionSettingsTypeDef",
    ) -> PutAppInstanceRetentionSettingsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.put_app_instance_retention_settings)
        [Show boto3-stubs documentation](./client.md#put-app-instance-retention-settings)
        """

    def put_app_instance_streaming_configurations(
        self,
        AppInstanceArn: str,
        AppInstanceStreamingConfigurations: List["AppInstanceStreamingConfigurationTypeDef"],
    ) -> PutAppInstanceStreamingConfigurationsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.put_app_instance_streaming_configurations)
        [Show boto3-stubs documentation](./client.md#put-app-instance-streaming-configurations)
        """

    def put_events_configuration(
        self,
        AccountId: str,
        BotId: str,
        OutboundEventsHTTPSEndpoint: str = None,
        LambdaFunctionArn: str = None,
    ) -> PutEventsConfigurationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.put_events_configuration)
        [Show boto3-stubs documentation](./client.md#put-events-configuration)
        """

    def put_retention_settings(
        self, AccountId: str, RetentionSettings: "RetentionSettingsTypeDef"
    ) -> PutRetentionSettingsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.put_retention_settings)
        [Show boto3-stubs documentation](./client.md#put-retention-settings)
        """

    def put_sip_media_application_logging_configuration(
        self,
        SipMediaApplicationId: str,
        SipMediaApplicationLoggingConfiguration: "SipMediaApplicationLoggingConfigurationTypeDef" = None,
    ) -> PutSipMediaApplicationLoggingConfigurationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.put_sip_media_application_logging_configuration)
        [Show boto3-stubs documentation](./client.md#put-sip-media-application-logging-configuration)
        """

    def put_voice_connector_emergency_calling_configuration(
        self,
        VoiceConnectorId: str,
        EmergencyCallingConfiguration: "EmergencyCallingConfigurationTypeDef",
    ) -> PutVoiceConnectorEmergencyCallingConfigurationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.put_voice_connector_emergency_calling_configuration)
        [Show boto3-stubs documentation](./client.md#put-voice-connector-emergency-calling-configuration)
        """

    def put_voice_connector_logging_configuration(
        self, VoiceConnectorId: str, LoggingConfiguration: "LoggingConfigurationTypeDef"
    ) -> PutVoiceConnectorLoggingConfigurationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.put_voice_connector_logging_configuration)
        [Show boto3-stubs documentation](./client.md#put-voice-connector-logging-configuration)
        """

    def put_voice_connector_origination(
        self, VoiceConnectorId: str, Origination: "OriginationTypeDef"
    ) -> PutVoiceConnectorOriginationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.put_voice_connector_origination)
        [Show boto3-stubs documentation](./client.md#put-voice-connector-origination)
        """

    def put_voice_connector_proxy(
        self,
        VoiceConnectorId: str,
        DefaultSessionExpiryMinutes: int,
        PhoneNumberPoolCountries: List[str],
        FallBackPhoneNumber: str = None,
        Disabled: bool = None,
    ) -> PutVoiceConnectorProxyResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.put_voice_connector_proxy)
        [Show boto3-stubs documentation](./client.md#put-voice-connector-proxy)
        """

    def put_voice_connector_streaming_configuration(
        self, VoiceConnectorId: str, StreamingConfiguration: "StreamingConfigurationTypeDef"
    ) -> PutVoiceConnectorStreamingConfigurationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.put_voice_connector_streaming_configuration)
        [Show boto3-stubs documentation](./client.md#put-voice-connector-streaming-configuration)
        """

    def put_voice_connector_termination(
        self, VoiceConnectorId: str, Termination: "TerminationTypeDef"
    ) -> PutVoiceConnectorTerminationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.put_voice_connector_termination)
        [Show boto3-stubs documentation](./client.md#put-voice-connector-termination)
        """

    def put_voice_connector_termination_credentials(
        self, VoiceConnectorId: str, Credentials: List[CredentialTypeDef] = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.put_voice_connector_termination_credentials)
        [Show boto3-stubs documentation](./client.md#put-voice-connector-termination-credentials)
        """

    def redact_channel_message(
        self, ChannelArn: str, MessageId: str, ChimeBearer: str = None
    ) -> RedactChannelMessageResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.redact_channel_message)
        [Show boto3-stubs documentation](./client.md#redact-channel-message)
        """

    def redact_conversation_message(
        self, AccountId: str, ConversationId: str, MessageId: str
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.redact_conversation_message)
        [Show boto3-stubs documentation](./client.md#redact-conversation-message)
        """

    def redact_room_message(self, AccountId: str, RoomId: str, MessageId: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.redact_room_message)
        [Show boto3-stubs documentation](./client.md#redact-room-message)
        """

    def regenerate_security_token(
        self, AccountId: str, BotId: str
    ) -> RegenerateSecurityTokenResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.regenerate_security_token)
        [Show boto3-stubs documentation](./client.md#regenerate-security-token)
        """

    def reset_personal_pin(self, AccountId: str, UserId: str) -> ResetPersonalPINResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.reset_personal_pin)
        [Show boto3-stubs documentation](./client.md#reset-personal-pin)
        """

    def restore_phone_number(self, PhoneNumberId: str) -> RestorePhoneNumberResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.restore_phone_number)
        [Show boto3-stubs documentation](./client.md#restore-phone-number)
        """

    def search_available_phone_numbers(
        self,
        AreaCode: str = None,
        City: str = None,
        Country: str = None,
        State: str = None,
        TollFreePrefix: str = None,
        PhoneNumberType: PhoneNumberType = None,
        MaxResults: int = None,
        NextToken: str = None,
    ) -> SearchAvailablePhoneNumbersResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.search_available_phone_numbers)
        [Show boto3-stubs documentation](./client.md#search-available-phone-numbers)
        """

    def send_channel_message(
        self,
        ChannelArn: str,
        Content: str,
        Type: ChannelMessageType,
        Persistence: ChannelMessagePersistenceType,
        ClientRequestToken: str,
        Metadata: str = None,
        ChimeBearer: str = None,
    ) -> SendChannelMessageResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.send_channel_message)
        [Show boto3-stubs documentation](./client.md#send-channel-message)
        """

    def tag_attendee(self, MeetingId: str, AttendeeId: str, Tags: List["TagTypeDef"]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.tag_attendee)
        [Show boto3-stubs documentation](./client.md#tag-attendee)
        """

    def tag_meeting(self, MeetingId: str, Tags: List["TagTypeDef"]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.tag_meeting)
        [Show boto3-stubs documentation](./client.md#tag-meeting)
        """

    def tag_resource(self, ResourceARN: str, Tags: List["TagTypeDef"]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.tag_resource)
        [Show boto3-stubs documentation](./client.md#tag-resource)
        """

    def untag_attendee(self, MeetingId: str, AttendeeId: str, TagKeys: List[str]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.untag_attendee)
        [Show boto3-stubs documentation](./client.md#untag-attendee)
        """

    def untag_meeting(self, MeetingId: str, TagKeys: List[str]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.untag_meeting)
        [Show boto3-stubs documentation](./client.md#untag-meeting)
        """

    def untag_resource(self, ResourceARN: str, TagKeys: List[str]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.untag_resource)
        [Show boto3-stubs documentation](./client.md#untag-resource)
        """

    def update_account(self, AccountId: str, Name: str = None) -> UpdateAccountResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.update_account)
        [Show boto3-stubs documentation](./client.md#update-account)
        """

    def update_account_settings(
        self, AccountId: str, AccountSettings: "AccountSettingsTypeDef"
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.update_account_settings)
        [Show boto3-stubs documentation](./client.md#update-account-settings)
        """

    def update_app_instance(
        self, AppInstanceArn: str, Name: str, Metadata: str = None
    ) -> UpdateAppInstanceResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.update_app_instance)
        [Show boto3-stubs documentation](./client.md#update-app-instance)
        """

    def update_app_instance_user(
        self, AppInstanceUserArn: str, Name: str, Metadata: str = None
    ) -> UpdateAppInstanceUserResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.update_app_instance_user)
        [Show boto3-stubs documentation](./client.md#update-app-instance-user)
        """

    def update_bot(
        self, AccountId: str, BotId: str, Disabled: bool = None
    ) -> UpdateBotResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.update_bot)
        [Show boto3-stubs documentation](./client.md#update-bot)
        """

    def update_channel(
        self,
        ChannelArn: str,
        Name: str,
        Mode: ChannelMode,
        Metadata: str = None,
        ChimeBearer: str = None,
    ) -> UpdateChannelResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.update_channel)
        [Show boto3-stubs documentation](./client.md#update-channel)
        """

    def update_channel_message(
        self,
        ChannelArn: str,
        MessageId: str,
        Content: str = None,
        Metadata: str = None,
        ChimeBearer: str = None,
    ) -> UpdateChannelMessageResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.update_channel_message)
        [Show boto3-stubs documentation](./client.md#update-channel-message)
        """

    def update_channel_read_marker(
        self, ChannelArn: str, ChimeBearer: str = None
    ) -> UpdateChannelReadMarkerResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.update_channel_read_marker)
        [Show boto3-stubs documentation](./client.md#update-channel-read-marker)
        """

    def update_global_settings(
        self,
        BusinessCalling: "BusinessCallingSettingsTypeDef",
        VoiceConnector: "VoiceConnectorSettingsTypeDef",
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.update_global_settings)
        [Show boto3-stubs documentation](./client.md#update-global-settings)
        """

    def update_phone_number(
        self,
        PhoneNumberId: str,
        ProductType: PhoneNumberProductType = None,
        CallingName: str = None,
    ) -> UpdatePhoneNumberResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.update_phone_number)
        [Show boto3-stubs documentation](./client.md#update-phone-number)
        """

    def update_phone_number_settings(self, CallingName: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.update_phone_number_settings)
        [Show boto3-stubs documentation](./client.md#update-phone-number-settings)
        """

    def update_proxy_session(
        self,
        VoiceConnectorId: str,
        ProxySessionId: str,
        Capabilities: List[Capability],
        ExpiryMinutes: int = None,
    ) -> UpdateProxySessionResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.update_proxy_session)
        [Show boto3-stubs documentation](./client.md#update-proxy-session)
        """

    def update_room(
        self, AccountId: str, RoomId: str, Name: str = None
    ) -> UpdateRoomResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.update_room)
        [Show boto3-stubs documentation](./client.md#update-room)
        """

    def update_room_membership(
        self, AccountId: str, RoomId: str, MemberId: str, Role: RoomMembershipRole = None
    ) -> UpdateRoomMembershipResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.update_room_membership)
        [Show boto3-stubs documentation](./client.md#update-room-membership)
        """

    def update_sip_media_application(
        self,
        SipMediaApplicationId: str,
        Name: str = None,
        Endpoints: List["SipMediaApplicationEndpointTypeDef"] = None,
    ) -> UpdateSipMediaApplicationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.update_sip_media_application)
        [Show boto3-stubs documentation](./client.md#update-sip-media-application)
        """

    def update_sip_rule(
        self,
        SipRuleId: str,
        Name: str,
        Disabled: bool = None,
        TargetApplications: List["SipRuleTargetApplicationTypeDef"] = None,
    ) -> UpdateSipRuleResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.update_sip_rule)
        [Show boto3-stubs documentation](./client.md#update-sip-rule)
        """

    def update_user(
        self,
        AccountId: str,
        UserId: str,
        LicenseType: License = None,
        UserType: UserType = None,
        AlexaForBusinessMetadata: "AlexaForBusinessMetadataTypeDef" = None,
    ) -> UpdateUserResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.update_user)
        [Show boto3-stubs documentation](./client.md#update-user)
        """

    def update_user_settings(
        self, AccountId: str, UserId: str, UserSettings: "UserSettingsTypeDef"
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.update_user_settings)
        [Show boto3-stubs documentation](./client.md#update-user-settings)
        """

    def update_voice_connector(
        self, VoiceConnectorId: str, Name: str, RequireEncryption: bool
    ) -> UpdateVoiceConnectorResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.update_voice_connector)
        [Show boto3-stubs documentation](./client.md#update-voice-connector)
        """

    def update_voice_connector_group(
        self,
        VoiceConnectorGroupId: str,
        Name: str,
        VoiceConnectorItems: List["VoiceConnectorItemTypeDef"],
    ) -> UpdateVoiceConnectorGroupResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Client.update_voice_connector_group)
        [Show boto3-stubs documentation](./client.md#update-voice-connector-group)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_accounts"]) -> ListAccountsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Paginator.ListAccounts)[Show boto3-stubs documentation](./paginators.md#listaccountspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_users"]) -> ListUsersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/chime.html#Chime.Paginator.ListUsers)[Show boto3-stubs documentation](./paginators.md#listuserspaginator)
        """
