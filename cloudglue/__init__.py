# cloudglue/__init__.py

import os
import re
from pathlib import Path


def _get_version():
    """Get version from pyproject.toml."""
    try:
        # Find pyproject.toml in the package root
        package_root = Path(__file__).parent.parent
        pyproject_path = package_root / "pyproject.toml"
        
        if pyproject_path.exists():
            with open(pyproject_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Extract version using regex
                match = re.search(r'^version\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
                if match:
                    return match.group(1)
    except Exception:
        pass
    
    # Fallback version if reading from pyproject.toml fails
    return "0.1.2"


# Define version dynamically from pyproject.toml
__version__ = _get_version()

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
