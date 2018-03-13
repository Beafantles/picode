"""
    A module to convert codes to pictures
"""

import sys
from argparse import ArgumentParser, FileType
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

__version__ = "1.1.1"

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
DEFAULT_SHOW_LINE_NUMBERS = False
DEFAULT_LINE_NUMBERS_PADDING = 10
DEFAULT_CODE_BACKGROUND_COLOR = "#151718"
DEFAULT_PICTURE_BACKGROUND_COLOR = "#A5B2BD"
DEFAULT_LINE_NUMBERS_COLOR = "#6D8A88"
DEFAULT_LINE_NUMBERS_BACKGROUND_COLOR = "#151718"
DEFAULT_HIGHLIGHT_COLOR = "#F7F0AB"
DEFAULT_LINE_NUMBERS_BOLD = False
DEFAULT_LINE_NUMBERS_ITALIC = False
DEFAULT_SHOW_LINE_NUMBERS_SEPARATOR = False
DEFAULT_STRIP_ALL = False
DEFAULT_STYLE = "monokai"

# ---------------------

DEFAULT_FONT_NAME_UNIX = "Bitstream Vera Sans Mono"
DEFAULT_FONT_NAME_WIN = "Courier New"


def to_pic(
        code: str = None,
        file_path: str = None,
        language: str = None,
        space_between_lines: int = DEFAULT_SPACE_BETWEEN_LINES,
        font_name: str = None,
        font_paths: list = [],
        font_size: int = DEFAULT_FONT_SIZE,
        padding: int = DEFAULT_PADDING,
        show_line_numbers: bool = DEFAULT_SHOW_LINE_NUMBERS,
        line_numbers_background_color:
        str = DEFAULT_LINE_NUMBERS_BACKGROUND_COLOR,
        line_numbers_color: str = DEFAULT_LINE_NUMBERS_COLOR,
        show_line_numbers_bold: bool = DEFAULT_LINE_NUMBERS_BOLD,
        show_line_numbers_italic: bool = DEFAULT_LINE_NUMBERS_ITALIC,
        show_line_numbers_separator: bool = DEFAULT_SHOW_LINE_NUMBERS_SEPARATOR,
        line_numbers_padding: int = DEFAULT_LINE_NUMBERS_PADDING,
        lines_highlighted: list = [],
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

    if not is_a_correct_hexadecimal_color(line_numbers_background_color):
        raise IncorrectColor(line_numbers_background_color +
                             " is not a valid hexadecimal color.")

    if not is_a_correct_hexadecimal_color(line_numbers_color):
        raise IncorrectColor(
            line_numbers_color + " is not a valid hexadecimal color.")

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

    formatter = None
    try:
        formatter = ImageFormatter(
            image_format="PNG",
            line_pad=space_between_lines,
            image_pad=padding,
            line_numbers=show_line_numbers,
            line_number_start=1,
            line_number_step=1,
            line_number_bg=line_numbers_background_color,
            line_number_fg=line_numbers_color,
            line_number_chars=len(str(nb_lines)),
            line_number_bold=show_line_numbers_bold,
            line_number_italic=show_line_numbers_italic,
            line_number_separator=show_line_numbers_separator,
            line_number_pad=line_numbers_padding,
            hl_lines=lines_highlighted,
            hl_color=highlight_color,
            style=style)
    except util.ClassNotFound:
        print("Warning: Couldn't find the style '" + style +
              "'. Using default style.")
        formatter = ImageFormatter(
            image_format="PNG",
            line_pad=space_between_lines,
            image_pad=padding,
            line_numbers=show_line_numbers,
            line_number_start=1,
            line_number_step=1,
            line_number_bg=line_numbers_background_color,
            line_number_fg=line_numbers_color,
            line_number_chars=len(str(nb_lines)),
            line_number_bold=show_line_numbers_bold,
            line_number_italic=show_line_numbers_italic,
            line_number_separator=show_line_numbers_separator,
            line_number_pad=line_numbers_padding,
            hl_lines=lines_highlighted,
            hl_color=highlight_color,
            style=DEFAULT_STYLE)
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
    if font_name:
        try:
            font_manager = FontManager(font_name, font_size)
        except FontNotFound:
            print("Warning: Couldn't find the font '" + font_name +
                  "'. Using default font.")
            font_manager = FontManager(
                DEFAULT_FONT_NAME_WIN if sys.platform.startswith("win") else
                DEFAULT_FONT_NAME_UNIX, font_size)
            font_manager.fonts = {
                "NORMAL": ImageFont.truetype(DEFAULT_FONT_PATHS[0], font_size),
                "ITALIC": ImageFont.truetype(DEFAULT_FONT_PATHS[1], font_size),
                "BOLD": ImageFont.truetype(DEFAULT_FONT_PATHS[2], font_size),
                "BOLDITALIC": ImageFont.truetype(DEFAULT_FONT_PATHS[3],
                                                 font_size)
            }
    else:
        try:
            font_manager = FontManager(
                DEFAULT_FONT_NAME_WIN if sys.platform.startswith("win") else
                DEFAULT_FONT_NAME_UNIX, font_size)
            font_manager.fonts = {
                "NORMAL": ImageFont.truetype(font_paths[0], font_size),
                "ITALIC": ImageFont.truetype(font_paths[1], font_size),
                "BOLD": ImageFont.truetype(font_paths[2], font_size),
                "BOLDITALIC": ImageFont.truetype(font_paths[3], font_size)
            }
        except (IndexError, OSError):
            print(
                "Warning: Couldn't properly load the font files. Using default font."
            )
            font_manager.fonts = {
                "NORMAL": ImageFont.truetype(DEFAULT_FONT_PATHS[0], font_size),
                "ITALIC": ImageFont.truetype(DEFAULT_FONT_PATHS[1], font_size),
                "BOLD": ImageFont.truetype(DEFAULT_FONT_PATHS[2], font_size),
                "BOLDITALIC": ImageFont.truetype(DEFAULT_FONT_PATHS[3],
                                                 font_size)
            }

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


def main(argv):

    parser = ArgumentParser(
        prog="picode",
        description="A tool to convert codes to pictures.",
        epilog="Version " + __version__)

    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="Shows version number and exit.")

    parser.add_argument(
        "files",
        nargs="*",
        help="Path to the file which is gonna be converted to picture.")

    parser.add_argument(
        "-o",
        "--output",
        nargs="*",
        metavar="output_file_name",
        help=
        "Specifies the names of the output pictures. No spaces in the names.")

    parser.add_argument(
        "-l",
        "--language",
        help="Specifies the programming language of the file.")

    parser.add_argument(
        "-sbl",
        "--space-between-lines",
        type=int,
        help="Specifies the space between each line.")

    parser.add_argument(
        "-fn",
        "--font-name",
        help=
        "Specifies the name of the font which is gonna be used for the picture. Use a monospaced font in order to get a decent result."
    )

    parser.add_argument(
        "-fp",
        "--font-paths",
        nargs=4,
        metavar=("Regular", "Italic", "Bold", "Italic+Bold"),
        help=
        "Specifies the paths of the font files which are gonna be used for the picture. The order is Regular, Italic, Bold, Bold + Italic. Use a monospaced font in order to get a decent result."
    )

    parser.add_argument(
        "-fs",
        "--font-size",
        type=int,
        help="Specifies the font size for the picture.")

    parser.add_argument(
        "-p", "--padding", type=int, help="Specifies the padding.")

    parser.add_argument(
        "-sln",
        "--show-line-numbers",
        action="store_true",
        help="Specifies if the line numbers must be shown or not.")

    parser.add_argument(
        "-lnbc",
        "--line-numbers-background-color",
        help="Specifies the background color for the line numbers.")

    parser.add_argument(
        "-lnc",
        "--line-numbers-color",
        help="Specifies the color of the line numbers.")

    parser.add_argument(
        "-slnb",
        "--show-line-numbers-bold",
        action="store_true",
        help="Specifies if the line numbers must be displayed in bold or not.")

    parser.add_argument(
        "-slni",
        "--show-line-numbers-italic",
        action="store_true",
        help="Specifies if the line numbers must be displayed in italic or not."
    )

    parser.add_argument(
        "-slns",
        "--show-line-numbers-separator",
        action="store_true",
        help=
        "Specifies if a separator between the line numbers and the code must be displayed or not."
    )

    parser.add_argument(
        "-lnp",
        "--line-numbers-padding",
        type=int,
        help="Specifies the padding between the code and the line numbers.")

    parser.add_argument(
        "-lh",
        "--lines-highlighted",
        nargs="*",
        metavar="line-number",
        type=int,
        help="Specifies the lines which must be highlighted.")

    parser.add_argument(
        "-hc",
        "--highlight-color",
        help="Specifies the color for the highlighted lines.")

    parser.add_argument(
        "-pbc",
        "--picture-background-color",
        help="Specifies the background color of the picture.")

    parser.add_argument(
        "-cbc",
        "--code-background-color",
        help="Specifies the background color of the code.")

    parser.add_argument(
        "-m",
        "--margin",
        type=int,
        help=
        "Specifies the margin between the code and the border of the picture.")

    parser.add_argument(
        "-sa",
        "--strip-all",
        action="store_true",
        help="Specifies if the code must be stripped or not.")

    parser.add_argument(
        "-s",
        "--style",
        help="Specifies the style which must be used for the picture.")

    args = parser.parse_args(argv[1:])

    if args.version:
        print(__version__)
        return 0

    if not args.files:
        print("No files were provided. Nothing to do.")
        return 0

    files = args.files
    output_files = args.output if args.output else []

    code_background_color = args.code_background_color if args.code_background_color else DEFAULT_CODE_BACKGROUND_COLOR
    font_name = args.font_name if args.font_name else None
    font_paths = args.font_paths if args.font_paths else []
    font_size = args.font_size if args.font_size else DEFAULT_FONT_SIZE
    highlight_color = args.highlight_color if args.highlight_color else DEFAULT_HIGHLIGHT_COLOR
    language = args.language if args.language else None
    line_numbers_background_color = args.line_numbers_background_color if args.line_numbers_background_color else DEFAULT_LINE_NUMBERS_BACKGROUND_COLOR
    line_numbers_color = args.line_numbers_color if args.line_numbers_color else DEFAULT_LINE_NUMBERS_COLOR
    line_numbers_padding = args.line_numbers_padding if args.line_numbers_padding else DEFAULT_LINE_NUMBERS_PADDING
    lines_highlighted = args.lines_highlighted if args.lines_highlighted else []
    margin = args.margin if args.margin else DEFAULT_MARGIN
    padding = args.padding if args.padding else DEFAULT_PADDING
    picture_background_color = args.picture_background_color if args.picture_background_color else DEFAULT_PICTURE_BACKGROUND_COLOR
    show_line_numbers = args.show_line_numbers
    show_line_numbers_bold = args.show_line_numbers_bold
    show_line_numbers_italic = args.show_line_numbers_italic
    show_line_numbers_separator = args.show_line_numbers_separator
    space_between_lines = args.space_between_lines if args.space_between_lines else DEFAULT_SPACE_BETWEEN_LINES
    strip_all = args.strip_all
    style = args.style if args.style else DEFAULT_STYLE

    for i, file in enumerate(files):
        try:
            im = to_pic(
                file_path=file,
                language=language,
                space_between_lines=space_between_lines,
                font_name=font_name,
                font_paths=font_paths,
                font_size=font_size,
                padding=padding,
                show_line_numbers=show_line_numbers,
                line_numbers_background_color=line_numbers_background_color,
                line_numbers_color=line_numbers_color,
                show_line_numbers_bold=show_line_numbers_bold,
                show_line_numbers_italic=show_line_numbers_italic,
                show_line_numbers_separator=show_line_numbers_separator,
                line_numbers_padding=line_numbers_padding,
                lines_highlighted=lines_highlighted,
                highlight_color=highlight_color,
                picture_background_color=picture_background_color,
                code_background_color=code_background_color,
                margin=margin,
                strip_all=strip_all,
                style=style)
        except PicodeException as e:
            print("Error n°" + str(e.error_code) + " : " + e.message)
            return e.error_code
        try:
            im.save(output_files[i])
        except IndexError:
            im.save(file[:file.rfind(".")] + ".png")


def run_main():
    sys.exit(main(sys.argv))


if __name__ == "__main__":
    run_main()
