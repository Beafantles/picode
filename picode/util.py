"""
    Utility functions
"""

import re

color_regex = re.compile("#[0-9ABCDEFabcdef]{6}")


class NoCodeNorFileName(Exception):

    def __init__(self, message):
        super(NoCodeNorFileName, self).__init__(message)


class ProvideCodeOrFileName(Exception):

    def __init__(self, message):
        super(ProvideCodeOrFileName, self).__init__(message)


class IncorrectLanguage(Exception):

    def __init__(self, message):
        super(IncorrectLanguage, self).__init__(message)


class ProvideFontNameOrFontPaths(Exception):

    def __init__(self, message):
        super(ProvideFontNameOrFontPaths, self).__init__(message)


class IncorrectFontPathsFormat(Exception):

    def __init__(self, message):
        super(IncorrectFontPathsFormat, self).__init__(message)


class IncorrectFontSize(Exception):

    def __init__(self, message):
        super(IncorrectFontSize, self).__init__(message)


class IncorrectColor(Exception):

    def __init__(self, message):
        super(IncorrectColor, self).__init__(message)


def is_a_correct_hexadecimal_color(color: str):
    return bool(color_regex.match(color))


def to_int(color: str):
    if not is_a_correct_hexadecimal_color(color):
        raise IncorrectColor(color + " is not a correct hexadecimal color")
    r = color[5:7]
    g = color[3:5]
    b = color[1:3]
    return int(r + g + b, 16)
