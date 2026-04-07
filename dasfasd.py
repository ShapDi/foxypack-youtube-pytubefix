from pytubefix import YouTube
from pytubefix.cli import on_progress

url = "https://www.youtube.com/watch?v=0QdKpxsEDeM"

yt = YouTube(
    url, use_oauth=True, allow_oauth_cache=True, on_progress_callback=on_progress
)
print(yt.views)
