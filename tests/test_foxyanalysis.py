import pytest
from foxypack_youtube_pytubefix import FoxyYouTubeAnalysis


@pytest.fixture(scope="session")
def content_analyzer():
    return FoxyYouTubeAnalysis()


@pytest.mark.analysis
def test_youtube_video_type_link_two(content_analyzer):
    analysis = content_analyzer.get_analysis("https://youtu.be/GhXMLM7vUJI2")
    analysis_two = content_analyzer.get_analysis("https://youtu.be/GhXMLM7vUJI2")
    assert analysis.answer_id != analysis_two.answer_id
    assert analysis.url == "https://youtube.com/watch?v=GhXMLM7vUJI2"
    assert analysis.social_platform == "youtube"
    assert analysis.type_content == "video"
    assert analysis.code == "GhXMLM7vUJI2"


@pytest.mark.analysis
def test_youtube_video_type_link_thee(content_analyzer):
    analysis = content_analyzer.get_analysis(
        "https://www.youtube.com/shorts/J-m4POZFGyM"
    )
    analysis_two = content_analyzer.get_analysis(
        "https://www.youtube.com/shorts/J-m4POZFGyM"
    )
    assert analysis.answer_id != analysis_two.answer_id
    assert analysis.url == "https://youtube.com/watch?v=J-m4POZFGyM"
    assert analysis.social_platform == "youtube"
    assert analysis.type_content == "shorts"
    assert analysis.code == "J-m4POZFGyM"


@pytest.mark.analysis
def test_youtube_video_type_link_four(content_analyzer):
    analysis = content_analyzer.get_analysis(
        "https://www.youtube.com/watch?v=M4HCrPSU0C0?start=92.40&end=96.30"
    )
    analysis_two = content_analyzer.get_analysis(
        "https://www.youtube.com/watch?v=M4HCrPSU0C0?start=92.40&end=96.30"
    )
    assert analysis.answer_id != analysis_two.answer_id
    assert analysis.url == "https://youtube.com/watch?v=M4HCrPSU0C0"
    assert analysis.social_platform == "youtube"
    assert analysis.type_content == "video"
    assert analysis.code == "M4HCrPSU0C0"


@pytest.mark.analysis
def test_youtube_channel_type_link_one(content_analyzer):
    analysis = content_analyzer.get_analysis("https://www.youtube.com/@AgnamoN")
    analysis_two = content_analyzer.get_analysis("https://www.youtube.com/@AgnamoN")
    assert analysis.answer_id != analysis_two.answer_id
    assert analysis.url == "https://www.youtube.com/@AgnamoN"
    assert analysis.social_platform == "youtube"
    assert analysis.type_content == "channel"
    assert analysis.code == "AgnamoN"


@pytest.mark.analysis
def test_youtube_channel_type_link_two(content_analyzer):
    analysis = content_analyzer.get_analysis(
        "https://www.youtube.com/channel/UC5C088kVlcF5ras7cBbdWxw"
    )
    analysis_two = content_analyzer.get_analysis(
        "https://www.youtube.com/channel/UC5C088kVlcF5ras7cBbdWxw"
    )
    assert analysis.answer_id != analysis_two.answer_id
    assert analysis.url == "https://www.youtube.com/channel/UC5C088kVlcF5ras7cBbdWxw"
    assert analysis.social_platform == "youtube"
    assert analysis.type_content == "channel"
    assert analysis.code == "UC5C088kVlcF5ras7cBbdWxw"
