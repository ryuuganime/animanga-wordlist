from json import dump, loads
from copy import deepcopy
from typing import Any

import requests

from .commons import pretty_print as print


class AnimeApi:
    """AnimeApi data fetcher"""

    def __init__(self) -> None:
        """Initialize AnimeApi data fetcher"""
        self._base_url = "https://raw.githubusercontent.com/nattadasu/animeApi/v2/animeApi.json"
        self._data = []

    def _fetch_animeapi_data(self) -> list[dict[str, Any]]:
        """
        Fetch data from AnimeApi

        Returns:
            list[dict[str, Any]]: JSON data
        """
        data = requests.get(
            f"{self._base_url}"
        ).text
        return loads(data)

    def save_animeapi_data(self) -> list[dict[str, Any]]:
        """
        Save data to file

        Returns:
            list[dict[str, Any]]: JSON data
        """
        print("AnimeApi", "Saving data to file...")
        data = self._fetch_animeapi_data()
        with open("raw/animeapi.json", "w", encoding="utf-8") as f:
            dump(data, f, ensure_ascii=False)
        print("AnimeApi", "Data saved to file", "Success", False)
        self._data = deepcopy(data)
        return self._data

    def close(self) -> None:
        """Close AnimeApi data fetcher"""
        self._data = []

__all__ = ["AnimeApi"]
