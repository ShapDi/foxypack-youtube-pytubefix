import json
import re
import datetime
from typing import Any

import regex
from bs4 import BeautifulSoup, ResultSet, Tag
from foxypack import (
    FoxyStat,
    InternalCollectionException,
)
from pytubefix import Channel, YouTube

from foxypack_youtube_pytubefix.answers import (
    YoutubeAnswersAnalysis,
    ExternalLink,
    HeavyYouTubeChannelAnswersStatistics,
    YouTubeChannelAnswersStatistics,
    HeavyYoutubeVideoAnswersStatistics,
    YoutubeVideoAnswersStatistics,
)


class YouTubeVideo(FoxyStat):
    def __init__(
        self,
        heavy_answers: bool = False,
    ):
        self._heavy_answers = heavy_answers

    @staticmethod
    def get_object_youtube(link: str) -> YouTube:
        youtube = YouTube(link, "WEB")
        return youtube

    @staticmethod
    def get_like_num(youtube: YouTube) -> bool | int:
        like_template = r"like this video along with (.*?) other people"
        text = str(youtube.initial_data)
        matches = re.findall(like_template, text, re.MULTILINE)
        if len(matches) >= 1:
            like_str = matches[0]
            return int(like_str.replace(",", ""))
        return False

    def get_statistics(
        self, object_analysis: YoutubeAnswersAnalysis
    ) -> HeavyYoutubeVideoAnswersStatistics | YoutubeVideoAnswersStatistics:
        if object_analysis.social_platform != "youtube" and (
            object_analysis.social_platform != "shorts"
            or object_analysis.social_platform != "video"
        ):
            raise InternalCollectionException
        object_youtube = self.get_object_youtube(object_analysis.url)
        if self._heavy_answers:
            return HeavyYoutubeVideoAnswersStatistics(
                title=object_youtube.title,
                likes=self.get_like_num(object_youtube),
                link=object_youtube.watch_url,
                channel_id=object_youtube.channel_id,
                views=object_youtube.views,
                system_id=object_youtube.video_id,
                channel_url=object_youtube.channel_url,
                publish_date=object_youtube.publish_date.date(),
                pytube_ob=object_youtube,
                duration=object_youtube.length,
                analysis_status=object_analysis,
            )
        else:
            return YoutubeVideoAnswersStatistics(
                title=object_youtube.title,
                likes=self.get_like_num(object_youtube),
                link=object_youtube.watch_url,
                channel_id=object_youtube.channel_id,
                views=object_youtube.views,
                system_id=object_youtube.video_id,
                channel_url=object_youtube.channel_url,
                publish_date=object_youtube.publish_date.date(),
                duration=object_youtube.length,
                analysis_status=object_analysis,
            )

    async def get_statistics_async(
        self, object_analysis: YoutubeAnswersAnalysis
    ) -> HeavyYoutubeVideoAnswersStatistics | YoutubeVideoAnswersStatistics:
        if object_analysis.social_platform != "youtube" and (
            object_analysis.social_platform != "shorts"
            or object_analysis.social_platform != "video"
        ):
            raise InternalCollectionException
        object_youtube = self.get_object_youtube(object_analysis.url)
        if self._heavy_answers:
            return HeavyYoutubeVideoAnswersStatistics(
                title=object_youtube.title,
                likes=self.get_like_num(object_youtube),
                link=object_youtube.watch_url,
                channel_id=object_youtube.channel_id,
                views=object_youtube.views,
                system_id=object_youtube.video_id,
                channel_url=object_youtube.channel_url,
                publish_date=object_youtube.publish_date.date(),
                pytube_ob=object_youtube,
                duration=object_youtube.length,
                analysis_status=object_analysis,
            )
        else:
            return YoutubeVideoAnswersStatistics(
                title=object_youtube.title,
                likes=self.get_like_num(object_youtube),
                link=object_youtube.watch_url,
                channel_id=object_youtube.channel_id,
                views=object_youtube.views,
                system_id=object_youtube.video_id,
                channel_url=object_youtube.channel_url,
                publish_date=object_youtube.publish_date.date(),
                duration=object_youtube.length,
                analysis_status=object_analysis,
            )


