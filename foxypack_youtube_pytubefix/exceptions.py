import socket
from typing import Any

import pytubefix.exceptions as pytubefix_exceptions

from foxypack.exceptions import (
    CollectionError,
    ContentBlockedError,
    ContentNotFoundError,
    ContentPrivateError,
    ContentRegionRestrictedError,
    FoxyError,
    ServiceUnavailableError,
    TimeoutError as FoxyTimeoutError,
)


class YouTubeAnalysisError(FoxyError):
    """Base exception for foxypack_youtube_pytubefix."""


class UnsupportedYouTubeUrlError(YouTubeAnalysisError):
    """Raised when the URL is not a supported YouTube video/channel URL."""

    def __init__(self, url: str) -> None:
        super().__init__(
            message="Unsupported YouTube URL",
            details={"url": url},
        )


class YouTubeStatisticsError(CollectionError):
    """Base exception for statistics collection in foxypack_youtube_pytubefix."""


class YouTubeDataExtractionError(YouTubeStatisticsError):
    """Raised when pytubefix object exists, but required fields cannot be extracted."""


def _build_pytubefix_exception_groups() -> dict[str, tuple[type[BaseException], ...]]:
    """
    Build exception groups dynamically to stay compatible with different pytubefix versions.
    """
    names = [
        "VideoUnavailable",
        "VideoPrivate",
        "VideoRegionBlocked",
        "MembersOnly",
        "RecordingUnavailable",
        "BotDetection",
        "AgeRestrictedError",
        "LiveStreamError",
        "RegexMatchError",
        "ExtractError",
        "HTMLParseError",
    ]

    resolved: dict[str, type[BaseException]] = {}
    for name in names:
        exc = getattr(pytubefix_exceptions, name, None)
        if isinstance(exc, type) and issubclass(exc, BaseException):
            resolved[name] = exc

    def pick(*exc_names: str) -> tuple[type[BaseException], ...]:
        return tuple(resolved[name] for name in exc_names if name in resolved)

    return {
        "private": pick("VideoPrivate", "MembersOnly", "AgeRestrictedError"),
        "region": pick("VideoRegionBlocked"),
        "not_found": pick("RecordingUnavailable"),
        "blocked": pick("BotDetection"),
        "parse": pick("RegexMatchError", "ExtractError", "HTMLParseError"),
        "service": pick("LiveStreamError"),
        "generic_unavailable": pick("VideoUnavailable"),
    }


_PYTUBEFIX_EXCEPTION_GROUPS = _build_pytubefix_exception_groups()


def map_pytubefix_exception(
    exc: Exception,
    *,
    url: str,
    platform: str = "youtube",
    content_id: str | None = None,
) -> FoxyError:
    """
    Map pytubefix/native exceptions to Foxy exceptions.
    """
    private_group = _PYTUBEFIX_EXCEPTION_GROUPS["private"]
    region_group = _PYTUBEFIX_EXCEPTION_GROUPS["region"]
    not_found_group = _PYTUBEFIX_EXCEPTION_GROUPS["not_found"]
    blocked_group = _PYTUBEFIX_EXCEPTION_GROUPS["blocked"]
    parse_group = _PYTUBEFIX_EXCEPTION_GROUPS["parse"]
    service_group = _PYTUBEFIX_EXCEPTION_GROUPS["service"]
    generic_unavailable_group = _PYTUBEFIX_EXCEPTION_GROUPS["generic_unavailable"]

    base_details: dict[str, Any] = {
        "url": url,
        "platform": platform,
    }
    if content_id is not None:
        base_details["content_id"] = content_id

    if private_group and isinstance(exc, private_group):
        return ContentPrivateError(
            message="YouTube content is private or requires authentication",
            url=url,
            platform=platform,
            content_id=content_id,
            cause=exc,
        )

    if region_group and isinstance(exc, region_group):
        return ContentRegionRestrictedError(
            message="YouTube content is region-restricted",
            url=url,
            platform=platform,
            content_id=content_id,
            cause=exc,
        )

    if not_found_group and isinstance(exc, not_found_group):
        return ContentNotFoundError(
            message="YouTube content is unavailable or removed",
            url=url,
            platform=platform,
            content_id=content_id,
            cause=exc,
        )

    if blocked_group and isinstance(exc, blocked_group):
        return ContentBlockedError(
            message="YouTube blocked access to the content",
            details=base_details,
            cause=exc,
        )

    if parse_group and isinstance(exc, parse_group):
        return ServiceUnavailableError(
            message="pytubefix could not parse YouTube response",
            details=base_details,
            cause=exc,
        )

    if service_group and isinstance(exc, service_group):
        return ServiceUnavailableError(
            message="YouTube service is temporarily unavailable for this content",
            details=base_details,
            cause=exc,
        )

    if generic_unavailable_group and isinstance(exc, generic_unavailable_group):
        return ContentNotFoundError(
            message="YouTube content is unavailable",
            url=url,
            platform=platform,
            content_id=content_id,
            cause=exc,
        )

    if isinstance(exc, socket.timeout):
        return FoxyTimeoutError(
            details=base_details,
            cause=exc,
        )

    if isinstance(exc, TimeoutError):
        return FoxyTimeoutError(
            details=base_details,
            cause=exc,
        )

    return ServiceUnavailableError(
        message="Unexpected error while collecting YouTube data",
        details=base_details,
        cause=exc,
    )
