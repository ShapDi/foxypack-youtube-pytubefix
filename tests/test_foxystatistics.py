import datetime
from types import SimpleNamespace

import pytest

from foxypack.exceptions import UnsupportedOperationError
from foxypack_youtube_pytubefix import FoxyYouTubeAnalysis, YouTubeChannel, YouTubeVideo
from foxypack_youtube_pytubefix.answers import (
    ExternalLink,
    HeavyYouTubeChannelAnswersStatistics,
    HeavyYoutubeVideoAnswersStatistics,
    YouTubeChannelAnswersStatistics,
    YoutubeVideoAnswersStatistics,
)
from foxypack_youtube_pytubefix.exceptions import YouTubeDataExtractionError
from foxypack_youtube_pytubefix.foxystatistics import Convert


@pytest.fixture
def analyzer() -> FoxyYouTubeAnalysis:
    return FoxyYouTubeAnalysis()


@pytest.fixture
def video_analysis(analyzer: FoxyYouTubeAnalysis):
    return analyzer.get_analysis("https://www.youtube.com/watch?v=SNfrBPoHCTY")


@pytest.fixture
def shorts_analysis(analyzer: FoxyYouTubeAnalysis):
    return analyzer.get_analysis("https://www.youtube.com/shorts/J-m4POZFGyM")


@pytest.fixture
def channel_analysis_handle(analyzer: FoxyYouTubeAnalysis):
    return analyzer.get_analysis("https://www.youtube.com/@KINOKOS")


@pytest.fixture
def fake_video_object():
    return SimpleNamespace(
        title="Test Video",
        watch_url="https://youtube.com/watch?v=SNfrBPoHCTY",
        channel_id="UC_VIDEO_CHANNEL",
        views=123456,
        video_id="SNfrBPoHCTY",
        channel_url="https://www.youtube.com/channel/UC_VIDEO_CHANNEL",
        publish_date=datetime.datetime(2024, 1, 15, 10, 30, 0),
        length=321,
        initial_data="like this video along with 4,321 other people",
    )


@pytest.fixture
def fake_channel_object():
    return SimpleNamespace(
        channel_name="Test Channel",
        channel_url="https://www.youtube.com/channel/UC_CHANNEL_ID",
        description="Test channel description",
        channel_id="UC_CHANNEL_ID",
        about_html="<html></html>",
    )


@pytest.mark.unit
@pytest.mark.statistics
def test_get_statistics_video_returns_expected_fields(
    monkeypatch, video_analysis, fake_video_object
):
    youtube_stat = YouTubeVideo()
    monkeypatch.setattr(
        youtube_stat, "get_object_youtube", lambda link: fake_video_object
    )

    stat = youtube_stat.get_statistics(video_analysis)
    assert isinstance(stat, YoutubeVideoAnswersStatistics)
    assert stat.title == "Test Video"
    assert stat.likes == 4321
    assert stat.link == "https://youtube.com/watch?v=SNfrBPoHCTY"
    assert stat.channel_id == "UC_VIDEO_CHANNEL"
    assert stat.views == 123456
    assert stat.system_id == "SNfrBPoHCTY"
    assert stat.channel_url == "https://www.youtube.com/channel/UC_VIDEO_CHANNEL"
    assert stat.publish_date == datetime.date(2024, 1, 15)
    assert stat.duration == 321
    assert stat.analysis_status == video_analysis


@pytest.mark.unit
@pytest.mark.statistics
def test_get_statistics_video_heavy_returns_heavy_answer(
    monkeypatch, video_analysis, fake_video_object
):
    youtube_stat = YouTubeVideo(heavy_answers=True)
    monkeypatch.setattr(
        youtube_stat, "get_object_youtube", lambda link: fake_video_object
    )

    stat = youtube_stat.get_statistics(video_analysis)

    assert isinstance(stat, HeavyYoutubeVideoAnswersStatistics)
    assert stat.pytube_ob is fake_video_object
    assert stat.system_id == "SNfrBPoHCTY"


@pytest.mark.unit
@pytest.mark.statistics
@pytest.mark.asyncio
async def test_get_statistics_video_async_returns_expected_fields(
    monkeypatch, video_analysis, fake_video_object
):
    youtube_stat = YouTubeVideo()
    monkeypatch.setattr(
        youtube_stat, "get_object_youtube", lambda link: fake_video_object
    )

    stat = await youtube_stat.get_statistics_async(video_analysis)

    assert isinstance(stat, YoutubeVideoAnswersStatistics)
    assert stat.system_id == "SNfrBPoHCTY"
    assert stat.title == "Test Video"
    assert stat.likes == 4321


