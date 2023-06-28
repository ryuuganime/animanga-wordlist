# from getopt import getopt, GetoptError
# import os
# import sys

from src.annict import Annict
from src.kaize import Kaize
from src.otakotaku import OtakOtaku
from src.silveryasha import SilverYasha
from src.trakt import Trakt
from src.animeapi import AnimeApi
from src.myanimelist_jikan import MyAnimeList
from src.anilist import AniList


def main() -> None:
    """
    ryuuganime/animanga-wordlist main function

    License:
        GNU Affero General Public License v3.0

    Usage:
        python3 main.py [options]

    Options:
        -h, --help, -? : Show this help message and exit
                 --env : Skip loading .env file and use environment variables instead

    Examples:
        python3 main.py --env
    """


if __name__ == "__main__":

    kz = Kaize()
    kza, kzm = kz.save_data()
    kz.close()

    oo = OtakOtaku()
    ooa = oo.save_otakotaku_data()
    oo.close()

    sy = SilverYasha()
    sya = sy.save_silveryasha_data()
    sy.close()

    tr = Trakt()
    tra = tr.save_trakt_data()
    tr.close()

    aa = AnimeApi()
    aaa = aa.save_animeapi_data()
    aa.close()

    mal = MyAnimeList()
    mala, malm, malpro, malmg = mal.fetch_data_all()

    al = AniList()
    ala, alm = al.save_anilist_data()
