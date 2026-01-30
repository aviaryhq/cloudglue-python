# cloudglue/client/resources/responses.py
"""Responses resource for CloudGlue API."""
from typing import List, Dict, Any, Optional

from cloudglue.sdk.models.create_response_request import CreateResponseRequest
from cloudglue.sdk.rest import ApiException

from cloudglue.client.resources.base import CloudGlueError


class Responses:
    """Handles response operations for the CloudGlue API."""

    def __init__(self, api):
        """Initialize with the API client."""
        self.api = api

    def create(
        self,
        input: List[Dict[str, Any]],
        model: str = "nimbus-001",
        knowledge_bases: Optional[List[Dict[str, Any]]] = None,
        background: Optional[bool] = None,
        **kwargs,
    ):
        """Create a new response.

        Args:
            input: List of input messages with role and content.
            model: The model to use for the response.
            knowledge_bases: List of knowledge base configurations to search.
            background: Whether to run in background mode.
            **kwargs: Additional parameters for the request.

        Returns:
            The Response object.

        Raises:
            CloudGlueError: If there is an error creating the response.
        """
        try:
            request = CreateResponseRequest(
                input=input,
                model=model,
                knowledge_bases=knowledge_bases,
                background=background,
                **kwargs,
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
