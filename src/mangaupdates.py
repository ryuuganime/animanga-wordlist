from typing import Any
from json import dump
from copy import deepcopy

import requests
from time import sleep

from .commons import pretty_print as print
from const import USER_AGENT


class MangaUpdates:
    """MangaUpdates API Parser"""

    def __init__(self, username: str, password:str) -> None:
        """
        Initialize MangaUpdates API Parser

        Args:
            username (str): Username
            password (str): Password
        """
        self._base_url = "https://api.mangaupdates.com/v1"
        self._headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        self._data: list[dict[str, Any]] = []
        self._username = username
        self._password = password

    def _login(self) -> str:
        """
        Login to MangaUpdates

        Returns:
            str: Session Token
        """
        req_body = {
            "username": self._username,
            "password": self._password,
        }
        req = requests.put(
            f"{self._base_url}/account/login",
            json=req_body,
            headers=self._headers
        )
        if req.status_code == 200:
            print("MangaUpdates", "Login successful", "Success", False)
            json = req.json()
            context = json["context"]
            return context["session_token"]
        else:
            print("MangaUpdates", f"Login failed, reason: {req.text}", "Error", False)
            raise Exception("Login failed")

    def _fetch_mangaupdates_data(self) -> list[dict[str, Any]]:
        """
        Fetch data from MangaUpdates

        Returns:
            list[dict[str, Any]]: JSON data
        """
        session_token = self._login()
        self._headers["Authorization"] = f"Bearer {session_token}"
        req_body = {
            "page": 0,
            "per_page": 100,
            "order_by": "title",
        }
        data: list[dict[str, Any]] = []
        while True:
            req_body["page"] = int(req_body["page"]) + 1
            page = req_body["page"]
            print("MangaUpdates", f"Fetching page {page}...")
            req = requests.post(
                f"{self._base_url}/series/search",
                json=req_body,
                headers=self._headers
            )
            if req.status_code == 200:
                if len(req.json()["results"]) == 0:
                    break
                for entry in req.json()["results"]:
                    record = entry["record"]
                    data.append({
                        "title": record["title"],
                        "id": record["series_id"],
                        "type": record["type"],
                        "url": record["url"],
                        "year": record["year"],
                    })
                sleep(1)
            else:
                print("MangaUpdates", f"Request failed, reason: {req.text}", "Error", False)
                break
        return data

    def save_mangaupdates_data(self) -> list[dict[str, Any]]:
        """
        Save data to file

        Returns:
            list[dict[str, Any]]: JSON data
        """
        data = self._fetch_mangaupdates_data()
        with open("raw/mangaupdates.json", "w", encoding="utf-8") as f:
            dump(data, f, ensure_ascii=False)
        print("MangaUpdates", "Data saved to file", "Success", False)
        self._data = deepcopy(data)
        return self._data

    def close(self) -> None:
        """Close MangaUpdates API Parser"""
        self._data = []
