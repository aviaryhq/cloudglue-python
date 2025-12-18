# cloudglue/client/resources/segments.py
"""Segments resource for CloudGlue API."""
import time
from typing import Dict, Any, Optional, Union

from cloudglue.sdk.models.new_segments import NewSegments
from cloudglue.sdk.models.shot_config import ShotConfig
from cloudglue.sdk.models.narrative_config import NarrativeConfig
from cloudglue.sdk.models.segments import Segments as SegmentsModel
from cloudglue.sdk.models.segments_list import SegmentsList
from cloudglue.sdk.rest import ApiException

from cloudglue.client.resources.base import CloudGlueError


class Segments:
    """Client for the CloudGlue Segments API."""

    def __init__(self, api):
        """Initialize the Segments client.

        Args:
            api: The SegmentsApi instance.
        """
        self.api = api

    @staticmethod
    def create_shot_config(
        detector: str = "adaptive",
        max_duration_seconds: int = 300,
        min_duration_seconds: int = 1,
    ) -> ShotConfig:
        """Create a shot-based segmentation configuration.

        Args:
            detector: Detection algorithm ('adaptive' or 'content')
            max_duration_seconds: Maximum duration for each segment in seconds (1-3600)
            min_duration_seconds: Minimum duration for each segment in seconds (1-3600)

        Returns:
            ShotConfig object
        """
        return ShotConfig(
            detector=detector,
            max_duration_seconds=max_duration_seconds,
            min_duration_seconds=min_duration_seconds,
        )

    @staticmethod
    def create_narrative_config(
        prompt: Optional[str] = None,
        strategy: Optional[str] = None,
        number_of_chapters: Optional[int] = None,
        min_chapters: Optional[int] = None,
        max_chapters: Optional[int] = None,
    ) -> NarrativeConfig:
        """Create a narrative-based segmentation configuration.

        Args:
            prompt: Optional custom prompt to guide the narrative segmentation analysis.
                This will be incorporated into the main segmentation prompt as additional guidance.
            strategy: Optional narrative segmentation strategy. Options:
                - 'balanced': Uses multimodal describe job for comprehensive analysis.
                  Default strategy, recommended for most videos. Supports YouTube URLs.
                - 'comprehensive': Uses a VLM to deeply analyze logical segments of video.
                  Only available for non-YouTube videos.
                Note: YouTube URLs automatically use the 'balanced' strategy regardless of
                the strategy field value. The 'comprehensive' strategy is not supported for YouTube URLs.
            number_of_chapters: Optional target number of chapters to generate.
                If provided, the AI will attempt to generate exactly this number of chapters.
                Must be >= 1 if provided.
            min_chapters: Optional minimum number of chapters to generate.
                If provided, the AI will attempt to generate at least this number of chapters.
                Must be >= 1 if provided.
            max_chapters: Optional maximum number of chapters to generate.
                If provided, the AI will attempt to generate at most this number of chapters.
                Must be >= 1 if provided.
        Returns:
            NarrativeConfig object
        """
        return NarrativeConfig(
            prompt=prompt,
            strategy=strategy,
            number_of_chapters=number_of_chapters,
            min_chapters=min_chapters,
            max_chapters=max_chapters,
        )

    def create(
        self,
        url: str,
        criteria: str,
        shot_config: Optional[Union[ShotConfig, Dict[str, Any]]] = None,
        narrative_config: Optional[Union[NarrativeConfig, Dict[str, Any]]] = None,
    ) -> SegmentsModel:
        """Create a new segmentation job.

        Args:
            url: Input video URL. Supports URIs of files uploaded to Cloudglue Files endpoint,
                public HTTP URLs, S3 files, and other data connected URLs. **⚠️ Note: YouTube URLs are supported for 
                narrative-based segmentation only.** Shot-based segmentation requires direct 
                video file access.
            criteria: Segmentation criteria ('shot' or 'narrative')
            shot_config: Configuration for shot-based segmentation (only when criteria is 'shot')
            narrative_config: Configuration for narrative-based segmentation (only when criteria is 'narrative')

        Returns:
            Segments object representing the created job

        Raises:
            CloudGlueError: If the request fails
        """
        try:
            # Convert dict configs to objects if needed
            if isinstance(shot_config, dict):
                shot_config = ShotConfig(**shot_config)
            if isinstance(narrative_config, dict):
                narrative_config = NarrativeConfig(**narrative_config)

            new_segments = NewSegments(
                url=url,
                criteria=criteria,
                shot_config=shot_config,
                narrative_config=narrative_config,
            )

            response = self.api.create_segments(new_segments)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def get(self, job_id: str) -> SegmentsModel:
        """Get a segmentation job by ID.

        Args:
            job_id: The unique identifier of the segmentation job

        Returns:
            Segments object

        Raises:
            CloudGlueError: If the request fails
        """
        try:
            response = self.api.get_segments(job_id)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def list(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        status: Optional[str] = None,
        criteria: Optional[str] = None,
        created_before: Optional[str] = None,
        created_after: Optional[str] = None,
        url: Optional[str] = None,
    ) -> SegmentsList:
        """List segmentation jobs.

        Args:
            limit: Maximum number of segmentation jobs to return (max 100)
            offset: Number of segmentation jobs to skip
            status: Filter segmentation jobs by status
            criteria: Filter segmentation jobs by criteria type
            created_before: Filter segmentation jobs created before a specific date (YYYY-MM-DD format)
            created_after: Filter segmentation jobs created after a specific date (YYYY-MM-DD format)
            url: Filter segmentation jobs by the input URL used for segmentation

        Returns:
            SegmentsList object

        Raises:
            CloudGlueError: If the request fails
        """
        try:
            response = self.api.list_segments(
                limit=limit,
                offset=offset,
                status=status,
                criteria=criteria,
                created_before=created_before,
                created_after=created_after,
                url=url,
            )
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def delete(self, job_id: str):
        """Delete a segments job.

        Args:
            job_id: The ID of the segments job to delete

        Returns:
            The deletion confirmation

        Raises:
            CloudGlueError: If there is an error deleting the segments job.
        """
        try:
            response = self.api.delete_segments(job_id=job_id)
            return response
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

    def run(
        self,
        url: str,
        criteria: str,
        shot_config: Optional[Union[ShotConfig, Dict[str, Any]]] = None,
        narrative_config: Optional[Union[NarrativeConfig, Dict[str, Any]]] = None,
        poll_interval: int = 5,
        timeout: int = 600,
    ) -> SegmentsModel:
        """Create a segmentation job and wait for it to complete.

        Args:
            url: Input video URL. Supports URIs of files uploaded to Cloudglue Files endpoint,
                public HTTP URLs, S3 files, and other data connected URLs. **⚠️ Note: YouTube URLs are supported for 
                narrative-based segmentation only.** Shot-based segmentation requires direct 
                video file access.
            criteria: Segmentation criteria ('shot' or 'narrative')
            shot_config: Configuration for shot-based segmentation (only when criteria is 'shot')
            narrative_config: Configuration for narrative-based segmentation (only when criteria is 'narrative')
            poll_interval: How often to check the job status (in seconds).
            timeout: Maximum time to wait for the job to complete (in seconds).

        Returns:
            Segments: The completed Segments object with status and segments data.

        Raises:
            CloudGlueError: If there is an error creating or processing the segmentation job.
            TimeoutError: If the job does not complete within the specified timeout.
        """
        try:
            # Create the segmentation job
            job = self.create(
                url=url,
                criteria=criteria,
                shot_config=shot_config,
                narrative_config=narrative_config,
            )
            job_id = job.job_id

            # Poll for completion
            elapsed = 0
            while elapsed < timeout:
                status = self.get(job_id=job_id)

                if status.status in ["completed", "failed"]:
                    return status

                time.sleep(poll_interval)
                elapsed += poll_interval

            raise TimeoutError(
                f"Segmentation job did not complete within {timeout} seconds"
            )
        except ApiException as e:
            raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
        except Exception as e:
            raise CloudGlueError(str(e))

