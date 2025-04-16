# cloudglue/client/__init__.py

from cloudglue.client.main import CloudGlue
from cloudglue.client.resources import CloudGlueError

__all__ = ["CloudGlue", "CloudGlueError"]
