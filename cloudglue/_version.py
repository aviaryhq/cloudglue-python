# cloudglue/_version.py
"""Version management for the cloudglue package."""

import importlib.metadata


def get_version():
    """Get version from package metadata."""
    try:
        return importlib.metadata.version("cloudglue")
    except importlib.metadata.PackageNotFoundError:
        # Fallback version if package metadata is not available
        return "0.1.3"


__version__ = get_version()
