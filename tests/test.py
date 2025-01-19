import unittest
from unittest.mock import MagicMock, mock_open, patch

from truthautonomy import MediaResponse, PostResponse, TruthSocial, TruthSocialAPIError


class TestTruthSocial(unittest.TestCase):
    def setUp(self):
        """Set up reusable test variables."""
        self.auth_bearer = "test_bearer_token"
        self.api = TruthSocial(auth_bearer=self.auth_bearer)

    def test_initialization(self):
        """Test initialization with and without an auth token."""
        with self.assertRaises(ValueError):
            TruthSocial(auth_bearer="")
        self.assertEqual(
            self.api.headers["Authorization"], f"Bearer {self.auth_bearer}"
        )

    @patch("truthautonomy.TruthSocial.cfs.post")
    def test_send_post(self, mock_post):
        """Test sending a post with valid data."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 1,
            "content": "Hello, TruthSocial!",
            "visibility": "public",
            "url": "https://example.com/post/1",
        }
        mock_post.return_value = mock_response

        response = self.api.send_post(content="Hello, TruthSocial!")
        self.assertIsInstance(response, PostResponse)
        self.assertEqual(response.content, "Hello, TruthSocial!")
        self.assertEqual(response.visibility, "public")

    @patch("truthautonomy.TruthSocial.cfs.post")
    def test_send_post_failure(self, mock_post):
        """Test sending a post with an API error."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response

        with self.assertRaises(TruthSocialAPIError) as context:
            self.api.send_post(content="Invalid Content")
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.message, "Bad Request")

    @patch("truthautonomy.TruthSocial.cfs.post")
    @patch("builtins.open", new_callable=mock_open, read_data="mock data")
    def test_upload_media(self, mock_open_file, mock_post):
        """Test uploading a media file."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 123,
            "type": "image",
            "url": "https://example.com/media/123",
        }
        mock_post.return_value = mock_response

        response = self.api.upload_media("path/to/mock_file.jpg")
        self.assertIsInstance(response, MediaResponse)
        self.assertEqual(response.id, 123)
        self.assertEqual(response.url, "https://example.com/media/123")

    @patch("truthautonomy.TruthSocial.cfs.post")
    @patch("builtins.open", new_callable=mock_open, read_data="mock data")
    def test_upload_media_failure(self, mock_open_file, mock_post):
        """Test uploading a media file with an API error."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Invalid Media"
        mock_post.return_value = mock_response

        with self.assertRaises(TruthSocialAPIError) as context:
            self.api.upload_media("path/to/invalid_file.jpg")
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.message, "Invalid Media")


if __name__ == "__main__":
    unittest.main()