class YouTubeChannel(FoxyStat):
    def __init__(
        self,
        heavy_answers: bool = False,
    ):
        self._heavy_answers = heavy_answers

    @staticmethod
    def transform_youtube_channel_link(url: str) -> str:
        pattern = r"https://www\.youtube\.com/@([\w-]+)"
        match = re.match(pattern, url)

        if match:
            channel_name = match.group(1)
            return f"https://www.youtube.com/c/{channel_name}/videos"

        else:
            return url

    @staticmethod
    def get_object_youtube(link: str) -> Channel:
        channel = Channel(link, "WEB", use_po_token=True)
        return channel

    @staticmethod
    def extract_json(text: ResultSet[Tag]) -> list[Any]:
        json_pattern = regex.compile(r"\{(?:[^{}]|(?R))*\}")
        json_matches = json_pattern.findall(str(text))
        extracted_json = []
        for match in json_matches:
            try:
                json_data = json.loads(match)
                extracted_json.append(json_data)
            except json.JSONDecodeError:
                pass
        return extracted_json

    def get_base_con(self, object_channel: Channel) -> list[Any]:
        soup = BeautifulSoup(object_channel.about_html, "html.parser")
        script = soup.find_all("script")
        data = self.extract_json(script)
        on = data[3].get("onResponseReceivedEndpoints")
        if on is None:
            on = data[4].get("onResponseReceivedEndpoints")
        return on

    def get_country(self, object_channel: Channel) -> str:
        data = self.get_base_con(object_channel)
        text_country = str(
            (
                data[0]
                .get("showEngagementPanelEndpoint")
                .get("engagementPanel")
                .get("engagementPanelSectionListRenderer")
                .get("content")
                .get("sectionListRenderer")
                .get("contents")[0]
                .get("itemSectionRenderer")
                .get("contents")[0]
                .get("aboutChannelRenderer")
                .get("metadata")
                .get("aboutChannelViewModel")
                .get("country")
            )
        )
        return text_country

    def get_view_count(self, object_youtube: Channel) -> int:
        data = self.get_base_con(object_youtube)
        text_view_count = (
            data[0]
            .get("showEngagementPanelEndpoint")
            .get("engagementPanel")
            .get("engagementPanelSectionListRenderer")
            .get("content")
            .get("sectionListRenderer")
            .get("contents")[0]
            .get("itemSectionRenderer")
            .get("contents")[0]
            .get("aboutChannelRenderer")
            .get("metadata")
            .get("aboutChannelViewModel")
            .get("viewCountText")
        )
        view_count = Convert.convert_views_to_int(text_view_count)
        return view_count

    def get_number_videos(self, object_youtube: Channel) -> int:
        data = self.get_base_con(object_youtube)
        number_videos = (
            data[0]
            .get("showEngagementPanelEndpoint", {})
            .get("engagementPanel", {})
            .get("engagementPanelSectionListRenderer", {})
            .get("content", {})
            .get("sectionListRenderer", {})
            .get("contents", [{}])[0]
            .get("itemSectionRenderer", {})
            .get("contents", [{}])[0]
            .get("aboutChannelRenderer", {})
            .get("metadata", {})
            .get("aboutChannelViewModel", {})
            .get("videoCountText")
        )
        number_videos = Convert.convert_number_videos(number_videos)
        return number_videos

    def get_subscriber(self, object_youtube: Channel) -> int:
        data = self.get_base_con(object_youtube)
        text_subscriber = (
            data[0]
            .get("showEngagementPanelEndpoint")
            .get("engagementPanel")
            .get("engagementPanelSectionListRenderer")
            .get("content")
            .get("sectionListRenderer")
            .get("contents")[0]
            .get("itemSectionRenderer")
            .get("contents")[0]
            .get("aboutChannelRenderer")
            .get("metadata")
            .get("aboutChannelViewModel")
            .get("subscriberCountText")
        )
        subscriber = Convert.convert_subscribers_to_int(text_subscriber)
        return subscriber

    def get_data_create(self, object_youtube: Channel) -> datetime.date:
        data = self.get_base_con(object_youtube)
        data_create = (
            data[0]
            .get("showEngagementPanelEndpoint", {})
            .get("engagementPanel", {})
            .get("engagementPanelSectionListRenderer", {})
            .get("content", {})
            .get("sectionListRenderer", {})
            .get("contents", [{}])[0]
            .get("itemSectionRenderer", {})
            .get("contents", [{}])[0]
            .get("aboutChannelRenderer", {})
            .get("metadata", {})
            .get("aboutChannelViewModel", {})
            .get("joinedDateText", {})
            .get("content")
        )
        data_create = Convert.convert_data_create(data_create)
        return data_create

    def get_description(self, object_youtube: Channel) -> str:
        data = self.get_base_con(object_youtube)
        text_description = str(
            (
                data[0]
                .get("showEngagementPanelEndpoint")
                .get("engagementPanel")
                .get("engagementPanelSectionListRenderer")
                .get("content")
                .get("sectionListRenderer")
                .get("contents")[0]
                .get("itemSectionRenderer")
                .get("contents")[0]
                .get("aboutChannelRenderer")
                .get("metadata")
                .get("aboutChannelViewModel")
                .get("description")
            )
        )
        return text_description

    def get_external_links(self, object_youtube: Channel) -> list[ExternalLink]:
        data = self.get_base_con(object_youtube)
        external_links = (
            data[0]
            .get("showEngagementPanelEndpoint")
            .get("engagementPanel")
            .get("engagementPanelSectionListRenderer")
            .get("content")
            .get("sectionListRenderer")
            .get("contents")[0]
            .get("itemSectionRenderer")
            .get("contents")[0]
            .get("aboutChannelRenderer")
            .get("metadata")
            .get("aboutChannelViewModel")
            .get("links")
        )
        return [
            ExternalLink(
                title=link_data.get("channelExternalLinkViewModel")
                .get("title")
                .get("content"),
                link=f"http://{link_data.get('channelExternalLinkViewModel').get('link').get('content')}",
            )
            for link_data in external_links
        ]

    def get_statistics(
        self, object_analysis: YoutubeAnswersAnalysis
    ) -> HeavyYouTubeChannelAnswersStatistics | YouTubeChannelAnswersStatistics:
        if (
            object_analysis.social_platform != "youtube"
            and object_analysis.social_platform != "channel"
        ):
            raise InternalCollectionException
        object_youtube = self.get_object_youtube(object_analysis.url)
        if self._heavy_answers:
            return HeavyYouTubeChannelAnswersStatistics(
                title=object_youtube.channel_name,
                link=object_youtube.channel_url,
                description=object_youtube.description,
                country=self.get_country(object_youtube),
                system_id=object_youtube.channel_id,
                view_count=self.get_view_count(object_youtube),
                subscribers=self.get_subscriber(object_youtube),
                creation_date=self.get_data_create(object_youtube),
                number_videos=self.get_number_videos(object_youtube),
                pytube_ob=object_youtube,
                external_link=self.get_external_links(object_youtube),
                analysis_status=object_analysis,
            )
        else:
            return YouTubeChannelAnswersStatistics(
                title=object_youtube.channel_name,
                link=object_youtube.channel_url,
                description=object_youtube.description,
                country=self.get_country(object_youtube),
                system_id=object_youtube.channel_id,
                view_count=self.get_view_count(object_youtube),
                subscribers=self.get_subscriber(object_youtube),
                creation_date=self.get_data_create(object_youtube),
                number_videos=self.get_number_videos(object_youtube),
                external_link=self.get_external_links(object_youtube),
                analysis_status=object_analysis,
            )

    async def get_statistics_async(
        self, object_analysis: YoutubeAnswersAnalysis
    ) -> HeavyYouTubeChannelAnswersStatistics | YouTubeChannelAnswersStatistics:
        if (
            object_analysis.social_platform != "youtube"
            and object_analysis.social_platform != "channel"
        ):
            raise InternalCollectionException
        object_youtube = self.get_object_youtube(object_analysis.url)
        if self._heavy_answers:
            return HeavyYouTubeChannelAnswersStatistics(
                title=object_youtube.channel_name,
                link=object_youtube.channel_url,
                description=object_youtube.description,
                country=self.get_country(object_youtube),
                system_id=object_youtube.channel_id,
                view_count=self.get_view_count(object_youtube),
                subscribers=self.get_subscriber(object_youtube),
                creation_date=self.get_data_create(object_youtube),
                number_videos=self.get_number_videos(object_youtube),
                pytube_ob=object_youtube,
                external_link=self.get_external_links(object_youtube),
                analysis_status=object_analysis,
            )
        else:
            return YouTubeChannelAnswersStatistics(
                title=object_youtube.channel_name,
                link=object_youtube.channel_url,
                description=object_youtube.description,
                country=self.get_country(object_youtube),
                system_id=object_youtube.channel_id,
                view_count=self.get_view_count(object_youtube),
                subscribers=self.get_subscriber(object_youtube),
                creation_date=self.get_data_create(object_youtube),
                number_videos=self.get_number_videos(object_youtube),
                external_link=self.get_external_links(object_youtube),
                analysis_status=object_analysis,
            )


class Convert:
    @staticmethod
    def convert_views_to_int(views_str: str) -> int:
        try:
            clean_str = views_str.replace(",", "").replace(" views", "").strip()
            return int(clean_str)
        except Exception:
            return 0

    @staticmethod
    def convert_subscribers_to_int(subscribers_str: str) -> int:
        clean_str = subscribers_str.replace(" subscribers", "").strip()

        if "K" in clean_str:
            return int(float(clean_str.replace("K", "")) * 1000)
        elif "M" in clean_str:
            return int(float(clean_str.replace("M", "")) * 1000000)
        else:
            return int(clean_str)

    @staticmethod
    def convert_number_videos(number_videos: str) -> int:
        try:
            return int(number_videos.split(" ")[0])
        except ValueError:
            long_int = number_videos.split(" ")[0].split(",")
            return int(f"{long_int[0]}{long_int[1]}")
        except Exception:
            return 0

    @staticmethod
    def convert_data_create(data_create: str) -> datetime.date:
        date_part = data_create.replace("Joined ", "")
        joined_date = datetime.datetime.strptime(date_part, "%b %d, %Y").date()
        return joined_date
