import datetime

import pytest

from foxypack_youtube_pytubefix import FoxyYouTubeAnalysis, YouTubeChannel, YouTubeVideo
from foxypack_youtube_pytubefix.answers import (
    YouTubeChannelAnswersStatistics,
    YoutubeVideoAnswersStatistics,
)


@pytest.fixture(scope="module")
def analyzer() -> FoxyYouTubeAnalysis:
    return FoxyYouTubeAnalysis()


@pytest.mark.integration
@pytest.mark.statistics
def test_video_statistics_real_watch_url(analyzer: FoxyYouTubeAnalysis):
    youtube_stat = YouTubeVideo()
    youtube_analysis = analyzer.get_analysis(
        "https://www.youtube.com/watch?v=SNfrBPoHCTY"
    )

    stat = youtube_stat.get_statistics(youtube_analysis)
    assert isinstance(stat, YoutubeVideoAnswersStatistics)
    assert stat.system_id
    assert stat.title
    assert isinstance(stat.views, int)
    assert stat.views >= 0
    assert stat.channel_id
    assert stat.link.startswith("https://")
    assert stat.channel_url.startswith("https://")
    assert isinstance(stat.duration, int)
    assert stat.duration >= 0
    assert stat.publish_date is None or isinstance(stat.publish_date, datetime.date)


@pytest.mark.integration
@pytest.mark.statistics
def test_video_statistics_real_short_url(analyzer: FoxyYouTubeAnalysis):
    youtube_stat = YouTubeVideo()
    youtube_analysis = analyzer.get_analysis("https://youtu.be/PZHESOq-Gkw")

    stat = youtube_stat.get_statistics(youtube_analysis)

    assert isinstance(stat, YoutubeVideoAnswersStatistics)
    assert stat.system_id
    assert stat.title
    assert isinstance(stat.views, int)
    assert stat.views >= 0


@pytest.mark.integration
@pytest.mark.statistics
def test_channel_statistics_real_handle_url(analyzer: FoxyYouTubeAnalysis):
    youtube_stat = YouTubeChannel()
    youtube_analysis = analyzer.get_analysis("https://www.youtube.com/@KINOKOS")

    stat = youtube_stat.get_statistics(youtube_analysis)

    assert isinstance(stat, YouTubeChannelAnswersStatistics)
    assert stat.title
    assert stat.link.startswith("https://")
    assert stat.system_id
    assert isinstance(stat.view_count, int)
    assert stat.view_count >= 0
    assert isinstance(stat.subscribers, int)
    assert stat.subscribers >= 0
    assert isinstance(stat.number_videos, int)
    assert stat.number_videos >= 0
    assert stat.creation_date is None or isinstance(stat.creation_date, datetime.date)
    assert isinstance(stat.external_link, list)


@pytest.mark.integration
@pytest.mark.statistics
def test_channel_statistics_real_channel_id_url(analyzer: FoxyYouTubeAnalysis):
    youtube_stat = YouTubeChannel()
    youtube_analysis = analyzer.get_analysis(
        "https://www.youtube.com/channel/UCj2QqbeCUZ82JMk492iGUQg"
    )

    stat = youtube_stat.get_statistics(youtube_analysis)
    assert isinstance(stat, YouTubeChannelAnswersStatistics)
    assert stat.title
    assert stat.system_id
    assert isinstance(stat.subscribers, int)
    assert stat.subscribers >= 0