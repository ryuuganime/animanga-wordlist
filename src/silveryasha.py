from json import dump, loads
from copy import deepcopy
from typing import Any

import requests

from .commons import pretty_print as print


class SilverYasha:
    """SilverYasha via AnimeAPI data fetcher"""

    def __init__(self) -> None:
        """Initialize SilverYasha via aniSilverYasha-IndexParser data fetcher"""
        self._base_url = "https://raw.githubusercontent.com/nattadasu/animeApi/v2/sy.raw.json"
        self._data = []

    def _fetch_silveryasha_data(self) -> dict[str, Any]:
        """
        Fetch data from SilverYasha via AnimeAPI

        Returns:
            dict[str, Any]: JSON data
        """
        data = requests.get(
            f"{self._base_url}"
        ).text
        return loads(data)

    def save_silveryasha_data(self) -> list[dict]:
        """
        Save data to file
        """
        print("SilverYasha", "Saving data to file...")
        data = self._fetch_silveryasha_data()
        with open("raw/silveryasha.json", "w", encoding="utf-8") as f:
            dump(data, f, ensure_ascii=False)
        print("SilverYasha", "Data saved to file")
        self._data = deepcopy(data)
        return self._data

    def close(self) -> None:
        """
        Close SilverYasha via AnimeAPI data fetcher
        """
        self._data = []

__all__ = ["SilverYasha"]
