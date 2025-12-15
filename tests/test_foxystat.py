from foxypack_youtube_pytubefix import FoxyYouTubeAnalysis, YouTubeVideo, YouTubeChannel


def test_get_statistics_video_one_link_format():
    """Test case for getting statistics for a video"""
    youtube_stat = YouTubeVideo()
    youtube_stat_two = YouTubeVideo()
    youtube_analysis = FoxyYouTubeAnalysis().get_analysis(
        "https://www.youtube.com/watch?v=SNfrBPoHCTY"
    )
    stat_one = youtube_stat.get_statistics(youtube_analysis)
    stat_two = youtube_stat_two.get_statistics(youtube_analysis)
    assert stat_one.answer_id != stat_two.answer_id
    assert stat_one.system_id == stat_two.system_id
    assert stat_one.title == stat_two.title
    assert stat_one.views == stat_two.views
    assert stat_one.publish_date == stat_two.publish_date
    assert stat_one.analysis_status == stat_two.analysis_status
    assert stat_one.channel_id == stat_two.channel_id
    assert stat_one.likes == stat_two.likes
    assert stat_one.link == stat_two.link
    assert stat_one.channel_url == stat_two.channel_url
    assert stat_one.duration == stat_two.duration

def test_get_statistics_video_two_link_format():
    """Test case for getting statistics for a video"""
    youtube_stat = YouTubeVideo()
    youtube_stat_two = YouTubeVideo()
    youtube_analysis = FoxyYouTubeAnalysis().get_analysis(
        "https://youtu.be/PZHESOq-Gkw?t=376"
    )
    stat_one = youtube_stat.get_statistics(youtube_analysis)
    stat_two = youtube_stat_two.get_statistics(youtube_analysis)
    assert stat_one.answer_id != stat_two.answer_id
    assert stat_one.system_id == stat_two.system_id
    assert stat_one.title == stat_two.title
    assert stat_one.views == stat_two.views
    assert stat_one.publish_date == stat_two.publish_date
    assert stat_one.analysis_status == stat_two.analysis_status
    assert stat_one.channel_id == stat_two.channel_id
    assert stat_one.likes == stat_two.likes
    assert stat_one.link == stat_two.link
    assert stat_one.channel_url == stat_two.channel_url
    assert stat_one.duration == stat_two.duration

def test_get_statistics_video_three_link_format():
    """Test case for getting statistics for a video"""
    youtube_stat = YouTubeVideo()
    youtube_stat_two = YouTubeVideo()
    youtube_analysis = FoxyYouTubeAnalysis().get_analysis(
        "https://youtu.be/PZHESOq-Gkw"
    )
    stat_one = youtube_stat.get_statistics(youtube_analysis)
    stat_two = youtube_stat_two.get_statistics(youtube_analysis)
    assert stat_one.answer_id != stat_two.answer_id
    assert stat_one.system_id == stat_two.system_id
    assert stat_one.title == stat_two.title
    assert stat_one.views == stat_two.views
    assert stat_one.publish_date == stat_two.publish_date
    assert stat_one.analysis_status == stat_two.analysis_status
    assert stat_one.channel_id == stat_two.channel_id
    assert stat_one.likes == stat_two.likes
    assert stat_one.link == stat_two.link
    assert stat_one.channel_url == stat_two.channel_url
    assert stat_one.duration == stat_two.duration


def test_get_statistics_channel_foxy_stat():
    """Test case for getting statistics for a channel"""
    youtube_stat = YouTubeChannel()
    youtube_stat_two = YouTubeChannel()
    youtube_analysis = FoxyYouTubeAnalysis().get_analysis(
        "https://www.youtube.com/@KINOKOS"
    )
    stat_one = youtube_stat.get_statistics(youtube_analysis)
    stat_two = youtube_stat_two.get_statistics(youtube_analysis)
    assert stat_one.answer_id != stat_two.answer_id
    assert stat_one.title == stat_two.title
    assert stat_one.link == stat_two.link
    assert stat_one.description == stat_two.description
    assert stat_one.country == stat_two.country
    assert stat_one.system_id == stat_two.system_id
    assert stat_one.view_count == stat_two.view_count
    assert stat_one.subscribers == stat_two.subscribers
    assert stat_one.creation_date == stat_two.creation_date
    assert stat_one.number_videos == stat_two.number_videos
    assert stat_one.external_link == stat_two.external_link
    assert stat_one.analysis_status == stat_two.analysis_status

def test_get_statistics_channel_foxy_stat_two():
    """Test case for getting statistics for a channel"""
    youtube_stat = YouTubeChannel()
    youtube_stat_two = YouTubeChannel()
    youtube_analysis = FoxyYouTubeAnalysis().get_analysis(
        "https://www.youtube.com/channel/UCj2QqbeCUZ82JMk492iGUQg"
    )
    stat_one = youtube_stat.get_statistics(youtube_analysis)
    stat_two = youtube_stat_two.get_statistics(youtube_analysis)
    assert stat_one.answer_id != stat_two.answer_id
    assert stat_one.title == stat_two.title
    assert stat_one.link == stat_two.link
    assert stat_one.description == stat_two.description
    assert stat_one.country == stat_two.country
    assert stat_one.system_id == stat_two.system_id
    assert stat_one.view_count == stat_two.view_count
    assert stat_one.subscribers == stat_two.subscribers
    assert stat_one.creation_date == stat_two.creation_date
    assert stat_one.number_videos == stat_two.number_videos
    assert stat_one.external_link == stat_two.external_link
    assert stat_one.analysis_status == stat_two.analysis_status
