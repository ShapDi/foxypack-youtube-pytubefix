import uuid
from enum import Enum
from typing import List

from foxypack.foxypack_abc.answers import (
    AnswersSocialContainer,
    AnswersAnalysis,
    AnswersSocialContent,
)
from pydantic import BaseModel, Field
from pytubefix import YouTube, Channel


class YouTubeEnum(Enum):
    shorts = "shorts"
    video = "video"
    channel = "channel"


class YoutubeAnswersAnalysis(AnswersAnalysis):
    code: str


class YoutubeVideoAnswersStatistics(AnswersSocialContent):
    channel_id: str
    likes: int
    link: str
    channel_url: str
    duration: int


class HeavyYoutubeVideoAnswersStatistics(YoutubeVideoAnswersStatistics):
    pytube_ob: YouTube

    model_config = {"arbitrary_types_allowed": True}


class ExternalLink(BaseModel):
    title: str
    link: str


class YouTubeChannelAnswersStatistics(AnswersSocialContainer):
    link: str
    description: str
    country: str
    view_count: int
    number_videos: int
    external_link: List[ExternalLink]


class HeavyYouTubeChannelAnswersStatistics(YouTubeChannelAnswersStatistics):
    pytube_ob: Channel

    model_config = {"arbitrary_types_allowed": True}
