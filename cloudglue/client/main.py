# cloudglue/client/main.py
from typing import Optional
import os

# Import from the generated SDK
from cloudglue.sdk.api.chat_api import ChatApi
from cloudglue.sdk.api.collections_api import CollectionsApi
from cloudglue.sdk.api.transcribe_api import TranscribeApi
from cloudglue.sdk.api.extract_api import ExtractApi
from cloudglue.sdk.api.files_api import FilesApi
from cloudglue.sdk.api.segmentations_api import SegmentationsApi
from cloudglue.sdk.api.search_api import SearchApi
from cloudglue.sdk.api.thumbnails_api import ThumbnailsApi
from cloudglue.sdk.configuration import Configuration
from cloudglue.sdk.api_client import ApiClient

# Import resource classes
from cloudglue.client.resources import Chat, Files, Transcribe, Extract, Collections, Segmentations, Search, Thumbnails
from cloudglue._version import __version__

# SDK client constants
SDK_CLIENT_NAME = "cloudglue-python"


class CloudGlue:
    """Main client for interacting with the CloudGlue API."""

    def __init__(
        self, api_key: Optional[str] = None, host: str = "https://api.cloudglue.dev/v1"
    ):
        """Initialize the CloudGlue client.

        Args:
            api_key: Your API key. If not provided, will try to use CLOUDGLUE_API_KEY env variable.
            host: API host to connect to.
        """
        self.api_key = api_key or os.environ.get("CLOUDGLUE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key must be provided either as an argument or via CLOUDGLUE_API_KEY environment variable"
            )

        # Set up configuration
        self.configuration = Configuration(host=host, access_token=self.api_key)
        self.api_client = ApiClient(self.configuration)
        
        # Set custom SDK headers
        self.api_client.set_default_header('x-sdk-client', SDK_CLIENT_NAME)
        self.api_client.set_default_header('x-sdk-version', __version__)

        # Initialize the specific API clients
        self.chat_api = ChatApi(self.api_client)
        self.collections_api = CollectionsApi(self.api_client)
        self.transcribe_api = TranscribeApi(self.api_client)
        self.extract_api = ExtractApi(self.api_client)
        self.files_api = FilesApi(self.api_client)
        self.segmentations_api = SegmentationsApi(self.api_client)
        self.search_api = SearchApi(self.api_client)
        self.thumbnails_api = ThumbnailsApi(self.api_client)

        # Set up resources with their respective API clients
        self.chat = Chat(self.chat_api)
        self.files = Files(self.files_api)
        self.transcribe = Transcribe(self.transcribe_api)
        self.extract = Extract(self.extract_api)
        self.collections = Collections(self.collections_api)
        self.segmentations = Segmentations(self.segmentations_api)
        self.search = Search(self.search_api)
        self.thumbnails = Thumbnails(self.thumbnails_api)

    def close(self):
        """Close the API client."""
        if hasattr(self, "api_client") and self.api_client:
            self.api_client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
