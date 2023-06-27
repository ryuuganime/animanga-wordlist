from getopt import getopt, GetoptError
import os
import sys

from src.annict import Annict
from src.kaize import Kaize
from src.otakotaku import OtakOtaku


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

