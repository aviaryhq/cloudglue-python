# cloudglue/client/resources/base.py
"""Base classes and exceptions for Cloudglue resources."""
from typing import Dict, Any


class CloudglueError(Exception):
    """Base exception for Cloudglue errors."""

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
        super(CloudglueError, self).__init__(self.message)

