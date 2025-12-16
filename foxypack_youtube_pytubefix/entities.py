from foxy_entities import SocialMediaEntity


class YoutubeProxy(SocialMediaEntity):
    proxy_str: str

    def __post_init__(self):
        self.proxy_comparison = {
            "http": f"{self.proxy_str}",
            "https": f"{self.proxy_str}",
        }