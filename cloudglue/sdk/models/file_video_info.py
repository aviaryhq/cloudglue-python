# coding: utf-8

"""
    Cloudglue API

    API for Cloudglue

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing import Optional, Set
from typing_extensions import Self

class FileVideoInfo(BaseModel):
    """
    Information about the video content
    """ # noqa: E501
    duration_seconds: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Duration of the video in seconds")
    height: Optional[StrictInt] = Field(default=None, description="Height of the video in pixels")
    width: Optional[StrictInt] = Field(default=None, description="Width of the video in pixels")
    format: Optional[StrictStr] = Field(default=None, description="Format of the video file")
    has_audio: Optional[StrictBool] = Field(default=None, description="Whether the video has audio")
    __properties: ClassVar[List[str]] = ["duration_seconds", "height", "width", "format", "has_audio"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of FileVideoInfo from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # set to None if duration_seconds (nullable) is None
        # and model_fields_set contains the field
        if self.duration_seconds is None and "duration_seconds" in self.model_fields_set:
            _dict['duration_seconds'] = None

        # set to None if height (nullable) is None
        # and model_fields_set contains the field
        if self.height is None and "height" in self.model_fields_set:
            _dict['height'] = None

        # set to None if width (nullable) is None
        # and model_fields_set contains the field
        if self.width is None and "width" in self.model_fields_set:
            _dict['width'] = None

        # set to None if format (nullable) is None
        # and model_fields_set contains the field
        if self.format is None and "format" in self.model_fields_set:
            _dict['format'] = None

        # set to None if has_audio (nullable) is None
        # and model_fields_set contains the field
        if self.has_audio is None and "has_audio" in self.model_fields_set:
            _dict['has_audio'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of FileVideoInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "duration_seconds": obj.get("duration_seconds"),
            "height": obj.get("height"),
            "width": obj.get("width"),
            "format": obj.get("format"),
            "has_audio": obj.get("has_audio")
        })
        return _obj


