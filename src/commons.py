import re
from typing import Literal

from .ansi import get_platform_rgb, return_ansi_code


def pretty_print(
    platform: str,
    message: str,
    status: Literal[
        "Success",
        "Error",
        "Warning",
        "Info",
        "Running"
    ] = "Running",
    cr: bool = True
) -> None:
    """
    Pretty print message

    Args:
        platform (str): Platform name
        message (str): Message
        status (Literal["Success", "Error", "Warning", "Info", "Running"], optional): Status. Defaults to "Running".
        cr (bool, optional): Carriage return. Defaults to True.
    """
    # only grab \w characters, remove everything else including spaces, if any
    platform_code = re.sub(r"[^\w]", "", platform.lower())

    ansi_code = return_ansi_code(get_platform_rgb(platform_code))

    match status:
        case "Success":
            tag_code = "\033[1;32m[SUCCESS]\033[0m"
        case "Error":
            tag_code = "\033[1;31m[ ERROR ]\033[0m"
        case "Warning":
            tag_code = "\033[1;33m[WARNING]\033[0m"
        case "Info":
            tag_code = "\033[1;34m[I N F O]\033[0m"
        case "Running":
            tag_code = "\033[1;36m[RUNNING]\033[0m"

    if cr:
        print(f"\033[2K\r{ansi_code}[{platform}]\033[0m {tag_code} {message}", end="")
    else:
        print(f"\n{ansi_code}[{platform}]\033[0m {tag_code} {message}")
