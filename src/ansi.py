platform_rgb: dict[str, int] = {
    "allcin": 0xEC0A0A,
    "anidb": 0x2A2F46,
    "anilist": 0x2F80ED,
    "animeplanet": 0xE75448,
    "anisearch": 0xFDA37C,
    "ann": 0x2D50A7,
    "annict": 0xF65B73,
    "imdb": 0xF5C518,
    "kaize": 0x692FC2,
    "kitsu": 0xF85235,
    "lastfm": 0xD51007,
    "livechart": 0x67A427,
    "myanimelist": 0x2F51A3,
    "notify": 0xDEA99E,
    "otakotaku": 0xBE2222,
    "shikimori": 0x2E2E2E,
    "shoboi": 0xE3F0FD,
    "silveryasha": 0x0172BB,
    "simkl": 0x0B0F10,
    "syoboi": 0xE3F0FD,
    "tmdb": 0x09B4E2,
    "trakt": 0xED1C24,
    "tvdb": 0x6CD491,
    "tvtime": 0xFBD737,
}

def int_to_rgb(value: int) -> tuple[int, int, int]:
    """
    Convert integer to RGB tuple

    Args:
        value (int): Integer value

    Returns:
        tuple[int, int, int]: RGB tuple
    """
    return (value >> 16, value >> 8 & 0xff, value & 0xff)

def get_platform_rgb(platform: str) -> int:
    """
    Get platform RGB value

    Args:
        platform (Literal["annict"]): Platform name

    Returns:
        int: RGB value
    """
    return platform_rgb.get(platform, 0x000000)


def return_ansi_code(hex_code: int, background: bool = False) -> str:
    """
    Return ANSI code

    Args:
        hex_code (int): Hex code
        background (bool, optional): Switch between foreground and background. Defaults to False.

    Returns:
        str: ANSI code
    """

    r, g, b = int_to_rgb(hex_code)

    if background:
        return f"\033[48;2;{r};{g};{b}m"
    return f"\033[38;2;{r};{g};{b}m"
