# cloudglue/client/resources/face_detection.py
"""Face Detection resource for CloudGlue API."""
import time
from typing import Dict, Any, Optional, Union

from cloudglue.sdk.models.face_detection_request import FaceDetectionRequest
from cloudglue.sdk.models.frame_extraction_config import FrameExtractionConfig
from cloudglue.sdk.rest import ApiException

from cloudglue.client.resources.base import CloudGlueError


class FaceDetection:
    """Client for the CloudGlue Face Detection API."""

    def __init__(self, api):
        """Initialize the FaceDetection client.

        Args:
            api: The FaceDetectionApi instance.
        """
        self.api = api

    @staticmethod
    def create_face_detection_request(
        url: str,
        frame_extraction_id: Optional[str] = None,
        frame_extraction_config: Optional[Union[FrameExtractionConfig, Dict[str, Any]]] = None,
        **kwargs
    ) -> FaceDetectionRequest:
        """Create a face detection request configuration.

        Args:
            url: URL of the target video to analyze
            frame_extraction_id: Optional ID of previously extracted frames
            frame_extraction_config: Optional frame extraction configuration
            **kwargs: Additional parameters

        Returns:
            FaceDetectionRequest object
        """
        request_params = {
            "url": url,
            "frame_extraction_id": frame_extraction_id,
            **kwargs
        }
        
        if frame_extraction_config is not None:
            if isinstance(frame_extraction_config, dict):
                request_params["frame_extraction_config"] = FrameExtractionConfig(**frame_extraction_config)
            else:
                request_params["frame_extraction_config"] = frame_extraction_config
                
        return FaceDetectionRequest(**request_params)

    def create(
        self,
        face_detection_request: Union[FaceDetectionRequest, Dict[str, Any]],
    ):
        """Create a face detection job.

        Args:
            face_detection_request: Face detection request parameters

        Returns:
            FaceDetection object

        Raises:
            CloudGlueError: If there is an error creating the face detection job.
        """
        try:
            if isinstance(face_detection_request, dict):
                face_detection_request = FaceDetectionRequest(**face_detection_request)
            
            response = self.api.create_face_detection(face_detection_request)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def get(
        self,
        face_detection_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """Get face detection results.

        Args:
            face_detection_id: The ID of the face detection to retrieve
            limit: Number of detected faces to return
            offset: Offset from the start of the detected faces list

        Returns:
            FaceDetection object

        Raises:
            CloudGlueError: If the request fails
        """
        try:
            response = self.api.get_face_detection(
                face_detection_id=face_detection_id,
                limit=limit,
                offset=offset,
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def list(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        created_before: Optional[str] = None,
        created_after: Optional[str] = None,
        status: Optional[str] = None,
    ):
        """List all face detection jobs.

        Args:
            limit: Number of face detection jobs to return (default 50, max 100)
            offset: Offset from the start of the face detection jobs list
            created_before: Filter jobs created before this date (YYYY-MM-DD format, UTC)
            created_after: Filter jobs created after this date (YYYY-MM-DD format, UTC)
            status: Filter by status ('pending', 'processing', 'completed', 'failed')

        Returns:
            FaceDetectionListResponse object containing list of face detection jobs

        Raises:
            CloudGlueError: If the request fails
        """
        try:
            response = self.api.list_face_detection(
                limit=limit,
                offset=offset,
                created_before=created_before,
                created_after=created_after,
                status=status,
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def delete(self, face_detection_id: str):
        """Delete a face detection analysis.

        Args:
            face_detection_id: The ID of the face detection to delete

        Returns:
            The deletion confirmation

        Raises:
            CloudGlueError: If there is an error deleting the face detection.
        """
        try:
            response = self.api.delete_face_detection(face_detection_id=face_detection_id)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def run(
        self,
        url: str,
        frame_extraction_id: Optional[str] = None,
        frame_extraction_config: Optional[Union[FrameExtractionConfig, Dict[str, Any]]] = None,
        poll_interval: int = 5,
        timeout: int = 600,
        **kwargs
    ):
        """Create and run a face detection job to completion.

        Args:
            url: URL of the target video to analyze
            frame_extraction_id: Optional ID of previously extracted frames
            frame_extraction_config: Optional frame extraction configuration
            poll_interval: How often to check the job status (in seconds)
            timeout: Maximum time to wait for the job to complete (in seconds)
            **kwargs: Additional parameters for the request

        Returns:
            FaceDetection: The completed face detection object with status and results

        Raises:
            CloudGlueError: If there is an error creating or processing the face detection job.
            TimeoutError: If the job does not complete within the specified timeout.
        """
        try:
            # Create the face detection job
            request = self.create_face_detection_request(
                url=url,
                frame_extraction_id=frame_extraction_id,
                frame_extraction_config=frame_extraction_config,
                **kwargs
            )
            job = self.create(request)
            face_detection_id = job.face_detection_id

            # Poll for completion
            elapsed = 0
            while elapsed < timeout:
                status = self.get(face_detection_id=face_detection_id)

                if status.status in ["completed", "failed"]:
                    return status

                time.sleep(poll_interval)
                elapsed += poll_interval

            raise TimeoutError(
                f"Face detection job did not complete within {timeout} seconds"
            )
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

