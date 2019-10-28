import enum
import os

import click
from PIL import Image, ImageDraw, ImageFont


CURRENT_DIR = os.path.dirname(__file__)

FONT_DIR = os.path.join(CURRENT_DIR, "roboto")

FONT_SIZE = 15

BADGE_IMAGE_HEIGHT = 25
"""Define global badge image height
set to 25px
"""

RADIUS_WIDTH = 2

WIDTH_PADDING = 5
"""Use to pad on right and left text
"""

TEXT_PADDING_RATIO = 7
"""Let's pretend that padding a single
char require 5px to be correctly fit
"""

LABEL_BACKGROUND_COLOR = (33, 33, 33)


class StatusColor(enum.Enum):
    """Define color class enumeration
    To use for each status section
    """

    FAILURE = 1
    PENDING = 2
    INFO = 3
    UNKNOWN = 4
    PASSING = 5


COLOR_PALLETTE = {
    StatusColor.FAILURE: (244, 67, 54),
    StatusColor.PENDING: (63, 81, 181),
    StatusColor.INFO: (103, 58, 183),
    StatusColor.UNKNOWN: (158, 158, 158),
    StatusColor.PASSING: (76, 175, 80),
}


class Border(enum.Enum):
    """This class aim to define
    border enumeration of a triangle/square
    """

    LEFT_TOP = 1
    LEFT_BOTTOM = 2
    RIGHT_TOP = 3
    RIGHT_BOTTOM = 4


class ConcatStrategy(enum.Enum):
    """This class aim to enum concatenation strategy
    to join images
    """

    HORIZONTAL = 1
    VERTICAL = 2


def radius_image(image, radius, *args):
    """This function add a radius border to an
    image

    Inspired by @fraxel
    https://stackoverflow.com/a/11291419

    Args:
        image (Image): a pillow image
        radius (int): how much radius to curve
        args (List[Border]): which side of the border to radius

    Return: an image radius shaped
    """

    circle = Image.new("L", (radius * 2, radius * 2), 0)

    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)

    alpha = Image.new("L", image.size, 255)

    width, height = image.size

    for side in args:

        if side == Border.LEFT_TOP:
            alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))

        if side == Border.LEFT_BOTTOM:
            alpha.paste(
                circle.crop((0, radius, radius, radius * 2)),
                (0, height - radius),
            )

        if side == Border.RIGHT_TOP:
            alpha.paste(
                circle.crop((radius, 0, radius * 2, radius)),
                (width - radius, 0),
            )

        if side == Border.RIGHT_BOTTOM:
            alpha.paste(
                circle.crop((radius, radius, radius * 2, radius * 2)),
                (width - radius, height - radius),
            )

    image.putalpha(alpha)
    return image


def build_image(size, color=None, radius=None):
    """This function create an image using the size
    and the color

    Args:
        size (Tuple[str, str]): width and height of the image
        color (Tuple[str, str, str]): RGB color code
        radius (Tuple[int, List[str]]): radius information

    Return: an PIL.Image
    """

    image = Image.new("RGB", size, color=color)

    if radius:
        radius_size, sides = radius
        image = radius_image(image, radius_size, *sides)

    return image


def set_text(image, label):
    """This function insert text over an image

    Args:
        image (PIL.Image): pillow image
        label (str): text to add on the image

    Return: a PIL.Image
    """
    font = ImageFont.truetype(
        os.path.join(FONT_DIR, "Roboto-Light.ttf"), FONT_SIZE
    )

    _, height = image.size

    padding = (height / 2) - (FONT_SIZE / 2)

    draw = ImageDraw.Draw(image)
    draw.text((WIDTH_PADDING, padding), label, font=font, fill=(255, 255, 255))

    return image


def badge_label(label, color=None):
    """This function create the label section of the badge

    Args:
        label (str): message to show in the badge title

    Return: and PIL.Image
    """

    width = len(label) * TEXT_PADDING_RATIO

    image = build_image(
        (width + WIDTH_PADDING, BADGE_IMAGE_HEIGHT),
        color=color,
        radius=None
    )

    return set_text(image, label)


def concat_images(strategy, *args):
    """This function take a strategy in argument
    how to concatenate images

    Args:
        strategy (ConcatStrategy): way to concatenate
        args (List[PIL.Image]): images to concat

    Return: a PIL.Image
    """

    widths, heights = zip(*(x.size for x in args))

    if strategy == ConcatStrategy.HORIZONTAL:
        size = (sum(widths), max(heights))

    if strategy == ConcatStrategy.VERTICAL:
        size = (max(widths), sum(heights))

    board = Image.new("RGB", size)

    offset = 0

    for image in args:

        if strategy == ConcatStrategy.HORIZONTAL:
            board.paste(image, (offset, 0))
            offset += image.size[0]

        if strategy == ConcatStrategy.VERTICAL:
            board.paste(image, (0, offset))
            offset += image.size[1]

    return board


def badge(label, message, status):
    """This function generate a badge image

    Args:
        label (str): the message display in the label section
        message (str): message to display in the status
        status (int): integer value representing the status

    Return: PIL.Image
    """
    image = concat_images(
        ConcatStrategy.HORIZONTAL,
        badge_label(label, color=LABEL_BACKGROUND_COLOR),
        badge_label(message, color=COLOR_PALLETTE[StatusColor(status)]),
    )

    return radius_image(
        image,
        RADIUS_WIDTH,
        Border.LEFT_TOP,
        Border.LEFT_BOTTOM,
        Border.RIGHT_TOP,
        Border.RIGHT_BOTTOM,
    )


@click.command("badge")
@click.option('--label', help="The badge label.")
@click.option('--message', help="Message to display in the badge.")
@click.option('--output', help="Image output path")
@click.option(
    '--status',
    type=click.Choice(map(str, range(1,6))),
    help="Status of badge color switch"
)
def cli(label, message, status, output):
    """Command line interface to
    use badge
    """

    badge(label, message, int(status)).save(output)
    print("Image path: " + output)


if __name__ == "__main__":
    cli()
