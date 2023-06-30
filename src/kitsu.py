"""Kitsu GraphQL API wrapper"""

from time import sleep
from typing import Any, Literal
from json import dump

import requests

from const import USER_AGENT
from src.commons import pretty_print as print_

def build_query(
    media_type: Literal["anime", "manga"],
    limit: int = 50,
    cursor: str | None = None) -> dict[str, Any]:
    """
    Build query

    Args:
        media_type (Literal["anime", "manga"]): Media type
        limit (int, optional): Limit. Defaults to 50.
        cursor (str | None, optional): Cursor. Defaults to None.

    Returns:
        dict[str, Any]: Query
    """

    if limit == 0 and cursor is not None:
        raise ValueError("Cursor cannot be used with limit = 0")

    if cursor:
        cursor_ = f', after: "{cursor}"'
    else:
        cursor_ = ""

    limit_ = f"first: {limit}{cursor_}"

    if limit > 0:
        query = f"""
        query {{
            {media_type}({limit_}) {{
                pageInfo {{
                    hasNextPage
                    endCursor
                }}
                nodes {{
                    id
                    titles {{
                        canonical
                        translated
                        original
                        romanized
                    }}
                    mappings (first: 20) {{
                        nodes {{
                            externalSite
                            externalId
                        }}
                    }}
                }}
                totalCount
            }}
        }}
        """
    else:
        query = f"""
        query {{
            {media_type} ({limit_}) {{
                totalCount
            }}
        }}
        """

    data = {
        "query": query,
    }

    return data


class Kitsu:
    """Kitsu Class"""

    def __init__(self) -> None:
        self._base_url = "https://kitsu.io/api/graphql"
        self._rate_limit = 1.2
        self._headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json"
        }

    def _fetch_data(self, query: dict[str, Any]) -> dict[str, Any]:
        """
        Fetch data from Kitsu GraphQL API

        Args:
            query (dict[str, Any]): Query

        Returns:
            dict[str, Any]: JSON data
        """
        req = requests.post(
            self._base_url,
            json=query,
            headers=self._headers,
            timeout=None
        )
        if req.status_code == 200:
            json = req.json()
            return json
        raise ConnectionError(
            f"Kitsu returned {req.status_code} status code")

    def _loop_media(
        self,
        media_type: Literal['anime', 'manga']
    ) -> list[dict[str, Any]]:
        """Loop media"""

        print_(
            "Kitsu",
            f"Getting total count for {media_type}..."
        )
        cursor: str | None = None
        data: list[dict[str, Any]] = []

        # get total count
        counter: dict[str, Any] = build_query(media_type=media_type, limit=1)
        counter = self._fetch_data(counter)
        counts = counter["data"][media_type]["totalCount"]
        pages = counts // 2000 + 1

        print_(
            "Kitsu",
            f"Total count for {media_type}: {counts}, estimated pages: {pages}",
            "Success",
            cr=False
        )

        page = 1
        while True:
            print_(
                "Kitsu",
                f"Getting page {page} for {media_type}...",
            )
            query = build_query(
                media_type=media_type,
                limit=2000,
                cursor=cursor
            )
            json = self._fetch_data(query)

            if not json["data"][media_type]["nodes"]:
                break

            data.extend(json["data"][media_type]["nodes"])

            if not json["data"][media_type]["pageInfo"]["hasNextPage"]:
                break

            cursor = json["data"][media_type]["pageInfo"]["endCursor"]

            page += 1
            sleep(self._rate_limit)

        return data

    def get_anime(self) -> list[dict[str, Any]]:
        """Get anime"""

        return self._loop_media("anime")

    def get_manga(self) -> list[dict[str, Any]]:
        """Get manga"""

        return self._loop_media("manga")

    def save_kitsu_data(self) -> list[list[dict[str, Any]]]:
        """Save Kitsu data"""

        anime = self.get_anime()
        with open("raw/kitsu_anime.json", "w", encoding="utf-8") as file:
            dump(anime, file, ensure_ascii=False)
        print_(
            "Kitsu",
            "Anime data has been saved",
            "Success",
            False)
        manga = self.get_manga()
        with open("raw/kitsu_manga.json", "w", encoding="utf-8") as file:
            dump(manga, file, ensure_ascii=False)
        print_(
            "Kitsu",
            "Manga data has been saved",
            "Success",
            False)

        return [anime, manga]

__all__ = ["Kitsu"]
