"""
    Utility functions
"""

import re

color_regex = re.compile("#[0-9ABCDEFabcdef]{6}")


class PicodeException(Exception):

    def __init__(self, error_code: int, message: str):
        self.error_code = error_code
        self.message = message
        super(PicodeException, self).__init__(message)


class NoCodeNorFileName(PicodeException):

    def __init__(self, message):
        super(NoCodeNorFileName, self).__init__(100, message)


class ProvideCodeOrFileName(PicodeException):

    def __init__(self, message):
        super(ProvideCodeOrFileName, self).__init__(101, message)


class IncorrectLanguage(PicodeException):

    def __init__(self, message):
        super(IncorrectLanguage, self).__init__(102, message)


class ProvideFontNameOrFontPaths(PicodeException):

    def __init__(self, message):
        super(ProvideFontNameOrFontPaths, self).__init__(103, message)


class IncorrectFontSize(PicodeException):

    def __init__(self, message):
        super(IncorrectFontSize, self).__init__(104, message)


class IncorrectColor(PicodeException):

    def __init__(self, message):
        super(IncorrectColor, self).__init__(105, message)


def is_a_correct_hexadecimal_color(color: str):
    return len(color) == 7 and bool(color_regex.match(color))


def to_int(color: str):
    if not is_a_correct_hexadecimal_color(color):
        raise IncorrectColor(color + " is not a correct hexadecimal color")
    r = color[5:7]
    g = color[3:5]
    b = color[1:3]
    return int(r + g + b, 16)
