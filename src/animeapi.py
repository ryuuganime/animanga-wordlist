"""AnimeApi data fetcher"""

from copy import deepcopy
from json import dump, loads
from typing import Any

import requests

from src.commons import pretty_print as print_


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
            f"{self._base_url}",
            timeout=None
        ).text
        return loads(data)

    def save_animeapi_data(self) -> list[dict[str, Any]]:
        """
        Save data to file

        Returns:
            list[dict[str, Any]]: JSON data
        """
        print_("AnimeApi", "Saving data to file...")
        data = self._fetch_animeapi_data()
        with open("raw/animeapi.json", "w", encoding="utf-8") as file:
            dump(data, file, ensure_ascii=False)
        print_("AnimeApi", "Data saved to file", "Success", False)
        self._data = deepcopy(data)
        return self._data

    def close(self) -> None:
        """Close AnimeApi data fetcher"""
        self._data = []

__all__ = ["AnimeApi"]
