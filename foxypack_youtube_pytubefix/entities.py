from foxy_entities import SocialMediaEntity


class YoutubeProxy(SocialMediaEntity):
    proxy_str: str

    def proxy_comparison(self) -> dict[str, str]:
        proxy_comparison = {
            "http": f"{self.proxy_str}",
            "https": f"{self.proxy_str}",
        }
        return proxy_comparison
