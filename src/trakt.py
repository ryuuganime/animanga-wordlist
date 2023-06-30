"""Trakt via AnimeAPI data fetcher"""

from json import dump, loads
from copy import deepcopy
from typing import Any

import requests

from src.commons import pretty_print as print_


class Trakt:
    """Trakt via AnimeAPI data fetcher"""

    def __init__(self) -> None:
        """Initialize Trakt via aniTrakt-IndexParser data fetcher"""
        self._base_url = "https://raw.githubusercontent.com/nattadasu/animeApi/v2/ati.raw.json"
        self._data = []

    def _fetch_trakt_data(self) -> list[dict[str, Any]]:
        """
        Fetch data from Trakt via AnimeAPI

        Returns:
            list[dict[str, Any]]: JSON data
        """
        data = requests.get(
            f"{self._base_url}",
            timeout=None
        ).text
        return loads(data)

    def save_trakt_data(self) -> list[dict[str, Any]]:
        """
        Save data to file

        Returns:
            list[dict[str, Any]]: JSON data
        """
        print_("Trakt", "Saving data to file...")
        data = self._fetch_trakt_data()
        with open("raw/trakt.json", "w", encoding="utf-8") as file:
            dump(data, file, ensure_ascii=False)
        print_("Trakt", "Data saved to file", "Success", False)
        self._data = deepcopy(data)
        return self._data

    def close(self) -> None:
        """Close Trakt via AnimeAPI data fetcher"""
        self._data = []

__all__ = ["Trakt"]
