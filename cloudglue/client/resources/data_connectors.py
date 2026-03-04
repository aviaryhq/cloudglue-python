# cloudglue/client/resources/data_connectors.py
"""Data Connectors resource for Cloudglue API."""
from typing import Optional

from cloudglue.sdk.rest import ApiException

from cloudglue.client.resources.base import CloudglueError


class DataConnectors:
    """Client for the Cloudglue Data Connectors API."""

    def __init__(self, api):
        """Initialize the DataConnectors client.

        Args:
            api: The DataConnectorsApi instance.
        """
        self.api = api

    def list(self):
        """List all active data connectors configured for your account.

        Returns:
            DataConnectorList object

        Raises:
            CloudglueError: If there is an error listing data connectors.
        """
        try:
            return self.api.list_data_connectors()
        except ApiException as e:
            raise CloudglueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudglueError(str(e))
