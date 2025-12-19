# cloudglue/client/resources/frames.py
"""Frames resource for CloudGlue API."""
from typing import Dict, Any, Optional, Union

from cloudglue.sdk.models.frame_extraction_config import FrameExtractionConfig
from cloudglue.sdk.models.frame_extraction_uniform_config import FrameExtractionUniformConfig
from cloudglue.sdk.models.frame_extraction_thumbnails_config import FrameExtractionThumbnailsConfig
from cloudglue.sdk.rest import ApiException

from cloudglue.client.resources.base import CloudGlueError


class Frames:
    """Client for the CloudGlue Frames API."""

    def __init__(self, api):
        """Initialize the Frames client.

        Args:
            api: The FramesApi instance.
        """
        self.api = api

    @staticmethod
    def create_uniform_config(
        frames_per_second: Optional[float] = 1.0,
        max_width: Optional[int] = 1024,
    ) -> FrameExtractionUniformConfig:
        """Create a uniform frame extraction configuration.

        Args:
            frames_per_second: Number of frames to extract per second (0.1-30)
            max_width: Maximum width of extracted frames in pixels (64-4096)

        Returns:
            FrameExtractionUniformConfig object
        """
        return FrameExtractionUniformConfig(
            frames_per_second=frames_per_second,
            max_width=max_width
        )

    @staticmethod
    def create_thumbnails_config(
        **kwargs
    ) -> FrameExtractionThumbnailsConfig:
        """Create a frame extraction thumbnails configuration.

        Args:
            **kwargs: Configuration parameters for thumbnails

        Returns:
            FrameExtractionThumbnailsConfig object
        """
        return FrameExtractionThumbnailsConfig(**kwargs)

    @staticmethod
    def create_frame_extraction_request(
        url: str,
        frame_extraction_config: Optional[Union[FrameExtractionConfig, Dict[str, Any]]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Create a frame extraction request configuration.

        Note: Frame extraction jobs are created through the Files API using 
        client.files.create_frame_extraction(). This method is for creating
        configuration dictionaries for other APIs that accept frame extraction parameters.

        Args:
            url: URL of the target video to extract frames from
            frame_extraction_config: Optional frame extraction configuration
            **kwargs: Additional parameters

        Returns:
            Dictionary with frame extraction request parameters
        """
        request_params = {
            "url": url,
            **kwargs
        }
        
        if frame_extraction_config is not None:
            if isinstance(frame_extraction_config, dict):
                request_params["frame_extraction_config"] = FrameExtractionConfig(**frame_extraction_config)
            else:
                request_params["frame_extraction_config"] = frame_extraction_config
                
        return request_params

    def get(
        self,
        frame_extraction_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """Get a specific frame extraction including its frames.

        Args:
            frame_extraction_id: The ID of the frame extraction to retrieve
            limit: Number of frames to return (max 100)
            offset: Offset from the start of the frames list

        Returns:
            The typed FrameExtraction object with frames and metadata

        Raises:
            CloudGlueError: If there is an error retrieving the frame extraction or processing the request.
        """
        try:
            response = self.api.get_frame_extraction(
                frame_extraction_id=frame_extraction_id,
                limit=limit,
                offset=offset,
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def delete(self, frame_extraction_id: str):
        """Delete a frame extraction.

        Args:
            frame_extraction_id: The ID of the frame extraction to delete

        Returns:
            The deletion confirmation

        Raises:
            CloudGlueError: If there is an error deleting the frame extraction or processing the request.
        """
        try:
            response = self.api.delete_frame_extraction(frame_extraction_id=frame_extraction_id)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

