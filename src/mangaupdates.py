from typing import Any, Literal
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
        self._session_token: str | None = None

    def _login(self) -> str:
        """
        Login to MangaUpdates

        Returns:
            str: Session Token
        """
        print("MangaUpdates", "Logging in...", "Info")
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

    def _logout(self) -> bool:
        """
        Logout from MangaUpdates

        Returns:
            bool: True if logout successful, False otherwise
        """
        print("MangaUpdates", "Logging out...", "Info")
        self._headers["Authorization"] = f"Bearer {self._session_token}"
        req = requests.post(
            f"{self._base_url}/account/logout",
            headers=self._headers
        )
        if req.status_code == 200:
            print("MangaUpdates", "Logout successful", "Success", False)
            return True
        else:
            print("MangaUpdates", f"Logout failed, reason: {req.text}", "Error", False)
            return False

    def _fetch_mangaupdates_data(self, path: Literal["publishers", "series"] = "series") -> list[dict[str, Any]]:
        """
        Fetch data from MangaUpdates

        Args:
            path (Literal["publishers", "series"], optional): Path to fetch data from. Defaults to "series".

        Returns:
            list[dict[str, Any]]: JSON data
        """
        self._headers["Authorization"] = f"Bearer {self._session_token}"
        req_body: dict[str, int | str] = {
            "page": 0,
            "perpage": 100,
        }
        match path:
            case "publishers":
                req_body["orderby"] = "name"
            case "series":
                req_body["order_by"] = "title"
        data: list[dict[str, Any]] = []
        while True:
            req_body["page"] = int(req_body["page"]) + 1
            page = req_body["page"]
            print("MangaUpdates", f"Fetching {path}, page {page}...")
            req = requests.post(
                f"{self._base_url}/{path}/search",
                json=req_body,
                headers=self._headers
            )
            json = req.json()
            if req.status_code != 200 or "status" in json:
                print("MangaUpdates", f"Request failed, reason: {req.text}", "Error", False)
                break
            if len(req.json()["results"]) == 0:
                break
            for entry in req.json()["results"]:
                record = entry["record"]
                match path:
                    case "series":
                        data.append({
                            "title": record["title"],
                            "id": record["series_id"],
                            "type": record["type"],
                            "url": record["url"],
                            "year": record["year"],
                        })
                    case "publishers":
                        data.append({
                            "name": record["name"],
                            "id": record["publisher_id"],
                            "url": record["url"],
                        })
            sleep(1)
        return data

    def save_mangaupdates_data(self) -> list[list[dict[str, Any]]]:
        """
        Save data to file

        Returns:
            list[dict[str, Any]]: JSON data
        """
        self._session_token = self._login()
        data = self._fetch_mangaupdates_data()
        with open("raw/mangaupdates_series.json", "w", encoding="utf-8") as f:
            dump(data, f, ensure_ascii=False)
        print("MangaUpdates", "Series data saved to file", "Success", False)
        data_pub = self._fetch_mangaupdates_data("publishers")
        with open("raw/mangaupdates_publishers.json", "w", encoding="utf-8") as f:
            dump(data_pub, f, ensure_ascii=False)
        print("MangaUpdates", "Publishers data saved to file", "Success", False)
        self._data_pub = deepcopy(data_pub)
        return [self._data, self._data_pub]

    def close(self) -> None:
        """Close MangaUpdates API Parser"""
        self._data = []
        self._logout()
