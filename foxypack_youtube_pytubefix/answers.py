from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List

from pytubefix import YouTube, Channel

from foxypack.foxypack_abc.answers import (
    AnswersSocialContainer,
    AnswersAnalysis,
    AnswersSocialContent,
)


class YouTubeEnum(Enum):
    shorts = "shorts"
    video = "video"
    channel = "channel"


@dataclass(slots=True, kw_only=True)
class YoutubeAnswersAnalysis(AnswersAnalysis):
    code: str

    def __post_init__(self) -> None:
        super().__post_init__()

        if not self.code or not self.code.strip():
            raise ValueError("code must not be empty")


@dataclass(slots=True, kw_only=True)
class YoutubeVideoAnswersStatistics(AnswersSocialContent):
    channel_id: str
    likes: int
    link: str
    channel_url: str
    duration: int

    def __post_init__(self) -> None:
        super().__post_init__()

        if not self.channel_id.strip():
            raise ValueError("channel_id must not be empty")

        if self.likes < 0:
            raise ValueError("likes must be >= 0")

        if self.duration < 0:
            raise ValueError("duration must be >= 0")

        if not self.link.strip():
            raise ValueError("link must not be empty")

        if not self.channel_url.strip():
            raise ValueError("channel_url must not be empty")


@dataclass(slots=True, kw_only=True)
class HeavyYoutubeVideoAnswersStatistics(YoutubeVideoAnswersStatistics):
    pytube_ob: YouTube


@dataclass(slots=True, kw_only=True)
class ExternalLink:
    title: str
    link: str

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("title must not be empty")

        if not self.link.strip():
            raise ValueError("link must not be empty")


@dataclass(slots=True, kw_only=True)
class YouTubeChannelAnswersStatistics(AnswersSocialContainer):
    link: str
    description: str
    country: str
    view_count: int
    number_videos: int
    external_link: List[ExternalLink] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__post_init__()

        if not self.link.strip():
            raise ValueError("link must not be empty")

        if self.view_count < 0:
            raise ValueError("view_count must be >= 0")

        if self.number_videos < 0:
            raise ValueError("number_videos must be >= 0")


@dataclass(slots=True, kw_only=True)
class HeavyYouTubeChannelAnswersStatistics(YouTubeChannelAnswersStatistics):
    pytube_ob: Channel
