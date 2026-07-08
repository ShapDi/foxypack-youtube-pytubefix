from datetime import date
from types import SimpleNamespace
from unittest.mock import patch

from foxypack.foxypack_abc.answers import AnswersAnalysis
from foxypack_youtube_pytubefix.answers import YoutubeVideoAnswersStatistics
from foxypack_youtube_pytubefix.foxysearch import FoxySearchKeyWord


@patch("foxypack_youtube_pytubefix.foxysearch.Search")
@patch.object(FoxySearchKeyWord, "_build_filter")
def test_get_search_result(mock_build_filter, mock_search):
    mock_filter = object()
    mock_build_filter.return_value = mock_filter

    mock_video = SimpleNamespace(
        video_id="abc123",
        title="Funny cats",
        views=123456,
        publish_date=date(2025, 1, 1),
        channel_id="channel-1",
        likes=100,
        watch_url="https://youtube.com/watch?v=abc123",
        channel_url="https://youtube.com/@cats",
        length=120,
    )

    mock_search.return_value.videos = [mock_video]

    search = FoxySearchKeyWord(upload_date="today")

    result = search.get_search_result("cats")

    mock_search.assert_called_once_with(
        query="cats",
        filters=mock_filter,
    )

    assert len(result) == 1

    video = result[0]
    print(video)
    assert isinstance(video, YoutubeVideoAnswersStatistics)
    assert video.system_id == "abc123"
    assert video.title == "Funny cats"
    assert video.views == 123456
    assert video.publish_date == date(2025, 1, 1)
    assert video.channel_id == "channel-1"
    assert video.likes == 100
    assert video.link == "https://youtube.com/watch?v=abc123"
    assert video.channel_url == "https://youtube.com/@cats"
    assert video.duration == 120