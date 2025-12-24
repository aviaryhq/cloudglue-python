# cloudglue/client/resources/face_match.py
"""Face Match resource for CloudGlue API."""
import base64
import os
import pathlib
import time
from typing import Dict, Any, Optional, Union

from cloudglue.sdk.models.face_match_request import FaceMatchRequest
from cloudglue.sdk.models.source_image import SourceImage
from cloudglue.sdk.models.frame_extraction_config import FrameExtractionConfig
from cloudglue.sdk.rest import ApiException

from cloudglue.client.resources.base import CloudGlueError


class FaceMatch:
    """Client for the CloudGlue Face Match API."""

    def __init__(self, api):
        """Initialize the FaceMatch client.

        Args:
            api: The FaceMatchApi instance.
        """
        self.api = api

    @staticmethod
    def encode_image_file(file_path: str) -> str:
        """Convert a local image file to base64 string.

        Args:
            file_path: Path to the image file (JPG/PNG only)

        Returns:
            Base64 encoded image string

        Raises:
            CloudGlueError: If file is not found, not a valid image type, or cannot be read
        """
        try:
            if not os.path.exists(file_path):
                raise CloudGlueError(f"File not found: {file_path}")
            
            # Check file extension
            file_ext = pathlib.Path(file_path).suffix.lower()
            if file_ext not in ['.jpg', '.jpeg', '.png']:
                raise CloudGlueError(f"Unsupported file type: {file_ext}. Only JPG and PNG are supported.")
            
            # Read and encode the file
            with open(file_path, 'rb') as image_file:
                image_data = image_file.read()
                base64_string = base64.b64encode(image_data).decode('utf-8')
                return base64_string
                
        except Exception as e:
            if isinstance(e, CloudGlueError):
                raise
            raise CloudGlueError(f"Error encoding image file: {str(e)}")

    @staticmethod
    def create_face_match_request(
        source_image: Union[str, Dict[str, Any]],
        target_video_url: str,
        max_faces: Optional[int] = None,
        face_detection_id: Optional[str] = None,
        frame_extraction_id: Optional[str] = None,
        frame_extraction_config: Optional[Union[FrameExtractionConfig, Dict[str, Any]]] = None,
        **kwargs
    ) -> FaceMatchRequest:
        """Create a face match request configuration.

        Args:
            source_image: Source image - can be:
                - URL string (public image URL)
                - Local file path (will be converted to base64)
                - Base64 string (raw base64 or with data: prefix)
                - Dictionary with 'url' or 'base64_image' keys
            target_video_url: URL of the target video to search in
            max_faces: Maximum number of faces to return
            face_detection_id: Optional ID of previously analyzed face detections
            frame_extraction_id: Optional ID of previously extracted frames
            frame_extraction_config: Optional frame extraction configuration
            **kwargs: Additional parameters

        Returns:
            FaceMatchRequest object

        Raises:
            CloudGlueError: If source_image format is invalid or file operations fail
        """
        try:
            # Handle source_image parameter
            source_image_obj = None
            
            if isinstance(source_image, dict):
                # Already in SourceImage format
                source_image_obj = SourceImage(**source_image)
            elif isinstance(source_image, str):
                if source_image.startswith(('http://', 'https://')):
                    # URL
                    source_image_obj = SourceImage(url=source_image)
                elif source_image.startswith('data:image/'):
                    # Data URL - extract base64 part
                    base64_part = source_image.split(',')[1] if ',' in source_image else source_image
                    source_image_obj = SourceImage(base64_image=base64_part)
                elif os.path.exists(source_image):
                    # File path
                    base64_data = FaceMatch.encode_image_file(source_image)
                    source_image_obj = SourceImage(base64_image=base64_data)
                else:
                    # Assume raw base64 string
                    source_image_obj = SourceImage(base64_image=source_image)
            else:
                raise CloudGlueError("source_image must be a string (URL, file path, or base64) or dictionary")
            
            request_params = {
                "source_image": source_image_obj,
                "target_video_url": target_video_url,
                "max_faces": max_faces,
                "face_detection_id": face_detection_id,
                "frame_extraction_id": frame_extraction_id,
                **kwargs
            }
            
            if frame_extraction_config is not None:
                if isinstance(frame_extraction_config, dict):
                    request_params["frame_extraction_config"] = FrameExtractionConfig(**frame_extraction_config)
                else:
                    request_params["frame_extraction_config"] = frame_extraction_config
                    
            return FaceMatchRequest(**request_params)
            
        except Exception as e:
            if isinstance(e, CloudGlueError):
                raise
            raise CloudGlueError(f"Error creating face match request: {str(e)}")

    def create(
        self,
        face_match_request: Union[FaceMatchRequest, Dict[str, Any]],
    ):
        """Create a face match job.

        Args:
            face_match_request: Face match request parameters

        Returns:
            FaceMatch object

        Raises:
            CloudGlueError: If there is an error creating the face match job.
        """
        try:
            if isinstance(face_match_request, dict):
                face_match_request = FaceMatchRequest(**face_match_request)
            
            response = self.api.create_face_match(face_match_request)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def get(
        self,
        face_match_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """Get face match results.

        Args:
            face_match_id: The ID of the face match to retrieve
            limit: Number of face matches to return
            offset: Offset from the start of the face matches list

        Returns:
            FaceMatch object

        Raises:
            CloudGlueError: If the request fails
        """
        try:
            response = self.api.get_face_match(
                face_match_id=face_match_id,
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
    ):
        """List all face match jobs.

        Args:
            limit: Number of face match jobs to return (default 50, max 100)
            offset: Offset from the start of the face match jobs list

        Returns:
            FaceMatchListResponse object containing list of face match jobs

        Raises:
            CloudGlueError: If the request fails
        """
        try:
            response = self.api.list_face_match(
                limit=limit,
                offset=offset,
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def delete(self, face_match_id: str):
        """Delete a face match analysis.

        Args:
            face_match_id: The ID of the face match to delete

        Returns:
            The deletion confirmation

        Raises:
            CloudGlueError: If there is an error deleting the face match.
        """
        try:
            response = self.api.delete_face_match(face_match_id=face_match_id)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def run(
        self,
        source_image: Union[str, Dict[str, Any]],
        target_video_url: str,
        max_faces: Optional[int] = None,
        face_detection_id: Optional[str] = None,
        frame_extraction_id: Optional[str] = None,
        frame_extraction_config: Optional[Union[FrameExtractionConfig, Dict[str, Any]]] = None,
        poll_interval: int = 5,
        timeout: int = 600,
        **kwargs
    ):
        """Create and run a face match job to completion.

        Args:
            source_image: Source image containing the face to search for
            target_video_url: URL of the target video to search in
            max_faces: Maximum number of faces to return
            face_detection_id: Optional ID of previously analyzed face detections
            frame_extraction_id: Optional ID of previously extracted frames
            frame_extraction_config: Optional frame extraction configuration
            poll_interval: How often to check the job status (in seconds)
            timeout: Maximum time to wait for the job to complete (in seconds)
            **kwargs: Additional parameters for the request

        Returns:
            FaceMatch: The completed face match object with status and results

        Raises:
            CloudGlueError: If there is an error creating or processing the face match job.
            TimeoutError: If the job does not complete within the specified timeout.
        """
        try:
            # Create the face match job
            request = self.create_face_match_request(
                source_image=source_image,
                target_video_url=target_video_url,
                max_faces=max_faces,
                face_detection_id=face_detection_id,
                frame_extraction_id=frame_extraction_id,
                frame_extraction_config=frame_extraction_config,
                **kwargs
            )
            job = self.create(request)
            face_match_id = job.face_match_id

            # Poll for completion
            elapsed = 0
            while elapsed < timeout:
                status = self.get(face_match_id=face_match_id)

                if status.status in ["completed", "failed"]:
                    return status

                time.sleep(poll_interval)
                elapsed += poll_interval

            raise TimeoutError(
                f"Face match job did not complete within {timeout} seconds"
            )
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

