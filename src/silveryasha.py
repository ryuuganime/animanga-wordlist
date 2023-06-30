"""Silver Yasha via AnimeAPI data fetcher"""

from json import dump, loads
from copy import deepcopy
from typing import Any

import requests

from src.commons import pretty_print as print_


class SilverYasha:
    """SilverYasha via AnimeAPI data fetcher"""

    def __init__(self) -> None:
        """Initialize Silver Yasha via aniSilverYasha-IndexParser data fetcher"""
        self._base_url = "https://raw.githubusercontent.com/nattadasu/animeApi/v2/sy.raw.json"
        self._data: list[dict[str, Any]] = []

    def _fetch_silveryasha_data(self) -> list[dict[str, Any]]:
        """
        Fetch data from SilverYasha via AnimeAPI

        Returns:
            list[dict[str, Any]]: JSON data
        """
        data = requests.get(
            f"{self._base_url}",
            timeout=None
        ).text
        return loads(data)

    def save_silveryasha_data(self) -> list[dict[str, Any]]:
        """
        Save data to file

        Returns:
            list[dict[str, Any]]: JSON data
        """
        print_("Silver Yasha", "Saving data to file...")
        data = self._fetch_silveryasha_data()
        with open("raw/silveryasha.json", "w", encoding="utf-8") as file:
            dump(data, file, ensure_ascii=False)
        print_("Silver Yasha", "Data saved to file", "Success", False)
        self._data = deepcopy(data)
        return self._data

    def close(self) -> None:
        """Close Silver Yasha via AnimeAPI data fetcher"""
        self._data = []

__all__ = ["SilverYasha"]
