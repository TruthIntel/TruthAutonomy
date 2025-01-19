class TruthSocialAPIError(Exception):
    """Custom exception for TruthSocial API errors."""

    def __init__(self, status_code: int, message: str):
        super().__init__(f"HTTP {status_code}: {message}")
        self.status_code = status_code
        self.message = message
