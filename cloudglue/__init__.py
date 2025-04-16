# cloudglue/__init__.py

# Import and re-export the client
from cloudglue.client.main import CloudGlue
from cloudglue.client.resources import CloudGlueError

# Re-export key models from the SDK
from cloudglue.sdk.models.chat_completion_request import ChatCompletionRequest
from cloudglue.sdk.models.chat_completion_response import ChatCompletionResponse

# Define version
__version__ = "0.0.9"

# Export key classes at the module level for clean imports
__all__ = [
    "CloudGlue",
    "ChatCompletionRequest",
    "ChatCompletionResponse",
    "CloudGlueError",
]
