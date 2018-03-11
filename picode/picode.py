"""
    A module to convert codes to pictures
"""

import sys
from PIL import Image, ImageFont, ImageDraw, ImageColor
from pygments import highlight
from pygments.lexers import guess_lexer, guess_lexer_for_filename, get_lexer_by_name
from pygments.formatters import ImageFormatter
from pygments.formatters.img import FontManager, FontNotFound
from io import BytesIO
from pygments.style import Style
from pygments.token import Token
from pygments import util
from os.path import dirname, abspath
import os
from picode.util import *

fonts_dir = dirname(abspath(__file__))

# Default configuration
# ---------------------

# Use monospaced font. Otherwise, the output would be horrible
DEFAULT_FONT_NAME = "Hack"
# Normal, Italic, Bold, BoldItalic
DEFAULT_FONT_PATHS = (os.path.join(fonts_dir, "data/Hack-Regular.ttf"),
                      os.path.join(fonts_dir, "data/Hack-Italic.ttf"),
                      os.path.join(fonts_dir, "data/Hack-Bold.ttf"),
                      os.path.join(fonts_dir, "data/Hack-BoldItalic.ttf"))

DEFAULT_FONT_SIZE = 14
DEFAULT_MARGIN = 30
DEFAULT_PADDING = 10
DEFAULT_SPACE_BETWEEN_LINES = 5
DEFAULT_SHOW_LINES_NUMBERS = True
DEFAULT_LINES_NUMBERS_PADDING = 10
DEFAULT_CODE_BACKGROUND_COLOR = "#151718"
DEFAULT_PICTURE_BACKGROUND_COLOR = "#A5B2BD"
DEFAULT_LINES_NUMBERS_COLOR = "#6D8A88"
DEFAULT_LINES_NUMBERS_BACKGROUND_COLOR = "#151718"
DEFAULT_HIGHLIGHT_COLOR = "#F7F0AB"
DEFAULT_LINES_NUMBERS_BOLD = False
DEFAULT_LINES_NUMBERS_ITALIC = False
DEFAULT_SHOW_LINES_NUMBERS_SEPARATOR = False
DEFAULT_STRIP_ALL = True
DEFAULT_STYLE = "monokai"

# ---------------------

DEFAULT_FONT_NAME_UNIX = "Bitstream Vera Sans Mono"
DEFAULT_FONT_NAME_WIN = "Courier New"


