from enum import Enum


class Sources(str, Enum):
    """
    A source available for retrieving data.
    """

    local = "local"
