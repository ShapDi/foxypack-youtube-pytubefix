from enum import Enum


class YouTubeEnum(Enum):
    shorts = "shorts"
    video = "video"
    channel = "channel"


class YouTubeHostEnum(str, Enum):
    YOUTUBE = "youtube.com"
    WWW_YOUTUBE = "www.youtube.com"
    M_YOUTUBE = "m.youtube.com"
    YOU_TUBE = "youtu.be"
    WWW_YOUTU_BE = "www.youtu.be"

    @classmethod
    def values(cls) -> set[str]:
        return {member.value for member in cls}

    @classmethod
    def is_youtube_host(cls, host: str) -> bool:
        return host.lower().strip() in cls.values()
