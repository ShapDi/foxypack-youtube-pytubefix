from foxypack_youtube_pytubefix import FoxyYouTubeAnalysis, YouTubeVideo


def test_get_statistics_video_foxy_stat():
    """Test case for getting statistics for a video"""
    youtube_stat = YouTubeVideo()
    youtube_stat_two = YouTubeVideo()
    youtube_analysis = FoxyYouTubeAnalysis().get_analysis('https://www.youtube.com/watch?v=SNfrBPoHCTY')
    stat_one = youtube_stat.get_statistics(youtube_analysis)
    stat_two = youtube_stat_two.get_statistics(youtube_analysis)
    assert stat_one.answer_id != stat_two.answer_id
    assert stat_one.system_id == stat_two.system_id
    assert stat_one.title == stat_two.title
    assert stat_one.views == stat_two.views
    assert stat_one.publish_date == stat_two.publish_date
    assert stat_one.analysis_status == stat_two.analysis_status
    assert stat_one.channel_id == stat_two.channel_id
    assert stat_one.likes== stat_two.likes
    assert stat_one.link == stat_two.link
    assert stat_one.channel_url == stat_two.channel_url
    assert stat_one.duration == stat_two.duration