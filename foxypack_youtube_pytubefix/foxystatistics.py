import datetime
import json
import re
from typing import Any

import regex
from bs4 import BeautifulSoup, ResultSet, Tag
from foxy_entities import EntitiesController
from foxy_entities.exceptions import PresenceObjectException
from pytubefix import Channel, YouTube
from typing_extensions import override

from foxypack.exceptions import ConfigurationError, FoxyError, UnsupportedOperationError
from foxypack.foxypack_abc.answers import AnswersAnalysis
from foxypack.foxypack_abc.foxystatistics import FoxyStatistics
from foxypack_youtube_pytubefix.answers import (
    ExternalLink,
    HeavyYouTubeChannelAnswersStatistics,
    HeavyYoutubeVideoAnswersStatistics,
    YouTubeChannelAnswersStatistics,
    YoutubeVideoAnswersStatistics,
)
from foxypack_youtube_pytubefix.entities import YoutubeProxy
from foxypack_youtube_pytubefix.exceptions import (
    YouTubeDataExtractionError,
    map_pytubefix_exception,
)


class YouTubeVideo(FoxyStatistics):
    def __init__(
        self,
        entities_controller: EntitiesController | None = None,
        heavy_answers: bool = False,
        auth: bool = False,
    ) -> None:
        self._heavy_answers = heavy_answers
        self._entities_controller = entities_controller
        self._auth = auth

    @staticmethod
    def _validate_analysis(answers_analysis: AnswersAnalysis) -> None:
        if answers_analysis.social_platform != "youtube":
            raise UnsupportedOperationError(
                message="YouTubeVideo supports only youtube platform",
                details={
                    "platform": answers_analysis.social_platform,
                    "type_content": answers_analysis.type_content,
                },
            )

        if answers_analysis.type_content not in {"video", "shorts"}:
            raise UnsupportedOperationError(
                message="YouTubeVideo supports only video and shorts content",
                details={
                    "platform": answers_analysis.social_platform,
                    "type_content": answers_analysis.type_content,
                },
            )

    def get_object_youtube(self, link: str) -> YouTube:
        kwargs: dict[str, Any] = {}

        if self._entities_controller is not None:
            try:
                proxy = self._entities_controller.get_entity(YoutubeProxy)
                kwargs["proxies"] = proxy.proxy_comparison()
                self._entities_controller.add_entity(proxy)
            except PresenceObjectException:
                pass
            except Exception as exc:
                raise ConfigurationError(
                    message="Failed to configure YouTube proxy",
                    details={"url": link},
                    cause=exc,
                ) from exc

        try:
            return YouTube(
                link,
                "WEB",
                use_oauth=self._auth,
                **kwargs,
            )
        except Exception as exc:
            raise map_pytubefix_exception(exc, url=link) from exc

    @staticmethod
    def get_like_num(youtube: YouTube) -> int | None:
        like_template = r"like this video along with (.*?) other people"
        text = str(getattr(youtube, "initial_data", ""))
        matches = re.findall(like_template, text, re.MULTILINE)

        if not matches:
            return None

        like_str = matches[0].replace(",", "").strip()
        try:
            return int(like_str)
        except ValueError:
            return None

    @staticmethod
    def get_comments_num(youtube: YouTube) -> int | None:

        try:
            text = str(getattr(youtube, "initial_data", ""))

            with open("initial_data.json", "w", encoding="utf-8") as f:
                json.dump(youtube.initial_data, f, ensure_ascii=False, indent=2)
            with open("initial_data2.txt", "w", encoding="utf-8") as f:
                f.write(str(youtube.watch_html))
            with open("data.txt", "w", encoding="utf-8") as f:
                json.dump(youtube.likes, f, ensure_ascii=False, indent=2)
        except Exception as exc:
            print(exc)

        return 0



    def _build_statistics(
        self,
        answers_analysis: AnswersAnalysis,
    ) -> HeavyYoutubeVideoAnswersStatistics | YoutubeVideoAnswersStatistics:
        self._validate_analysis(answers_analysis)
        object_youtube = self.get_object_youtube(answers_analysis.url)

        try:
            publish_date = object_youtube.publish_date
            publish_date_value = publish_date.date() if publish_date else None

            payload = {
                "title": object_youtube.title,
                "likes": object_youtube.likes,
                "link": object_youtube.watch_url,
                "channel_id": object_youtube.channel_id,
                "views": object_youtube.views,
                "system_id": object_youtube.video_id,
                "channel_url": object_youtube.channel_url,
                "publish_date": publish_date_value,
                "duration": object_youtube.length,
                "analysis_status": answers_analysis,
                "comments": self.get_comments_num(object_youtube),
            }

            if self._heavy_answers:
                payload["pytube_ob"] = object_youtube
                return HeavyYoutubeVideoAnswersStatistics(**payload)

            return YoutubeVideoAnswersStatistics(**payload)

        except FoxyError:
            raise
        except Exception as exc:
            raise YouTubeDataExtractionError(
                message="Failed to extract video statistics from pytubefix object",
                details={
                    "url": answers_analysis.url,
                    "platform": answers_analysis.social_platform,
                    "type_content": answers_analysis.type_content,
                },
                cause=exc,
            ) from exc

    @override
    def get_statistics(
        self,
        answers_analysis: AnswersAnalysis,
    ) -> HeavyYoutubeVideoAnswersStatistics | YoutubeVideoAnswersStatistics:
        return self._build_statistics(answers_analysis)

    @override
    async def get_statistics_async(
        self,
        answers_analysis: AnswersAnalysis,
    ) -> HeavyYoutubeVideoAnswersStatistics | YoutubeVideoAnswersStatistics:
        return self._build_statistics(answers_analysis)


