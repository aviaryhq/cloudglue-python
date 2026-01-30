# cloudglue/client/resources/responses.py
"""Responses resource for CloudGlue API."""
from typing import List, Dict, Any, Optional, Union

from cloudglue.sdk.models.create_response_request import CreateResponseRequest
from cloudglue.sdk.models.response_knowledge_base import ResponseKnowledgeBase
from cloudglue.sdk.rest import ApiException

from cloudglue.client.resources.base import CloudGlueError


class Responses:
    """Handles response operations for the CloudGlue API."""

    def __init__(self, api):
        """Initialize with the API client."""
        self.api = api

    def create(
        self,
        input: Union[str, List[Dict[str, Any]]],
        collections: List[str],
        model: str = "nimbus-001",
        instructions: Optional[str] = None,
        temperature: Optional[float] = None,
        background: Optional[bool] = None,
        include: Optional[List[str]] = None,
    ):
        """Create a new response.

        Args:
            input: The input for the response. Can be a simple string (treated as user message)
                or a list of message dicts with 'role' and 'content' keys.
            collections: List of collection IDs to search for relevant context.
            model: The model to use for the response (default: 'nimbus-001').
            instructions: Optional system instructions to guide the model's behavior.
            temperature: Sampling temperature for the model (0-2, default: 0.7).
            background: Set to True to process the response in the background.
            include: Additional data to include in the response annotations.

        Returns:
            The Response object.

        Raises:
            CloudGlueError: If there is an error creating the response.
        """
        try:
            knowledge_base = ResponseKnowledgeBase(collections=collections)
            request = CreateResponseRequest(
                input=input,
                model=model,
                knowledge_base=knowledge_base,
                instructions=instructions,
                temperature=temperature,
                background=background,
                include=include,
            )
            return self.api.create_response(create_response_request=request)
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def get(self, response_id: str):
        """Get a specific response by ID.

        Args:
            response_id: The ID of the response to retrieve.

        Returns:
            The Response object.

        Raises:
            CloudGlueError: If there is an error retrieving the response.
        """
        try:
            return self.api.get_response(id=response_id)
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
    ):
        """List responses with optional filtering.

        Args:
            limit: Maximum number of responses to return.
            offset: Number of responses to skip.
            status: Filter by status.
            created_before: Filter by creation date (YYYY-MM-DD format, UTC).
            created_after: Filter by creation date (YYYY-MM-DD format, UTC).

        Returns:
            ResponseList object containing responses.

        Raises:
            CloudGlueError: If there is an error listing responses.
        """
        try:
            return self.api.list_responses(
                limit=limit,
                offset=offset,
                status=status,
                created_before=created_before,
                created_after=created_after,
            )
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def delete(self, response_id: str):
        """Delete a response.

        Args:
            response_id: The ID of the response to delete.

        Returns:
            Deletion confirmation.

        Raises:
            CloudGlueError: If there is an error deleting the response.
        """
        try:
            return self.api.delete_response(id=response_id)
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def cancel(self, response_id: str):
        """Cancel a background response that is in progress.

        Args:
            response_id: The ID of the response to cancel.

        Returns:
            The Response object (may be completed, failed, or cancelled).

        Raises:
            CloudGlueError: If there is an error cancelling the response.
        """
        try:
            return self.api.cancel_response(id=response_id)
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))
