"""Backward-compatible imports for the historical misspelled module name."""

from .services.oss import get_signed_video_url, get_video_url, get_video_url2

__all__ = ["get_signed_video_url", "get_video_url", "get_video_url2"]
