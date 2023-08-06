from typing import Iterable, Tuple

from .string import StringHelper
from .pattern import url_pattern


def unzip_arguments(args: tuple, kwargs: dict, pairs: Iterable[Tuple[int, str]]):
    """
    This is a helper function used extract to arguments from :args and :kwargs
    """
    unzipped = []
    for pair in pairs:
        try:
            unzipped.append(args[pair[0]])
        except IndexError:
            unzipped.append(kwargs[pair[1]])

    return unzipped
