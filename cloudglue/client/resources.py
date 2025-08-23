# cloudglue/client/resources.py
from typing import List, Dict, Any, Optional, Union
import os
import pathlib
import time

from cloudglue.sdk.models.chat_completion_request import ChatCompletionRequest
from cloudglue.sdk.models.chat_completion_request_filter import ChatCompletionRequestFilter
from cloudglue.sdk.models.chat_completion_request_filter_metadata_inner import ChatCompletionRequestFilterMetadataInner
from cloudglue.sdk.models.chat_completion_request_filter_video_info_inner import ChatCompletionRequestFilterVideoInfoInner  
from cloudglue.sdk.models.chat_completion_request_filter_file_inner import ChatCompletionRequestFilterFileInner
from cloudglue.sdk.models.new_transcribe import NewTranscribe
from cloudglue.sdk.models.new_extract import NewExtract
from cloudglue.sdk.models.new_collection import NewCollection
from cloudglue.sdk.models.add_collection_file import AddCollectionFile
from cloudglue.sdk.models.add_you_tube_collection_file import AddYouTubeCollectionFile
from cloudglue.sdk.models.file_update import FileUpdate
from cloudglue.sdk.models.segmentation_config import SegmentationConfig
from cloudglue.sdk.models.segmentation_uniform_config import SegmentationUniformConfig
from cloudglue.sdk.models.segmentation_shot_detector_config import SegmentationShotDetectorConfig
from cloudglue.sdk.models.search_request import SearchRequest
from cloudglue.sdk.models.search_filter import SearchFilter
from cloudglue.sdk.models.search_filter_criteria import SearchFilterCriteria
from cloudglue.sdk.models.search_filter_file_inner import SearchFilterFileInner
from cloudglue.sdk.models.search_filter_video_info_inner import SearchFilterVideoInfoInner
from cloudglue.sdk.rest import ApiException
from cloudglue.sdk.models.thumbnails_config import ThumbnailsConfig
from cloudglue.sdk.api.segmentations_api import SegmentationsApi
from cloudglue.sdk.models.create_file_segmentation_request import CreateFileSegmentationRequest


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
        force_search: Optional[bool] = None,
        include_citations: Optional[bool] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ):
        """Create a chat completion.

        Args:
            messages: List of message dictionaries with "role" and "content" keys.
            model: The model to use for completion.
            collections: List of collection IDs to search.
            filter: Filter criteria to constrain search results. Can be a ChatCompletionRequestFilter object
                   or a dictionary with 'metadata', 'video_info', and/or 'file' keys.
            force_search: Whether to force a search. If None, uses API default.
            include_citations: Whether to include citations in the response. If None, uses API default.
            max_tokens: Maximum number of tokens to generate. If None, uses API default.
            temperature: Sampling temperature. If None, uses API default.
            top_p: Nucleus sampling parameter. If None, uses API default.
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
                force_search=force_search,
                include_citations=include_citations,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
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
        default_segmentation_config: Optional[Union[SegmentationConfig, Dict[str, Any]]] = None,
    ):
        """Create a new collection.

        Args:
            collection_type: Type of collection ('entities', 'rich-transcripts')
            name: Name of the collection (must be unique)
            description: Optional description of the collection
            extract_config: Optional configuration for extraction processing
            transcribe_config: Optional configuration for transcription processing
            default_segmentation_config: Default segmentation configuration for files in this collection

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

            request = NewCollection(
                collection_type=collection_type,
                name=name,
                description=description,
                extract_config=extract_config,
                transcribe_config=transcribe_config,
                default_segmentation_config=default_segmentation_config,
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

    def add_video(
        self,
        collection_id: str,
        file_id: str,
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
            file_id: The ID of the file to add to the collection
            url: The URL of the file to add to the collection (optional, derived from file_id if not provided)
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
            if segmentation_id and segmentation_config:
                raise ValueError("Cannot provide both segmentation_id and segmentation_config")

            # Handle segmentation_config parameter
            if isinstance(segmentation_config, dict):
                segmentation_config = SegmentationConfig.from_dict(segmentation_config)

            # Create request object using the SDK model
            request = AddCollectionFile(
                file_id=file_id,
                url=url or f"cloudglue://files/{file_id}",  # Default URL format if not provided
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
            elapsed = 0
            terminal_states = ["ready", "completed", "failed", "not_applicable"]

            while elapsed < timeout:
                status = self.get_video(collection_id=collection_id, file_id=file_id)

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

    def add_youtube_video(
        self,
        collection_id: str,
        url: str,
        metadata: Optional[Dict[str, Any]] = None,
        segmentation_id: Optional[str] = None,
        segmentation_config: Optional[Union[SegmentationConfig, Dict[str, Any]]] = None,
        wait_until_finish: bool = False,
        poll_interval: int = 5,
        timeout: int = 600,
    ):
        """Add a YouTube video to a collection by URL.

        Args:
            collection_id: The ID of the collection
            url: The URL of the YouTube video to add
            metadata: Optional user-provided metadata about the YouTube video
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
            if segmentation_id and segmentation_config:
                raise ValueError("Cannot provide both segmentation_id and segmentation_config")

            # Handle segmentation_config parameter
            if isinstance(segmentation_config, dict):
                segmentation_config = SegmentationConfig.from_dict(segmentation_config)

            # Create request object using the SDK model
            request = AddYouTubeCollectionFile(
                url=url,
                metadata=metadata,
                segmentation_id=segmentation_id,
                segmentation_config=segmentation_config,
            )

            # Use the standard method to get a properly typed object
            response = self.api.add_you_tube_video(
                collection_id=collection_id, add_you_tube_collection_file=request
            )

            # If not waiting for completion, return immediately
            if not wait_until_finish:
                return response

            # Otherwise poll until completion or timeout
            file_id = response.file_id
            elapsed = 0
            terminal_states = ["ready", "completed", "failed", "not_applicable"]

            while elapsed < timeout:
                status = self.get_video(collection_id=collection_id, file_id=file_id)

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

        Returns:
            The typed CollectionFileList object with videos and metadata

        Raises:
            CloudGlueError: If there is an error listing the videos or processing the request.
        """
        try:
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
        response_format: Optional[str] = None,
    ):
        """Get the rich transcript of a video in a collection.

        Args:
            collection_id: The ID of the collection
            file_id: The ID of the file to retrieve the rich transcript for
            response_format: The format of the response, one of 'json' or 'markdown' (json by default)

        Returns:
            The typed RichTranscript object with video rich transcript data

        Raises:
            CloudGlueError: If there is an error retrieving the rich transcript or processing the request.
        """
        try:
            # Use the standard method to get a properly typed object
            response = self.api.get_transcripts(
                collection_id=collection_id, file_id=file_id, response_format=response_format
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def get_video_entities(self, collection_id: str, file_id: str):
        """Get the entities extracted from a video in a collection.

        Args:
            collection_id: The ID of the collection
            file_id: The ID of the file to retrieve entities for

        Returns:
            The typed Entities object with video entities data

        Raises:
            CloudGlueError: If there is an error retrieving the entities or processing the request.
        """
        try:
            # Use the standard method to get a properly typed object
            response = self.api.get_entities(
                collection_id=collection_id,
                file_id=file_id,
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

    def get(self, job_id: str):
        """Get the status of an extraction job.

        Args:
            job_id: The ID of the extraction job.

        Returns:
            Extract: A typed Extract object containing the job status and extracted data if available.

        Raises:
            CloudGlueError: If there is an error retrieving the extraction job or processing the request.
        """
        try:
            response = self.api.get_extract(job_id=job_id)
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


class Files:
    """Handles file operations."""

    def __init__(self, api):
        """Initialize with the API client."""
        self.api = api

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

        Returns:
            A list of file objects.

        Raises:
            CloudGlueError: If there is an error listing files or processing the request.
        """
        try:
            return self.api.list_files(
                status=status,
                created_before=created_before,
                created_after=created_after,
                limit=limit,
                offset=offset,
                order=order,
                sort=sort,
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
            operator: Comparison operator ('NotEqual', 'Equal', 'LessThan', 'GreaterThan', 'In', 'ContainsAny', 'ContainsAll')
            value_text: Text value for scalar comparison (used with NotEqual, Equal, LessThan, GreaterThan)
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
            operator: Comparison operator ('NotEqual', 'Equal', 'LessThan', 'GreaterThan', 'In', 'ContainsAny', 'ContainsAll')
            value_text: Text value for scalar comparison (used with NotEqual, Equal, LessThan, GreaterThan)
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
            operator: Comparison operator ('NotEqual', 'Equal', 'LessThan', 'GreaterThan', 'In', 'ContainsAny', 'ContainsAll')
            value_text: Text value for scalar comparison (used with NotEqual, Equal, LessThan, GreaterThan)
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
                - 'operator': Comparison operator
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
        query: str,
        limit: Optional[int] = None,
        filter: Optional[Union[SearchFilter, Dict[str, Any]]] = None,
        **kwargs,
    ):
        """Search across video files and segments to find relevant content.

        Args:
            scope: Search scope - 'file' searches at file level (requires collections with enable_summary=true), 
                   'segment' searches at segment level
            collections: List of collection IDs to search within. Must be rich-transcript collections 
                        (collection_type='rich-transcripts'). For file-level search, collections must have 
                        'enable_summary: true' in transcribe_config.
            query: Text search query to find relevant content
            limit: Maximum number of search results to return (1-100, default 10)
            filter: Filter criteria to constrain search results. Can be a SearchFilter object
                   or a dictionary with 'metadata', 'video_info', and/or 'file' keys.
            **kwargs: Additional parameters for the request.

        Returns:
            SearchResponse: The API response with search results.

        Raises:
            CloudGlueError: If there is an error making the API request or processing the response.

        Example:
            # Search for content in collections
            results = client.search.search(
                scope="segment",
                collections=["collection_123"],
                query="machine learning tutorial",
                limit=20
            )
            
            # Search with filters
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
            
            request = SearchRequest(
                scope=scope,
                collections=collections,
                query=query,
                limit=limit,
                filter=filter,
                **kwargs,
            )
            return self.api.search_content(search_request=request)
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
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


class Chat:
    """Chat namespace for the CloudGlue client."""

    def __init__(self, api):
        """Initialize with the API client."""
        self.api = api
        self.completions = Completions(api)
