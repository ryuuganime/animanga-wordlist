import os
import time
from copy import deepcopy
from json import dump
from typing import Any

import requests

from const import USER_AGENT
from .commons import pretty_print as print


class Annict:
    """Annict API wrapper"""
    def __init__(self, access_token: str) -> None:
        """Initialize Annict API wrapper"""
        self._base_url = "https://api.annict.com/v1"
        if not access_token:
            self._access_token = os.environ.get("ANNICT_ACCESS_TOKEN")
        else:
            self._access_token = access_token
        self._headers = {
            "User-Agent": USER_AGENT
        }
        self._data: list[dict[str, Any]] = []

    def _fetch_annict_data(self, page: int, limit: int = 50) -> dict[str, Any]:
        """
        Fetch data from Annict API

        Args:
            page (int): Page number
            limit (int, optional): Number of items per page. Defaults to 50.

        Returns:
            dict[str, Any]: JSON data
        """
        return requests.get(
            f"{self._base_url}/works",
            params={
                "fields": "title,title_kana,title_en",
                "page": page,
                "per_page": limit,
                "access_token": self._access_token
            },
            headers=self._headers
        ).json()

    def fetch_annict_data_all(self) -> list[dict[str, Any]]:
        """
        Fetch all data from Annict API

        Returns:
            list[dict[str, Any]]: JSON data
        """

        # check total count
        print("Annict", "Fetching total count", "Running")
        counter = self._fetch_annict_data(1, 1)
        total_count = counter["total_count"]
        print("Annict", f"Total count: {total_count}, pages: {total_count // 50 + 1}", "Success", False)

        # fetch all data, loop through pages by 50 items
        data: list[dict[str, Any]] = []
        for page in range(1, total_count // 50 + 2):
            # if fails, retry up to 3 times
            for _ in range(3):
                try:
                    print("Annict", f"Fetching page {page} of {total_count // 50 + 1}")
                    data.extend(self._fetch_annict_data(page)["works"])
                    time.sleep(3)
                    break
                except Exception:
                    print("Annict", f"Failed to fetch data on page {page}, retrying...", "Warning", False)
                    continue
            else:
                print("Annict", f"Failed to fetch data on page {page}, skipping...", "Error", False)
                continue
        self._data = deepcopy(data)
        print("Annict", f"Fetched {len(data)} items")
        return data

    # save data to file once fetched
    def save_data(self, path: str = "raw/annict.json") -> None:
        """
        Save data to file

        Args:
            path (str, optional): Path to file. Defaults to "annict.json".
        """
        with open(path, "w") as file:
            dump(self._data, file)

    def close(self) -> None:
        """Close Annict API wrapper"""
        self._data = []

__all__ = ["Annict"]
