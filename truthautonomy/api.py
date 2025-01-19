import json
from typing import Any, List, Optional
import cloudscraper
from .exceptions import TruthSocialAPIError
from .models import MediaResponse, PostResponse


class TruthSocial:
    API_URL = "https://truthsocial.com/api/v1/statuses"
    MEDIA_URL = "https://truthsocial.com/api/v1/media"

    def __init__(self, auth_bearer: str):
        if not auth_bearer:
            raise ValueError("Bearer token is required")
        self.headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Authorization": f"Bearer {auth_bearer}",
            "Origin": "https://truthsocial.com",
            "Referer": "https://truthsocial.com",
        }
        self.cfs = cloudscraper.create_scraper()

    def send_post(
        self,
        content: str,
        media_files: Optional[List[str]] = None,
        visibility: str = "public",
        **kwargs,
    ) -> PostResponse:
        """
        Sends a post to the TruthSocial API.

        Args:
            content (str): The text content of the post.
            media_files (Optional[List[str]]): List of file paths or media IDs to attach.
            visibility (str): Post visibility (e.g., "public", "private").

        Returns:
            PostResponse: Parsed response object for the created post.
        """
        media_ids = self._handle_media_upload(media_files)

        payload = {
            "status": content,
            "media_ids": media_ids,
            "visibility": visibility,
            "content_type": kwargs.get("content_type", "text/plain"),
            "in_reply_to_id": kwargs.get("in_reply_to_id"),
            "quote_id": kwargs.get("quote_id"),
            "poll": kwargs.get("poll"),
            "group_timeline_visible": kwargs.get("group_timeline_visible", False),
        }

        response = self.cfs.post(
            self.API_URL,
            headers={**self.headers, "Content-Type": "application/json"},
            json=payload,
        )

        if response.status_code != 200:
            raise TruthSocialAPIError(response.status_code, response.text)

        return PostResponse(response.json())

    def upload_media(self, file_path: str) -> MediaResponse:
        """
        Uploads a media file to the TruthSocial API.

        Args:
            file_path (str): The path to the media file.

        Returns:
            MediaResponse: Parsed response containing the media details.
        """
        with open(file_path, "rb") as file:
            files = {"file": file}
            response = self.cfs.post(self.MEDIA_URL, headers=self.headers, files=files)

        if response.status_code != 200:
            raise TruthSocialAPIError(response.status_code, response.text)

        return MediaResponse(response.json())

    def _handle_media_upload(self, media_files: Optional[List[str]]) -> List[int]:
        """
        Handles the upload of media files and collects their IDs.

        Args:
            media_files (Optional[List[str]]): List of file paths or media IDs.

        Returns:
            List[int]: List of media IDs.
        """
        media_ids = []
        if media_files:
            for media_file in media_files:
                if media_file.isdigit():
                    media_ids.append(int(media_file))
                else:
                    media_response = self.upload_media(media_file)
                    if media_response.id:
                        media_ids.append(media_response.id)
        return media_ids

    def print_response(self, response: Any):
        """
        Prints the parsed response in a user-friendly format.

        Args:
            response (Any): The parsed response object.
        """
        print(json.dumps(response.__dict__, indent=4))
