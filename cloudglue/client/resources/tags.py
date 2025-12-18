# cloudglue/client/resources/tags.py
"""Tags resource for CloudGlue API."""
from typing import Optional

from cloudglue.sdk.models.create_video_tag_request import CreateVideoTagRequest
from cloudglue.sdk.models.update_video_tag_request import UpdateVideoTagRequest
from cloudglue.sdk.rest import ApiException

from cloudglue.client.resources.base import CloudGlueError


class Tags:
    """Client for the CloudGlue Tags API."""

    def __init__(self, api):
        """Initialize the Tags client.

        Args:
            api: The TagsApi instance.
        """
        self.api = api

    def create(
        self,
        label: str,
        value: str,
        file_id: str,
        segment_id: Optional[str] = None,
    ):
        """Create a new tag for a file or segment.

        Args:
            label: The label of the tag
            value: The value of the tag
            file_id: The ID of the file to tag
            segment_id: Optional ID of the segment to tag (for segment-level tags)

        Returns:
            VideoTag object

        Raises:
            CloudGlueError: If there is an error creating the tag.
        """
        try:
            request = CreateVideoTagRequest(
                label=label,
                value=value,
                file_id=file_id,
                segment_id=segment_id,
            )
            response = self.api.create_tag(request)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def get(self, tag_id: str):
        """Get a tag by ID.

        Args:
            tag_id: The ID of the tag to retrieve

        Returns:
            VideoTag object

        Raises:
            CloudGlueError: If there is an error retrieving the tag.
        """
        try:
            response = self.api.get_tag(tag_id=tag_id)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def update(
        self,
        tag_id: str,
        label: Optional[str] = None,
        value: Optional[str] = None,
    ):
        """Update a tag.

        Args:
            tag_id: The ID of the tag to update
            label: Optional new label for the tag
            value: Optional new value for the tag

        Returns:
            VideoTag object

        Raises:
            CloudGlueError: If there is an error updating the tag.
        """
        try:
            request = UpdateVideoTagRequest(
                label=label,
                value=value,
            )
            response = self.api.update_tag(tag_id=tag_id, update_video_tag_request=request)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def delete(self, tag_id: str):
        """Delete a tag.

        Args:
            tag_id: The ID of the tag to delete

        Returns:
            The deletion confirmation

        Raises:
            CloudGlueError: If there is an error deleting the tag.
        """
        try:
            response = self.api.delete_tag(tag_id=tag_id)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def list(
        self,
        type: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """List all tags.

        Args:
            type: Filter tags by type ('file' or 'segment')
            limit: Maximum number of tags to return (max 100)
            offset: Number of tags to skip

        Returns:
            ListVideoTagsResponse object

        Raises:
            CloudGlueError: If there is an error listing tags.
        """
        try:
            response = self.api.list_tags(
                type=type,
                limit=limit,
                offset=offset,
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def list_file_tags(self, file_id: str):
        """List all tags for a specific file.

        Args:
            file_id: The ID of the file

        Returns:
            ListVideoTagsResponse object

        Raises:
            CloudGlueError: If there is an error listing file tags.
        """
        try:
            response = self.api.list_file_tags(file_id=file_id)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def list_file_segment_tags(self, file_id: str, segment_id: str):
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

