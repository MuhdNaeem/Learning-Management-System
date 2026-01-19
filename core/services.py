"""
YouTube Service module for generating secure embed URLs.

This module handles YouTube video embedding with access control.
Videos should be uploaded as "Unlisted" on YouTube, and access
is controlled through the LMS backend enrollment system.
"""
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class YouTubeService:
    """
    Service class for YouTube video operations.
    Generates secure embed URLs for YouTube videos with access control.
    """
    
    def __init__(self):
        """Initialize YouTube service."""
        self.embed_domain = getattr(settings, 'YOUTUBE_EMBED_DOMAIN', None)
    
    def get_embed_url(self, video_id, autoplay=False, controls=True, modestbranding=True):
        """
        Generate YouTube embed URL for a video.
        
        Args:
            video_id (str): YouTube video ID (e.g., "dQw4w9WgXcQ")
            autoplay (bool): Whether to autoplay the video. Default: False
            controls (bool): Whether to show video controls. Default: True
            modestbranding (bool): Reduce YouTube branding. Default: True
        
        Returns:
            str: YouTube embed URL
        
        Raises:
            ValueError: If video_id is empty or invalid.
        """
        if not video_id:
            raise ValueError("video_id cannot be empty")
        
        # Clean video_id (extract ID from full URL if provided)
        video_id = self._extract_video_id(video_id)
        
        if not video_id:
            raise ValueError("Invalid YouTube video ID")
        
        # Build embed URL
        base_url = "https://www.youtube.com/embed/"
        params = []
        
        if not autoplay:
            params.append("autoplay=0")
        else:
            params.append("autoplay=1")
        
        if not controls:
            params.append("controls=0")
        
        if modestbranding:
            params.append("modestbranding=1")
        
        # Add domain restriction if configured
        if self.embed_domain:
            params.append(f"origin={self.embed_domain}")
        
        # Add privacy-enhanced mode
        params.append("rel=0")  # Don't show related videos from other channels
        
        query_string = "&".join(params) if params else ""
        embed_url = f"{base_url}{video_id}"
        
        if query_string:
            embed_url = f"{embed_url}?{query_string}"
        
        logger.info(f"Generated YouTube embed URL for video: {video_id}")
        return embed_url
    
    def get_watch_url(self, video_id):
        """
        Get YouTube watch URL (for reference, not for embedding).
        
        Args:
            video_id (str): YouTube video ID
        
        Returns:
            str: YouTube watch URL
        """
        video_id = self._extract_video_id(video_id)
        return f"https://www.youtube.com/watch?v={video_id}"
    
    def _extract_video_id(self, video_id_or_url):
        """
        Extract YouTube video ID from various URL formats or return as-is if already an ID.
        
        Supports:
        - https://www.youtube.com/watch?v=VIDEO_ID
        - https://youtu.be/VIDEO_ID
        - https://www.youtube.com/embed/VIDEO_ID
        - VIDEO_ID (if already just the ID)
        
        Args:
            video_id_or_url (str): YouTube URL or video ID
        
        Returns:
            str: Extracted video ID
        """
        if not video_id_or_url:
            return None
        
        # If it's already just an ID (no special characters except alphanumeric, dash, underscore)
        if len(video_id_or_url) <= 20 and all(c.isalnum() or c in ['-', '_'] for c in video_id_or_url):
            return video_id_or_url
        
        # Try to extract from various URL formats
        import re
        
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]{11})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, video_id_or_url)
            if match:
                return match.group(1)
        
        # If no pattern matches, return as-is (might be invalid)
        return video_id_or_url
    
    def validate_video_id(self, video_id):
        """
        Validate YouTube video ID format.
        
        Args:
            video_id (str): Video ID to validate
        
        Returns:
            bool: True if valid format, False otherwise
        """
        if not video_id:
            return False
        
        # Extract ID if it's a URL
        video_id = self._extract_video_id(video_id)
        
        # YouTube video IDs are typically 11 characters (alphanumeric, dash, underscore)
        if len(video_id) == 11 and all(c.isalnum() or c in ['-', '_'] for c in video_id):
            return True
        
        return False


# Singleton instance
_youtube_service = None


def get_youtube_service():
    """
    Get or create the YouTube service singleton instance.
    
    Returns:
        YouTubeService: The YouTube service instance
    """
    global _youtube_service
    if _youtube_service is None:
        _youtube_service = YouTubeService()
    return _youtube_service
