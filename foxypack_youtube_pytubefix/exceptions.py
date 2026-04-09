from foxypack.exceptions import FoxyError


class YouTubeAnalysisError(FoxyError):
    """Base exception for foxypack_youtube_pytubefix."""


class UnsupportedYouTubeUrlError(YouTubeAnalysisError):
    """Raised when the URL is not a supported YouTube video/channel URL."""

    def __init__(self, url: str) -> None:
        super().__init__(
            message="Unsupported YouTube URL",
            details={"url": url},
        )
