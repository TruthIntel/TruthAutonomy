from typing import Any, Dict, List, Optional


class MediaResponse:
    """Represents the response for a media upload."""

    def __init__(self, data: Dict[str, Any]):
        self.id: Optional[int] = data.get("id")
        self.type: Optional[str] = data.get("type")
        self.url: Optional[str] = data.get("url")
        self.preview_url: Optional[str] = data.get("preview_url")
        self.text_url: Optional[str] = data.get("text_url")
        self.meta: Optional[Dict[str, Any]] = data.get("meta")


class PostResponse:
    """Represents the response for a post creation."""

    def __init__(self, data: Dict[str, Any]):
        self.id: Optional[int] = data.get("id")
        self.created_at: Optional[str] = data.get("created_at")
        self.content: Optional[str] = data.get("content")
        self.visibility: Optional[str] = data.get("visibility")
        self.url: Optional[str] = data.get("url")
        self.replies_count: Optional[int] = data.get("replies_count")
        self.reblogs_count: Optional[int] = data.get("reblogs_count")
        self.favourites_count: Optional[int] = data.get("favourites_count")
        self.application: Optional[str] = data.get("application", {}).get("name")
        self.tags: List[str] = [tag.get("name") for tag in data.get("tags", [])]
        account_data = data.get("account", {})
        self.account: Dict[str, Any] = {
            "username": account_data.get("username"),
            "id": account_data.get("id"),
            "url": account_data.get("url"),
            "created_at": account_data.get("created_at"),
            "statuses_count": account_data.get("statuses_count"),
        }
