import requests
from time import sleep
from json import dump
from typing import Any, Literal

from .commons import pretty_print as print
from const import USER_AGENT


class AniList:
    """Parse AniList data from AniList GraphQL API"""

    def __init__(self) -> None:
        self._base_url = "https://graphql.anilist.co"
        self._rate_limit = 1.2
        self._headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json"
        }

    def _fetch_data(self, query: str, variables: dict[str, str]) -> dict[str, str]:
        """
        Fetch data from AniList GraphQL API

        Args:
            query (str): Query
            variables (dict[str, str]): Variables

        Returns:
            dict[str, str]: JSON data
        """
        req = requests.post(
            self._base_url,
            json={
                "query": query,
                "variables": variables
            },
            headers=self._headers
        )
        if req.status_code == 200:
            json = req.json()
            return json
        else:
            raise ConnectionError(f"AniList returned {req.status_code} status code")

    def _fetch_media(self, media_type: Literal["ANIME", "MANGA"], page: int = 1, per_page: int = 50) -> dict[str, str]:
        """
        Fetch media from AniList GraphQL API

        Args:
            media_type (Literal["ANIME", "MANGA"]): Media type
            page (int, optional): Page number. Defaults to 1.
            per_page (int, optional): Number of items per page. Defaults to 50.

        Returns:
            dict[str, str]: JSON data
        """
        query = """
        query ($page: Int, $perPage: Int) {
            Page (page: $page, perPage: $perPage) {
                pageInfo {
                    total
                    perPage
                    currentPage
                    lastPage
                    hasNextPage
                }
                media (type: %s, sort: TITLE_ROMAJI) {
                    id
                    title {
                        romaji
                        english
                        native
                    }
                    idMal
                    synonyms
                }
            }
        }
        """ % media_type

        variables = {
            "page": page,
            "perPage": per_page
        }

        return self._fetch_data(query, variables)

    def _loop_fetch_manga(self) -> list[dict[str, Any]]:
        """
        Loop fetch manga from AniList GraphQL API

        Returns:
            list[dict[str, Any]]: List of manga
        """
        page = 1
        total = 0
        data: list[dict[str, Any]] = []
        while True:
            print("AniList", f"Fetching manga, page {page}...", "Running")
            entry = self._fetch_media("MANGA", page)
            data.extend(entry["data"]["Page"]["media"])
            if entry["data"]["Page"]["pageInfo"]["hasNextPage"]:
                page += 1
            else:
                break
            total += len(entry["data"]["Page"]["media"])
            sleep(self._rate_limit)
        print("AniList", f"Fetched {total} manga", "Success", False)
        return data

    def _loop_fetch_anime(self) -> list[dict[str, Any]]:
        """
        Loop fetch anime from AniList GraphQL API

        Returns:
            list[dict[str, Any]]: List of anime
        """
        page = 1
        total = 0
        data: list[dict[str, Any]] = []
        while True:
            print("AniList", f"Fetching anime, page {page}...", "Running")
            entry = self._fetch_media("ANIME", page)
            data.extend(entry["data"]["Page"]["media"])
            if entry["data"]["Page"]["pageInfo"]["hasNextPage"]:
                page += 1
            else:
                break
            total += len(entry["data"]["Page"]["media"])
            sleep(self._rate_limit)
        print("AniList", f"Fetched {total} anime", "Success", False)
        return data


    def save_anilist_data(self) -> list[list[dict[str, any]]]:
        """
        Save AniList data to JSON file

        Returns:
            list[list[dict[str, any]]]: List of anime and manga
        """
        anime = self._loop_fetch_anime()
        print("AniList", "Saving anime data...")
        with open("raw/anilist_anime.json", "w", encoding="utf-8") as f:
            dump(anime, f, ensure_ascii=False)
        print("AniList", "Saved anime data", "Success", False)
        manga = self._loop_fetch_manga()
        print("AniList", "Saving manga data...")
        with open("raw/anilist_manga.json", "w", encoding="utf-8") as f:
            dump(manga, f, ensure_ascii=False)
        print("AniList", "Saved manga data", "Success", False)

        return [anime, manga]


__all__ = ["AniList"]