def to_pic(code: str = "",
           file_path: str = "",
           language: str = "",
           space_between_lines: int = DEFAULT_SPACE_BETWEEN_LINES,
           font_name: str = "",
           font_paths: list = [],
           font_size: int = DEFAULT_FONT_SIZE,
           padding: int = DEFAULT_PADDING,
           show_lines_numbers: bool = DEFAULT_SHOW_LINES_NUMBERS,
           lines_numbers_background_color:
           str = DEFAULT_LINES_NUMBERS_BACKGROUND_COLOR,
           lines_numbers_color: str = DEFAULT_LINES_NUMBERS_COLOR,
           show_lines_numbers_bold: bool = DEFAULT_LINES_NUMBERS_BOLD,
           show_lines_numbers_italic: bool = DEFAULT_LINES_NUMBERS_ITALIC,
           show_lines_numbers_separator:
           bool = DEFAULT_SHOW_LINES_NUMBERS_SEPARATOR,
           lines_numbers_padding: int = DEFAULT_LINES_NUMBERS_PADDING,
           lines_to_be_highlighted: list = [],
           highlight_color: str = DEFAULT_HIGHLIGHT_COLOR,
           picture_background_color: str = DEFAULT_PICTURE_BACKGROUND_COLOR,
           code_background_color: str = DEFAULT_CODE_BACKGROUND_COLOR,
           margin: int = DEFAULT_MARGIN,
           strip_all: bool = DEFAULT_STRIP_ALL,
           style=DEFAULT_STYLE):

    if not code and not file_path:
        raise NoCodeNorFileName(
            "Please provide a code or the path to a code file.")

    if code and file_path:
        raise ProvideCodeOrFileName(
            "Please provide a code or a file name but not both.")

    if font_name and font_paths:
        raise ProvideFontNameOrFontPaths(
            "Please provide a font name or the font paths but not both.")

    if not font_name and not font_paths:
        font_paths = DEFAULT_FONT_PATHS

    if font_size < 1:
        raise IncorrectFontSize("The font size must be >= 1.")

    if not is_a_correct_hexadecimal_color(lines_numbers_background_color):
        raise IncorrectColor(lines_numbers_background_color +
                             " is not a valid hexadecimal color.")

    if not is_a_correct_hexadecimal_color(lines_numbers_color):
        raise IncorrectColor(
            lines_numbers_color + " is not a valid hexadecimal color.")

    if not is_a_correct_hexadecimal_color(highlight_color):
        raise IncorrectColor(
            highlight_color + " is not a valid hexadecimal color.")

    if not is_a_correct_hexadecimal_color(picture_background_color):
        raise IncorrectColor(
            picture_background_color + " is not a valid hexadecimal color.")

    if not is_a_correct_hexadecimal_color(code_background_color):
        raise IncorrectColor(
            code_background_color + " is not a valid hexadecimal color.")

    lexer = None

    if file_path:
        with open(file_path, "r") as file:
            code = file.read()
        if language:
            try:
                lexer = get_lexer_by_name(language, stripall=strip_all)
            except util.ClassNotFound:
                raise IncorrectLanguage(
                    "There is no lexer for the programming language '" +
                    language + "'.")
        else:
            lexer = guess_lexer_for_filename(file_path, code)

    nb_lines = code.count("\n")

    if not lexer:
        if language:
            try:
                lexer = get_lexer_by_name(language, stripall=strip_all)
            except util.ClassNotFound:
                raise IncorrectLanguage(
                    "There is no lexer for the programming language '" +
                    language + "'.")
        else:
            lexer = guess_lexer(code, stripall=strip_all)

    formatter = ImageFormatter(
        image_format="PNG",
        line_pad=space_between_lines,
        image_pad=padding,
        line_numbers=show_lines_numbers,
        line_number_start=1,
        line_number_step=1,
        line_number_bg=lines_numbers_background_color,
        line_number_fg=lines_numbers_color,
        line_number_chars=len(str(nb_lines)),
        line_number_bold=show_lines_numbers_bold,
        line_number_italic=show_lines_numbers_italic,
        line_number_separator=show_lines_numbers_separator,
        line_number_pad=lines_numbers_padding,
        hl_lines=lines_to_be_highlighted,
        hl_color=highlight_color,
        style=style)
    formatter.background_color = to_int(code_background_color)

    # This is a tricky thing below
    # As we can't provide a font file path to instantiate a FontManager, I
    # improved Font Manger behavior manually. This allows us to use fonts
    # which are not natively installed on the device.
    # See https://github.com/nex3/pygments/blob/master/pygments/formatters/img.py
    # ---------------------------------------------------------------------------

    # Let's create a correct font manager, which can handle already installed
    # fonts but also files from files
    font_manager = None
    try:
        font_manager = FontManager(font_name, font_size)
    except FontNotFound:
        print("Couldn't find the font '" + font_name + "'. Using default font.")
        font_manager = FontManager(
            DEFAULT_FONT_NAME_WIN if sys.platform.startswith("win") else
            DEFAULT_FONT_NAME_UNIX, font_size)
    try:
        font_manager.fonts = {
            "NORMAL": ImageFont.truetype(font_paths[0], font_size),
            "ITALIC": ImageFont.truetype(font_paths[1], font_size),
            "BOLD": ImageFont.truetype(font_paths[2], font_size),
            "BOLDITALIC": ImageFont.truetype(font_paths[3], font_size)
        }
    except IndexError:
        raise IncorrectFontPathsFormat(
            "The font paths must be a list of 4 elements, representing the paths to the regular, italic, bold and bold+italic font files."
        )

    # Now, let's set this new font manager to our formatter and adapt font width and height
    formatter.fonts = font_manager
    formatter.fontw, formatter.fonth = font_manager.get_char_size()

    # ---------------------------------------------------------------------------

    result = highlight(code, lexer, formatter)

    code_image = Image.open(BytesIO(result))
    code_width, code_height = code_image.size

    im = Image.new(
        "RGB", (margin * 2 + code_width, margin * 2 + code_height),
        color=to_int(picture_background_color))

    im.paste(code_image,
             (margin, margin, margin + code_width, margin + code_height))

    return im
