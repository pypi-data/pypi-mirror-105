"""
Type annotations for polly service type definitions.

[Open documentation](./type_defs.md)

Usage::

    ```python
    from mypy_boto3_polly.type_defs import DescribeVoicesOutputTypeDef

    data: DescribeVoicesOutputTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List

from botocore.response import StreamingBody

from .literals import (
    Engine,
    Gender,
    LanguageCode,
    OutputFormat,
    SpeechMarkType,
    TaskStatus,
    TextType,
    VoiceId,
)

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "DescribeVoicesOutputTypeDef",
    "GetLexiconOutputTypeDef",
    "GetSpeechSynthesisTaskOutputTypeDef",
    "LexiconAttributesTypeDef",
    "LexiconDescriptionTypeDef",
    "LexiconTypeDef",
    "ListLexiconsOutputTypeDef",
    "ListSpeechSynthesisTasksOutputTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "StartSpeechSynthesisTaskOutputTypeDef",
    "SynthesisTaskTypeDef",
    "SynthesizeSpeechOutputTypeDef",
    "VoiceTypeDef",
)

DescribeVoicesOutputTypeDef = TypedDict(
    "DescribeVoicesOutputTypeDef",
    {
        "Voices": List["VoiceTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetLexiconOutputTypeDef = TypedDict(
    "GetLexiconOutputTypeDef",
    {
        "Lexicon": "LexiconTypeDef",
        "LexiconAttributes": "LexiconAttributesTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetSpeechSynthesisTaskOutputTypeDef = TypedDict(
    "GetSpeechSynthesisTaskOutputTypeDef",
    {
        "SynthesisTask": "SynthesisTaskTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

LexiconAttributesTypeDef = TypedDict(
    "LexiconAttributesTypeDef",
    {
        "Alphabet": str,
        "LanguageCode": LanguageCode,
        "LastModified": datetime,
        "LexiconArn": str,
        "LexemesCount": int,
        "Size": int,
    },
    total=False,
)

LexiconDescriptionTypeDef = TypedDict(
    "LexiconDescriptionTypeDef",
    {
        "Name": str,
        "Attributes": "LexiconAttributesTypeDef",
    },
    total=False,
)

LexiconTypeDef = TypedDict(
    "LexiconTypeDef",
    {
        "Content": str,
        "Name": str,
    },
    total=False,
)

ListLexiconsOutputTypeDef = TypedDict(
    "ListLexiconsOutputTypeDef",
    {
        "Lexicons": List["LexiconDescriptionTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListSpeechSynthesisTasksOutputTypeDef = TypedDict(
    "ListSpeechSynthesisTasksOutputTypeDef",
    {
        "NextToken": str,
        "SynthesisTasks": List["SynthesisTaskTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
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

StartSpeechSynthesisTaskOutputTypeDef = TypedDict(
    "StartSpeechSynthesisTaskOutputTypeDef",
    {
        "SynthesisTask": "SynthesisTaskTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SynthesisTaskTypeDef = TypedDict(
    "SynthesisTaskTypeDef",
    {
        "Engine": Engine,
        "TaskId": str,
        "TaskStatus": TaskStatus,
        "TaskStatusReason": str,
        "OutputUri": str,
        "CreationTime": datetime,
        "RequestCharacters": int,
        "SnsTopicArn": str,
        "LexiconNames": List[str],
        "OutputFormat": OutputFormat,
        "SampleRate": str,
        "SpeechMarkTypes": List[SpeechMarkType],
        "TextType": TextType,
        "VoiceId": VoiceId,
        "LanguageCode": LanguageCode,
    },
    total=False,
)

SynthesizeSpeechOutputTypeDef = TypedDict(
    "SynthesizeSpeechOutputTypeDef",
    {
        "AudioStream": StreamingBody,
        "ContentType": str,
        "RequestCharacters": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

VoiceTypeDef = TypedDict(
    "VoiceTypeDef",
    {
        "Gender": Gender,
        "Id": VoiceId,
        "LanguageCode": LanguageCode,
        "LanguageName": str,
        "Name": str,
        "AdditionalLanguageCodes": List[LanguageCode],
        "SupportedEngines": List[Engine],
    },
    total=False,
)
