from typing import Any, Literal

from pydantic import Field, validator

from azuma.validators import is_valid_date_format

from .detection import Detection
from .log_source import LogSource
from .related import Related
from .yaml_model import YAMLBaseModel


class Rule(YAMLBaseModel):
    title: str = Field(
        ...,
        max_length=256,
        min_length=1,
        description="A brief title for the rule that should contain what the rules is supposed to detect (max. 256 characters)",
    )
    detection: Detection = Field(
        ...,
        description="A set of search-identifiers that represent properties of searches on log data.",
    )
    logsource: LogSource = Field(
        ...,
        description="This section describes the log data on which the detection is meant to be applied to. It describes the log source, the platform, the application and the type that is required in the detection.",
    )

    id: str | None = Field(
        default=None,
        description="Sigma rules should be identified by a globally unique identifier in the id attribute. For this purpose randomly generated UUIDs (version 4) are recommended but not mandatory.",
    )
    license: str | None = Field(
        default=None,
        description="License of the rule according the SPDX ID specification.",
    )
    author: str | None = Field(
        default=None,
        description="Creator of the rule. (can be a name, nickname, twitter handle…etc)",
    )
    date: str | None = Field(
        default=None, description="Creation date of the rule. Use the format YYYY/MM/DD"
    )
    modified: str | None = Field(
        default=None,
        description="Last modification date of the rule. Use the format YYYY/MM/DD",
    )
    description: str | None = Field(
        default=None,
        max_length=65535,
        description="A short description of the rule and the malicious activity that can be detected (max. 65,535 characters)",
    )

    status: None | (
        Literal["stable", "test", "experimental", "deprecated", "unsupported"]
    ) = Field(default=None, description="The status of the rule")
    level: None | (
        Literal["informational", "low", "medium", "high", "critical"]
    ) = Field(
        default=None,
        description="The level field contains one of five string values. It describes the criticality of a triggered rule. While low and medium level events have an informative character, events with high and critical level should lead to immediate reviews by security analysts.",
    )

    references: list[str] | None = Field(
        default=None,
        description="References to the source that the rule was derived from. These could be blog articles, technical papers, presentations or even tweets.",
    )
    tags: list[str] | None = Field(default=None)
    flaivepositives: list[str] | None = Field(
        default=None, description="A list of known false positives that may occur."
    )
    fields: list[str] | None = Field(
        default=None,
        description="A list of log fields that could be interesting in further analysis of the event and should be displayed to the analyst.",
    )

    related: list[Related] | None = Field(default=None)

    @validator("detection", pre=True)
    def transform_detection(cls, v: Any):
        return Detection.parse_obj(v)

    @validator("date", "modified")
    def validate_date_format(cls, v: str | None):
        if v is None:
            return v

        if not is_valid_date_format(v):
            raise ValueError("Use YYYY/MM/DD format")

        return v

    def match(self, event: dict[Any, Any]) -> bool:
        """Check whether an event is matched with the rule or not

        Args:
            event (dict[Any, Any]): Event

        Returns:
            bool: Returns True if an event is matched with the rule. False if not
        """
        if not isinstance(event, dict):
            raise ValueError("event should be a dict")

        return self.detection.condition(self, event)
