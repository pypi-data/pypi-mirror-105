"""
Type annotations for lex-models service type definitions.

[Open documentation](./type_defs.md)

Usage::

    ```python
    from mypy_boto3_lex_models.type_defs import BotAliasMetadataTypeDef

    data: BotAliasMetadataTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List

from .literals import (
    ChannelStatus,
    ChannelType,
    ContentType,
    Destination,
    ExportStatus,
    ExportType,
    FulfillmentActivityType,
    ImportStatus,
    Locale,
    LogType,
    MergeStrategy,
    ObfuscationSetting,
    ResourceType,
    SlotConstraint,
    SlotValueSelectionStrategy,
    Status,
)

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "BotAliasMetadataTypeDef",
    "BotChannelAssociationTypeDef",
    "BotMetadataTypeDef",
    "BuiltinIntentMetadataTypeDef",
    "BuiltinIntentSlotTypeDef",
    "BuiltinSlotTypeMetadataTypeDef",
    "CodeHookTypeDef",
    "ConversationLogsRequestTypeDef",
    "ConversationLogsResponseTypeDef",
    "CreateBotVersionResponseTypeDef",
    "CreateIntentVersionResponseTypeDef",
    "CreateSlotTypeVersionResponseTypeDef",
    "EnumerationValueTypeDef",
    "FollowUpPromptTypeDef",
    "FulfillmentActivityTypeDef",
    "GetBotAliasResponseTypeDef",
    "GetBotAliasesResponseTypeDef",
    "GetBotChannelAssociationResponseTypeDef",
    "GetBotChannelAssociationsResponseTypeDef",
    "GetBotResponseTypeDef",
    "GetBotVersionsResponseTypeDef",
    "GetBotsResponseTypeDef",
    "GetBuiltinIntentResponseTypeDef",
    "GetBuiltinIntentsResponseTypeDef",
    "GetBuiltinSlotTypesResponseTypeDef",
    "GetExportResponseTypeDef",
    "GetImportResponseTypeDef",
    "GetIntentResponseTypeDef",
    "GetIntentVersionsResponseTypeDef",
    "GetIntentsResponseTypeDef",
    "GetSlotTypeResponseTypeDef",
    "GetSlotTypeVersionsResponseTypeDef",
    "GetSlotTypesResponseTypeDef",
    "GetUtterancesViewResponseTypeDef",
    "InputContextTypeDef",
    "IntentMetadataTypeDef",
    "IntentTypeDef",
    "KendraConfigurationTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "LogSettingsRequestTypeDef",
    "LogSettingsResponseTypeDef",
    "MessageTypeDef",
    "OutputContextTypeDef",
    "PaginatorConfigTypeDef",
    "PromptTypeDef",
    "PutBotAliasResponseTypeDef",
    "PutBotResponseTypeDef",
    "PutIntentResponseTypeDef",
    "PutSlotTypeResponseTypeDef",
    "SlotDefaultValueSpecTypeDef",
    "SlotDefaultValueTypeDef",
    "SlotTypeConfigurationTypeDef",
    "SlotTypeDef",
    "SlotTypeMetadataTypeDef",
    "SlotTypeRegexConfigurationTypeDef",
    "StartImportResponseTypeDef",
    "StatementTypeDef",
    "TagTypeDef",
    "UtteranceDataTypeDef",
    "UtteranceListTypeDef",
)

BotAliasMetadataTypeDef = TypedDict(
    "BotAliasMetadataTypeDef",
    {
        "name": str,
        "description": str,
        "botVersion": str,
        "botName": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "checksum": str,
        "conversationLogs": "ConversationLogsResponseTypeDef",
    },
    total=False,
)

BotChannelAssociationTypeDef = TypedDict(
    "BotChannelAssociationTypeDef",
    {
        "name": str,
        "description": str,
        "botAlias": str,
        "botName": str,
        "createdDate": datetime,
        "type": ChannelType,
        "botConfiguration": Dict[str, str],
        "status": ChannelStatus,
        "failureReason": str,
    },
    total=False,
)

BotMetadataTypeDef = TypedDict(
    "BotMetadataTypeDef",
    {
        "name": str,
        "description": str,
        "status": Status,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "version": str,
    },
    total=False,
)

BuiltinIntentMetadataTypeDef = TypedDict(
    "BuiltinIntentMetadataTypeDef",
    {
        "signature": str,
        "supportedLocales": List[Locale],
    },
    total=False,
)

BuiltinIntentSlotTypeDef = TypedDict(
    "BuiltinIntentSlotTypeDef",
    {
        "name": str,
    },
    total=False,
)

BuiltinSlotTypeMetadataTypeDef = TypedDict(
    "BuiltinSlotTypeMetadataTypeDef",
    {
        "signature": str,
        "supportedLocales": List[Locale],
    },
    total=False,
)

CodeHookTypeDef = TypedDict(
    "CodeHookTypeDef",
    {
        "uri": str,
        "messageVersion": str,
    },
)

ConversationLogsRequestTypeDef = TypedDict(
    "ConversationLogsRequestTypeDef",
    {
        "logSettings": List["LogSettingsRequestTypeDef"],
        "iamRoleArn": str,
    },
)

ConversationLogsResponseTypeDef = TypedDict(
    "ConversationLogsResponseTypeDef",
    {
        "logSettings": List["LogSettingsResponseTypeDef"],
        "iamRoleArn": str,
    },
    total=False,
)

CreateBotVersionResponseTypeDef = TypedDict(
    "CreateBotVersionResponseTypeDef",
    {
        "name": str,
        "description": str,
        "intents": List["IntentTypeDef"],
        "clarificationPrompt": "PromptTypeDef",
        "abortStatement": "StatementTypeDef",
        "status": Status,
        "failureReason": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "idleSessionTTLInSeconds": int,
        "voiceId": str,
        "checksum": str,
        "version": str,
        "locale": Locale,
        "childDirected": bool,
        "enableModelImprovements": bool,
        "detectSentiment": bool,
    },
    total=False,
)

CreateIntentVersionResponseTypeDef = TypedDict(
    "CreateIntentVersionResponseTypeDef",
    {
        "name": str,
        "description": str,
        "slots": List["SlotTypeDef"],
        "sampleUtterances": List[str],
        "confirmationPrompt": "PromptTypeDef",
        "rejectionStatement": "StatementTypeDef",
        "followUpPrompt": "FollowUpPromptTypeDef",
        "conclusionStatement": "StatementTypeDef",
        "dialogCodeHook": "CodeHookTypeDef",
        "fulfillmentActivity": "FulfillmentActivityTypeDef",
        "parentIntentSignature": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "version": str,
        "checksum": str,
        "kendraConfiguration": "KendraConfigurationTypeDef",
        "inputContexts": List["InputContextTypeDef"],
        "outputContexts": List["OutputContextTypeDef"],
    },
    total=False,
)

CreateSlotTypeVersionResponseTypeDef = TypedDict(
    "CreateSlotTypeVersionResponseTypeDef",
    {
        "name": str,
        "description": str,
        "enumerationValues": List["EnumerationValueTypeDef"],
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "version": str,
        "checksum": str,
        "valueSelectionStrategy": SlotValueSelectionStrategy,
        "parentSlotTypeSignature": str,
        "slotTypeConfigurations": List["SlotTypeConfigurationTypeDef"],
    },
    total=False,
)

_RequiredEnumerationValueTypeDef = TypedDict(
    "_RequiredEnumerationValueTypeDef",
    {
        "value": str,
    },
)
_OptionalEnumerationValueTypeDef = TypedDict(
    "_OptionalEnumerationValueTypeDef",
    {
        "synonyms": List[str],
    },
    total=False,
)


class EnumerationValueTypeDef(_RequiredEnumerationValueTypeDef, _OptionalEnumerationValueTypeDef):
    pass


FollowUpPromptTypeDef = TypedDict(
    "FollowUpPromptTypeDef",
    {
        "prompt": "PromptTypeDef",
        "rejectionStatement": "StatementTypeDef",
    },
)

_RequiredFulfillmentActivityTypeDef = TypedDict(
    "_RequiredFulfillmentActivityTypeDef",
    {
        "type": FulfillmentActivityType,
    },
)
_OptionalFulfillmentActivityTypeDef = TypedDict(
    "_OptionalFulfillmentActivityTypeDef",
    {
        "codeHook": "CodeHookTypeDef",
    },
    total=False,
)


class FulfillmentActivityTypeDef(
    _RequiredFulfillmentActivityTypeDef, _OptionalFulfillmentActivityTypeDef
):
    pass


GetBotAliasResponseTypeDef = TypedDict(
    "GetBotAliasResponseTypeDef",
    {
        "name": str,
        "description": str,
        "botVersion": str,
        "botName": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "checksum": str,
        "conversationLogs": "ConversationLogsResponseTypeDef",
    },
    total=False,
)

GetBotAliasesResponseTypeDef = TypedDict(
    "GetBotAliasesResponseTypeDef",
    {
        "BotAliases": List["BotAliasMetadataTypeDef"],
        "nextToken": str,
    },
    total=False,
)

GetBotChannelAssociationResponseTypeDef = TypedDict(
    "GetBotChannelAssociationResponseTypeDef",
    {
        "name": str,
        "description": str,
        "botAlias": str,
        "botName": str,
        "createdDate": datetime,
        "type": ChannelType,
        "botConfiguration": Dict[str, str],
        "status": ChannelStatus,
        "failureReason": str,
    },
    total=False,
)

GetBotChannelAssociationsResponseTypeDef = TypedDict(
    "GetBotChannelAssociationsResponseTypeDef",
    {
        "botChannelAssociations": List["BotChannelAssociationTypeDef"],
        "nextToken": str,
    },
    total=False,
)

GetBotResponseTypeDef = TypedDict(
    "GetBotResponseTypeDef",
    {
        "name": str,
        "description": str,
        "intents": List["IntentTypeDef"],
        "enableModelImprovements": bool,
        "nluIntentConfidenceThreshold": float,
        "clarificationPrompt": "PromptTypeDef",
        "abortStatement": "StatementTypeDef",
        "status": Status,
        "failureReason": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "idleSessionTTLInSeconds": int,
        "voiceId": str,
        "checksum": str,
        "version": str,
        "locale": Locale,
        "childDirected": bool,
        "detectSentiment": bool,
    },
    total=False,
)

GetBotVersionsResponseTypeDef = TypedDict(
    "GetBotVersionsResponseTypeDef",
    {
        "bots": List["BotMetadataTypeDef"],
        "nextToken": str,
    },
    total=False,
)

GetBotsResponseTypeDef = TypedDict(
    "GetBotsResponseTypeDef",
    {
        "bots": List["BotMetadataTypeDef"],
        "nextToken": str,
    },
    total=False,
)

GetBuiltinIntentResponseTypeDef = TypedDict(
    "GetBuiltinIntentResponseTypeDef",
    {
        "signature": str,
        "supportedLocales": List[Locale],
        "slots": List["BuiltinIntentSlotTypeDef"],
    },
    total=False,
)

GetBuiltinIntentsResponseTypeDef = TypedDict(
    "GetBuiltinIntentsResponseTypeDef",
    {
        "intents": List["BuiltinIntentMetadataTypeDef"],
        "nextToken": str,
    },
    total=False,
)

GetBuiltinSlotTypesResponseTypeDef = TypedDict(
    "GetBuiltinSlotTypesResponseTypeDef",
    {
        "slotTypes": List["BuiltinSlotTypeMetadataTypeDef"],
        "nextToken": str,
    },
    total=False,
)

GetExportResponseTypeDef = TypedDict(
    "GetExportResponseTypeDef",
    {
        "name": str,
        "version": str,
        "resourceType": ResourceType,
        "exportType": ExportType,
        "exportStatus": ExportStatus,
        "failureReason": str,
        "url": str,
    },
    total=False,
)

GetImportResponseTypeDef = TypedDict(
    "GetImportResponseTypeDef",
    {
        "name": str,
        "resourceType": ResourceType,
        "mergeStrategy": MergeStrategy,
        "importId": str,
        "importStatus": ImportStatus,
        "failureReason": List[str],
        "createdDate": datetime,
    },
    total=False,
)

GetIntentResponseTypeDef = TypedDict(
    "GetIntentResponseTypeDef",
    {
        "name": str,
        "description": str,
        "slots": List["SlotTypeDef"],
        "sampleUtterances": List[str],
        "confirmationPrompt": "PromptTypeDef",
        "rejectionStatement": "StatementTypeDef",
        "followUpPrompt": "FollowUpPromptTypeDef",
        "conclusionStatement": "StatementTypeDef",
        "dialogCodeHook": "CodeHookTypeDef",
        "fulfillmentActivity": "FulfillmentActivityTypeDef",
        "parentIntentSignature": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "version": str,
        "checksum": str,
        "kendraConfiguration": "KendraConfigurationTypeDef",
        "inputContexts": List["InputContextTypeDef"],
        "outputContexts": List["OutputContextTypeDef"],
    },
    total=False,
)

GetIntentVersionsResponseTypeDef = TypedDict(
    "GetIntentVersionsResponseTypeDef",
    {
        "intents": List["IntentMetadataTypeDef"],
        "nextToken": str,
    },
    total=False,
)

GetIntentsResponseTypeDef = TypedDict(
    "GetIntentsResponseTypeDef",
    {
        "intents": List["IntentMetadataTypeDef"],
        "nextToken": str,
    },
    total=False,
)

GetSlotTypeResponseTypeDef = TypedDict(
    "GetSlotTypeResponseTypeDef",
    {
        "name": str,
        "description": str,
        "enumerationValues": List["EnumerationValueTypeDef"],
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "version": str,
        "checksum": str,
        "valueSelectionStrategy": SlotValueSelectionStrategy,
        "parentSlotTypeSignature": str,
        "slotTypeConfigurations": List["SlotTypeConfigurationTypeDef"],
    },
    total=False,
)

GetSlotTypeVersionsResponseTypeDef = TypedDict(
    "GetSlotTypeVersionsResponseTypeDef",
    {
        "slotTypes": List["SlotTypeMetadataTypeDef"],
        "nextToken": str,
    },
    total=False,
)

GetSlotTypesResponseTypeDef = TypedDict(
    "GetSlotTypesResponseTypeDef",
    {
        "slotTypes": List["SlotTypeMetadataTypeDef"],
        "nextToken": str,
    },
    total=False,
)

GetUtterancesViewResponseTypeDef = TypedDict(
    "GetUtterancesViewResponseTypeDef",
    {
        "botName": str,
        "utterances": List["UtteranceListTypeDef"],
    },
    total=False,
)

InputContextTypeDef = TypedDict(
    "InputContextTypeDef",
    {
        "name": str,
    },
)

IntentMetadataTypeDef = TypedDict(
    "IntentMetadataTypeDef",
    {
        "name": str,
        "description": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "version": str,
    },
    total=False,
)

IntentTypeDef = TypedDict(
    "IntentTypeDef",
    {
        "intentName": str,
        "intentVersion": str,
    },
)

_RequiredKendraConfigurationTypeDef = TypedDict(
    "_RequiredKendraConfigurationTypeDef",
    {
        "kendraIndex": str,
        "role": str,
    },
)
_OptionalKendraConfigurationTypeDef = TypedDict(
    "_OptionalKendraConfigurationTypeDef",
    {
        "queryFilterString": str,
    },
    total=False,
)


class KendraConfigurationTypeDef(
    _RequiredKendraConfigurationTypeDef, _OptionalKendraConfigurationTypeDef
):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": List["TagTypeDef"],
    },
    total=False,
)

_RequiredLogSettingsRequestTypeDef = TypedDict(
    "_RequiredLogSettingsRequestTypeDef",
    {
        "logType": LogType,
        "destination": Destination,
        "resourceArn": str,
    },
)
_OptionalLogSettingsRequestTypeDef = TypedDict(
    "_OptionalLogSettingsRequestTypeDef",
    {
        "kmsKeyArn": str,
    },
    total=False,
)


class LogSettingsRequestTypeDef(
    _RequiredLogSettingsRequestTypeDef, _OptionalLogSettingsRequestTypeDef
):
    pass


LogSettingsResponseTypeDef = TypedDict(
    "LogSettingsResponseTypeDef",
    {
        "logType": LogType,
        "destination": Destination,
        "kmsKeyArn": str,
        "resourceArn": str,
        "resourcePrefix": str,
    },
    total=False,
)

_RequiredMessageTypeDef = TypedDict(
    "_RequiredMessageTypeDef",
    {
        "contentType": ContentType,
        "content": str,
    },
)
_OptionalMessageTypeDef = TypedDict(
    "_OptionalMessageTypeDef",
    {
        "groupNumber": int,
    },
    total=False,
)


class MessageTypeDef(_RequiredMessageTypeDef, _OptionalMessageTypeDef):
    pass


OutputContextTypeDef = TypedDict(
    "OutputContextTypeDef",
    {
        "name": str,
        "timeToLiveInSeconds": int,
        "turnsToLive": int,
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredPromptTypeDef = TypedDict(
    "_RequiredPromptTypeDef",
    {
        "messages": List["MessageTypeDef"],
        "maxAttempts": int,
    },
)
_OptionalPromptTypeDef = TypedDict(
    "_OptionalPromptTypeDef",
    {
        "responseCard": str,
    },
    total=False,
)


class PromptTypeDef(_RequiredPromptTypeDef, _OptionalPromptTypeDef):
    pass


PutBotAliasResponseTypeDef = TypedDict(
    "PutBotAliasResponseTypeDef",
    {
        "name": str,
        "description": str,
        "botVersion": str,
        "botName": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "checksum": str,
        "conversationLogs": "ConversationLogsResponseTypeDef",
        "tags": List["TagTypeDef"],
    },
    total=False,
)

PutBotResponseTypeDef = TypedDict(
    "PutBotResponseTypeDef",
    {
        "name": str,
        "description": str,
        "intents": List["IntentTypeDef"],
        "enableModelImprovements": bool,
        "nluIntentConfidenceThreshold": float,
        "clarificationPrompt": "PromptTypeDef",
        "abortStatement": "StatementTypeDef",
        "status": Status,
        "failureReason": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "idleSessionTTLInSeconds": int,
        "voiceId": str,
        "checksum": str,
        "version": str,
        "locale": Locale,
        "childDirected": bool,
        "createVersion": bool,
        "detectSentiment": bool,
        "tags": List["TagTypeDef"],
    },
    total=False,
)

PutIntentResponseTypeDef = TypedDict(
    "PutIntentResponseTypeDef",
    {
        "name": str,
        "description": str,
        "slots": List["SlotTypeDef"],
        "sampleUtterances": List[str],
        "confirmationPrompt": "PromptTypeDef",
        "rejectionStatement": "StatementTypeDef",
        "followUpPrompt": "FollowUpPromptTypeDef",
        "conclusionStatement": "StatementTypeDef",
        "dialogCodeHook": "CodeHookTypeDef",
        "fulfillmentActivity": "FulfillmentActivityTypeDef",
        "parentIntentSignature": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "version": str,
        "checksum": str,
        "createVersion": bool,
        "kendraConfiguration": "KendraConfigurationTypeDef",
        "inputContexts": List["InputContextTypeDef"],
        "outputContexts": List["OutputContextTypeDef"],
    },
    total=False,
)

PutSlotTypeResponseTypeDef = TypedDict(
    "PutSlotTypeResponseTypeDef",
    {
        "name": str,
        "description": str,
        "enumerationValues": List["EnumerationValueTypeDef"],
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "version": str,
        "checksum": str,
        "valueSelectionStrategy": SlotValueSelectionStrategy,
        "createVersion": bool,
        "parentSlotTypeSignature": str,
        "slotTypeConfigurations": List["SlotTypeConfigurationTypeDef"],
    },
    total=False,
)

SlotDefaultValueSpecTypeDef = TypedDict(
    "SlotDefaultValueSpecTypeDef",
    {
        "defaultValueList": List["SlotDefaultValueTypeDef"],
    },
)

SlotDefaultValueTypeDef = TypedDict(
    "SlotDefaultValueTypeDef",
    {
        "defaultValue": str,
    },
)

SlotTypeConfigurationTypeDef = TypedDict(
    "SlotTypeConfigurationTypeDef",
    {
        "regexConfiguration": "SlotTypeRegexConfigurationTypeDef",
    },
    total=False,
)

_RequiredSlotTypeDef = TypedDict(
    "_RequiredSlotTypeDef",
    {
        "name": str,
        "slotConstraint": SlotConstraint,
    },
)
_OptionalSlotTypeDef = TypedDict(
    "_OptionalSlotTypeDef",
    {
        "description": str,
        "slotType": str,
        "slotTypeVersion": str,
        "valueElicitationPrompt": "PromptTypeDef",
        "priority": int,
        "sampleUtterances": List[str],
        "responseCard": str,
        "obfuscationSetting": ObfuscationSetting,
        "defaultValueSpec": "SlotDefaultValueSpecTypeDef",
    },
    total=False,
)


class SlotTypeDef(_RequiredSlotTypeDef, _OptionalSlotTypeDef):
    pass


SlotTypeMetadataTypeDef = TypedDict(
    "SlotTypeMetadataTypeDef",
    {
        "name": str,
        "description": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "version": str,
    },
    total=False,
)

SlotTypeRegexConfigurationTypeDef = TypedDict(
    "SlotTypeRegexConfigurationTypeDef",
    {
        "pattern": str,
    },
)

StartImportResponseTypeDef = TypedDict(
    "StartImportResponseTypeDef",
    {
        "name": str,
        "resourceType": ResourceType,
        "mergeStrategy": MergeStrategy,
        "importId": str,
        "importStatus": ImportStatus,
        "tags": List["TagTypeDef"],
        "createdDate": datetime,
    },
    total=False,
)

_RequiredStatementTypeDef = TypedDict(
    "_RequiredStatementTypeDef",
    {
        "messages": List["MessageTypeDef"],
    },
)
_OptionalStatementTypeDef = TypedDict(
    "_OptionalStatementTypeDef",
    {
        "responseCard": str,
    },
    total=False,
)


class StatementTypeDef(_RequiredStatementTypeDef, _OptionalStatementTypeDef):
    pass


TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "key": str,
        "value": str,
    },
)

UtteranceDataTypeDef = TypedDict(
    "UtteranceDataTypeDef",
    {
        "utteranceString": str,
        "count": int,
        "distinctUsers": int,
        "firstUtteredDate": datetime,
        "lastUtteredDate": datetime,
    },
    total=False,
)

UtteranceListTypeDef = TypedDict(
    "UtteranceListTypeDef",
    {
        "botVersion": str,
        "utterances": List["UtteranceDataTypeDef"],
    },
    total=False,
)
