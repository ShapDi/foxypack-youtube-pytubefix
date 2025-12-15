import urllib.parse

from foxypack import FoxyAnalysis, DenialAnalyticsException

from foxypack_youtube_pytubefix.answers import YoutubeAnswersAnalysis, YouTubeEnum


class FoxyYouTubeAnalysis(FoxyAnalysis):
    @staticmethod
    def get_code(link: str) -> str | None:
        parsed_url = urllib.parse.urlparse(link)
        if "watch" in parsed_url.path:
            query_params = urllib.parse.parse_qs(parsed_url.query).get("v")
            if query_params is not None:
                return query_params[0].split("?")[0]
        elif "shorts" in parsed_url.path:
            return parsed_url.path.split("/shorts/")[1].split("?")[0]
        elif "@" in parsed_url.path:
            return parsed_url.path.split("@")[1]
        elif "channel" in parsed_url.path:
            return parsed_url.path.split("channel/")[1]
        elif "/" in parsed_url.path:
            return parsed_url.path.split("/")[1]
        return None

    @staticmethod
    def clean_link(link: str) -> str:
        parsed_url = urllib.parse.urlparse(link)
        if "watch" in parsed_url.path:
            query_params = urllib.parse.parse_qs(parsed_url.query).get("v")
            if query_params is not None:
                return f"https://youtube.com/watch?v={query_params[0].split('?')[0]}"
        elif "shorts" in parsed_url.path:
            shorts_id = parsed_url.path.split("/shorts/")[1].split("?")[0]
            return f"https://youtube.com/watch?v={shorts_id}"
        elif "@" in parsed_url.path:
            return f"https://www.youtube.com/@{parsed_url.path.split('@')[1]}"
        elif "channel" in parsed_url.path:
            return (
                f"https://www.youtube.com/channel{parsed_url.path.split('channel')[1]}"
            )
        elif "/" in parsed_url.path:
            shorts_id = parsed_url.path.split("/")[1]
            return f"https://youtube.com/watch?v={shorts_id}"
        return parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path

    @staticmethod
    def get_type_content(link: str) -> str | None:
        parsed_url = urllib.parse.urlparse(link)
        if "watch" in parsed_url.path:
            return YouTubeEnum.video.value
        if "youtu.be" in parsed_url.netloc:
            return YouTubeEnum.video.value
        elif "shorts" in parsed_url.path:
            return YouTubeEnum.shorts.value
        elif "@" in parsed_url.path or "channel" in parsed_url.path:
            return YouTubeEnum.channel.value
        return None

    def get_analysis(self, url: str) -> YoutubeAnswersAnalysis:
        type_content = self.get_type_content(url)
        if type_content is None:
            raise DenialAnalyticsException(url)
        return YoutubeAnswersAnalysis(
            url=self.clean_link(url),
            social_platform="youtube",
            type_content=type_content,
            code=self.get_code(url),
        )
