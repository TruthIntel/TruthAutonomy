import json
import random
import time
from datetime import datetime, timezone
from typing import Any, Iterator, List, Optional

import cloudscraper
from dateutil.parser import parse as date_parse

from .exceptions import TruthSocialAPIError
from .models import MediaResponse, PostResponse
from .utils import logger


class TruthSocial:
    """Client to interact with the TruthSocial API."""

    BASE_URL = "https://truthsocial.com"

    def __init__(self, auth_bearer: str):
        """
        Initializes the TruthSocial client with an authorization bearer token.

        Args:
            auth_bearer (str): Bearer token for API authentication.

        Raises:
            ValueError: If the bearer token is not provided.
        """
        if not auth_bearer:
            raise ValueError("Bearer token is required")

        self.headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Authorization": f"Bearer {auth_bearer}",
            "Origin": self.BASE_URL,
            "Referer": self.BASE_URL,
        }
        self.cfs = cloudscraper.create_scraper()

    def _get_paginated(
        self, url: str, params: dict = None, resume: str = None
    ) -> Iterator:
        """
        Fetches paginated results for a given URL.

        Args:
            url (str): The URL to fetch.
            params (dict, optional): Additional query parameters.
            resume (str, optional): The pagination token to resume from.

        Yields:
            dict: Paginated API responses.
        """
        next_link = self.BASE_URL + url
        if resume:
            next_link += f"?max_id={resume}"

        while next_link:
            resp = self.cfs.get(url, params=params, headers=self.headers)
            link_header = resp.headers.get("Link", "")
            next_link = self._get_next_page_link(link_header)
            logger.info(f"Next: {next_link}, resp: {resp}, headers: {resp.headers}")
            yield resp.json()
            self._check_ratelimit(resp)

    def _check_ratelimit(self, response):
        """Checks rate limit headers and applies delay if necessary."""
        if "X-RateLimit-Remaining" in response.headers:
            remaining = int(response.headers["X-RateLimit-Remaining"])
            if remaining == 0:
                reset = int(response.headers["X-RateLimit-Reset"])
                delay = reset - int(time.time())
                logger.warning(f"Rate limit reached. Sleeping for {delay} seconds.")
                time.sleep(delay)

    def _get_next_page_link(self, link_header: str) -> Optional[str]:
        """
        Extracts the 'next' page link from pagination headers.

        Args:
            link_header (str): The 'Link' header value from the API response.

        Returns:
            Optional[str]: The next page URL or None.
        """
        next_link = None
        for link in link_header.split(","):
            parts = link.split(";")
            if len(parts) == 2 and parts[1].strip() == 'rel="next"':
                next_link = parts[0].strip("<>")
                break
        return next_link

    def _handle_media_upload(self, media_files: Optional[List[str]]) -> List[int]:
        """
        Handles media uploads and returns a list of media IDs.

        Args:
            media_files (Optional[List[str]]): List of media file paths to upload.

        Returns:
            List[int]: A list of media IDs.
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

    def user_likes(
        self, post: str, include_all: bool = False, top_num: int = 40
    ) -> Iterator:
        """
        Fetches the users who liked a post.

        Args:
            post (str): The post URL.
            include_all (bool, optional): If True, fetch all users who liked the post. Defaults to False.
            top_num (int, optional): The number of top users to return. Defaults to 40.

        Yields:
            dict: User information who liked the post.
        """
        post = post.split("/")[-1]
        top_num = max(1, int(top_num))
        n_output = 0
        for followers_batch in self._get_paginated(
            f"/api/v1/statuses/{post}/favourited_by", params={"limit": 80}
        ):
            for f in followers_batch:
                yield f
                n_output += 1
                if not include_all and n_output >= top_num:
                    return

    def user_followers(
        self,
        user_handle: str = None,
        user_id: str = None,
        maximum: int = 1000,
        resume: str = None,
    ) -> Iterator:
        """
        Fetches followers of a user with pagination.

        Args:
            user_handle (str, optional): The user handle.
            user_id (str, optional): The user ID.
            maximum (int, optional): The maximum number of followers to return. Defaults to 1000.
            resume (str, optional): The pagination token to resume from.

        Yields:
            dict: User information of followers.
        """
        assert user_handle or user_id, "Either user_handle or user_id must be provided"
        user_id = user_id or self.lookup(user_handle)["id"]
        return self._paginate_user_list(
            f"/api/v1/accounts/{user_id}/followers", resume, maximum
        )

    def user_following(
        self,
        user_handle: str = None,
        user_id: str = None,
        maximum: int = 1000,
        resume: str = None,
    ) -> Iterator:
        """
        Fetches users that a given user is following.

        Args:
            user_handle (str, optional): The user handle.
            user_id (str, optional): The user ID.
            maximum (int, optional): The maximum number of following users to return. Defaults to 1000.
            resume (str, optional): The pagination token to resume from.

        Yields:
            dict: User information of following users.
        """
        assert user_handle or user_id, "Either user_handle or user_id must be provided"
        user_id = user_id or self.lookup(user_handle)["id"]
        return self._paginate_user_list(
            f"/api/v1/accounts/{user_id}/following", resume, maximum
        )

    def _paginate_user_list(self, url: str, resume: str, maximum: int) -> Iterator:
        """
        Helper method to paginate user lists.

        Args:
            url (str): The URL for the user list.
            resume (str): The pagination token to resume from.
            maximum (int): The maximum number of users to return.

        Yields:
            dict: User information.
        """
        n_output = 0
        for followers_batch in self._get_paginated(url, resume=resume):
            for f in followers_batch:
                yield f
                n_output += 1
                if n_output >= maximum:
                    return

    def lookup(self, user_handle: str = None) -> Optional[dict]:
        """
        Lookup a user's information.

        Args:
            user_handle (str): The user handle.

        Returns:
            Optional[dict]: The user's information.
        """
        assert user_handle
        return self._get(
            f"/api/v1/accounts/lookup", params={"acct": user_handle.removeprefix("@")}
        )

    def send_post(
        self,
        content: str,
        media_files: Optional[List[str]] = None,
        visibility: str = "public",
        **kwargs,
    ) -> PostResponse:
        """
        Sends a post with optional media to the API.

        Args:
            content (str): The content of the post.
            media_files (Optional[List[str]], optional): List of media file paths to attach to the post. Defaults to None.
            visibility (str, optional): The visibility of the post. Defaults to 'public'.
            **kwargs: Additional parameters for the post.

        Returns:
            PostResponse: The response containing the post's details.
        """
        media_ids = self._handle_media_upload(media_files)
        payload = self._build_post_payload(content, media_ids, visibility, **kwargs)
        response = self.cfs.post(
            self.BASE_URL + "/api/v1/statuses",
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
            file_path (str): Path to the media file.

        Returns:
            MediaResponse: The response containing the uploaded media details.
        """
        with open(file_path, "rb") as file:
            files = {"file": file}
            response = self.cfs.post(
                self.BASE_URL + "/api/v1/media", headers=self.headers, files=files
            )

        if response.status_code != 200:
            raise TruthSocialAPIError(response.status_code, response.text)

        return MediaResponse(response.json())

    def _build_post_payload(self, content, media_ids, visibility, **kwargs):
        """
        Constructs the payload for the post request.

        Args:
            content (str): The content of the post.
            media_ids (List[int]): List of media IDs attached to the post.
            visibility (str): The visibility of the post.
            **kwargs: Additional parameters for the post.

        Returns:
            dict: The payload for the post request.
        """
        return {
            "status": content,
            "media_ids": media_ids,
            "visibility": visibility,
            "content_type": kwargs.get("content_type", "text/plain"),
            "in_reply_to_id": kwargs.get("in_reply_to_id"),
            "quote_id": kwargs.get("quote_id"),
            "poll": kwargs.get("poll"),
            "group_timeline_visible": kwargs.get("group_timeline_visible", False),
        }

    def random_interactions(self):
        """
        Simulates random user interactions like likes, follows, and reads.
        """
        interactions = ["like", "follow", "read"]
        action = random.choice(interactions)

        if action == "like":
            logger.info("User liked a post!")
        elif action == "follow":
            logger.info("User followed a profile!")
        elif action == "read":
            logger.info("User read a post!")

    def random_trending_tags(self) -> dict:
        """
        Simulates random trending tags.

        Returns:
            dict: Dictionary containing random trending tags.
        """
        return {"trending_tags": [f"#{random.choice(['fun', 'news', 'tech', 'life'])}"]}

    def random_suggestions(self) -> dict:
        """
        Simulates random suggested users or groups.

        Returns:
            dict: Dictionary with suggested users and groups.
        """
        return {
            "suggested_users": [f"User{random.randint(1, 100)}" for _ in range(5)],
            "suggested_groups": [f"Group{random.randint(1, 100)}" for _ in range(3)],
        }

    def trending(self, limit=10):
        """
        Fetches trending posts.

        Args:
            limit (int, optional): The number of trending posts to return. Defaults to 10.

        Returns:
            dict: The trending posts.
        """
        return self._get(f"/api/v1/trends?limit={limit}")

    def tags(self):
        """
        Fetches trending tags.

        Returns:
            dict: The trending tags.
        """
        return self._get("/api/v1/trends")

    def suggested(self, maximum: int = 50) -> dict:
        """
        Fetches suggested users to follow.

        Args:
            maximum (int, optional): The maximum number of users to suggest. Defaults to 50.

        Returns:
            dict: Suggested users.
        """
        return self._get(f"/api/v2/suggestions?limit={maximum}")

    def group_tags(self):
        """
        Fetches trending group tags.

        Returns:
            dict: The trending group tags.
        """
        return self._get("/api/v1/groups/tags")

    def group_posts(self, group_id: str, limit=20):
        """
        Fetches posts from a specific group.

        Args:
            group_id (str): The ID of the group.
            limit (int, optional): The number of posts to return. Defaults to 20.

        Returns:
            dict: Posts from the group.
        """
        return self._get(f"/api/v1/groups/{group_id}/posts", params={"limit": limit})

    def _get(self, url: str, params: Optional[dict] = None) -> Any:
        """
        Helper method to perform GET requests.

        Args:
            url (str): The endpoint URL.
            params (dict, optional): The query parameters for the request.

        Returns:
            Any: The response object.
        """
        return self.cfs.get(
            self.BASE_URL + url, params=params, headers=self.headers
        ).json()

    def pull_statuses(
        self,
        username: str,
        replies: bool = False,
        verbose: bool = False,
        created_after: datetime = None,
        since_id: Optional[str] = None,
        pinned: bool = False,
    ) -> Iterator[dict]:
        params = {}
        user_id = self.lookup(username)["id"]
        page_counter = 0
        keep_going = True

        while keep_going:
            try:
                url = f"/api/v1/accounts/{user_id}/statuses"
                if pinned:
                    url += "?pinned=true&with_muted=true"
                elif not replies:
                    url += "?exclude_replies=true"
                if verbose:
                    logger.debug(f"{url} {params}")
                result = self._get(url, params=params)
                page_counter += 1
            except json.JSONDecodeError as e:
                logger.error(f"Unable to pull user #{user_id}'s statuses: {e}")
                break
            except Exception as e:
                logger.error(f"Error while pulling statuses for user #{user_id}: {e}")
                break

            if "error" in result or not result:
                logger.error(f"Error pulling statuses for user #{user_id}: {result}")
                break

            posts = sorted(result, key=lambda k: k["id"], reverse=True)
            params["max_id"] = posts[-1]["id"]

            if pinned:
                keep_going = False

            for post in posts:
                post["_pulled"] = datetime.now().isoformat()
                post_at = date_parse.parse(post["created_at"]).replace(
                    tzinfo=timezone.utc
                )
                if (created_after and post_at <= created_after) or (
                    since_id and post["id"] <= since_id
                ):
                    keep_going = False
                    break
                if verbose:
                    logger.debug(f"{post['id']} {post['created_at']}")
                yield post

    def pull_comments(
        self,
        post: str,
        include_all: bool = False,
        only_first: bool = False,
        top_num: int = 40,
    ) -> Iterator[dict]:
        post = post.split("/")[-1]
        n_output = 0
        for comments_batch in self._get_paginated(
            f"/api/v1/statuses/{post}/context/descendants",
            params=dict(sort="oldest"),
        ):
            for comment in comments_batch:
                if (only_first and comment["in_reply_to_id"] == post) or not only_first:
                    yield comment
                    n_output += 1
                    if not include_all and n_output >= top_num:
                        return

    def search(
        self,
        query: str,
        searchtype: str = "",
        limit: int = 40,
        resolve: bool = True,
        offset: int = 0,
        min_id: str = "0",
        max_id: Optional[str] = None,
    ) -> Iterator[dict]:
        """
        searchtype can be accounts|statuses|hashtags|groups
        """
        while offset < limit:
            params = {
                "q": query,
                "resolve": resolve,
                "limit": limit,
                "type": searchtype,
                "offset": offset,
                "min_id": min_id,
                "max_id": max_id,
            }
            resp = self._get("/api/v2/search", params=params)
            offset += limit
            if not resp or all(not value for value in resp.values()):
                break
            yield resp