class YouTubeChannel(FoxyStatistics):
    def __init__(
        self,
        entities_controller: EntitiesController | None = None,
        heavy_answers: bool = False,
        auth: bool = False,
    ) -> None:
        self._entities_controller = entities_controller
        self._heavy_answers = heavy_answers
        self._auth = auth

    def _validate_analysis(self, answers_analysis: AnswersAnalysis) -> None:
        if answers_analysis.social_platform != "youtube":
            raise UnsupportedOperationError(
                message="YouTubeChannel supports only youtube platform",
                details={
                    "platform": answers_analysis.social_platform,
                    "type_content": answers_analysis.type_content,
                },
            )

        if answers_analysis.type_content != "channel":
            raise UnsupportedOperationError(
                message="YouTubeChannel supports only channel content",
                details={
                    "platform": answers_analysis.social_platform,
                    "type_content": answers_analysis.type_content,
                },
            )

    @staticmethod
    def transform_youtube_channel_link(url: str) -> str:
        pattern = r"https://www\.youtube\.com/@([\w-]+)"
        match = re.match(pattern, url)

        if match:
            channel_name = match.group(1)
            return f"https://www.youtube.com/c/{channel_name}/videos"

        return url

    def get_object_youtube(self, link: str) -> Channel:
        kwargs: dict[str, Any] = {}
        normalized_link = self.transform_youtube_channel_link(link)

        if self._entities_controller is not None:
            try:
                proxy = self._entities_controller.get_entity(YoutubeProxy)
                kwargs["proxies"] = proxy.proxy_comparison()
                self._entities_controller.add_entity(proxy)
            except PresenceObjectException:
                pass
            except Exception as exc:
                raise ConfigurationError(
                    message="Failed to configure YouTube proxy",
                    details={"url": normalized_link},
                    cause=exc,
                ) from exc

        try:
            return Channel(
                normalized_link,
                "WEB",
                use_oauth=self._auth,
                **kwargs,
            )
        except Exception as exc:
            raise map_pytubefix_exception(exc, url=normalized_link) from exc

    @staticmethod
    def extract_json(text: ResultSet[Tag]) -> list[Any]:
        json_pattern = regex.compile(r"\{(?:[^{}]|(?R))*\}")
        json_matches = json_pattern.findall(str(text))
        extracted_json: list[Any] = []

        for match in json_matches:
            try:
                json_data = json.loads(match)
                extracted_json.append(json_data)
            except json.JSONDecodeError:
                continue

        return extracted_json

    @staticmethod
    def _dig(data: Any, *path: Any, default: Any = None) -> Any:
        current = data
        for key in path:
            try:
                if isinstance(key, int):
                    current = current[key]
                else:
                    current = current.get(key)
            except (AttributeError, IndexError, KeyError, TypeError):
                return default

            if current is None:
                return default

        return current

    def get_base_con(self, object_channel: Channel) -> list[Any]:
        try:
            soup = BeautifulSoup(object_channel.about_html, "html.parser")
            script = soup.find_all("script")
            data = self.extract_json(script)

            for item in data:
                endpoints = item.get("onResponseReceivedEndpoints")
                if endpoints is not None:
                    return endpoints

            raise YouTubeDataExtractionError(
                message="Could not find channel metadata block in about_html",
                details={
                    "channel_url": getattr(object_channel, "channel_url", None),
                    "channel_id": getattr(object_channel, "channel_id", None),
                },
            )
        except FoxyError:
            raise
        except Exception as exc:
            raise YouTubeDataExtractionError(
                message="Failed to parse channel about_html",
                details={
                    "channel_url": getattr(object_channel, "channel_url", None),
                    "channel_id": getattr(object_channel, "channel_id", None),
                },
                cause=exc,
            ) from exc

    def _get_about_channel_view_model(self, object_channel: Channel) -> dict[str, Any]:
        data = self.get_base_con(object_channel)

        model = self._dig(
            data,
            0,
            "showEngagementPanelEndpoint",
            "engagementPanel",
            "engagementPanelSectionListRenderer",
            "content",
            "sectionListRenderer",
            "contents",
            0,
            "itemSectionRenderer",
            "contents",
            0,
            "aboutChannelRenderer",
            "metadata",
            "aboutChannelViewModel",
            default=None,
        )

        if not isinstance(model, dict):
            raise YouTubeDataExtractionError(
                message="Could not extract aboutChannelViewModel",
                details={
                    "channel_url": getattr(object_channel, "channel_url", None),
                    "channel_id": getattr(object_channel, "channel_id", None),
                },
            )

        return model

    def get_country(self, object_channel: Channel) -> str:
        model = self._get_about_channel_view_model(object_channel)
        return str(model.get("country") or "")

    def get_view_count(self, object_channel: Channel) -> int:
        model = self._get_about_channel_view_model(object_channel)
        text_view_count = model.get("viewCountText")
        return Convert.convert_views_to_int(text_view_count)

    def get_number_videos(self, object_channel: Channel) -> int:
        model = self._get_about_channel_view_model(object_channel)
        number_videos = model.get("videoCountText")
        return Convert.convert_number_videos(number_videos)

    def get_subscriber(self, object_channel: Channel) -> int:
        model = self._get_about_channel_view_model(object_channel)
        text_subscriber = model.get("subscriberCountText")
        return Convert.convert_subscribers_to_int(text_subscriber)

    def get_data_create(self, object_channel: Channel) -> datetime.date | None:
        model = self._get_about_channel_view_model(object_channel)
        data_create = self._dig(model, "joinedDateText", "content", default=None)
        return Convert.convert_data_create(data_create)

    def get_description(self, object_channel: Channel) -> str:
        model = self._get_about_channel_view_model(object_channel)
        return str(model.get("description") or "")

    def get_external_links(self, object_channel: Channel) -> list[ExternalLink]:
        model = self._get_about_channel_view_model(object_channel)
        external_links = model.get("links") or []

        result: list[ExternalLink] = []
        for link_data in external_links:
            view_model = link_data.get("channelExternalLinkViewModel", {})
            title = self._dig(view_model, "title", "content", default="") or ""
            raw_link = self._dig(view_model, "link", "content", default="") or ""

            if raw_link and not raw_link.startswith(("http://", "https://")):
                raw_link = f"http://{raw_link}"

            result.append(
                ExternalLink(
                    title=title,
                    link=raw_link,
                )
            )

        return result

    def _build_statistics(
        self,
        answers_analysis: AnswersAnalysis,
    ) -> HeavyYouTubeChannelAnswersStatistics | YouTubeChannelAnswersStatistics:
        self._validate_analysis(answers_analysis)
        object_youtube = self.get_object_youtube(answers_analysis.url)

        try:
            payload = {
                "title": object_youtube.channel_name,
                "link": object_youtube.channel_url,
                "description": getattr(object_youtube, "description", "")
                or self.get_description(object_youtube),
                "country": self.get_country(object_youtube),
                "system_id": object_youtube.channel_id,
                "view_count": self.get_view_count(object_youtube),
                "subscribers": self.get_subscriber(object_youtube),
                "creation_date": self.get_data_create(object_youtube),
                "number_videos": self.get_number_videos(object_youtube),
                "external_link": self.get_external_links(object_youtube),
                "analysis_status": answers_analysis,
            }

            if self._heavy_answers:
                payload["pytube_ob"] = object_youtube
                return HeavyYouTubeChannelAnswersStatistics(**payload)

            return YouTubeChannelAnswersStatistics(**payload)

        except FoxyError:
            raise
        except Exception as exc:
            raise YouTubeDataExtractionError(
                message="Failed to extract channel statistics from pytubefix object",
                details={
                    "url": answers_analysis.url,
                    "platform": answers_analysis.social_platform,
                    "type_content": answers_analysis.type_content,
                },
                cause=exc,
            ) from exc

    @override
    def get_statistics(
        self,
        answers_analysis: AnswersAnalysis,
    ) -> HeavyYouTubeChannelAnswersStatistics | YouTubeChannelAnswersStatistics:
        return self._build_statistics(answers_analysis)

    @override
    async def get_statistics_async(
        self,
        answers_analysis: AnswersAnalysis,
    ) -> HeavyYouTubeChannelAnswersStatistics | YouTubeChannelAnswersStatistics:
        return self._build_statistics(answers_analysis)


