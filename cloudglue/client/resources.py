# cloudglue/client/resources.py
from typing import List, Dict, Any, Optional, Union
import os
import pathlib
import time
import json

from cloudglue.sdk.models.chat_completion_request import ChatCompletionRequest
from cloudglue.sdk.models.new_describe import NewDescribe
from cloudglue.sdk.models.new_extract import NewExtract
from cloudglue.sdk.models.new_collection import NewCollection
from cloudglue.sdk.models.add_collection_file import AddCollectionFile
from cloudglue.sdk.models.add_you_tube_collection_file import AddYouTubeCollectionFile
from cloudglue.sdk.rest import ApiException


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

    def create(
        self,
        messages: List[Dict[str, str]],
        model: str = "nimbus-001",
        collections: Optional[List[str]] = None,
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
            request = ChatCompletionRequest(
                model=model,
                messages=messages,
                collections=collections or [],
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
        name: str,
        description: Optional[str] = None,
        describe_config: Optional[Dict[str, Any]] = None,
        extract_config: Optional[Dict[str, Any]] = None,
    ):
        """Create a new collection.

        Args:
            name: Name of the collection (must be unique)
            description: Optional description of the collection
            describe_config: Optional configuration for description processing
                             Contains enable_speech, enable_scene_text, enable_visual_scene_description
            extract_config: Optional configuration for extraction processing

        Returns:
            The typed Collection object with all properties

        Raises:
            CloudGlueError: If there is an error creating the collection or processing the request.
        """
        try:
            # Create request object using the SDK model
            if description is None:  # TODO(kdr): temporary fix for API
                description = ""

            request = NewCollection(
                name=name,
                description=description,
                describe_config=describe_config,
                extract_config=extract_config,
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
    ):
        """List collections.

        Args:
            limit: Maximum number of collections to return (max 100)
            offset: Number of collections to skip
            order: Field to sort by ('created_at'). Defaults to 'created_at'
            sort: Sort direction ('asc', 'desc'). Defaults to 'desc'

        Returns:
            The typed CollectionList object with collections and metadata

        Raises:
            CloudGlueError: If there is an error listing collections or processing the request.
        """
        try:
            # Use the standard method to get a properly typed object
            response = self.api.list_collections(
                limit=limit, offset=offset, order=order, sort=sort
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
        wait_until_finish: bool = False,
        poll_interval: int = 5,
        timeout: int = 600,
    ):
        """Add a video file to a collection.

        Args:
            collection_id: The ID of the collection
            file_id: The ID of the file to add to the collection
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
            # Create request object using the SDK model
            request = AddCollectionFile(file_id=file_id)

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
        wait_until_finish: bool = False,
        poll_interval: int = 5,
        timeout: int = 600,
    ):
        """Add a YouTube video to a collection by URL.

        Args:
            collection_id: The ID of the collection
            url: The URL of the YouTube video to add
            metadata: Optional user-provided metadata about the YouTube video
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
            # Create request object using the SDK model
            request = AddYouTubeCollectionFile(url=url, metadata=metadata)

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
        order: Optional[str] = None,
        sort: Optional[str] = None,
    ):
        """List videos in a collection.

        Args:
            collection_id: The ID of the collection
            limit: Maximum number of videos to return (max 100)
            offset: Number of videos to skip
            status: Filter by processing status ('pending', 'processing', 'ready', 'failed')
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

    def get_video_description(
        self,
        collection_id: str,
        file_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """Get the description of a video in a collection.

        Args:
            collection_id: The ID of the collection
            file_id: The ID of the file to retrieve the description for
            limit: Maximum number of segments to return
            offset: Number of segments to skip

        Returns:
            The typed Description object with video description data

        Raises:
            CloudGlueError: If there is an error retrieving the description or processing the request.
        """
        try:
            # Use the standard method to get a properly typed object
            response = self.api.get_description(
                collection_id=collection_id, file_id=file_id, limit=limit, offset=offset
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
    ):
        """Create a new extraction job.

        Args:
            url: The URL of the video to extract data from. Can be a YouTube URL or a cloudglue file URI.
            prompt: A natural language description of what to extract. Required if schema is not provided.
            schema: A JSON schema defining the structure of the data to extract. Required if prompt is not provided.

        Returns:
            Extract: A typed Extract object containing job_id, status, and other fields.

        Raises:
            CloudGlueError: If there is an error creating the extraction job or processing the request.
        """
        try:
            if not prompt and not schema:
                raise ValueError("Either prompt or schema must be provided")

            # Set up the request object
            request = NewExtract(url=url, prompt=prompt, var_schema=schema)

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

    def run(
        self,
        url: str,
        prompt: Optional[str] = None,
        schema: Optional[Dict[str, Any]] = None,
        poll_interval: int = 5,
        timeout: int = 600,
    ):
        """Create an extraction job and wait for it to complete.

        Args:
            url: The URL of the video to extract data from. Can be a YouTube URL or a cloudglue file URI.
            prompt: A natural language description of what to extract. Required if schema is not provided.
            schema: A JSON schema defining the structure of the data to extract. Required if prompt is not provided.
            poll_interval: How often to check the job status (in seconds).
            timeout: Maximum time to wait for the job to complete (in seconds).

        Returns:
            Extract: The completed Extract object with status and data.

        Raises:
            CloudGlueError: If there is an error creating or processing the extraction job.
        """
        try:
            # Create the extraction job
            job = self.create(url=url, prompt=prompt, schema=schema)
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


class Describe:
    """Handles video description operations."""

    def __init__(self, api):
        """Initialize with the API client."""
        self.api = api

    def create(
        self,
        url: str,
        enable_speech: bool = True,
        enable_scene_text: bool = True,
        enable_visual_scene_description: bool = True,
    ):
        """Create a new describe job for a video.

        Args:
            url: Input video URL. Can be YouTube URLs or URIs of uploaded files.
            enable_speech: Whether to generate speech transcript.
            enable_scene_text: Whether to generate scene text.
            enable_visual_scene_description: Whether to generate visual scene description.

        Returns:
            The typed Describe job object with job_id and status.

        Raises:
            CloudGlueError: If there is an error creating the describe job or processing the request.
        """
        try:
            request = NewDescribe(
                url=url,
                enable_speech=enable_speech,
                enable_scene_text=enable_scene_text,
                enable_visual_scene_description=enable_visual_scene_description,
            )

            # Use the regular SDK method to create the job
            response = self.api.create_describe(new_describe=request)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    # TODO (kdr): asyncio version of this
    def get(self, job_id: str):
        """Get the current state of a describe job.

        Args:
            job_id: The unique identifier of the describe job.

        Returns:
            The typed Describe job object with status and data.

        Raises:
            CloudGlueError: If there is an error retrieving the describe job or processing the request.
        """
        try:
            # Use the standard method to get a properly typed object
            response = self.api.get_describe(job_id=job_id)
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
        enable_speech: bool = True,
        enable_scene_text: bool = True,
        enable_visual_scene_description: bool = True,
    ):
        """Create a describe job and wait for it to complete.

        Args:
            url: Input video URL. Can be YouTube URLs or URIs of uploaded files.
            poll_interval: Seconds between status checks.
            timeout: Total seconds to wait before giving up.
            enable_speech: Whether to generate speech transcript.
            enable_scene_text: Whether to generate scene text.
            enable_visual_scene_description: Whether to generate visual scene description.

        Returns:
            The completed typed Describe job object.

        Raises:
            CloudGlueError: If there is an error creating or processing the describe job.
        """
        try:
            # Create the job
            job = self.create(
                url=url,
                enable_speech=enable_speech,
                enable_scene_text=enable_scene_text,
                enable_visual_scene_description=enable_visual_scene_description,
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

    def upload(
        self,
        file_path: str,
        metadata: Optional[Dict[str, Any]] = None,
        wait_until_finish: bool = False,
        poll_interval: int = 5,
        timeout: int = 600,
    ):
        """Upload a file to CloudGlue.

        Args:
            file_path: Path to the local file to upload.
            metadata: Optional user-provided metadata about the file.
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

            response = self.api.upload_file(file=file_tuple, metadata=metadata)

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
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order: Optional[str] = None,
        sort: Optional[str] = None,
    ):
        """List available files.

        Args:
            status: Optional filter by file status ('processing', 'ready', 'failed').
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
                status=status, limit=limit, offset=offset, order=order, sort=sort
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


class Chat:
    """Chat namespace for the CloudGlue client."""

    def __init__(self, api):
        """Initialize with the API client."""
        self.api = api
        self.completions = Completions(api)
