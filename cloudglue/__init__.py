# cloudglue/__init__.py

from cloudglue._version import __version__

# Import and re-export the client
from cloudglue.client.main import CloudGlue
from cloudglue.client.resources import CloudGlueError

# Re-export key models from the SDK
from cloudglue.sdk.models.chat_completion_request import ChatCompletionRequest
from cloudglue.sdk.models.chat_completion_response import ChatCompletionResponse
from cloudglue.sdk.models.chat_completion_request_filter import ChatCompletionRequestFilter
from cloudglue.sdk.models.chat_completion_request_filter_metadata_inner import ChatCompletionRequestFilterMetadataInner
from cloudglue.sdk.models.chat_completion_request_filter_video_info_inner import ChatCompletionRequestFilterVideoInfoInner
from cloudglue.sdk.models.chat_completion_request_filter_file_inner import ChatCompletionRequestFilterFileInner
from cloudglue.sdk.models.file_update import FileUpdate

# Export key classes at the module level for clean imports
__all__ = [
    "CloudGlue",
    "ChatCompletionRequest",
    "ChatCompletionResponse",
    "ChatCompletionRequestFilter",
    "ChatCompletionRequestFilterMetadataInner",
    "ChatCompletionRequestFilterVideoInfoInner",
    "ChatCompletionRequestFilterFileInner",
    "FileUpdate",
    "CloudGlueError",
]
