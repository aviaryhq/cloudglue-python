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

    def list(
        self,
        file_id: str,
        start_time_after: Optional[float] = None,
        end_time_before: Optional[float] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """List all segments for a file.

        Args:
            file_id: The ID of the file
            start_time_after: Filter segments by start time (seconds)
            end_time_before: Filter segments by end time (seconds)
            limit: Number of segments to return (max 100)
            offset: Offset from the start of the list

        Returns:
            FileSegmentListResponse containing segments

        Raises:
            CloudGlueError: If there is an error listing segments.
        """
        try:
            response = self.api.list_file_segments(
                file_id=file_id,
                start_time_after=start_time_after,
                end_time_before=end_time_before,
                limit=limit,
                offset=offset,
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def get_describe(
        self,
        file_id: str,
        segment_id: str,
        job_id: str,
        response_format: Optional[str] = None,
    ):
        """Get a specific describe output for a file segment by job ID.

        Args:
            file_id: The ID of the file
            segment_id: The ID of the segment
            job_id: The ID of the describe job
            response_format: Output format for the describe data ('json' or 'markdown')

        Returns:
            SegmentDescribe object

        Raises:
            CloudGlueError: If there is an error retrieving the segment describe.
        """
        try:
            response = self.api.get_file_segment_describe(
                file_id=file_id,
                segment_id=segment_id,
                job_id=job_id,
                response_format=response_format,
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def list_describes(
        self,
        file_id: str,
        segment_id: str,
        include_data: Optional[bool] = None,
        response_format: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """List all describe outputs for a file segment.

        Args:
            file_id: The ID of the file
            segment_id: The ID of the segment
            include_data: Include the describe data in the response
            response_format: Output format for the describe data ('json' or 'markdown')
            limit: Number of describes to return (max 100)
            offset: Offset from the start of the list

        Returns:
            SegmentDescribeListResponse containing segment describes

        Raises:
            CloudGlueError: If there is an error listing segment describes.
        """
        try:
            response = self.api.list_file_segment_describes(
                file_id=file_id,
                segment_id=segment_id,
                include_data=include_data,
                response_format=response_format,
                limit=limit,
                offset=offset,
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

