from json import dump, loads
from typing import Any
from copy import deepcopy

import requests
from bs4 import BeautifulSoup as bs
from time import sleep

from .commons import pretty_print as print


class KaizeAnime:
    """Kaize via AnimeAPI data fetcher"""

    def __init__(self) -> None:
        """Initialize Kaize via AnimeAPI data fetcher"""
        self._base_url = "https://raw.githubusercontent.com/nattadasu/animeApi/v2/kz.unmapped.raw.json"
        self._data: list[dict[str, Any]] = []

    def _fetch_kaize_data(self) -> list[dict[str, Any]]:
        """
        Fetch data from Kaize via AnimeAPI

        Returns:
            list[dict[str, Any]]: JSON data
        """
        data = requests.get(
            f"{self._base_url}"
        ).text
        return loads(data)

    def save_kaize_data(self) -> list[dict[str, Any]]:
        """
        Save data to file

        Returns:
            list[dict[str, Any]]: JSON data
        """
        print("Kaize", "Saving Anime data to file...")
        data = self._fetch_kaize_data()
        with open("raw/kaize_anime.json", "w", encoding="utf-8") as f:
            dump(data, f, ensure_ascii=False)
        print("Kaize", "Anime data saved to file", "Success", False)
        self._data = deepcopy(data)
        return data

    def close(self) -> None:
        """Close Kaize via AnimeAPI data fetcher"""
        self._data = []

class KaizeManga:
    """Scrape Kaize's Manga index"""

    def __init__(self):
        """Initialize Kaize's Manga index scraper"""
        self._base_url = "https://kaize.io/manga/top"
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br"
        }
        self._data: list[dict[str, Any]] = []

    def _check_available_page(self) -> int:
        """
        Check available page by looping hundredth, tenth, and finally the unit

        Returns:
            int: Available page
        """
        url = self._base_url
        headers = self._headers

        def make_request(page: int):
            response = requests.get(f"{url}?page={page}", headers=headers)
            response.raise_for_status()
            return response.text

        def extract_data(html: str) -> list[Any]:
            soup = bs(html, "html.parser")
            return soup.find_all("div", {"class": "manga-list-element"})

        def is_valid_page(data: list[Any]) -> bool:
            return len(data) > 0 and data[0].find("div", {"class": "rank"})

        kzp = 0
        kzpg = 0

        # Check in hundreds
        while True:
            print("Kaize", f"Checking manga index in hundreds, page {kzp}")
            html = make_request(kzp)
            data = extract_data(html)
            if is_valid_page(data):
                kzpg = kzp
                kzp += 100
                sleep(3)
            else:
                break

        # Check in tens
        kzp = kzpg + 10
        while True:
            print("Kaize", f"Checking manga index in tens, page {kzp}")
            html = make_request(kzp)
            data = extract_data(html)
            if is_valid_page(data):
                kzpg = kzp
                kzp += 10
                sleep(3)
            else:
                break

        # Check in ones
        kzp = kzpg + 1
        while True:
            print("Kaize", f"Checking manga index in ones, page {kzp}")
            html = make_request(kzp)
            data = extract_data(html)
            if is_valid_page(data):
                kzpg = kzp
                kzp += 1
                sleep(3)
            else:
                break

        print("Kaize", f"Done checking, total pages in manga index: {kzpg}", "Success", False)

        return kzpg

    def _fetch_kaize_index(self, page: int = 1) -> list[dict[str, Any]]:
        """
        Fetch Kaize's Manga index

        Args:
            page (int, optional): Page. Defaults to 1.

        Returns:
            List[Dict[str, Any]]: Kaize's Manga index
        """
        url = self._base_url
        headers = self._headers
        uri = f"{url}?page={page}"
        response = requests.get(uri, headers=headers)
        response.raise_for_status()
        soup = bs(response.text, "html.parser")
        manga_elements = soup.find_all("div", {"class": "manga-list-element"})
        result: list[dict[str, Any]] = []

        for element in manga_elements:
            rank = element.find("div", {"class": "rank"}).text
            rank = int(rank.replace("#", "").strip())
            title = element.find("a", {"class": "name"}).text
            link = element.find("a", {"class": "name"})["href"].split("/")[-1]
            result.append({"rank": rank, "title": title, "slug": link})

        return result

    def save_kaize_data(self) -> list[dict[str, Any]]:
        """
        Save data to file

        Returns:
            list[dict[str, Any]]: Kaize's Manga index
        """
        print("Kaize", "Saving Manga data to file...", "Info", False)
        pages = self._check_available_page()
        result: list[dict[str, Any]] = []
        for page in range(1, pages + 1):
            print("Kaize", f"Fetching manga, page {page} of {pages}")
            result.extend(self._fetch_kaize_index(page))
            # sleep(1)
        with open("raw/kaize_manga.json", "w", encoding="utf-8") as f:
            dump(result, f, ensure_ascii=False)
        print("Kaize", "Data saved to file", "Success", False)
        return result

    def close(self) -> None:
        """Close Kaize's Manga index scraper"""
        self._data = []

class Kaize:
    """Generic Wrapper for KaizeAnime and KaizeManga"""

    def __init__(self) -> None:
        """Initialize Kaize Wrapper"""
        self._anime = KaizeAnime()
        self._manga = KaizeManga()

    def save_data(self) -> list[list[dict[str, Any]]]:
        """Save data to file"""
        anime = self._anime.save_kaize_data()
        manga = self._manga.save_kaize_data()

        return [anime, manga]

    def close(self) -> None:
        """Close Kaize Wrapper"""
        self._anime.close()
        self._manga.close()

__all__ = ["KaizeAnime", "KaizeManga", "Kaize"]
