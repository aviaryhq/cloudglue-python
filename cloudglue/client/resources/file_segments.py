# cloudglue/client/resources/file_segments.py
"""File Segments resource for CloudGlue API."""
from typing import Dict, Any, Optional

from cloudglue.sdk.models.update_file_segment_request import UpdateFileSegmentRequest
from cloudglue.sdk.rest import ApiException

from cloudglue.client.resources.base import CloudGlueError


class FileSegments:
    """Client for the CloudGlue File Segments API."""

    def __init__(self, api):
        """Initialize the FileSegments client.

        Args:
            api: The FileSegmentsApi instance.
        """
        self.api = api

    def get(self, file_id: str, segment_id: str):
        """Get a specific file segment.

        Args:
            file_id: The ID of the file
            segment_id: The ID of the segment

        Returns:
            FileSegment object

        Raises:
            CloudGlueError: If there is an error retrieving the segment.
        """
        try:
            response = self.api.get_file_segment(file_id=file_id, segment_id=segment_id)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def update(
        self,
        file_id: str,
        segment_id: str,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """Update a file segment's metadata.

        Args:
            file_id: The ID of the file
            segment_id: The ID of the segment
            metadata: Optional metadata to update on the segment

        Returns:
            FileSegment object

        Raises:
            CloudGlueError: If there is an error updating the segment.
        """
        try:
            request = UpdateFileSegmentRequest(metadata=metadata)
            response = self.api.update_file_segment(
                file_id=file_id,
                segment_id=segment_id,
                update_file_segment_request=request,
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def list_tags(self, file_id: str, segment_id: str):
        """List all tags for a specific file segment.

        Args:
            file_id: The ID of the file
            segment_id: The ID of the segment

        Returns:
            ListVideoTagsResponse object

        Raises:
            CloudGlueError: If there is an error listing segment tags.
        """
        try:
            response = self.api.list_file_segment_tags(file_id=file_id, segment_id=segment_id)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

