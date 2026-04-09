import urllib.parse
from dataclasses import dataclass

from typing_extensions import override

from foxypack import FoxyAnalysis
from foxypack_youtube_pytubefix.answers import YoutubeAnswersAnalysis
from foxypack_youtube_pytubefix.enums import YouTubeHostEnum, YouTubeEnum
from foxypack_youtube_pytubefix.exceptions import UnsupportedYouTubeUrlError


@dataclass(frozen=True)
class ParsedYouTubeLink:
    clean_url: str
    code: str
    type_content: str


class FoxyYouTubeAnalysis(FoxyAnalysis):
    """YouTube URL analyzer for videos, shorts and channels."""

    @staticmethod
    def _normalize_netloc(netloc: str) -> str:
        return netloc.lower().strip()

    @classmethod
    def _is_youtube_host(cls, netloc: str) -> bool:
        return YouTubeHostEnum.is_youtube_host(netloc)

    @classmethod
    def _parse_url(cls, link: str) -> ParsedYouTubeLink:
        parsed_url = urllib.parse.urlparse(link)
        netloc = cls._normalize_netloc(parsed_url.netloc)
        path = parsed_url.path or ""
        query = urllib.parse.parse_qs(parsed_url.query)

        if not parsed_url.scheme or not netloc:
            raise UnsupportedYouTubeUrlError(link)

        if not cls._is_youtube_host(netloc):
            raise UnsupportedYouTubeUrlError(link)

        if netloc in {
            YouTubeHostEnum.YOU_TUBE.value,
            YouTubeHostEnum.WWW_YOUTU_BE.value,
        }:
            video_id = path.strip("/").split("/")[0]
            if not video_id:
                raise UnsupportedYouTubeUrlError(link)

            return ParsedYouTubeLink(
                clean_url=f"https://youtube.com/watch?v={video_id}",
                code=video_id,
                type_content=YouTubeEnum.video.value,
            )

        if path == "/watch":
            video_id_list = query.get("v")
            if not video_id_list or not video_id_list[0]:
                raise UnsupportedYouTubeUrlError(link)

            video_id = video_id_list[0].split("?", 1)[0]
            return ParsedYouTubeLink(
                clean_url=f"https://youtube.com/watch?v={video_id}",
                code=video_id,
                type_content=YouTubeEnum.video.value,
            )

        if path.startswith("/shorts/"):
            short_id = path.split("/shorts/", 1)[1].split("/", 1)[0].split("?", 1)[0]
            if not short_id:
                raise UnsupportedYouTubeUrlError(link)

            return ParsedYouTubeLink(
                clean_url=f"https://youtube.com/watch?v={short_id}",
                code=short_id,
                type_content=YouTubeEnum.shorts.value,
            )

        if path.startswith("/@"):
            handle = path.split("/@", 1)[1].split("/", 1)[0].strip()
            if not handle:
                raise UnsupportedYouTubeUrlError(link)

            return ParsedYouTubeLink(
                clean_url=f"https://www.youtube.com/@{handle}",
                code=handle,
                type_content=YouTubeEnum.channel.value,
            )

        if path.startswith("/channel/"):
            channel_id = path.split("/channel/", 1)[1].split("/", 1)[0].strip()
            if not channel_id:
                raise UnsupportedYouTubeUrlError(link)

            return ParsedYouTubeLink(
                clean_url=f"https://www.youtube.com/channel/{channel_id}",
                code=channel_id,
                type_content=YouTubeEnum.channel.value,
            )

        raise UnsupportedYouTubeUrlError(link)

    @classmethod
    def get_code(cls, link: str) -> str:
        return cls._parse_url(link).code

    @classmethod
    def clean_link(cls, link: str) -> str:
        return cls._parse_url(link).clean_url

    @classmethod
    def get_type_content(cls, link: str) -> str:
        return cls._parse_url(link).type_content

    @override
    def get_analysis(self, url: str) -> YoutubeAnswersAnalysis:
        parsed = self._parse_url(url)
        return YoutubeAnswersAnalysis(
            url=parsed.clean_url,
            social_platform="youtube",
            type_content=parsed.type_content,
            code=parsed.code,
        )
