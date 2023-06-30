"""Otak Otaku via AnimeAPI data fetcher"""

from json import dump, loads
from copy import deepcopy
from typing import Any

import requests

from src.commons import pretty_print as print_


class OtakOtaku:
    """Otak Otaku via AnimeAPI data fetcher"""

    def __init__(self) -> None:
        """Initialize OtakOtaku via AnimeAPI data fetcher"""
        self._base_url = "https://raw.githubusercontent.com/nattadasu/animeApi/v2/oo.raw.json"
        self._data: list[dict[str, Any]] = []

    def _fetch_otakotaku_data(self) -> list[dict[str, Any]]:
        """
        Fetch data from Otak Otaku via AnimeAPI

        Returns:
            list[dict[str, Any]]: JSON data
        """
        data = requests.get(
            f"{self._base_url}",
            timeout=None
        ).text
        return loads(data)

    def save_otakotaku_data(self) -> list[dict[str, Any]]:
        """
        Save data to file

        Returns:
            list[dict[str, Any]]: JSON data
        """
        print_("Otak Otaku", "Saving data to file...")
        data = self._fetch_otakotaku_data()
        with open("raw/otakotaku.json", "w", encoding="utf-8") as file:
            dump(data, file, ensure_ascii=False)
        print_("Otak Otaku", "Data saved to file", "Success", False)
        self._data = deepcopy(data)
        return self._data

    def close(self) -> None:
        """Close Otak Otaku via AnimeAPI data fetcher"""
        self._data = []

__all__ = ["OtakOtaku"]
