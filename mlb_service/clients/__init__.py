"""clients package — exports get_mlb_client() factory."""

from .mlb_client import MLBClient, get_mlb_client

__all__ = ["MLBClient", "get_mlb_client"]
