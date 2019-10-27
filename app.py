import enum
import os

from PIL import Image, ImageDraw, ImageFont


CURRENT_DIR = os.path.dirname(__file__)

FONT_DIR = os.path.join(CURRENT_DIR, "roboto")

FONT_SIZE = 15

TAG_IMAGE_HEIGHT = 25
"""Define global tag image height
set to 25px
"""

BORDER_RADIUS = 5

WIDTH_PADDING = 5
"""Use to pad on right and left text
"""

TEXT_PADDING_RATIO = 7
"""Let's pretend that padding a single
char require 5px to be correctly fit
"""


class Border(enum.Enum):
    """This class aim to define
    border enumeration of a triangle/square
    """

    LEFT_TOP = 1
    LEFT_BOTTOM = 2
    RIGHT_TOP = 3
    RIGHT_BOTTOM = 4


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


def build_image(size, color, radius=None):
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


def tag_label(label):
    """This function create the label section of the tag

    Args:
        label (str): message to show in the tag title

    Return: and PIL.Image
    """

    width = (len(label) * TEXT_PADDING_RATIO)

    image = build_image(
        (width + WIDTH_PADDING, TAG_IMAGE_HEIGHT),
        (33, 33, 33),
        radius=None
    )

    return set_text(image, label)


if __name__ == "__main__":

    label = tag_label("Echo")

    #  Save image
    label.save("toto.png")
