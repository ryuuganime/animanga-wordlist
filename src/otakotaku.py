from json import dump, loads
from copy import deepcopy
from typing import Any

import requests

from .commons import pretty_print as print


class OtakOtaku:
    """OtakOtaku via AnimeAPI data fetcher"""

    def __init__(self) -> None:
        """Initialize OtakOtaku via AnimeAPI data fetcher"""
        self._base_url = "https://raw.githubusercontent.com/nattadasu/animeApi/v2/oo.raw.json"
        self._data = []

    def _fetch_otakotaku_data(self) -> dict[str, Any]:
        """
        Fetch data from OtakOtaku via AnimeAPI

        Returns:
            dict[str, Any]: JSON data
        """
        data = requests.get(
            f"{self._base_url}"
        ).text
        return loads(data)

    def save_otakotaku_data(self) -> list[dict]:
        """
        Save data to file
        """
        print("OtakOtaku", "Saving data to file...")
        data = self._fetch_otakotaku_data()
        with open("raw/otakotaku.json", "w", encoding="utf-8") as f:
            dump(data, f, ensure_ascii=False)
        print("OtakOtaku", "Data saved to file")
        self._data = deepcopy(data)
        return self._data

    def close(self) -> None:
        """
        Close OtakOtaku via AnimeAPI data fetcher
        """
        self._data = []

__all__ = ["OtakOtaku"]
