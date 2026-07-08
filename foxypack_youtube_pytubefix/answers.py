from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from pytubefix import YouTube, Channel

from foxypack.foxypack_abc.answers import (
    AnswersSocialContainer,
    AnswersAnalysis,
    AnswersSocialContent,
)


@dataclass(slots=True, kw_only=True)
class YoutubeAnswersAnalysis(AnswersAnalysis):
    code: str


@dataclass(slots=True, kw_only=True)
class YoutubeVideoAnswersStatistics(AnswersSocialContent):
    channel_id: str
    likes: int
    link: str
    channel_url: str
    duration: int


@dataclass(slots=True, kw_only=True)
class HeavyYoutubeVideoAnswersStatistics(YoutubeVideoAnswersStatistics):
    pytube_ob: YouTube


@dataclass(slots=True, kw_only=True)
class ExternalLink:
    title: str
    link: str


@dataclass(slots=True, kw_only=True)
class YouTubeChannelAnswersStatistics(AnswersSocialContainer):
    link: str
    description: str
    country: str
    view_count: int
    number_videos: int
    external_link: List[ExternalLink] = field(default_factory=list)


@dataclass(slots=True, kw_only=True)
class HeavyYouTubeChannelAnswersStatistics(YouTubeChannelAnswersStatistics):
    pytube_ob: Channel
