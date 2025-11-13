# cloudglue/client/resources.py
from typing import List, Dict, Any, Optional, Union
import os
import pathlib
import time
import json
import base64
import mimetypes

from cloudglue.sdk.models.chat_completion_request import ChatCompletionRequest
from cloudglue.sdk.models.chat_completion_request_filter import ChatCompletionRequestFilter
from cloudglue.sdk.models.chat_completion_request_filter_metadata_inner import ChatCompletionRequestFilterMetadataInner
from cloudglue.sdk.models.chat_completion_request_filter_video_info_inner import ChatCompletionRequestFilterVideoInfoInner  
from cloudglue.sdk.models.chat_completion_request_filter_file_inner import ChatCompletionRequestFilterFileInner
from cloudglue.sdk.models.new_transcribe import NewTranscribe
from cloudglue.sdk.models.new_describe import NewDescribe
from cloudglue.sdk.models.new_extract import NewExtract
from cloudglue.sdk.models.new_collection import NewCollection
from cloudglue.sdk.models.add_collection_file import AddCollectionFile
from cloudglue.sdk.models.file_update import FileUpdate
from cloudglue.sdk.models.segmentation_config import SegmentationConfig
from cloudglue.sdk.models.segmentation_uniform_config import SegmentationUniformConfig
from cloudglue.sdk.models.segmentation_shot_detector_config import SegmentationShotDetectorConfig
from cloudglue.sdk.models.segmentation_manual_config import SegmentationManualConfig
from cloudglue.sdk.models.segmentation_manual_config_segments_inner import SegmentationManualConfigSegmentsInner
from cloudglue.sdk.models.search_request import SearchRequest
from cloudglue.sdk.models.search_filter import SearchFilter
from cloudglue.sdk.models.search_filter_criteria import SearchFilterCriteria
from cloudglue.sdk.models.search_filter_file_inner import SearchFilterFileInner
from cloudglue.sdk.models.search_filter_video_info_inner import SearchFilterVideoInfoInner
from cloudglue.sdk.rest import ApiException
from cloudglue.sdk.models.thumbnails_config import ThumbnailsConfig
from cloudglue.sdk.api.segmentations_api import SegmentationsApi
from cloudglue.sdk.models.create_file_segmentation_request import CreateFileSegmentationRequest
from cloudglue.sdk.models.new_segments import NewSegments
from cloudglue.sdk.models.shot_config import ShotConfig
from cloudglue.sdk.models.narrative_config import NarrativeConfig
from cloudglue.sdk.models.segments import Segments
from cloudglue.sdk.models.segments_list import SegmentsList
from cloudglue.sdk.models.delete_segments200_response import DeleteSegments200Response
from cloudglue.sdk.models.collection_update import CollectionUpdate
from cloudglue.sdk.models.frame_extraction import FrameExtraction
from cloudglue.sdk.models.delete_frame_extraction200_response import DeleteFrameExtraction200Response
from cloudglue.sdk.models.face_detection import FaceDetection
from cloudglue.sdk.models.face_detection_request import FaceDetectionRequest
from cloudglue.sdk.models.delete_face_detection200_response import DeleteFaceDetection200Response
from cloudglue.sdk.models.face_match import FaceMatch
from cloudglue.sdk.models.face_match_request import FaceMatchRequest
from cloudglue.sdk.models.delete_face_match200_response import DeleteFaceMatch200Response
from cloudglue.sdk.models.source_image import SourceImage
from cloudglue.sdk.models.frame_extraction_config import FrameExtractionConfig
from cloudglue.sdk.models.create_file_frame_extraction_request import CreateFileFrameExtractionRequest
from cloudglue.sdk.models.frame_extraction_uniform_config import FrameExtractionUniformConfig
from cloudglue.sdk.models.frame_extraction_thumbnails_config import FrameExtractionThumbnailsConfig
from cloudglue.sdk.models.new_collection_face_detection_config import NewCollectionFaceDetectionConfig
from cloudglue.sdk.models.collection_face_detection_config_frame_extraction_config import CollectionFaceDetectionConfigFrameExtractionConfig
from cloudglue.sdk.models.collection_face_detection_config_thumbnails_config import CollectionFaceDetectionConfigThumbnailsConfig
from cloudglue.sdk.models.collection_face_detection_config_frame_extraction_config_uniform_config import CollectionFaceDetectionConfigFrameExtractionConfigUniformConfig
from cloudglue.sdk.models.file_face_detections import FileFaceDetections
from cloudglue.sdk.models.search_request_source_image import SearchRequestSourceImage


class CloudGlueError(Exception):
    """Base exception for CloudGlue errors."""

    def __init__(
        self,
        message: str,
        status_code: int = None,
        data: Any = None,
        headers: Dict[str, str] = None,
        reason: str = None,
    ):
        self.message = message
        self.status_code = status_code
        self.data = data
        self.headers = headers
        self.reason = reason
        super(CloudGlueError, self).__init__(self.message)


class Completions:
    """Handles chat completions operations."""

    def __init__(self, api):
        """Initialize with the API client."""
        self.api = api

    @staticmethod
    def _create_metadata_filter(
        path: str,
        operator: str,
        value_text: Optional[str] = None,
        value_text_array: Optional[List[str]] = None,
    ) -> ChatCompletionRequestFilterMetadataInner:
        """Create a metadata filter.
        
        Args:
            path: JSON path on metadata object (e.g. 'my_custom_field', 'category.subcategory')
            operator: Comparison operator ('NotEqual', 'Equal', 'LessThan', 'GreaterThan', 'In', 'ContainsAny', 'ContainsAll')
            value_text: Text value for scalar comparison (used with NotEqual, Equal, LessThan, GreaterThan, In)
            value_text_array: Array of values for array comparisons (used with ContainsAny, ContainsAll)
            
        Returns:
            ChatCompletionRequestFilterMetadataInner object
        """
        return ChatCompletionRequestFilterMetadataInner(
            path=path,
            operator=operator,
            value_text=value_text,
            value_text_array=value_text_array,
        )

    @staticmethod
    def _create_video_info_filter(
        path: str,
        operator: str,
        value_text: Optional[str] = None,
        value_text_array: Optional[List[str]] = None,
    ) -> ChatCompletionRequestFilterVideoInfoInner:
        """Create a video info filter.
        
        Args:
            path: JSON path on video_info object (e.g. 'has_audio', 'duration_seconds')
            operator: Comparison operator ('NotEqual', 'Equal', 'LessThan', 'GreaterThan', 'In', 'ContainsAny', 'ContainsAll')
            value_text: Text value for scalar comparison (used with NotEqual, Equal, LessThan, GreaterThan, In)
            value_text_array: Array of values for array comparisons (used with ContainsAny, ContainsAll)
            
        Returns:
            ChatCompletionRequestFilterVideoInfoInner object
        """
        return ChatCompletionRequestFilterVideoInfoInner(
            path=path,
            operator=operator,
            value_text=value_text,
            value_text_array=value_text_array,
        )

    @staticmethod
    def _create_file_filter(
        path: str,
        operator: str,
        value_text: Optional[str] = None,
        value_text_array: Optional[List[str]] = None,
    ) -> ChatCompletionRequestFilterFileInner:
        """Create a file filter.
        
        Args:
            path: JSON path on file object (e.g. 'uri', 'id', 'filename', 'created_at', 'bytes')
            operator: Comparison operator ('NotEqual', 'Equal', 'LessThan', 'GreaterThan', 'In', 'ContainsAny', 'ContainsAll')
            value_text: Text value for scalar comparison (used with NotEqual, Equal, LessThan, GreaterThan, In)
            value_text_array: Array of values for array comparisons (used with ContainsAny, ContainsAll)
            
        Returns:
            ChatCompletionRequestFilterFileInner object
        """
        return ChatCompletionRequestFilterFileInner(
            path=path,
            operator=operator,
            value_text=value_text,
            value_text_array=value_text_array,
        )

    @staticmethod
    def _create_filter(
        metadata: Optional[List[ChatCompletionRequestFilterMetadataInner]] = None,
        video_info: Optional[List[ChatCompletionRequestFilterVideoInfoInner]] = None,
        file: Optional[List[ChatCompletionRequestFilterFileInner]] = None,
    ) -> ChatCompletionRequestFilter:
        """Create a chat completion filter.
        
        Args:
            metadata: List of metadata filters
            video_info: List of video info filters  
            file: List of file filters
            
        Returns:
            ChatCompletionRequestFilter object
        """
        return ChatCompletionRequestFilter(
            metadata=metadata,
            video_info=video_info,
            file=file,
        )

    @staticmethod
    def create_filter(
        metadata_filters: Optional[List[Dict[str, Any]]] = None,
        video_info_filters: Optional[List[Dict[str, Any]]] = None,
        file_filters: Optional[List[Dict[str, Any]]] = None,
    ) -> ChatCompletionRequestFilter:
        """Create a chat completion filter using simple dictionaries.
        
        This is the main method for creating filters. It allows you to create filters 
        using simple dictionaries instead of working with the underlying filter objects.
        
        Args:
            metadata_filters: List of metadata filter dictionaries. Each dict should have:
                - 'path': JSON path on metadata object
                - 'operator': Comparison operator
                - 'value_text': (optional) Text value for scalar comparison  
                - 'value_text_array': (optional) Array of values for array comparisons
            video_info_filters: List of video info filter dictionaries (same structure)
            file_filters: List of file filter dictionaries (same structure)
            
        Returns:
            ChatCompletionRequestFilter object
            
        Example:
            filter = client.chat.completions.create_filter(
                metadata_filters=[
                    {'path': 'category', 'operator': 'Equal', 'value_text': 'tutorial'},
                    {'path': 'tags', 'operator': 'ContainsAny', 'value_text_array': ['python', 'programming']}
                ],
                video_info_filters=[
                    {'path': 'duration_seconds', 'operator': 'LessThan', 'value_text': '600'}
                ]
            )
        """
        metadata_objs = None
        if metadata_filters:
            metadata_objs = [
                ChatCompletionRequestFilterMetadataInner(**f) for f in metadata_filters
            ]
            
        video_info_objs = None
        if video_info_filters:
            video_info_objs = [
                ChatCompletionRequestFilterVideoInfoInner(**f) for f in video_info_filters
            ]
            
        file_objs = None
        if file_filters:
            file_objs = [
                ChatCompletionRequestFilterFileInner(**f) for f in file_filters
            ]
            
        return ChatCompletionRequestFilter(
            metadata=metadata_objs,
            video_info=video_info_objs,
            file=file_objs,
        )

    def create(
        self,
        messages: List[Dict[str, str]],
        model: str = "nimbus-001",
        collections: Optional[List[str]] = None,
        filter: Optional[Union[ChatCompletionRequestFilter, Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
        **kwargs,
    ):
        """Create a chat completion.

        Args:
            messages: List of message dictionaries with "role" and "content" keys.
            model: The model to use for completion.
            collections: List of collection IDs to search.
            filter: Filter criteria to constrain search results. Can be a ChatCompletionRequestFilter object
                   or a dictionary with 'metadata', 'video_info', and/or 'file' keys.
            temperature: Sampling temperature. If None, uses API default.
            **kwargs: Additional parameters for the request.

        Returns:
            The API response with generated completion.

        Raises:
            CloudGlueError: If there is an error making the API request or processing the response.
        """
        try:
            # Handle filter parameter
            if filter is not None:
                if isinstance(filter, dict):
                    # Convert dictionary to ChatCompletionRequestFilter
                    filter = ChatCompletionRequestFilter.from_dict(filter)
                elif isinstance(filter, ChatCompletionRequestFilter):
                    # Already the correct type, no conversion needed
                    pass
                else:
                    raise ValueError("filter must be a ChatCompletionRequestFilter object or dictionary")
            
            request = ChatCompletionRequest(
                model=model,
                messages=messages,
                collections=collections or [],
                filter=filter,
                temperature=temperature,
                **kwargs,
            )
            return self.api.create_completion(chat_completion_request=request)
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))


