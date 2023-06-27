from json import dump, loads
from typing import Any
from copy import deepcopy

import requests

from .commons import pretty_print as print


class Kaize:
    """Kaize via AnimeAPI data fetcher"""

    def __init__(self) -> None:
        """Initialize Kaize via AnimeAPI data fetcher"""
        self._base_url = "https://raw.githubusercontent.com/nattadasu/animeApi/v2/kz.unmapped.raw.json"
        self._data = []

    def _fetch_kaize_data(self) -> dict[str, Any]:
        """
        Fetch data from Kaize via AnimeAPI

        Returns:
            dict[str, Any]: JSON data
        """
        data = requests.get(
            f"{self._base_url}"
        ).text
        return loads(data)

    def save_kaize_data(self) -> list[dict]:
        """
        Save data to file
        """
        print("Kaize", "Saving data to file...")
        data = self._fetch_kaize_data()
        with open("raw/kaize.json", "w", encoding="utf-8") as f:
            dump(data, f, ensure_ascii=False)
        print("Kaize", "Data saved to file")
        self._data = deepcopy(data)
        return data

    def close(self) -> None:
        """
        Close Kaize via AnimeAPI data fetcher
        """
        self._data = []

__all__ = ["Kaize"]
