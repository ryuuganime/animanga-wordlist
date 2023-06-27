from .ansi import get_platform_rgb, return_ansi_code

def pretty_print(platform: str, message: str, cr: bool = True) -> None:
    """
    Pretty print message

    Args:
        platform (str): Platform name
        message (str): Message
    """
    platform_code = platform.lower()

    ansi_code = return_ansi_code(get_platform_rgb(platform_code))

    if cr:
        print(f"\r{ansi_code}[{platform}]\033[0m {message}", end="")
    else:
        print(f"{ansi_code}[{platform}]\033[0m {message}")
