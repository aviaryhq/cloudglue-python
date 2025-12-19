# cloudglue/client/resources/thumbnails.py
"""Thumbnails resource for CloudGlue API."""
from typing import Optional

from cloudglue.sdk.models.thumbnails_config import ThumbnailsConfig

from cloudglue.client.resources.base import CloudGlueError


class Thumbnails:
    """Thumbnails API client"""

    def __init__(self, api):
        self.api = api

    def get_thumbnails(
        self,
        file_id: str,
        is_default: Optional[bool] = None,
        segmentation_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        type: Optional[str] = None,
    ):
        """
        Get thumbnails for a file.
        
        Args:
            file_id: The ID of the file
            is_default: Filter thumbnails by default status. If true, will only return the default thumbnail for the file
            segmentation_id: Filter thumbnails by segmentation ID
            limit: Number of thumbnails to return
            offset: Offset from the start of the list
            type: Filter thumbnails by type ('segment', 'keyframe', 'file', 'frame')
            
        Returns:
            ThumbnailList response
        """
        try:
            response = self.api.get_thumbnails(
                file_id=file_id,
                is_default=is_default,
                segmentation_id=segmentation_id,
                limit=limit,
                offset=offset,
                type=type,
            )
            return response
        except Exception as e:
            if hasattr(e, 'status') and hasattr(e, 'data'):
                raise CloudGlueError(
                    message=str(e),
                    status_code=e.status,
                    data=e.data,
                    headers=getattr(e, 'headers', None),
                    reason=getattr(e, 'reason', None),
                )
            raise e

    def get_segmentation_thumbnails(
        self,
        segmentation_id: str,
        segment_ids: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        type: Optional[str] = None,
    ):
        """
        Get thumbnails for a segmentation.
        
        Args:
            segmentation_id: The ID of the segmentation to retrieve thumbnails for
            segment_ids: Filter thumbnails by segment IDs. If provided, will only return thumbnails for the specified segments. Comma separated list of segment IDs.
            limit: Number of thumbnails to return
            offset: Offset from the start of the list
            type: Filter thumbnails by type ('segment', 'keyframe', 'file', 'frame')
            
        Returns:
            ThumbnailList response
        """
        try:
            response = self.api.get_segmentation_thumbnails(
                segmentation_id=segmentation_id,
                segment_ids=segment_ids,
                limit=limit,
                offset=offset,
                type=type,
            )
            return response
        except Exception as e:
            if hasattr(e, 'status') and hasattr(e, 'data'):
                raise CloudGlueError(
                    message=str(e),
                    status_code=e.status,
                    data=e.data,
                    headers=getattr(e, 'headers', None),
                    reason=getattr(e, 'reason', None),
                )
            raise e

    @staticmethod
    def create_thumbnails_config(enable_segment_thumbnails: bool = True):
        """
        Create a thumbnails configuration object.
        
        Args:
            enable_segment_thumbnails: Whether to enable segment thumbnails
            
        Returns:
            ThumbnailsConfig object
        """                
        return ThumbnailsConfig(
            enable_segment_thumbnails=enable_segment_thumbnails
        )

