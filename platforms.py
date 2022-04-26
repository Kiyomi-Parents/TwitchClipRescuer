import re
from enum import Enum
from typing import Tuple


class Platform(Enum):
    Twitch = (
        r"((https?://)?(clips\.twitch\.tv)/[\w-]+)",
        r"((https?://)?((\w+\.)twitch\.tv)/(\w+/)?clip/[\w-]+)"
    )
    Unknown = ("(.*)",)


def _get_platform(text: str) -> Tuple[Platform, str]:
    for platform in Platform.__members__.values():
        for pattern in platform.value:
            m = re.match(pattern, text)
            if m:
                return platform, m.group(0)
