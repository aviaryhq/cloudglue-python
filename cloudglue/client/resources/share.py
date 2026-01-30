# cloudglue/client/resources/share.py
"""Share resource for CloudGlue API."""
from typing import Dict, Any, Optional

from cloudglue.sdk.models.create_shareable_asset_request import CreateShareableAssetRequest
from cloudglue.sdk.models.update_shareable_asset_request import UpdateShareableAssetRequest
from cloudglue.sdk.rest import ApiException

from cloudglue.client.resources.base import CloudGlueError


class Share:
    """Handles shareable asset operations for the CloudGlue API."""

    def __init__(self, api):
        """Initialize with the API client."""
        self.api = api

    def create(
        self,
        asset_type: str,
        asset_id: str,
        name: Optional[str] = None,
        expires_at: Optional[str] = None,
    ):
        """Create a publicly available shareable asset.

        Args:
            asset_type: The type of asset to share (e.g., 'file', 'collection').
            asset_id: The ID of the asset to share.
            name: Optional name for the shareable asset.
            expires_at: Optional expiration date (ISO 8601 format).

        Returns:
            ShareableAsset object with the public URL.

        Raises:
            CloudGlueError: If there is an error creating the shareable asset.
        """
        try:
            request = CreateShareableAssetRequest(
                asset_type=asset_type,
                asset_id=asset_id,
                name=name,
                expires_at=expires_at,
            )
            return self.api.create_shareable_asset(create_shareable_asset_request=request)
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def get(self, shareable_asset_id: str):
        """Get a specific shareable asset by ID.

        Args:
            shareable_asset_id: The ID of the shareable asset to retrieve.

        Returns:
            ShareableAsset object.

        Raises:
            CloudGlueError: If there is an error retrieving the shareable asset.
        """
        try:
            return self.api.get_shareable_asset(id=shareable_asset_id)
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def list(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        asset_type: Optional[str] = None,
        created_before: Optional[str] = None,
        created_after: Optional[str] = None,
    ):
        """List shareable assets with optional filtering.

        Args:
            limit: Maximum number of assets to return.
            offset: Number of assets to skip.
            asset_type: Filter by asset type.
            created_before: Filter by creation date (YYYY-MM-DD format, UTC).
            created_after: Filter by creation date (YYYY-MM-DD format, UTC).

        Returns:
            ShareableAssetListResponse object.

        Raises:
            CloudGlueError: If there is an error listing shareable assets.
        """
        try:
            return self.api.list_shareable_assets(
                limit=limit,
                offset=offset,
                asset_type=asset_type,
                created_before=created_before,
                created_after=created_after,
            )
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def update(
        self,
        shareable_asset_id: str,
        name: Optional[str] = None,
        expires_at: Optional[str] = None,
    ):
        """Update a shareable asset.

        Args:
            shareable_asset_id: The ID of the shareable asset to update.
            name: New name for the shareable asset.
            expires_at: New expiration date (ISO 8601 format).

        Returns:
            Updated ShareableAsset object.

        Raises:
            CloudGlueError: If there is an error updating the shareable asset.
        """
        try:
            request = UpdateShareableAssetRequest(
                name=name,
                expires_at=expires_at,
            )
            return self.api.update_shareable_asset(
                id=shareable_asset_id,
                update_shareable_asset_request=request,
            )
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def delete(self, shareable_asset_id: str):
        """Delete a shareable asset.

        Args:
            shareable_asset_id: The ID of the shareable asset to delete.

        Returns:
            Deletion confirmation.

        Raises:
            CloudGlueError: If there is an error deleting the shareable asset.
        """
        try:
            return self.api.delete_shareable_asset(id=shareable_asset_id)
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))