@pytest.mark.unit
@pytest.mark.statistics
def test_get_statistics_video_supports_shorts(
    monkeypatch, shorts_analysis, fake_video_object
):
    youtube_stat = YouTubeVideo()
    monkeypatch.setattr(
        youtube_stat, "get_object_youtube", lambda link: fake_video_object
    )

    stat = youtube_stat.get_statistics(shorts_analysis)

    assert isinstance(stat, YoutubeVideoAnswersStatistics)
    assert stat.system_id == "SNfrBPoHCTY"


@pytest.mark.unit
@pytest.mark.statistics
def test_get_statistics_video_invalid_analysis_type_raises(channel_analysis_handle):
    youtube_stat = YouTubeVideo()

    with pytest.raises(UnsupportedOperationError):
        youtube_stat.get_statistics(channel_analysis_handle)


@pytest.mark.unit
@pytest.mark.statistics
def test_get_like_num_returns_none_when_no_match():
    fake_video = SimpleNamespace(initial_data="no likes text here")
    assert YouTubeVideo.get_like_num(fake_video) is None


@pytest.mark.unit
@pytest.mark.statistics
def test_get_like_num_returns_none_for_invalid_number():
    fake_video = SimpleNamespace(
        initial_data="like this video along with not_a_number other people"
    )
    assert YouTubeVideo.get_like_num(fake_video) is None


@pytest.mark.unit
@pytest.mark.statistics
def test_get_statistics_video_raises_data_extraction_error(monkeypatch, video_analysis):
    youtube_stat = YouTubeVideo()
    broken_video_object = SimpleNamespace(
        title="Broken Video",
        initial_data="like this video along with 1 other people",
    )
    monkeypatch.setattr(
        youtube_stat, "get_object_youtube", lambda link: broken_video_object
    )

    with pytest.raises(YouTubeDataExtractionError):
        youtube_stat.get_statistics(video_analysis)


@pytest.mark.unit
@pytest.mark.statistics
def test_get_statistics_channel_returns_expected_fields(
    monkeypatch, channel_analysis_handle, fake_channel_object
):
    youtube_stat = YouTubeChannel()

    monkeypatch.setattr(
        youtube_stat, "get_object_youtube", lambda link: fake_channel_object
    )
    monkeypatch.setattr(youtube_stat, "get_country", lambda obj: "Japan")
    monkeypatch.setattr(youtube_stat, "get_view_count", lambda obj: 987654)
    monkeypatch.setattr(youtube_stat, "get_subscriber", lambda obj: 150000)
    monkeypatch.setattr(
        youtube_stat, "get_data_create", lambda obj: datetime.date(2020, 3, 15)
    )
    monkeypatch.setattr(youtube_stat, "get_number_videos", lambda obj: 120)
    monkeypatch.setattr(
        youtube_stat,
        "get_external_links",
        lambda obj: [ExternalLink(title="Website", link="https://example.com")],
    )

    stat = youtube_stat.get_statistics(channel_analysis_handle)

    assert isinstance(stat, YouTubeChannelAnswersStatistics)
    assert stat.title == "Test Channel"
    assert stat.link == "https://www.youtube.com/channel/UC_CHANNEL_ID"
    assert stat.description == "Test channel description"
    assert stat.country == "Japan"
    assert stat.system_id == "UC_CHANNEL_ID"
    assert stat.view_count == 987654
    assert stat.subscribers == 150000
    assert stat.creation_date == datetime.date(2020, 3, 15)
    assert stat.number_videos == 120
    assert stat.external_link == [
        ExternalLink(title="Website", link="https://example.com")
    ]
    assert stat.analysis_status == channel_analysis_handle


@pytest.mark.unit
@pytest.mark.statistics
def test_get_statistics_channel_heavy_returns_heavy_answer(
    monkeypatch, channel_analysis_handle, fake_channel_object
):
    youtube_stat = YouTubeChannel(heavy_answers=True)

    monkeypatch.setattr(
        youtube_stat, "get_object_youtube", lambda link: fake_channel_object
    )
    monkeypatch.setattr(youtube_stat, "get_country", lambda obj: "Japan")
    monkeypatch.setattr(youtube_stat, "get_view_count", lambda obj: 987654)
    monkeypatch.setattr(youtube_stat, "get_subscriber", lambda obj: 150000)
    monkeypatch.setattr(
        youtube_stat, "get_data_create", lambda obj: datetime.date(2020, 3, 15)
    )
    monkeypatch.setattr(youtube_stat, "get_number_videos", lambda obj: 120)
    monkeypatch.setattr(youtube_stat, "get_external_links", lambda obj: [])

    stat = youtube_stat.get_statistics(channel_analysis_handle)

    assert isinstance(stat, HeavyYouTubeChannelAnswersStatistics)
    assert stat.pytube_ob is fake_channel_object
    assert stat.system_id == "UC_CHANNEL_ID"


