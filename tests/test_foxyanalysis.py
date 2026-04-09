import pytest

from foxypack_youtube_pytubefix import FoxyYouTubeAnalysis
from foxypack_youtube_pytubefix.exceptions import UnsupportedYouTubeUrlError


@pytest.fixture(scope="session")
def analyzer() -> FoxyYouTubeAnalysis:
    return FoxyYouTubeAnalysis()


@pytest.mark.analysis
@pytest.mark.parametrize(
    ("url", "clean_url", "type_content", "code"),
    [
        (
            "https://youtu.be/GhXMLM7vUJI2",
            "https://youtube.com/watch?v=GhXMLM7vUJI2",
            "video",
            "GhXMLM7vUJI2",
        ),
        (
            "https://www.youtube.com/shorts/J-m4POZFGyM",
            "https://youtube.com/watch?v=J-m4POZFGyM",
            "shorts",
            "J-m4POZFGyM",
        ),
        (
            "https://www.youtube.com/watch?v=M4HCrPSU0C0",
            "https://youtube.com/watch?v=M4HCrPSU0C0",
            "video",
            "M4HCrPSU0C0",
        ),
        (
            "https://www.youtube.com/@AgnamoN",
            "https://www.youtube.com/@AgnamoN",
            "channel",
            "AgnamoN",
        ),
        (
            "https://www.youtube.com/channel/UC5C088kVlcF5ras7cBbdWxw",
            "https://www.youtube.com/channel/UC5C088kVlcF5ras7cBbdWxw",
            "channel",
            "UC5C088kVlcF5ras7cBbdWxw",
        ),
    ],
)
def test_get_analysis_success(analyzer, url, clean_url, type_content, code):
    analysis = analyzer.get_analysis(url)

    assert analysis.url == clean_url
    assert analysis.social_platform == "youtube"
    assert analysis.type_content == type_content
    assert analysis.code == code


@pytest.mark.analysis
@pytest.mark.parametrize(
    "url",
    [
        "https://example.com/watch?v=GhXMLM7vUJI2",
        "https://www.youtube.com/",
        "https://www.youtube.com/watch",
        "https://www.youtube.com/shorts/",
        "https://www.youtube.com/@",
        "https://www.youtube.com/channel/",
        "",
        "not_a_url",
    ],
)
def test_get_analysis_invalid_url(analyzer, url):
    with pytest.raises(UnsupportedYouTubeUrlError):
        analyzer.get_analysis(url)


@pytest.mark.analysis
def test_youtube_analysis_normalizes_host_case(analyzer):
    analysis = analyzer.get_analysis("https://YouTuBe.com/watch?v=M4HCrPSU0C0")

    assert analysis.url == "https://youtube.com/watch?v=M4HCrPSU0C0"
    assert analysis.type_content == "video"
    assert analysis.code == "M4HCrPSU0C0"
