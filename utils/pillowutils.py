from collections import Counter
from typing import Tuple, Union

from PIL import Image, ImageDraw, ImageFont


def get_dominant(image, average=False):
    colour_bands = [0, 0, 0]

    if average:
        colour_tuple = [None, None, None]

        for channel in range(3):
            # Get data for one channel at a time
            pixels = image.getdata(band=channel)
            values = []
            for pixel in pixels:
                values.append(pixel)
            colour_tuple[channel] = int(sum(values) / len(values))
        return tuple(colour_tuple)
    else:
        for band in range(3):
            pixels = image.getdata(band=band)
            c = Counter(pixels)
            colour_bands[band] = c.most_common(1)[0][0]

        return tuple(colour_bands)


def get_brightness(image) -> int:
    """
    Returns an integer between 0-255
    """
    dom_col = get_dominant(image, average=True)
    return (dom_col[0] * 0.299) + (dom_col[1] * 0.587) + (dom_col[2] * 0.114)


def mask_ellipsis(img: Image, offset: int = 0):
    img_mask = Image.new('L', img.size, 0)
    mask = ImageDraw.Draw(img_mask)
    mask.ellipse((offset, offset, img_mask.width - offset, img_mask.height - offset), fill=255)
    img.putalpha(img_mask)


def arc_bar(img: Image, xy: Tuple[int, int], size: Tuple[int, int],
            progress_pc: int, width: int,
            fill: Union[Tuple[int, int, int], Tuple[int, int, int, int]]):
    draw = ImageDraw.Draw(img)
    draw.arc((xy, size), start=-90, end=-90 + 3.6 * min(progress_pc, 100), width=width, fill=fill)


def font_auto_scale(font: ImageFont, text: str, desired_width: int, size_max: int,
                    size_min: int, stepping: int = 1) -> ImageFont:
    for size in range(size_max, size_min - 1, -stepping):
        new_font: ImageFont.FreeTypeFont = font.font_variant(size=size)
        longest_line = max(new_font.getsize(line)[0] for line in text.splitlines())
        if longest_line <= desired_width:
            return new_font

    fallback = font.font_variant(size=size_min)
    return fallback
