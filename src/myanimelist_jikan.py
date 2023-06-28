import requests
from json import dump
from typing import Any, Literal
from time import sleep

from .commons import pretty_print as print
from const import USER_AGENT

class ConnectionError(Exception):
    """Connection Error"""

class MyAnimeList:
    """Parse MyAnimeList data from Jikan API"""

    def __init__(self) -> None:
        """Initialize MyAnimeList data fetcher"""
        self._base_url = "https://api.jikan.moe/v4"
        self._rate_limit = 1.2
        self._headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json"
        }


    def _fetch_data(
        self,
        path: Literal["anime", "manga", "characters", "people", "producers", "magazines"],
        order_by: Literal["mal_id", "title", "name"] = "title",
        page: int = 1,
        limit: int = 25
    ) -> dict[str, Any]:
        """
        Fetch data from Jikan API

        Args:
            path (Literal["anime", "manga", "characters", "people", "producers", "magazines"]): Path to fetch
            order_by (Literal["mal_id", "title", "name"], optional): Order by. Defaults to "title".
            page (int, optional): Page number. Defaults to 1.
            limit (int, optional): Number of items per page. Defaults to 25.

        Returns:
            dict[str,Any]: JSON data
        """
        if path == "producers":
            order_by = "mal_id"
        if order_by == "title" and path not in ["manga", "anime"]:
            order_by = "name"
        if limit > 25:
            raise ValueError("Limit cannot be more than 25")
        req = requests.get(
            f"{self._base_url}/{path}",
            params={
                "order_by": order_by,
                "page": page,
                "limit": limit
            },
            headers=self._headers
        )
        if req.status_code == 200:
            json = req.json()
            return json
        raise ConnectionError(f"Status code: {req.status_code}, Reason: {req.reason}")

    def _fetcher(self, path: Literal["anime", "manga", "characters", "people", "producers", "magazines"]) -> list[dict[str, Any]]:
        """Do a fetch"""
        print("MyAnimeList", f"Checking total count for {path}")
        entries = self._fetch_data(path=path, limit=1)
        total_count = entries["pagination"]["items"]["total"]
        pages = total_count // 50 + 1
        print("MyAnimeList", f"Total count for {path}: {total_count}, pages: {pages}", "Success", False)
        sleep(self._rate_limit)
        data: list[dict[str, Any]] = []
        for page in range(1, pages + 1):
            print("MyAnimeList", f"Fetching {path} data, page {page} of {pages}")
            data += self._fetch_data(path=path, page=page)["data"]
            sleep(self._rate_limit)
        print("MyAnimeList", f"{path.capitalize()} data fetched, total pages: {pages}", "Success", False)
        # save data
        with open(f"raw/myanimelist_{path}.json", "w", encoding="utf-8") as f:
            dump(data, f, ensure_ascii=False)
        sleep(2)
        return data

    def fetch_data_all(self) -> list[list[dict[str, Any]]]:
        """Fetch all data from Jikan API"""
        # Anime
        anime = self._fetcher("anime")
        sleep(self._rate_limit)
        # Manga
        manga = self._fetcher("manga")
        sleep(self._rate_limit)
        # Producers
        studio = self._fetcher("producers")
        sleep(self._rate_limit)
        # Magazines
        publisher = self._fetcher("magazines")
        sleep(self._rate_limit)

        return [
            anime,
            manga,
            studio,
            publisher
        ]

    def close(self) -> None:
        """Close MyAnimeList data fetcher"""