class Convert:
    @staticmethod
    def convert_views_to_int(views_str: str | None) -> int:
        if not views_str:
            return 0

        try:
            clean_str = str(views_str).replace(",", "").replace(" views", "").strip()
            return int(clean_str)
        except Exception:
            return 0

    @staticmethod
    def convert_subscribers_to_int(subscribers_str: str | None) -> int:
        if not subscribers_str:
            return 0

        try:
            clean_str = str(subscribers_str).replace(" subscribers", "").strip()

            if "K" in clean_str:
                return int(float(clean_str.replace("K", "").strip()) * 1000)
            if "M" in clean_str:
                return int(float(clean_str.replace("M", "").strip()) * 1_000_000)

            return int(clean_str)
        except Exception:
            return 0

    @staticmethod
    def convert_number_videos(number_videos: str | None) -> int:
        if not number_videos:
            return 0

        try:
            return int(str(number_videos).split(" ")[0])
        except ValueError:
            try:
                long_int = str(number_videos).split(" ")[0].split(",")
                return int("".join(long_int))
            except Exception:
                return 0
        except Exception:
            return 0

    @staticmethod
    def convert_data_create(data_create: str | None) -> datetime.date | None:
        if not data_create:
            return None

        try:
            date_part = str(data_create).replace("Joined ", "").strip()
            return datetime.datetime.strptime(date_part, "%b %d, %Y").date()
        except Exception:
            return None
