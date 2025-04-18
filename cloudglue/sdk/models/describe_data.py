# coding: utf-8

"""
    cloudglue API

    API for cloudglue

    The version of the OpenAPI document: 0.0.9
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from cloudglue.sdk.models.describe_data_segment_docs_inner import DescribeDataSegmentDocsInner
from typing import Optional, Set
from typing_extensions import Self

class DescribeData(BaseModel):
    """
    The comprehensive description data for the video
    """ # noqa: E501
    url: Optional[StrictStr] = Field(default=None, description="The URL of the processed video")
    title: Optional[StrictStr] = Field(default=None, description="Generated title for the video")
    summary: Optional[StrictStr] = Field(default=None, description="Generated summary of the video content")
    segment_docs: Optional[List[DescribeDataSegmentDocsInner]] = Field(default=None, description="Array of video segments with detailed information")
    __properties: ClassVar[List[str]] = ["url", "title", "summary", "segment_docs"]

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
        """Create an instance of DescribeData from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in segment_docs (list)
        _items = []
        if self.segment_docs:
            for _item_segment_docs in self.segment_docs:
                if _item_segment_docs:
                    _items.append(_item_segment_docs.to_dict())
            _dict['segment_docs'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DescribeData from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "url": obj.get("url"),
            "title": obj.get("title"),
            "summary": obj.get("summary"),
            "segment_docs": [DescribeDataSegmentDocsInner.from_dict(_item) for _item in obj["segment_docs"]] if obj.get("segment_docs") is not None else None
        })
        return _obj


