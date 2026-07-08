from __future__ import annotations

from os import cpu_count
from typing import Literal

from foxypack.foxypack_abc.foxysearch import FoxySearch
from pytubefix.contrib.search import Filter, Search

from foxypack_youtube_pytubefix.answers import YoutubeVideoAnswersStatistics

UploadDate = Literal[
    "last_hour",
    "today",
    "this_week",
    "this_month",
    "this_year",
]

SearchType = Literal[
    "video",
    "channel",
    "playlist",
    "movie",
]

Duration = Literal[
    "under_4_minutes",
    "between_4_20_minutes",
    "over_20_minutes",
]

SortBy = Literal[
    "relevance",
    "upload_date",
    "view_count",
    "rating",
]

Feature = Literal[
    "creative_commons",
    "hd",
    "hdr",
    "live",
    "location",
    "purchased",
    "subtitles",
    "vr180",
]


_UPLOAD_DATE_MAP = {
    "last_hour": Filter.UploadDate.LAST_HOUR,
    "today": Filter.UploadDate.TODAY,
    "this_week": Filter.UploadDate.THIS_WEEK,
    "this_month": Filter.UploadDate.THIS_MONTH,
    "this_year": Filter.UploadDate.THIS_YEAR,
}

_SEARCH_TYPE_MAP = {
    "video": Filter.Type.VIDEO,
    "channel": Filter.Type.CHANNEL,
    "playlist": Filter.Type.PLAYLIST,
    "movie": Filter.Type.MOVIE,
}

_DURATION_MAP = {
    "under_4_minutes": Filter.Duration.UNDER_4_MINUTES,
    "between_4_20_minutes": Filter.Duration.BETWEEN_4_20_MINUTES,
    "over_20_minutes": Filter.Duration.OVER_20_MINUTES,
}

_SORT_BY_MAP = {
    "relevance": Filter.SortBy.RELEVANCE,
    "upload_date": Filter.SortBy.UPLOAD_DATE,
    "view_count": Filter.SortBy.VIEW_COUNT,
    "rating": Filter.SortBy.RATING,
}

_FEATURE_MAP = {
    "creative_commons": Filter.Features.CREATIVE_COMMONS,
    "hd": Filter.Features.HD,
    "hdr": Filter.Features.HDR,
    "live": Filter.Features.LIVE,
    "location": Filter.Features.LOCATION,
    "purchased": Filter.Features.PURCHASED,
    "subtitles": Filter.Features.SUBTITLES_CC,
    "vr180": Filter.Features.VR180,
}


class FoxySearchKeyWord(FoxySearch):
    def __init__(
        self,
        *,
        upload_date: UploadDate | None = None,
        search_type: SearchType | None = None,
        duration: Duration | None = None,
        sort_by: SortBy | None = None,
        features: list[Feature] | None = None,
    ) -> None:
        self.upload_date = upload_date
        self.search_type = search_type
        self.duration = duration
        self.sort_by = sort_by
        self.features = features or []

    def _build_filter(self) -> Filter | None:
        builder = Filter.create()
        has_filters = False

        if self.upload_date is not None:
            builder.upload_date(_UPLOAD_DATE_MAP[self.upload_date])
            has_filters = True

        if self.search_type is not None:
            builder.type(_SEARCH_TYPE_MAP[self.search_type])
            has_filters = True

        if self.duration is not None:
            builder.duration(_DURATION_MAP[self.duration])
            has_filters = True

        if self.sort_by is not None:
            builder.sort_by(_SORT_BY_MAP[self.sort_by])
            has_filters = True

        if self.features:
            builder.feature(
                [_FEATURE_MAP[feature] for feature in self.features]
            )
            has_filters = True

        if not has_filters:
            return None

        return builder

    def get_search_result(
            self,
            query: str,
    ) -> list[YoutubeVideoAnswersStatistics]:
        search = Search(
            query=query,
            filters=self._build_filter(),
        )

        result: list[YoutubeVideoAnswersStatistics] = []

        for video in search.videos:
            try:
                result.append(
                    YoutubeVideoAnswersStatistics(
                        system_id=video.video_id,
                        title=video.title,
                        views=video.views,
                        publish_date=video.publish_date,
                        channel_id=video.channel_id,
                        likes=video.likes,
                        link=video.watch_url,
                        channel_url=video.channel_url,
                        duration=video.length,
                        analysis_status=None
                    )
                )
            except:
                continue

        return result