@pytest.mark.unit
@pytest.mark.statistics
@pytest.mark.asyncio
async def test_get_statistics_channel_async_returns_expected_fields(
    monkeypatch, channel_analysis_handle, fake_channel_object
):
    youtube_stat = YouTubeChannel()

    monkeypatch.setattr(
        youtube_stat, "get_object_youtube", lambda link: fake_channel_object
    )
    monkeypatch.setattr(youtube_stat, "get_country", lambda obj: "Japan")
    monkeypatch.setattr(youtube_stat, "get_view_count", lambda obj: 987654)
    monkeypatch.setattr(youtube_stat, "get_subscriber", lambda obj: 150000)
    monkeypatch.setattr(
        youtube_stat, "get_data_create", lambda obj: datetime.date(2020, 3, 15)
    )
    monkeypatch.setattr(youtube_stat, "get_number_videos", lambda obj: 120)
    monkeypatch.setattr(youtube_stat, "get_external_links", lambda obj: [])

    stat = await youtube_stat.get_statistics_async(channel_analysis_handle)

    assert isinstance(stat, YouTubeChannelAnswersStatistics)
    assert stat.system_id == "UC_CHANNEL_ID"
    assert stat.title == "Test Channel"


@pytest.mark.unit
@pytest.mark.statistics
def test_get_statistics_channel_invalid_analysis_type_raises(video_analysis):
    youtube_stat = YouTubeChannel()

    with pytest.raises(UnsupportedOperationError):
        youtube_stat.get_statistics(video_analysis)


@pytest.mark.unit
@pytest.mark.statistics
def test_get_statistics_channel_raises_data_extraction_error(
    monkeypatch, channel_analysis_handle
):
    youtube_stat = YouTubeChannel()
    broken_channel_object = SimpleNamespace(
        channel_name="Broken Channel",
        channel_url="https://www.youtube.com/channel/BROKEN",
    )
    monkeypatch.setattr(
        youtube_stat, "get_object_youtube", lambda link: broken_channel_object
    )

    with pytest.raises(YouTubeDataExtractionError):
        youtube_stat.get_statistics(channel_analysis_handle)


@pytest.mark.unit
@pytest.mark.statistics
def test_transform_youtube_channel_link_handle():
    transformed = YouTubeChannel.transform_youtube_channel_link(
        "https://www.youtube.com/@KINOKOS"
    )
    assert transformed == "https://www.youtube.com/c/KINOKOS/videos"


@pytest.mark.unit
@pytest.mark.statistics
def test_transform_youtube_channel_link_channel_id_keeps_original():
    original = "https://www.youtube.com/channel/UCj2QqbeCUZ82JMk492iGUQg"
    transformed = YouTubeChannel.transform_youtube_channel_link(original)
    assert transformed == original


@pytest.mark.unit
@pytest.mark.statistics
@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("1,234 views", 1234),
        ("999 views", 999),
        (None, 0),
        ("invalid", 0),
    ],
)
def test_convert_views_to_int(value, expected):
    assert Convert.convert_views_to_int(value) == expected


@pytest.mark.unit
@pytest.mark.statistics
@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("1.5K subscribers", 1500),
        ("2M subscribers", 2000000),
        ("999 subscribers", 999),
        (None, 0),
        ("invalid", 0),
    ],
)
def test_convert_subscribers_to_int(value, expected):
    assert Convert.convert_subscribers_to_int(value) == expected


@pytest.mark.unit
@pytest.mark.statistics
@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("123 videos", 123),
        ("1,234 videos", 1234),
        (None, 0),
        ("invalid", 0),
    ],
)
def test_convert_number_videos(value, expected):
    assert Convert.convert_number_videos(value) == expected


@pytest.mark.unit
@pytest.mark.statistics
@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("Joined Mar 15, 2020", datetime.date(2020, 3, 15)),
        (None, None),
        ("invalid", None),
    ],
)
def test_convert_data_create(value, expected):
    assert Convert.convert_data_create(value) == expected
