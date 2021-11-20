from typing import List

from instagrapi.types import Hashtag, Location, UserShort, Track
from instagrapi.extractors import (
    extract_location, extract_hashtag_v1, extract_track,
    extract_user_short
)


class FbSearchMixin:

    def fbsearch_places(self, query: str, lat: float = 40.74, lng: float = -73.94) -> List[Location]:
        params = {
            'search_surface': 'places_search_page',
            'timezone_offset': self.timezone_offset,
            'lat': lat,
            'lng': lng,
            'count': 30,
            'query': query,
        }
        result = self.private_request("fbsearch/places/", params=params)
        locations = []
        for item in result['items']:
            locations.append(extract_location(item['location']))
        return locations

    def fbsearch_topsearch_flat(self, query: str) -> List[dict]:
        params = {
            "search_surface": "top_search_page",
            "context": "blended",
            "timezone_offset": self.timezone_offset,
            "count": 30,
            "query": query,
        }
        result = self.private_request("fbsearch/topsearch_flat/", params=params)
        return result["list"]

    def search_users(self, query: str) -> List[UserShort]:
        params = {
            "search_surface": "user_search_page",
            "timezone_offset": self.timezone_offset,
            "count": 30,
            "q": query,
        }
        result = self.private_request("users/search/", params=params)
        return [extract_user_short(item) for item in result["users"]]

    def search_music(self, query: str) -> List[Track]:
        params = {
            "query": query,
            "browse_session_id": self.generate_uuid(),
        }
        result = self.private_request("music/audio_global_search/", params=params)
        return [extract_track(item["track"]) for item in result["items"]]

    def search_hashtags(self, query: str) -> List[Hashtag]:
        params = {
            "search_surface": "hashtag_search_page",
            "timezone_offset": self.timezone_offset,
            "count": 30,
            "q": query,
        }
        result = self.private_request("tags/search/", params=params)
        return [extract_hashtag_v1(ht) for ht in result["results"]]
