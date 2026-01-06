# cloudglue/client/resources/chat.py
"""Chat and Completions resources for CloudGlue API."""
from typing import List, Dict, Any, Optional, Union

from cloudglue.sdk.models.chat_completion_request import ChatCompletionRequest
from cloudglue.sdk.models.chat_completion_request_filter import ChatCompletionRequestFilter
from cloudglue.sdk.models.chat_completion_request_filter_metadata_inner import ChatCompletionRequestFilterMetadataInner
from cloudglue.sdk.models.chat_completion_request_filter_video_info_inner import ChatCompletionRequestFilterVideoInfoInner
from cloudglue.sdk.models.chat_completion_request_filter_file_inner import ChatCompletionRequestFilterFileInner
from cloudglue.sdk.rest import ApiException

from cloudglue.client.resources.base import CloudGlueError


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

    def get(self, id: str):
        """Retrieve a chat completion by ID.

        Args:
            id: The ID of the chat completion to retrieve.

        Returns:
            The chat completion response.

        Raises:
            CloudGlueError: If there is an error making the API request or processing the response.
        """
        try:
            return self.api.get_chat_completion(id=id)
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
    ):
        """List chat completions with optional filtering.

        Args:
            limit: Maximum number of chat completions to return (max 100).
            offset: Number of chat completions to skip.
            created_before: Filter completions created before this date (YYYY-MM-DD format, UTC).
            created_after: Filter completions created after this date (YYYY-MM-DD format, UTC).

        Returns:
            A list response containing chat completions.

        Raises:
            CloudGlueError: If there is an error making the API request or processing the response.
        """
        try:
            return self.api.list_chat_completions(
                limit=limit,
                offset=offset,
                created_before=created_before,
                created_after=created_after,
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