class Collections:
    """Client for the CloudGlue Collections API."""

    def __init__(self, api):
        """Initialize the Collections client.

        Args:
            api: The DefaultApi instance.
        """
        self.api = api

    def create(
        self,
        collection_type: str,
        name: str,
        description: Optional[str] = None,
        extract_config: Optional[Dict[str, Any]] = None,
        transcribe_config: Optional[Dict[str, Any]] = None,
        describe_config: Optional[Dict[str, Any]] = None,
        default_segmentation_config: Optional[Union[SegmentationConfig, Dict[str, Any]]] = None,
        face_detection_config: Optional[Union[NewCollectionFaceDetectionConfig, Dict[str, Any]]] = None,
    ):
        """Create a new collection.

        Args:
            collection_type: Type of collection ('entities', 'rich-transcripts', 'media-descriptions', 'face-analysis')
            name: Name of the collection (must be unique)
            description: Optional description of the collection
            extract_config: Optional configuration for extraction processing
            transcribe_config: Optional configuration for transcription processing
            describe_config: Optional configuration for media description processing
            default_segmentation_config: Default segmentation configuration for files in this collection
            face_detection_config: Optional configuration for face detection processing

        Returns:
            The typed Collection object with all properties

        Raises:
            CloudGlueError: If there is an error creating the collection or processing the request.
        """
        try:
            # Create request object using the SDK model
            if description is None:  # TODO(kdr): temporary fix for API
                description = ""

            # Handle default_segmentation_config parameter
            if isinstance(default_segmentation_config, dict):
                default_segmentation_config = SegmentationConfig.from_dict(default_segmentation_config)

            # Handle face_detection_config parameter
            if isinstance(face_detection_config, dict):
                face_detection_config = NewCollectionFaceDetectionConfig.from_dict(face_detection_config)

            request = NewCollection(
                collection_type=collection_type,
                name=name,
                description=description,
                extract_config=extract_config,
                transcribe_config=transcribe_config,
                describe_config=describe_config,
                default_segmentation_config=default_segmentation_config,
                face_detection_config=face_detection_config,
            )
            # Use the standard method to get a properly typed object
            response = self.api.create_collection(new_collection=request)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def list(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order: Optional[str] = None,
        sort: Optional[str] = None,
        collection_type: Optional[str] = None,
    ):
        """List collections.

        Args:
            limit: Maximum number of collections to return (max 100)
            offset: Number of collections to skip
            order: Field to sort by ('created_at'). Defaults to 'created_at'
            sort: Sort direction ('asc', 'desc'). Defaults to 'desc'
            collection_type: Filter by collection type ('video', 'audio', 'image', 'text')

        Returns:
            The typed CollectionList object with collections and metadata

        Raises:
            CloudGlueError: If there is an error listing collections or processing the request.
        """
        try:
            # Use the standard method to get a properly typed object
            response = self.api.list_collections(
                limit=limit, offset=offset, order=order, sort=sort, collection_type=collection_type
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def get(self, collection_id: str):
        """Get a specific collection by ID.

        Args:
            collection_id: The ID of the collection to retrieve

        Returns:
            The typed Collection object with all properties

        Raises:
            CloudGlueError: If there is an error retrieving the collection or processing the request.
        """
        try:
            # Use the standard method to get a properly typed object
            response = self.api.get_collection(collection_id=collection_id)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def delete(self, collection_id: str):
        """Delete a collection.

        Args:
            collection_id: The ID of the collection to delete

        Returns:
            The typed DeleteResponse object with deletion confirmation

        Raises:
            CloudGlueError: If there is an error deleting the collection or processing the request.
        """
        try:
            # Use the standard method to get a properly typed object
            response = self.api.delete_collection(collection_id=collection_id)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def update(
        self,
        collection_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        """Update a collection.

        Args:
            collection_id: The ID of the collection to update
            name: New name for the collection
            description: New description for the collection

        Returns:
            The updated Collection object

        Raises:
            CloudGlueError: If there is an error updating the collection or processing the request.
        """
        try:
            # Create update request object
            update_data = {}
            if name is not None:
                update_data["name"] = name
            if description is not None:
                update_data["description"] = description
            
            if not update_data:
                raise CloudGlueError("At least one field (name or description) must be provided for update")
            
            collection_update = CollectionUpdate(**update_data)
            response = self.api.update_collection(
                collection_id=collection_id,
                collection_update=collection_update
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def add_video(
        self,
        collection_id: str,
        file_id: Optional[str] = None,
        url: Optional[str] = None,
        segmentation_id: Optional[str] = None,
        segmentation_config: Optional[Union[SegmentationConfig, Dict[str, Any]]] = None,
        wait_until_finish: bool = False,
        poll_interval: int = 5,
        timeout: int = 600,
    ):
        """Add a video file to a collection.

        Args:
            collection_id: The ID of the collection
            file_id: The ID of the file to add to the collection (optional, either file_id or url is required)
            url: The URL of the file to add to the collection (optional, either file_id or url is required)
            segmentation_id: Segmentation job id to use. Cannot be provided together with segmentation_config.
            segmentation_config: Configuration for video segmentation. Cannot be provided together with segmentation_id.
            wait_until_finish: Whether to wait for the video processing to complete
            poll_interval: How often to check the video status (in seconds) if waiting
            timeout: Maximum time to wait for processing (in seconds) if waiting

        Returns:
            The typed CollectionFile object with association details. If wait_until_finish
            is True, waits for processing to complete and returns the final video state.

        Raises:
            CloudGlueError: If there is an error adding the video or processing the request.
        """
        try:
            # Validate that either file_id or url is provided
            if not file_id and not url:
                raise CloudGlueError("Either file_id or url must be provided")
            
            if segmentation_id and segmentation_config:
                raise ValueError("Cannot provide both segmentation_id and segmentation_config")

            # Handle segmentation_config parameter
            if isinstance(segmentation_config, dict):
                segmentation_config = SegmentationConfig.from_dict(segmentation_config)

            # Create request object using the SDK model
            # The post-processing script fixes the generated model to properly handle
            # the oneOf constraint (either file_id or url, not both required)
            request = AddCollectionFile(
                file_id=file_id,
                url=url,
                segmentation_id=segmentation_id,
                segmentation_config=segmentation_config,
            )

            # Use the standard method to get a properly typed object
            response = self.api.add_video(
                collection_id=collection_id, add_collection_file=request
            )

            # If not waiting for completion, return immediately
            if not wait_until_finish:
                return response

            # Otherwise poll until completion or timeout
            response_file_id = response.file_id
            elapsed = 0
            terminal_states = ["ready", "completed", "failed", "not_applicable"]

            while elapsed < timeout:
                status = self.get_video(collection_id=collection_id, file_id=response_file_id)

                if status.status in terminal_states:
                    return status

                time.sleep(poll_interval)
                elapsed += poll_interval

            raise TimeoutError(
                f"Video processing did not complete within {timeout} seconds"
            )

        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def get_video(self, collection_id: str, file_id: str):
        """Get information about a specific video in a collection.

        Args:
            collection_id: The ID of the collection
            file_id: The ID of the file to retrieve

        Returns:
            The typed CollectionFile object with video details

        Raises:
            CloudGlueError: If there is an error retrieving the video or processing the request.
        """
        try:
            # Use the standard method to get a properly typed object
            response = self.api.get_video(collection_id=collection_id, file_id=file_id)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def list_videos(
        self,
        collection_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        status: Optional[str] = None,
        added_before: Optional[str] = None,
        added_after: Optional[str] = None,
        order: Optional[str] = None,
        sort: Optional[str] = None,
        filter: Optional[Union[SearchFilter, Dict[str, Any]]] = None,
    ):
        """List videos in a collection.

        Args:
            collection_id: The ID of the collection
            limit: Maximum number of videos to return (max 100)
            offset: Number of videos to skip
            status: Filter by processing status ('pending', 'processing', 'ready', 'failed')
            added_before: Filter by videos added before a specific date, YYYY-MM-DD format in UTC
            added_after: Filter by videos added after a specific date, YYYY-MM-DD format in UTC
            order: Field to sort by ('created_at'). Defaults to 'created_at'
            sort: Sort direction ('asc', 'desc'). Defaults to 'desc'
            filter: Optional filter object or dictionary for advanced filtering by metadata, video info, or file properties.
                   Use Files.create_filter() to create filter objects.
        Returns:
            The typed CollectionFileList object with videos and metadata

        Raises:
            CloudGlueError: If there is an error listing the videos or processing the request.
        """
        try:
            # Convert filter dict to SearchFilter object if needed
            filter_obj = None
            if filter is not None:
                if isinstance(filter, dict):
                    # Convert dict to SearchFilter object
                    filter_obj = SearchFilter(**filter)
                else:
                    filter_obj = filter

            # Use the standard method to get a properly typed object
            response = self.api.list_videos(
                collection_id=collection_id,
                limit=limit,
                offset=offset,
                status=status,
                added_before=added_before,
                added_after=added_after,
                order=order,
                sort=sort,
                filter=json.dumps(filter_obj.to_dict()) if filter_obj else None,
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def remove_video(self, collection_id: str, file_id: str):
        """Remove a video from a collection.

        Args:
            collection_id: The ID of the collection
            file_id: The ID of the file to remove

        Returns:
            The typed DeleteResponse object with removal confirmation

        Raises:
            CloudGlueError: If there is an error removing the video or processing the request.
        """
        try:
            # Use the standard method to get a properly typed object
            response = self.api.delete_video(
                collection_id=collection_id, file_id=file_id
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def get_rich_transcripts(
        self,
        collection_id: str,
        file_id: str,
        start_time_seconds: Optional[float] = None,
        end_time_seconds: Optional[float] = None,
        response_format: Optional[str] = None,
    ):
        """Get the rich transcript of a video in a collection.

        Args:
            collection_id: The ID of the collection
            file_id: The ID of the file to retrieve the rich transcript for
            start_time_seconds: The start time in seconds to filter the rich transcript
            end_time_seconds: The end time in seconds to filter the rich transcript
            response_format: The format of the response, one of 'json' or 'markdown' (json by default)

        Returns:
            The typed RichTranscript object with video rich transcript data

        Raises:
            CloudGlueError: If there is an error retrieving the rich transcript or processing the request.
        """
        try:
            # Use the standard method to get a properly typed object
            response = self.api.get_transcripts(
                collection_id=collection_id, file_id=file_id, start_time_seconds=start_time_seconds, end_time_seconds=end_time_seconds, response_format=response_format
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def get_video_entities(
        self, 
        collection_id: str, 
        file_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """Get the entities extracted from a video in a collection.

        Args:
            collection_id: The ID of the collection
            file_id: The ID of the file to retrieve entities for
            limit: Maximum number of segment entities to return (1-100)
            offset: Number of segment entities to skip

        Returns:
            The typed FileEntities object with video entities data

        Raises:
            CloudGlueError: If there is an error retrieving the entities or processing the request.
        """
        try:
            # Use the standard method to get a properly typed object
            response = self.api.get_entities(
                collection_id=collection_id,
                file_id=file_id,
                limit=limit,
                offset=offset,
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def list_entities(
        self,
        collection_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order: Optional[str] = None,
        sort: Optional[str] = None,
        added_before: Optional[str] = None,
        added_after: Optional[str] = None,
    ):
        """List all extracted entities for files in a collection.

        This API is only available when a collection is created with collection_type 'entities'.

        Args:
            collection_id: The ID of the collection
            limit: Maximum number of files to return
            offset: Number of files to skip
            order: Order the files by a specific field
            sort: Sort the files in ascending or descending order
            added_before: Filter files added before a specific date (YYYY-MM-DD format), in UTC timezone
            added_after: Filter files added after a specific date (YYYY-MM-DD format), in UTC timezone

        Returns:
            Collection entities list response

        Raises:
            CloudGlueError: If the request fails
        """
        try:
            response = self.api.list_collection_entities(
                collection_id=collection_id,
                limit=limit,
                offset=offset,
                order=order,
                sort=sort,
                added_before=added_before,
                added_after=added_after,
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(
                f"Failed to list entities in collection {collection_id}: {str(e)}"
            )

    def list_rich_transcripts(
        self,
        collection_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order: Optional[str] = None,
        sort: Optional[str] = None,
        added_before: Optional[str] = None,
        added_after: Optional[str] = None,
        response_format: Optional[str] = None,
    ):
        """List all rich transcription data for files in a collection.

        This API is only available when a collection is created with collection_type 'rich-transcripts'.

        Args:
            collection_id: The ID of the collection
            limit: Maximum number of files to return
            offset: Number of files to skip
            order: Order the files by a specific field
            sort: Sort the files in ascending or descending order
            added_before: Filter files added before a specific date (YYYY-MM-DD format), in UTC timezone
            added_after: Filter files added after a specific date (YYYY-MM-DD format), in UTC timezone
            response_format: Format for the response

        Returns:
            Collection rich transcripts list response

        Raises:
            CloudGlueError: If the request fails
        """
        try:
            response = self.api.list_collection_rich_transcripts(
                collection_id=collection_id,
                limit=limit,
                offset=offset,
                order=order,
                sort=sort,
                added_before=added_before,
                added_after=added_after,
                response_format=response_format,
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(
                f"Failed to list rich transcripts in collection {collection_id}: {str(e)}"
            )

    def get_media_descriptions(
        self,
        collection_id: str,
        file_id: str,
        start_time_seconds: Optional[float] = None,
        end_time_seconds: Optional[float] = None,
        response_format: Optional[str] = None,
    ):
        """Get the media descriptions of a video in a collection.

        Args:
            collection_id: The ID of the collection
            file_id: The ID of the file to retrieve the media descriptions for
            start_time_seconds: The start time in seconds to filter the media descriptions
            end_time_seconds: The end time in seconds to filter the media descriptions
            response_format: The format of the response, one of 'json' or 'markdown' (json by default)

        Returns:
            The typed MediaDescription object with video media description data

        Raises:
            CloudGlueError: If there is an error retrieving the media descriptions or processing the request.
        """
        try:
            # Use the standard method to get a properly typed object
            response = self.api.get_media_descriptions(
                collection_id=collection_id, file_id=file_id, start_time_seconds=start_time_seconds, end_time_seconds=end_time_seconds, response_format=response_format
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def list_media_descriptions(
        self,
        collection_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order: Optional[str] = None,
        sort: Optional[str] = None,
        added_before: Optional[str] = None,
        added_after: Optional[str] = None,
        response_format: Optional[str] = None,
    ):
        """List all media description data for files in a collection.

        This API is only available when a collection is created with collection_type 'media-descriptions'.

        Args:
            collection_id: The ID of the collection
            limit: Maximum number of files to return
            offset: Number of files to skip
            order: Order the files by a specific field
            sort: Sort the files in ascending or descending order
            added_before: Filter files added before a specific date (YYYY-MM-DD format), in UTC timezone
            added_after: Filter files added after a specific date (YYYY-MM-DD format), in UTC timezone
            response_format: Format for the response

        Returns:
            Collection media descriptions list response

        Raises:
            CloudGlueError: If the request fails
        """
        try:
            response = self.api.list_collection_media_descriptions(
                collection_id=collection_id,
                limit=limit,
                offset=offset,
                order=order,
                sort=sort,
                added_before=added_before,
                added_after=added_after,
                response_format=response_format,
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(
                f"Failed to list media descriptions in collection {collection_id}: {str(e)}"
            )

    def get_face_detections(
        self,
        collection_id: str,
        file_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """Retrieve face detections for a specific file in a collection.

        This API is only available when a collection is created with collection_type 'face-analysis'.

        Args:
            collection_id: The ID of the collection
            file_id: The ID of the file
            limit: Maximum number of faces to return (1-100, default 50)
            offset: Number of faces to skip (default 0)

        Returns:
            FileFaceDetections object containing detected faces

        Raises:
            CloudGlueError: If the request fails
        """
        try:
            response = self.api.get_face_detections(
                collection_id=collection_id,
                file_id=file_id,
                limit=limit,
                offset=offset,
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(
                f"Failed to get face detections for file {file_id} in collection {collection_id}: {str(e)}"
            )


class Extract:
    """Client for the CloudGlue Extract API."""

    def __init__(self, api):
        """Initialize the Extract client.

        Args:
            api: The DefaultApi instance.
        """
        self.api = api

    def create(
        self,
        url: str,
        prompt: Optional[str] = None,
        schema: Optional[Dict[str, Any]] = None,
        enable_video_level_entities: Optional[bool] = None,
        enable_segment_level_entities: Optional[bool] = None,
        segmentation_id: Optional[str] = None,
        segmentation_config: Optional[Union[SegmentationConfig, Dict[str, Any]]] = None,
        thumbnails_config: Optional[Union[Dict[str, Any], Any]] = None,
    ):
        """Create a new extraction job.

        Args:
            url: The URL of the video to extract data from. Can be a YouTube URL or a cloudglue file URI.
            prompt: A natural language description of what to extract. Required if schema is not provided.
            schema: A JSON schema defining the structure of the data to extract. Required if prompt is not provided.
            enable_video_level_entities: Whether to extract entities at the video level
            enable_segment_level_entities: Whether to extract entities at the segment level
            segmentation_id: Segmentation job id to use. Cannot be provided together with segmentation_config.
            segmentation_config: Configuration for video segmentation. Cannot be provided together with segmentation_id.
            thumbnails_config: Optional configuration for segment thumbnails

        Returns:
            Extract: A typed Extract object containing job_id, status, and other fields.

        Raises:
            CloudGlueError: If there is an error creating the extraction job or processing the request.
        """
        try:
            if not prompt and not schema:
                raise ValueError("Either prompt or schema must be provided")

            if segmentation_id and segmentation_config:
                raise ValueError("Cannot provide both segmentation_id and segmentation_config")

            # Handle segmentation_config parameter
            if isinstance(segmentation_config, dict):
                segmentation_config = SegmentationConfig.from_dict(segmentation_config)

            # Handle thumbnails_config parameter
            thumbnails_config_obj = None
            if thumbnails_config is not None:
                if isinstance(thumbnails_config, dict):
                    thumbnails_config_obj = ThumbnailsConfig.from_dict(thumbnails_config)
                else:
                    thumbnails_config_obj = thumbnails_config

            # Set up the request object
            request = NewExtract(
                url=url,
                prompt=prompt,
                var_schema=schema,
                enable_video_level_entities=enable_video_level_entities,
                enable_segment_level_entities=enable_segment_level_entities,
                segmentation_id=segmentation_id,
                segmentation_config=segmentation_config,
                thumbnails_config=thumbnails_config_obj,
            )

            # Use the standard method to get a properly typed Extract object
            response = self.api.create_extract(new_extract=request)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def get(
        self, 
        job_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        ):
        """Get the status of an extraction job.

        Args:
            job_id: The ID of the extraction job.
            limit: Maximum number of segment entities to return (1-100)
            offset: Number of segment entities to skip
        Returns:
            Extract: A typed Extract object containing the job status and extracted data if available.

        Raises:
            CloudGlueError: If there is an error retrieving the extraction job or processing the request.
        """
        try:
            response = self.api.get_extract(job_id=job_id, limit=limit, offset=offset)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))
        
    def list(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        status: Optional[str] = None,
        created_before: Optional[str] = None,
        created_after: Optional[str] = None,
        url: Optional[str] = None,
    ):
        """List extraction jobs.

        Args:
            limit: Maximum number of jobs to return.
            offset: Number of jobs to skip.
            status: Filter by job status.
            created_before: Filter by jobs created before a specific date, YYYY-MM-DD format in UTC.
            created_after: Filter by jobs created after a specific date, YYYY-MM-DD format in UTC.
            url: Filter by jobs with a specific URL.
        Returns:
            A list of extraction jobs.

        Raises:
            CloudGlueError: If there is an error listing the extraction jobs or processing the request.
        """
        try:
            return self.api.list_extracts(
                limit=limit,
                offset=offset,
                status=status,
                created_before=created_before,
                created_after=created_after,
                url=url,
            )
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def run(
        self,
        url: str,
        prompt: Optional[str] = None,
        schema: Optional[Dict[str, Any]] = None,
        enable_video_level_entities: Optional[bool] = None,
        enable_segment_level_entities: Optional[bool] = None,
        segmentation_id: Optional[str] = None,
        segmentation_config: Optional[Union[SegmentationConfig, Dict[str, Any]]] = None,
        thumbnails_config: Optional[Union[Dict[str, Any], Any]] = None,
        poll_interval: int = 5,
        timeout: int = 600,
    ):
        """Create an extraction job and wait for it to complete.

        Args:
            url: The URL of the video to extract data from. Can be a YouTube URL or a cloudglue file URI.
            prompt: A natural language description of what to extract. Required if schema is not provided.
            schema: A JSON schema defining the structure of the data to extract. Required if prompt is not provided.
            enable_video_level_entities: Whether to extract entities at the video level
            enable_segment_level_entities: Whether to extract entities at the segment level
            segmentation_id: Segmentation job id to use. Cannot be provided together with segmentation_config.
            segmentation_config: Configuration for video segmentation. Cannot be provided together with segmentation_id.
            thumbnails_config: Optional configuration for segment thumbnails
            poll_interval: How often to check the job status (in seconds).
            timeout: Maximum time to wait for the job to complete (in seconds).

        Returns:
            Extract: The completed Extract object with status and data.

        Raises:
            CloudGlueError: If there is an error creating or processing the extraction job.
        """
        try:
            # Create the extraction job
            job = self.create(
                url=url,
                prompt=prompt,
                schema=schema,
                enable_video_level_entities=enable_video_level_entities,
                enable_segment_level_entities=enable_segment_level_entities,
                segmentation_id=segmentation_id,
                segmentation_config=segmentation_config,
                thumbnails_config=thumbnails_config,
            )
            job_id = job.job_id

            # Poll for completion
            elapsed = 0
            while elapsed < timeout:
                status = self.get(job_id=job_id)

                if status.status in ["completed", "failed"]:
                    return status

                time.sleep(poll_interval)
                elapsed += poll_interval

            raise TimeoutError(
                f"Extraction job did not complete within {timeout} seconds"
            )
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))


class Transcribe:
    """Handles rich video transcription operations."""

    def __init__(self, api):
        """Initialize with the API client."""
        self.api = api

    def create(
        self,
        url: str,
        enable_summary: bool = True,
        enable_speech: bool = True,
        enable_scene_text: bool = False,
        enable_visual_scene_description: bool = False,
        enable_audio_description: bool = False,
        segmentation_id: Optional[str] = None,
        segmentation_config: Optional[Union[SegmentationConfig, Dict[str, Any]]] = None,
        thumbnails_config: Optional[Union[Dict[str, Any], Any]] = None,
    ):
        """Create a new transcribe job for a video.

        Args:
            url: Input video URL. Can be YouTube URLs or URIs of uploaded files.
            enable_summary: Whether to generate a summary of the video.
            enable_speech: Whether to generate speech transcript.
            enable_scene_text: Whether to generate scene text.
            enable_visual_scene_description: Whether to generate visual scene description.
            enable_audio_description: Whether to generate audio description.
            segmentation_id: Segmentation job id to use. Cannot be provided together with segmentation_config.
            segmentation_config: Configuration for video segmentation. Cannot be provided together with segmentation_id.
            thumbnails_config: Optional configuration for segment thumbnails

        Returns:
            The typed Transcribe job object with job_id and status.

        Raises:
            CloudGlueError: If there is an error creating the transcribe job or processing the request.
        """
        try:
            if segmentation_id and segmentation_config:
                raise ValueError("Cannot provide both segmentation_id and segmentation_config")

            # Handle segmentation_config parameter
            if isinstance(segmentation_config, dict):
                segmentation_config = SegmentationConfig.from_dict(segmentation_config)

            # Handle thumbnails_config parameter
            thumbnails_config_obj = None
            if thumbnails_config is not None:
                if isinstance(thumbnails_config, dict):
                    thumbnails_config_obj = ThumbnailsConfig.from_dict(thumbnails_config)
                else:
                    thumbnails_config_obj = thumbnails_config

            request = NewTranscribe(
                url=url,
                enable_summary=enable_summary,
                enable_speech=enable_speech,
                enable_scene_text=enable_scene_text,
                enable_visual_scene_description=enable_visual_scene_description,
                enable_audio_description=enable_audio_description,
                segmentation_id=segmentation_id,
                segmentation_config=segmentation_config,
                thumbnails_config=thumbnails_config_obj,
            )

            # Use the regular SDK method to create the job
            response = self.api.create_transcribe(new_transcribe=request)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    # TODO (kdr): asyncio version of this
    def get(self, job_id: str, response_format: Optional[str] = None):
        """Get the current state of a transcribe job.

        Args:
            job_id: The unique identifier of the transcribe job.
            response_format: The format of the response, one of 'json' or 'markdown' (json by default)

        Returns:
            The typed Transcribe job object with status and data.

        Raises:
            CloudGlueError: If there is an error retrieving the transcribe job or processing the request.
        """
        try:
            # Use the standard method to get a properly typed object
            response = self.api.get_transcribe(job_id=job_id, response_format=response_format)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))
        
    def list(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        status: Optional[str] = None,
        created_before: Optional[str] = None,
        created_after: Optional[str] = None,
        response_format: Optional[str] = None,
        url: Optional[str] = None,
    ):
        """List transcribe jobs.

        Args:
            limit: Maximum number of jobs to return.
            offset: Number of jobs to skip.
            status: Filter by job status.
            created_before: Filter by jobs created before a specific date, YYYY-MM-DD format in UTC.
            created_after: Filter by jobs created after a specific date, YYYY-MM-DD format in UTC.
            response_format: The format of the response, one of 'json' or 'markdown' (json by default)
            url: Filter by jobs with a specific URL.

        Returns:
            A list of transcribe jobs.

        Raises:
            CloudGlueError: If there is an error listing the transcribe jobs or processing the request.
        """
        try:
            return self.api.list_transcribes(
                limit=limit,
                offset=offset,
                status=status,
                created_before=created_before,
                created_after=created_after,
                response_format=response_format,
                url=url,
            )
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def run(
        self,
        url: str,
        poll_interval: int = 5,
        timeout: int = 600,
        enable_summary: bool = True,
        enable_speech: bool = True,
        enable_scene_text: bool = False,
        enable_visual_scene_description: bool = False,
        enable_audio_description: bool = False,
        segmentation_id: Optional[str] = None,
        segmentation_config: Optional[Union[SegmentationConfig, Dict[str, Any]]] = None,
        thumbnails_config: Optional[Union[Dict[str, Any], Any]] = None,
        response_format: Optional[str] = None,
    ):
        """Create a transcribe job and wait for it to complete.

        Args:
            url: Input video URL. Can be YouTube URLs or URIs of uploaded files.
            poll_interval: Seconds between status checks.
            timeout: Total seconds to wait before giving up.
            enable_summary: Whether to generate a summary of the video.
            enable_speech: Whether to generate speech transcript.
            enable_scene_text: Whether to generate scene text.
            enable_visual_scene_description: Whether to generate visual scene description.
            enable_audio_description: Whether to generate audio description.
            segmentation_id: Segmentation job id to use. Cannot be provided together with segmentation_config.
            segmentation_config: Configuration for video segmentation. Cannot be provided together with segmentation_id.
            thumbnails_config: Optional configuration for segment thumbnails
            response_format: The format of the response, one of 'json' or 'markdown' (json by default)
        Returns:
            The completed typed Transcribe job object.

        Raises:
            CloudGlueError: If there is an error creating or processing the transcribe job.
        """
        try:
            # Create the job
            job = self.create(
                url=url,
                enable_summary=enable_summary,
                enable_speech=enable_speech,
                enable_scene_text=enable_scene_text,
                enable_visual_scene_description=enable_visual_scene_description,
                enable_audio_description=enable_audio_description,
                segmentation_id=segmentation_id,
                segmentation_config=segmentation_config,
                thumbnails_config=thumbnails_config,
            )

            job_id = job.job_id

            # Poll for completion
            elapsed = 0
            while elapsed < timeout:
                status = self.get(job_id=job_id, response_format=response_format)

                if status.status in ["completed", "failed"]:
                    return status

                time.sleep(poll_interval)
                elapsed += poll_interval

            raise TimeoutError(
                f"Transcribe job did not complete within {timeout} seconds"
            )

        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))


class Describe:
    """Handles media description operations."""

    def __init__(self, api):
        """Initialize with the API client."""
        self.api = api

    def create(
        self,
        url: str,
        enable_summary: bool = True,
        enable_speech: bool = True,
        enable_scene_text: bool = True,
        enable_visual_scene_description: bool = True,
        enable_audio_description: bool = True,
        segmentation_id: Optional[str] = None,
        segmentation_config: Optional[Union[SegmentationConfig, Dict[str, Any]]] = None,
        thumbnails_config: Optional[Union[Dict[str, Any], Any]] = None,
    ):
        """Create a new media description job for a video.

        Args:
            url: Input video URL. Can be YouTube URLs or URIs of uploaded files.
            enable_summary: Whether to generate video-level and segment-level summaries and titles.
            enable_speech: Whether to generate speech transcript.
            enable_scene_text: Whether to generate scene text extraction.
            enable_visual_scene_description: Whether to generate visual scene description.
            enable_audio_description: Whether to generate audio description.
            segmentation_id: Segmentation job id to use. Cannot be provided together with segmentation_config.
            segmentation_config: Configuration for video segmentation. Cannot be provided together with segmentation_id.
            thumbnails_config: Optional configuration for segment thumbnails

        Returns:
            The typed Describe job object with job_id and status.

        Raises:
            CloudGlueError: If there is an error creating the describe job or processing the request.
        """
        try:
            if segmentation_id and segmentation_config:
                raise ValueError("Cannot provide both segmentation_id and segmentation_config")

            # Handle segmentation_config parameter
            if isinstance(segmentation_config, dict):
                segmentation_config = SegmentationConfig.from_dict(segmentation_config)

            # Handle thumbnails_config parameter
            thumbnails_config_obj = None
            if thumbnails_config is not None:
                if isinstance(thumbnails_config, dict):
                    thumbnails_config_obj = ThumbnailsConfig.from_dict(thumbnails_config)
                else:
                    thumbnails_config_obj = thumbnails_config

            request = NewDescribe(
                url=url,
                enable_summary=enable_summary,
                enable_speech=enable_speech,
                enable_scene_text=enable_scene_text,
                enable_visual_scene_description=enable_visual_scene_description,
                enable_audio_description=enable_audio_description,
                segmentation_id=segmentation_id,
                segmentation_config=segmentation_config,
                thumbnails_config=thumbnails_config_obj,
            )

            # Use the regular SDK method to create the job
            response = self.api.create_describe(new_describe=request)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def get(
        self,
        job_id: str,
        response_format: Optional[str] = None,
        start_time_seconds: Optional[float] = None,
        end_time_seconds: Optional[float] = None,
    ):
        """Get the status and data of a media description job.

        Args:
            job_id: The unique identifier of the description job.
            response_format: The format of the response, one of 'json' or 'markdown' (json by default)
            start_time_seconds: The start time in seconds to filter the media descriptions
            end_time_seconds: The end time in seconds to filter the media descriptions  
        Returns:
            The typed Describe job object with current status and data (if completed).

        Raises:
            CloudGlueError: If there is an error retrieving the describe job or processing the request.
        """
        try:
            # Use the standard method to get a properly typed object
            response = self.api.get_describe(job_id=job_id, response_format=response_format, start_time_seconds=start_time_seconds, end_time_seconds=end_time_seconds)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def list(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        status: Optional[str] = None,
        created_before: Optional[str] = None,
        created_after: Optional[str] = None,
        response_format: Optional[str] = None,
        url: Optional[str] = None,
    ):
        """List all media description jobs with optional filtering.

        Args:
            limit: Maximum number of description jobs to return.
            offset: Number of description jobs to skip.
            status: Filter description jobs by status.
            created_before: Filter description jobs created before a specific date (YYYY-MM-DD format), in UTC timezone.
            created_after: Filter description jobs created after a specific date (YYYY-MM-DD format), in UTC timezone.
            response_format: The format of the response, one of 'json' or 'markdown' (json by default)
            url: Filter description jobs by the input URL used for description.

        Returns:
            The typed DescribeList object with array of describe jobs.

        Raises:
            CloudGlueError: If there is an error retrieving the describe jobs or processing the request.
        """
        try:
            # Use the standard method to get a properly typed object
            response = self.api.list_describes(
                limit=limit,
                offset=offset,
                status=status,
                created_before=created_before,
                created_after=created_after,
                response_format=response_format,
                url=url,
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def run(
        self,
        url: str,
        poll_interval: int = 5,
        timeout: int = 600,
        enable_summary: bool = True,
        enable_speech: bool = True,
        enable_scene_text: bool = True,
        enable_visual_scene_description: bool = True,
        enable_audio_description: bool = False,
        segmentation_id: Optional[str] = None,
        segmentation_config: Optional[Union[SegmentationConfig, Dict[str, Any]]] = None,
        thumbnails_config: Optional[Union[Dict[str, Any], Any]] = None,
        response_format: Optional[str] = None,
    ):
        """Create a media description job and wait for it to complete.

        Args:
            url: Input video URL. Can be YouTube URLs or URIs of uploaded files.
            poll_interval: Seconds between status checks.
            timeout: Total seconds to wait before giving up.
            enable_summary: Whether to generate video-level and segment-level summaries and titles.
            enable_speech: Whether to generate speech transcript.
            enable_scene_text: Whether to generate scene text extraction.
            enable_visual_scene_description: Whether to generate visual scene description.
            enable_audio_description: Whether to generate audio description.
            segmentation_id: Segmentation job id to use. Cannot be provided together with segmentation_config.
            segmentation_config: Configuration for video segmentation. Cannot be provided together with segmentation_id.
            thumbnails_config: Optional configuration for segment thumbnails
            response_format: The format of the response, one of 'json' or 'markdown' (json by default)
        Returns:
            The completed typed Describe job object.

        Raises:
            CloudGlueError: If there is an error creating or processing the describe job.
        """
        try:
            # Create the job
            job = self.create(
                url=url,
                enable_summary=enable_summary,
                enable_speech=enable_speech,
                enable_scene_text=enable_scene_text,
                enable_visual_scene_description=enable_visual_scene_description,
                enable_audio_description=enable_audio_description,
                segmentation_id=segmentation_id,
                segmentation_config=segmentation_config,
                thumbnails_config=thumbnails_config,
            )

            job_id = job.job_id

            # Poll for completion
            elapsed = 0
            while elapsed < timeout:
                status = self.get(job_id=job_id, response_format=response_format)

                if status.status in ["completed", "failed"]:
                    return status

                time.sleep(poll_interval)
                elapsed += poll_interval

            raise TimeoutError(
                f"Describe job did not complete within {timeout} seconds"
            )

        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))


class Files:
    """Handles file operations."""

    def __init__(self, api):
        """Initialize with the API client."""
        self.api = api

    @staticmethod
    def _create_metadata_filter(
        path: str,
        operator: str,
        value_text: Optional[str] = None,
        value_text_array: Optional[List[str]] = None,
    ) -> SearchFilterCriteria:
        """Create a metadata filter for file listing.
        
        Args:
            path: JSON path on metadata object (e.g. 'my_custom_field', 'category.subcategory')
            operator: Comparison operator ('NotEqual', 'Equal', 'LessThan', 'GreaterThan', 'In', 'ContainsAny', 'ContainsAll', 'Like')
            value_text: Text value for scalar comparison (used with NotEqual, Equal, LessThan, GreaterThan, Like)
            value_text_array: Array of values for array comparisons (used with ContainsAny, ContainsAll, In)
            
        Returns:
            SearchFilterCriteria object
        """
        return SearchFilterCriteria(
            path=path,
            operator=operator,
            value_text=value_text,
            value_text_array=value_text_array,
        )

    @staticmethod
    def _create_video_info_filter(
        path: str,
        operator: str,
        value_text: Optional[str] = None,
        value_text_array: Optional[List[str]] = None,
    ) -> SearchFilterVideoInfoInner:
        """Create a video info filter for file listing.
        
        Args:
            path: JSON path on video_info object ('duration_seconds', 'has_audio')
            operator: Comparison operator ('NotEqual', 'Equal', 'LessThan', 'GreaterThan', 'In', 'ContainsAny', 'ContainsAll', 'Like')
            value_text: Text value for scalar comparison (used with NotEqual, Equal, LessThan, GreaterThan, Like)
            value_text_array: Array of values for array comparisons (used with ContainsAny, ContainsAll, In)
            
        Returns:
            SearchFilterVideoInfoInner object
        """
        return SearchFilterVideoInfoInner(
            path=path,
            operator=operator,
            value_text=value_text,
            value_text_array=value_text_array,
        )

    @staticmethod
    def _create_file_filter(
        path: str,
        operator: str,
        value_text: Optional[str] = None,
        value_text_array: Optional[List[str]] = None,
    ) -> SearchFilterFileInner:
        """Create a file property filter for file listing.
        
        Args:
            path: JSON path on file object ('bytes', 'filename', 'uri', 'created_at', 'id')
            operator: Comparison operator ('NotEqual', 'Equal', 'LessThan', 'GreaterThan', 'In', 'ContainsAny', 'ContainsAll', 'Like')
            value_text: Text value for scalar comparison (used with NotEqual, Equal, LessThan, GreaterThan, Like)
            value_text_array: Array of values for array comparisons (used with ContainsAny, ContainsAll, In)
            
        Returns:
            SearchFilterFileInner object
        """
        return SearchFilterFileInner(
            path=path,
            operator=operator,
            value_text=value_text,
            value_text_array=value_text_array,
        )

    @staticmethod
    def create_filter(
        metadata_filters: Optional[List[Dict[str, Any]]] = None,
        video_info_filters: Optional[List[Dict[str, Any]]] = None,
        file_filters: Optional[List[Dict[str, Any]]] = None,
    ) -> SearchFilter:
        """Create a filter object for file listing.

        Args:
            metadata_filters: List of metadata filter dictionaries. Each dict should contain:
                - path: JSON path on metadata object (e.g. 'my_custom_field', 'category.subcategory')
                - operator: Comparison operator ('NotEqual', 'Equal', 'LessThan', 'GreaterThan', 'In', 'ContainsAny', 'ContainsAll', 'Like')
                - value_text: Text value for scalar comparison (used with NotEqual, Equal, LessThan, GreaterThan, Like)
                - value_text_array: Array of values for array comparisons (used with ContainsAny, ContainsAll, In)
            video_info_filters: List of video info filter dictionaries. Each dict should contain:
                - path: JSON path on video_info object ('duration_seconds', 'has_audio')
                - operator: Comparison operator ('NotEqual', 'Equal', 'LessThan', 'GreaterThan', 'In', 'ContainsAny', 'ContainsAll', 'Like')
                - value_text: Text value for scalar comparison (used with NotEqual, Equal, LessThan, GreaterThan, Like)
                - value_text_array: Array of values for array comparisons (used with ContainsAny, ContainsAll, In)
            file_filters: List of file property filter dictionaries. Each dict should contain:
                - path: JSON path on file object ('bytes', 'filename', 'uri', 'created_at', 'id')
                - operator: Comparison operator ('NotEqual', 'Equal', 'LessThan', 'GreaterThan', 'In', 'ContainsAny', 'ContainsAll', 'Like')
                - value_text: Text value for scalar comparison (used with NotEqual, Equal, LessThan, GreaterThan, Like)
                - value_text_array: Array of values for array comparisons (used with ContainsAny, ContainsAll, In)

        Returns:
            SearchFilter object

        Examples:
            # Filter by metadata
            filter_obj = Files.create_filter(
                metadata_filters=[
                    {"path": "speaker", "operator": "Equal", "value_text": "John"}
                ]
            )

            # Filter by video info
            filter_obj = Files.create_filter(
                video_info_filters=[
                    {"path": "duration_seconds", "operator": "GreaterThan", "value_text": "60"}
                ]
            )

            # Filter by file properties
            filter_obj = Files.create_filter(
                file_filters=[
                    {"path": "filename", "operator": "Like", "value_text": "%.mp4"}
                ]
            )

            # Combined filtering
            filter_obj = Files.create_filter(
                metadata_filters=[
                    {"path": "speaker", "operator": "Equal", "value_text": "John"}
                ],
                video_info_filters=[
                    {"path": "has_audio", "operator": "Equal", "value_text": "true"}
                ],
                file_filters=[
                    {"path": "filename", "operator": "Like", "value_text": "%.mp4"}
                ]
            )
        """
        metadata = None
        if metadata_filters:
            metadata = [
                Files._create_metadata_filter(**filter_dict) for filter_dict in metadata_filters
            ]

        video_info = None
        if video_info_filters:
            video_info = [
                Files._create_video_info_filter(**filter_dict) for filter_dict in video_info_filters
            ]

        file = None
        if file_filters:
            file = [
                Files._create_file_filter(**filter_dict) for filter_dict in file_filters
            ]

        return SearchFilter(
            metadata=metadata,
            video_info=video_info,
            file=file,
        )

    def upload(
        self,
        file_path: str,
        metadata: Optional[Dict[str, Any]] = None,
        enable_segment_thumbnails: Optional[bool] = None,
        wait_until_finish: bool = False,
        poll_interval: int = 5,
        timeout: int = 600,
    ):
        """Upload a file to CloudGlue.

        Args:
            file_path: Path to the local file to upload.
            metadata: Optional user-provided metadata about the file.
            enable_segment_thumbnails: Whether to generate thumbnails for each segment.
            wait_until_finish: Whether to wait for the file processing to complete.
            poll_interval: How often to check the file status (in seconds) if waiting.
            timeout: Maximum time to wait for processing (in seconds) if waiting.

        Returns:
            The uploaded file object. If wait_until_finish is True, waits for processing
            to complete and returns the final file state.

        Raises:
            CloudGlueError: If there is an error uploading or processing the file.
        """
        try:
            file_path = pathlib.Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")

            # Read the file as bytes and create a tuple of (filename, bytes)
            with open(file_path, "rb") as f:
                file_bytes = f.read()

            filename = os.path.basename(file_path)
            file_tuple = (filename, file_bytes)

            response = self.api.upload_file(
                file=file_tuple, 
                metadata=metadata,
                enable_segment_thumbnails=enable_segment_thumbnails
            )

            # If not waiting for completion, return immediately
            if not wait_until_finish:
                return response

            # Otherwise poll until completion or timeout
            file_id = response.id
            elapsed = 0
            terminal_states = ["ready", "completed", "failed", "not_applicable"]

            while elapsed < timeout:
                status = self.get(file_id=file_id)

                if status.status in terminal_states:
                    return status

                time.sleep(poll_interval)
                elapsed += poll_interval

            raise TimeoutError(
                f"File processing did not complete within {timeout} seconds"
            )

        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def list(
        self,
        status: Optional[str] = None,
        created_before: Optional[str] = None,
        created_after: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order: Optional[str] = None,
        sort: Optional[str] = None,
        filter: Optional[Union[SearchFilter, Dict[str, Any]]] = None,
    ):
        """List available files.

        Args:
            status: Optional filter by file status ('processing', 'ready', 'failed').
            created_before: Optional filter by files created before a specific date, YYYY-MM-DD format in UTC
            created_after: Optional filter by files created after a specific date, YYYY-MM-DD format in UTC
            limit: Optional maximum number of files to return (default 50, max 100).
            offset: Optional number of files to skip.
            order: Optional field to sort by ('created_at', 'filename'). Defaults to 'created_at'.
            sort: Optional sort direction ('asc', 'desc'). Defaults to 'desc'.
            filter: Optional filter object or dictionary for advanced filtering by metadata, video info, or file properties.
                   Use Files.create_filter() to create filter objects.

        Returns:
            A list of file objects.

        Raises:
            CloudGlueError: If there is an error listing files or processing the request.
        """
        try:
            # Convert filter dict to SearchFilter object if needed
            filter_obj = None
            if filter is not None:
                if isinstance(filter, dict):
                    # Convert dict to SearchFilter object
                    filter_obj = SearchFilter(**filter)
                else:
                    filter_obj = filter

            return self.api.list_files(
                status=status,
                created_before=created_before,
                created_after=created_after,
                limit=limit,
                offset=offset,
                order=order,
                sort=sort,
                filter=json.dumps(filter_obj.to_dict()) if filter_obj else None,
            )
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def get(self, file_id: str):
        """Get details about a specific file.

        Args:
            file_id: The ID of the file to retrieve.

        Returns:
            The file object.

        Raises:
            CloudGlueError: If there is an error retrieving the file or processing the request.
        """
        try:
            return self.api.get_file(file_id=file_id)
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def delete(self, file_id: str):
        """Delete a file.

        Args:
            file_id: The ID of the file to delete.

        Returns:
            The deletion confirmation.

        Raises:
            CloudGlueError: If there is an error deleting the file or processing the request.
        """
        try:
            return self.api.delete_file(file_id=file_id)
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def update(
        self,
        file_id: str,
        filename: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """Update a file's filename and/or metadata.

        Args:
            file_id: The ID of the file to update.
            filename: Optional new filename for the file.
            metadata: Optional user-provided metadata about the file.

        Returns:
            The updated file object.

        Raises:
            CloudGlueError: If there is an error updating the file or processing the request.
        """
        try:
            # Create the update request object
            file_update = FileUpdate(
                filename=filename,
                metadata=metadata,
            )
            
            return self.api.update_file(file_id=file_id, file_update=file_update)
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def create_segmentation(
        self,
        file_id: str,
        segmentation_config: Union[SegmentationConfig, Dict[str, Any]],
        thumbnails_config: Optional[Union[Dict[str, Any], Any]] = None,
        wait_until_finish: bool = False,
        poll_interval: int = 5,
        timeout: int = 600,
    ):
        """Create a new segmentation for a file.

        Args:
            file_id: The ID of the file to segment
            segmentation_config: Segmentation configuration (SegmentationConfig object or dictionary)
            thumbnails_config: Optional configuration for segment thumbnails
            wait_until_finish: Whether to wait for the segmentation to complete
            poll_interval: How often to check the segmentation status (in seconds) if waiting
            timeout: Maximum time to wait for processing (in seconds) if waiting

        Returns:
            The created Segmentation object. If wait_until_finish is True, waits for processing
            to complete and returns the final segmentation state.

        Raises:
            CloudGlueError: If there is an error creating the segmentation or processing the request.

        Example:
            # Create uniform segmentation
            config = client.segmentations.create_uniform_config(window_seconds=20)
            segmentation = client.files.create_segmentation(
                file_id="file_123",
                segmentation_config=config,
                wait_until_finish=True
            )
        """
        try:            
            # Handle segmentation_config parameter
            if isinstance(segmentation_config, dict):
                segmentation_config = SegmentationConfig.from_dict(segmentation_config)
            elif not isinstance(segmentation_config, SegmentationConfig):
                raise ValueError("segmentation_config must be a SegmentationConfig object or dictionary")

            # Handle thumbnails_config parameter
            thumbnails_config_obj = None
            if thumbnails_config is not None:
                if isinstance(thumbnails_config, dict):
                    thumbnails_config_obj = ThumbnailsConfig.from_dict(thumbnails_config)
                else:
                    thumbnails_config_obj = thumbnails_config

            # Create the request object
            request = CreateFileSegmentationRequest(
                strategy=segmentation_config.strategy,
                uniform_config=segmentation_config.uniform_config,
                shot_detector_config=segmentation_config.shot_detector_config,
                manual_config=segmentation_config.manual_config,
                start_time_seconds=segmentation_config.start_time_seconds,
                end_time_seconds=segmentation_config.end_time_seconds,
                thumbnails_config=thumbnails_config_obj,
            )

            response = self.api.create_file_segmentation(
                file_id=file_id,
                create_file_segmentation_request=request,
            )

            # If not waiting for completion, return immediately
            if not wait_until_finish:
                return response

            # Otherwise poll until completion or timeout
            segmentation_id = response.segmentation_id
            elapsed = 0
            terminal_states = ["completed", "failed", "not_applicable"]

            # Import SegmentationsApi here to avoid circular imports            
            segmentations_api = SegmentationsApi(self.api.api_client)

            while elapsed < timeout:
                status = segmentations_api.get_segmentation(segmentation_id=segmentation_id)

                if status.status in terminal_states:
                    return status

                time.sleep(poll_interval)
                elapsed += poll_interval

            raise TimeoutError(
                f"Segmentation processing did not complete within {timeout} seconds"
            )

        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def list_segmentations(
        self,
        file_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """List segmentations for a specific file.

        Args:
            file_id: The ID of the file to list segmentations for
            limit: Maximum number of segmentations to return (max 100)
            offset: Number of segmentations to skip

        Returns:
            A SegmentationList object containing segmentation objects for the file

        Raises:
            CloudGlueError: If there is an error listing the segmentations or processing the request.
        """
        try:
            response = self.api.list_file_segmentations(
                file_id=file_id,
                limit=limit,
                offset=offset,
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def get_thumbnails(
        self,
        file_id: str,
        is_default: Optional[bool] = None,
        segmentation_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """
        Get thumbnails for a file.
        
        Args:
            file_id: The ID of the file
            is_default: Filter thumbnails by default status. If true, will only return the default thumbnail for the file
            segmentation_id: Filter thumbnails by segmentation ID
            limit: Number of thumbnails to return
            offset: Offset from the start of the list
            
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
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def create_frame_extraction(
        self,
        file_id: str,
        strategy: str = "uniform",
        uniform_config: Optional[Union[FrameExtractionUniformConfig, Dict[str, Any]]] = None,
        thumbnails_config: Optional[Union[FrameExtractionThumbnailsConfig, Dict[str, Any]]] = None,
        start_time_seconds: Optional[float] = None,
        end_time_seconds: Optional[float] = None,
        wait_until_finish: bool = False,
        poll_interval: int = 5,
        timeout: int = 600,
    ):
        """Create a frame extraction job for a file.

        Args:
            file_id: The ID of the file to extract frames from
            strategy: Frame extraction strategy - currently only 'uniform' is supported
            uniform_config: Configuration for uniform frame extraction (frames_per_second, max_width)
            thumbnails_config: Configuration for frame thumbnails (optional)
            start_time_seconds: Start time in seconds to begin extracting frames
            end_time_seconds: End time in seconds to stop extracting frames
            wait_until_finish: Whether to wait for the job to complete
            poll_interval: How often to check the job status (in seconds)
            timeout: Maximum time to wait for the job to complete (in seconds)

        Returns:
            FrameExtraction: The frame extraction job object

        Raises:
            CloudGlueError: If there is an error creating the frame extraction job
        """
        try:
            # Convert config dicts to objects if needed
            uniform_config_obj = None
            if uniform_config is not None:
                if isinstance(uniform_config, dict):
                    uniform_config_obj = FrameExtractionUniformConfig(**uniform_config)
                else:
                    uniform_config_obj = uniform_config
            
            thumbnails_config_obj = None
            if thumbnails_config is not None:
                if isinstance(thumbnails_config, dict):
                    thumbnails_config_obj = FrameExtractionThumbnailsConfig(**thumbnails_config)
                else:
                    thumbnails_config_obj = thumbnails_config

            # Create the request object
            request = CreateFileFrameExtractionRequest(
                strategy=strategy,
                uniform_config=uniform_config_obj,
                thumbnails_config=thumbnails_config_obj,
                start_time_seconds=start_time_seconds,
                end_time_seconds=end_time_seconds
            )

            # Create the frame extraction job
            response = self.api.create_file_frame_extraction(
                file_id=file_id,
                create_file_frame_extraction_request=request
            )

            # If wait_until_finish is True, poll until completion
            if wait_until_finish:
                start_time = time.time()
                while time.time() - start_time < timeout:
                    # Check if the job is complete
                    if hasattr(response, 'status') and response.status in ['completed', 'failed']:
                        break
                    
                    # Wait before checking again
                    time.sleep(poll_interval)
                    
                    # Get updated status
                    try:
                        from cloudglue.client.main import CloudGlue
                        client = CloudGlue()  # This is not ideal but we need access to frames API
                        response = client.frames.get(response.id)
                    except Exception:
                        # If we can't get status, just return what we have
                        break
                        
                # Check if we timed out
                if hasattr(response, 'status') and response.status not in ['completed', 'failed']:
                    raise CloudGlueError(f"Frame extraction job timed out after {timeout} seconds")

            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))


class Segmentations:
    """Client for the CloudGlue Segmentations API."""

    def __init__(self, api):
        """Initialize the Segmentations client.

        Args:
            api: The SegmentationsApi instance.
        """
        self.api = api

    @staticmethod
    def create_uniform_config(
        window_seconds: Union[int, float],
        hop_seconds: Optional[Union[int, float]] = None,
        start_time_seconds: Optional[Union[int, float]] = None,
        end_time_seconds: Optional[Union[int, float]] = None,
    ) -> SegmentationConfig:
        """Create a uniform segmentation configuration.

        Args:
            window_seconds: The duration of each segment in seconds (2-60)
            hop_seconds: The offset between the start of new windows. Defaults to window_seconds if not provided
            start_time_seconds: Optional start time of the video in seconds to start segmenting from
            end_time_seconds: Optional end time of the video in seconds to stop segmenting at

        Returns:
            SegmentationConfig configured for uniform segmentation

        Example:
            # 20-second segments with no overlap
            config = client.segmentations.create_uniform_config(window_seconds=20)
            
            # 30-second segments with 15-second overlap
            config = client.segmentations.create_uniform_config(
                window_seconds=30, 
                hop_seconds=15
            )
        """
        uniform_config = SegmentationUniformConfig(
            window_seconds=window_seconds,
            hop_seconds=hop_seconds,
        )
        
        return SegmentationConfig(
            strategy="uniform",
            uniform_config=uniform_config,
            start_time_seconds=start_time_seconds,
            end_time_seconds=end_time_seconds,
        )

    @staticmethod
    def create_shot_detector_config(
        detector: str,
        threshold: Optional[Union[int, float]] = None,
        min_seconds: Optional[Union[int, float]] = None,
        max_seconds: Optional[Union[int, float]] = None,
        start_time_seconds: Optional[Union[int, float]] = None,
        end_time_seconds: Optional[Union[int, float]] = None,
    ) -> SegmentationConfig:
        """Create a shot detector segmentation configuration.

        Args:
            detector: The detector strategy ('adaptive' for dynamic footage, 'content' for controlled footage)
            threshold: Detection sensitivity threshold (lower values create more segments)
            min_seconds: The minimum length of a shot in seconds (2-60)
            max_seconds: The maximum length of a shot in seconds (2-60)
            start_time_seconds: Optional start time of the video in seconds to start segmenting from
            end_time_seconds: Optional end time of the video in seconds to stop segmenting at

        Returns:
            SegmentationConfig configured for shot detection

        Example:
            # Adaptive detector for dynamic content
            config = client.segmentations.create_shot_detector_config(
                detector="adaptive",
                threshold=3.0,
                min_seconds=5,
                max_seconds=30
            )
            
            # Content detector for controlled footage
            config = client.segmentations.create_shot_detector_config(
                detector="content",
                threshold=27.0
            )
        """
        shot_detector_config = SegmentationShotDetectorConfig(
            detector=detector,
            threshold=threshold,
            min_seconds=min_seconds,
            max_seconds=max_seconds,
        )
        
        return SegmentationConfig(
            strategy="shot-detector",
            shot_detector_config=shot_detector_config,
            start_time_seconds=start_time_seconds,
            end_time_seconds=end_time_seconds,
        )

    @staticmethod
    def create_manual_config(
        segments: List[Dict[str, Union[int, float]]],
    ) -> SegmentationConfig:
        """Create a manual segmentation configuration.

        Args:
            segments: List of segment definitions, each containing:
                - start_time: Start time of the segment in seconds
                - end_time: End time of the segment in seconds

        Returns:
            SegmentationConfig configured for manual segmentation

        Example:
            # Manual segmentation with specific time ranges
            config = client.segmentations.create_manual_config(
                segments=[
                    {"start_time": 0, "end_time": 30},
                    {"start_time": 30, "end_time": 60},
                    {"start_time": 60, "end_time": 90}
                ]
            )
        """
        # Convert dict segments to SegmentationManualConfigSegmentsInner objects
        segment_objects = [
            SegmentationManualConfigSegmentsInner(
                start_time=seg.get("start_time"),
                end_time=seg.get("end_time")
            )
            for seg in segments
        ]
        
        manual_config = SegmentationManualConfig(
            segments=segment_objects,
        )
        
        return SegmentationConfig(
            strategy="manual",
            manual_config=manual_config,
        )

    def get(
        self,
        segmentation_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """Get a specific segmentation including its segments.

        Args:
            segmentation_id: The ID of the segmentation to retrieve
            limit: Number of segments to return (max 100)
            offset: Offset from the start of the segments list

        Returns:
            The typed Segmentation object with segments and metadata

        Raises:
            CloudGlueError: If there is an error retrieving the segmentation or processing the request.
        """
        try:
            response = self.api.get_segmentation(
                segmentation_id=segmentation_id,
                limit=limit,
                offset=offset,
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def delete(self, segmentation_id: str):
        """Delete a segmentation.

        Args:
            segmentation_id: The ID of the segmentation to delete

        Returns:
            The deletion confirmation

        Raises:
            CloudGlueError: If there is an error deleting the segmentation or processing the request.
        """
        try:
            response = self.api.delete_segmentation(segmentation_id=segmentation_id)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def get_thumbnails(
        self,
        segmentation_id: str,
        segment_ids: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """
        Get thumbnails for a segmentation.
        
        Args:
            segmentation_id: The ID of the segmentation to retrieve thumbnails for
            segment_ids: Filter thumbnails by segment IDs. If provided, will only return thumbnails for the specified segments. Comma separated list of segment IDs.
            limit: Number of thumbnails to return
            offset: Offset from the start of the list
            
        Returns:
            ThumbnailList response
        """
        try:
            response = self.api.get_segmentation_thumbnails(
                segmentation_id=segmentation_id,
                segment_ids=segment_ids,
                limit=limit,
                offset=offset,
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))


class Segments:
    """Client for the CloudGlue Segments API."""

    def __init__(self, api):
        """Initialize the Segments client.

        Args:
            api: The SegmentsApi instance.
        """
        self.api = api

    @staticmethod
    def create_shot_config(
        detector: str = "adaptive",
        max_duration_seconds: int = 300,
        min_duration_seconds: int = 1,
    ) -> ShotConfig:
        """Create a shot-based segmentation configuration.

        Args:
            detector: Detection algorithm ('adaptive' or 'content')
            max_duration_seconds: Maximum duration for each segment in seconds (1-3600)
            min_duration_seconds: Minimum duration for each segment in seconds (1-3600)

        Returns:
            ShotConfig object
        """
        return ShotConfig(
            detector=detector,
            max_duration_seconds=max_duration_seconds,
            min_duration_seconds=min_duration_seconds,
        )

    @staticmethod
    def create_narrative_config(
        prompt: Optional[str] = None,
        strategy: Optional[str] = None,
        number_of_chapters: Optional[int] = None,
    ) -> NarrativeConfig:
        """Create a narrative-based segmentation configuration.

        Args:
            prompt: Optional custom prompt to guide the narrative segmentation analysis.
                This will be incorporated into the main segmentation prompt as additional guidance.
            strategy: Optional narrative segmentation strategy. Options:
                - 'balanced': Uses multimodal describe job for comprehensive analysis.
                  Default strategy, recommended for most videos. Supports YouTube URLs.
                - 'comprehensive': Uses a VLM to deeply analyze logical segments of video.
                  Only available for non-YouTube videos.
                Note: YouTube URLs automatically use the 'balanced' strategy regardless of
                the strategy field value. The 'comprehensive' strategy is not supported for YouTube URLs.
            number_of_chapters: Optional target number of chapters to generate.
                If provided, the AI will attempt to generate exactly this number of chapters.
                Must be >= 1 if provided.

        Returns:
            NarrativeConfig object
        """
        return NarrativeConfig(
            prompt=prompt,
            strategy=strategy,
            number_of_chapters=number_of_chapters,
        )

    def create(
        self,
        url: str,
        criteria: str,
        shot_config: Optional[Union[ShotConfig, Dict[str, Any]]] = None,
        narrative_config: Optional[Union[NarrativeConfig, Dict[str, Any]]] = None,
    ) -> Segments:
        """Create a new segmentation job.

        Args:
            url: Input video URL. Supports URIs of files uploaded to Cloudglue Files endpoint,
                public HTTP URLs, S3 files, and other data connected URLs. **⚠️ Note: YouTube URLs are supported for 
                narrative-based segmentation only.** Shot-based segmentation requires direct 
                video file access.
            criteria: Segmentation criteria ('shot' or 'narrative')
            shot_config: Configuration for shot-based segmentation (only when criteria is 'shot')
            narrative_config: Configuration for narrative-based segmentation (only when criteria is 'narrative')

        Returns:
            Segments object representing the created job

        Raises:
            CloudGlueError: If the request fails
        """
        try:
            # Convert dict configs to objects if needed
            if isinstance(shot_config, dict):
                shot_config = ShotConfig(**shot_config)
            if isinstance(narrative_config, dict):
                narrative_config = NarrativeConfig(**narrative_config)

            new_segments = NewSegments(
                url=url,
                criteria=criteria,
                shot_config=shot_config,
                narrative_config=narrative_config,
            )

            response = self.api.create_segments(new_segments)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def get(self, job_id: str) -> Segments:
        """Get a segmentation job by ID.

        Args:
            job_id: The unique identifier of the segmentation job

        Returns:
            Segments object

        Raises:
            CloudGlueError: If the request fails
        """
        try:
            response = self.api.get_segments(job_id)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def list(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        status: Optional[str] = None,
        criteria: Optional[str] = None,
        created_before: Optional[str] = None,
        created_after: Optional[str] = None,
        url: Optional[str] = None,
    ) -> SegmentsList:
        """List segmentation jobs.

        Args:
            limit: Maximum number of segmentation jobs to return (max 100)
            offset: Number of segmentation jobs to skip
            status: Filter segmentation jobs by status
            criteria: Filter segmentation jobs by criteria type
            created_before: Filter segmentation jobs created before a specific date (YYYY-MM-DD format)
            created_after: Filter segmentation jobs created after a specific date (YYYY-MM-DD format)
            url: Filter segmentation jobs by the input URL used for segmentation

        Returns:
            SegmentsList object

        Raises:
            CloudGlueError: If the request fails
        """
        try:
            response = self.api.list_segments(
                limit=limit,
                offset=offset,
                status=status,
                criteria=criteria,
                created_before=created_before,
                created_after=created_after,
                url=url,
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def delete(self, job_id: str):
        """Delete a segments job.

        Args:
            job_id: The ID of the segments job to delete

        Returns:
            The deletion confirmation

        Raises:
            CloudGlueError: If there is an error deleting the segments job.
        """
        try:
            response = self.api.delete_segments(job_id=job_id)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def run(
        self,
        url: str,
        criteria: str,
        shot_config: Optional[Union[ShotConfig, Dict[str, Any]]] = None,
        narrative_config: Optional[Union[NarrativeConfig, Dict[str, Any]]] = None,
        poll_interval: int = 5,
        timeout: int = 600,
    ) -> Segments:
        """Create a segmentation job and wait for it to complete.

        Args:
            url: Input video URL. Supports URIs of files uploaded to Cloudglue Files endpoint,
                public HTTP URLs, S3 files, and other data connected URLs. **⚠️ Note: YouTube URLs are supported for 
                narrative-based segmentation only.** Shot-based segmentation requires direct 
                video file access.
            criteria: Segmentation criteria ('shot' or 'narrative')
            shot_config: Configuration for shot-based segmentation (only when criteria is 'shot')
            narrative_config: Configuration for narrative-based segmentation (only when criteria is 'narrative')
            poll_interval: How often to check the job status (in seconds).
            timeout: Maximum time to wait for the job to complete (in seconds).

        Returns:
            Segments: The completed Segments object with status and segments data.

        Raises:
            CloudGlueError: If there is an error creating or processing the segmentation job.
            TimeoutError: If the job does not complete within the specified timeout.
        """
        try:
            # Create the segmentation job
            job = self.create(
                url=url,
                criteria=criteria,
                shot_config=shot_config,
                narrative_config=narrative_config,
            )
            job_id = job.job_id

            # Poll for completion
            elapsed = 0
            while elapsed < timeout:
                status = self.get(job_id=job_id)

                if status.status in ["completed", "failed"]:
                    return status

                time.sleep(poll_interval)
                elapsed += poll_interval

            raise TimeoutError(
                f"Segmentation job did not complete within {timeout} seconds"
            )
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))


class Search:
    """Client for the CloudGlue Search API."""

    def __init__(self, api):
        """Initialize the Search client.

        Args:
            api: The SearchApi instance.
        """
        self.api = api

    @staticmethod
    def _create_metadata_filter(
        path: str,
        operator: str,
        value_text: Optional[str] = None,
        value_text_array: Optional[List[str]] = None,
    ) -> SearchFilterCriteria:
        """Create a metadata filter for search.
        
        Args:
            path: JSON path on metadata object (e.g. 'my_custom_field', 'category.subcategory')
            operator: Comparison operator ('NotEqual', 'Equal', 'LessThan', 'GreaterThan', 'In', 'ContainsAny', 'ContainsAll', 'Like')
            value_text: Text value for scalar comparison (used with NotEqual, Equal, LessThan, GreaterThan, Like)
            value_text_array: Array of values for array comparisons (used with ContainsAny, ContainsAll, In)
            
        Returns:
            SearchFilterCriteria object
        """
        return SearchFilterCriteria(
            path=path,
            operator=operator,
            value_text=value_text,
            value_text_array=value_text_array,
        )

    @staticmethod
    def _create_video_info_filter(
        path: str,
        operator: str,
        value_text: Optional[str] = None,
        value_text_array: Optional[List[str]] = None,
    ) -> SearchFilterVideoInfoInner:
        """Create a video info filter for search.
        
        Args:
            path: Video info field ('duration_seconds', 'has_audio')
            operator: Comparison operator ('NotEqual', 'Equal', 'LessThan', 'GreaterThan', 'In', 'ContainsAny', 'ContainsAll', 'Like')
            value_text: Text value for scalar comparison (used with NotEqual, Equal, LessThan, GreaterThan, Like)
            value_text_array: Array of values for array comparisons (used with ContainsAny, ContainsAll, In)
            
        Returns:
            SearchFilterVideoInfoInner object
        """
        return SearchFilterVideoInfoInner(
            path=path,
            operator=operator,
            value_text=value_text,
            value_text_array=value_text_array,
        )

    @staticmethod
    def _create_file_filter(
        path: str,
        operator: str,
        value_text: Optional[str] = None,
        value_text_array: Optional[List[str]] = None,
    ) -> SearchFilterFileInner:
        """Create a file filter for search.
        
        Args:
            path: File field ('bytes', 'filename', 'uri', 'created_at', 'id')
            operator: Comparison operator ('NotEqual', 'Equal', 'LessThan', 'GreaterThan', 'In', 'ContainsAny', 'ContainsAll', 'Like')
            value_text: Text value for scalar comparison (used with NotEqual, Equal, LessThan, GreaterThan, Like)
            value_text_array: Array of values for array comparisons (used with ContainsAny, ContainsAll, In)
            
        Returns:
            SearchFilterFileInner object
        """
        return SearchFilterFileInner(
            path=path,
            operator=operator,
            value_text=value_text,
            value_text_array=value_text_array,
        )

    @staticmethod
    def create_filter(
        metadata_filters: Optional[List[Dict[str, Any]]] = None,
        video_info_filters: Optional[List[Dict[str, Any]]] = None,
        file_filters: Optional[List[Dict[str, Any]]] = None,
    ) -> SearchFilter:
        """Create a search filter using simple dictionaries.
        
        This is the main method for creating search filters. It allows you to create filters 
        using simple dictionaries instead of working with the underlying filter objects.
        
        Args:
            metadata_filters: List of metadata filter dictionaries. Each dict should have:
                - 'path': JSON path on metadata object
                - 'operator': Comparison operator ('NotEqual', 'Equal', 'LessThan', 'GreaterThan', 'In', 'ContainsAny', 'ContainsAll', 'Like')
                - 'value_text': (optional) Text value for scalar comparison  
                - 'value_text_array': (optional) Array of values for array comparisons
            video_info_filters: List of video info filter dictionaries (same structure)
            file_filters: List of file filter dictionaries (same structure)
            
        Returns:
            SearchFilter object
            
        Example:
            filter = client.search.create_filter(
                metadata_filters=[
                    {'path': 'category', 'operator': 'Equal', 'value_text': 'tutorial'},
                    {'path': 'tags', 'operator': 'ContainsAny', 'value_text_array': ['python', 'programming']}
                ],
                video_info_filters=[
                    {'path': 'duration_seconds', 'operator': 'LessThan', 'value_text': '600'}
                ]
            )
        """
        metadata_objs = None
        if metadata_filters:
            metadata_objs = [
                SearchFilterCriteria(**f) for f in metadata_filters
            ]
            
        video_info_objs = None
        if video_info_filters:
            video_info_objs = [
                SearchFilterVideoInfoInner(**f) for f in video_info_filters
            ]
            
        file_objs = None
        if file_filters:
            file_objs = [
                SearchFilterFileInner(**f) for f in file_filters
            ]
            
        return SearchFilter(
            metadata=metadata_objs,
            video_info=video_info_objs,
            file=file_objs,
        )

    def search(
        self,
        scope: str,
        collections: List[str],
        query: Optional[str] = None,
        limit: Optional[int] = None,
        filter: Optional[Union[SearchFilter, Dict[str, Any]]] = None,
        source_image: Optional[Union[str, Dict[str, Any]]] = None,
        group_by_key: Optional[str] = None,
        threshold: Optional[Union[int, float]] = None,
        sort_by: Optional[str] = None,
        **kwargs,
    ):
        """Search across video files and segments to find relevant content.

        Args:
            scope: Search scope - 'file' searches at file level (requires collections with enable_summary=true), 
                   'segment' searches at segment level, 'face' searches for faces in videos using image matching
            collections: List of collection IDs to search within. 
                        For text search (scope='file' or 'segment'): Must be rich-transcript collections 
                        (collection_type='rich-transcripts' or 'media-descriptions'). For file-level search, 
                        collections must have 'enable_summary: true' in transcribe_config.
                        For face search (scope='face'): Must be face-analysis collections (collection_type='face-analysis').
            query: Text search query to find relevant content (required for scope='file' or 'segment', not used for scope='face')
            limit: Maximum number of search results to return (1-100, default 10). When group_by_key is specified,
                   this applies to total items across groups (not the number of groups).
            filter: Filter criteria to constrain search results. Can be a SearchFilter object
                   or a dictionary with 'metadata', 'video_info', and/or 'file' keys.
            source_image: Source image for face search (required for scope='face'). Can be:
                - URL string (public image URL)
                - Local file path (will be converted to base64)
                - Base64 string (raw base64 or with data: prefix)
                - Dictionary with 'url' or 'base64' keys
            group_by_key: Optional key to group results by. Currently only 'file' is supported.
                         Cannot be used with scope='file'. When specified, results are grouped by file_id.
            threshold: Optional minimum score threshold to filter results. Can be any real number.
            sort_by: Optional sort order for results. Default: 'score'. When group_by_key is specified,
                    can also use 'item_count' to sort by number of items per group.
            **kwargs: Additional parameters for the request.

        Returns:
            SearchResponse: The API response with search results.

        Raises:
            CloudGlueError: If there is an error making the API request or processing the response.

        Example:
            # Text search for content in collections
            results = client.search.search(
                scope="segment",
                collections=["collection_123"],
                query="machine learning tutorial",
                limit=20
            )
            
            # Text search with filters
            search_filter = client.search.create_filter(
                metadata_filters=[
                    {'path': 'category', 'operator': 'Equal', 'value_text': 'tutorial'}
                ]
            )
            results = client.search.search(
                scope="file",
                collections=["collection_123"],
                query="python programming",
                filter=search_filter
            )
            
            # Face search
            results = client.search.search(
                scope="face",
                collections=["face_collection_123"],
                source_image="https://example.com/image.jpg",
                limit=20
            )
        """
        try:
            # Handle filter parameter
            if filter is not None:
                if isinstance(filter, dict):
                    # Convert dictionary to SearchFilter
                    filter = SearchFilter.from_dict(filter)
                elif isinstance(filter, SearchFilter):
                    # Already the correct type, no conversion needed
                    pass
                else:
                    raise ValueError("filter must be a SearchFilter object or dictionary")
            
            # Handle source_image parameter for face search
            source_image_obj = None
            if source_image is not None:
                if isinstance(source_image, dict):
                    # Already in SearchRequestSourceImage format
                    source_image_obj = SearchRequestSourceImage(**source_image)
                elif isinstance(source_image, str):
                    if source_image.startswith(('http://', 'https://')):
                        # URL
                        source_image_obj = SearchRequestSourceImage(url=source_image)
                    elif source_image.startswith('data:image/'):
                        # Data URL - extract base64 part
                        base64_part = source_image.split(',')[1] if ',' in source_image else source_image
                        source_image_obj = SearchRequestSourceImage(base64=base64_part)
                    elif os.path.exists(source_image):
                        # File path - encode to base64
                        # Check file extension
                        file_ext = pathlib.Path(source_image).suffix.lower()
                        if file_ext not in ['.jpg', '.jpeg', '.png']:
                            raise CloudGlueError(f"Unsupported file type: {file_ext}. Only JPG and PNG are supported.")
                        
                        # Read and encode the file
                        with open(source_image, 'rb') as image_file:
                            image_data = image_file.read()
                            base64_string = base64.b64encode(image_data).decode('utf-8')
                            source_image_obj = SearchRequestSourceImage(base64=base64_string)
                    else:
                        # Assume raw base64 string
                        source_image_obj = SearchRequestSourceImage(base64=source_image)
                else:
                    raise CloudGlueError("source_image must be a string (URL, file path, or base64) or dictionary")
            
            request = SearchRequest(
                scope=scope,
                collections=collections,
                query=query,
                limit=limit,
                filter=filter,
                source_image=source_image_obj,
                group_by_key=group_by_key,
                threshold=threshold,
                sort_by=sort_by,
                **kwargs,
            )
            return self.api.search_content(search_request=request)
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            if isinstance(e, CloudGlueError):
                raise
            raise CloudGlueError(str(e))


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
    ):
        """
        Get thumbnails for a file.
        
        Args:
            file_id: The ID of the file
            is_default: Filter thumbnails by default status. If true, will only return the default thumbnail for the file
            segmentation_id: Filter thumbnails by segmentation ID
            limit: Number of thumbnails to return
            offset: Offset from the start of the list
            
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
    ):
        """
        Get thumbnails for a segmentation.
        
        Args:
            segmentation_id: The ID of the segmentation to retrieve thumbnails for
            segment_ids: Filter thumbnails by segment IDs. If provided, will only return thumbnails for the specified segments. Comma separated list of segment IDs.
            limit: Number of thumbnails to return
            offset: Offset from the start of the list
            
        Returns:
            ThumbnailList response
        """
        try:
            response = self.api.get_segmentation_thumbnails(
                segmentation_id=segmentation_id,
                segment_ids=segment_ids,
                limit=limit,
                offset=offset,
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


class Chat:
    """Chat namespace for the CloudGlue client."""

    def __init__(self, api):
        """Initialize with the API client."""
        self.api = api
        self.completions = Completions(api)
