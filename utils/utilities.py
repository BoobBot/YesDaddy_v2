import datetime
import math
import random
from io import BytesIO
from typing import Iterator, Sequence

import aiohttp
import discord
import holidays
from PIL import Image

from config.settings_config import affinity_titles, divorce_titles, claim_titles

xp_constant = 100


def is_today_weekend_or_holiday():
    today = datetime.date.today()
    # TODO: Add more countries
    country_code = ['US', 'CA', 'UK']
    # Check if today is a weekend
    if today.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
        return True

    # Check if today is a holiday
    if today in holidays.CountryHoliday(country_code):
        return True

    return False


def get_title(rank, title_type):
    titles = None
    if title_type == "affinity":
        titles = affinity_titles
    elif title_type == "divorce":
        titles = divorce_titles
    elif title_type == "claim":
        titles = claim_titles
    if titles is not None:
        for threshold, title in titles.items():
            if rank >= threshold:
                return title
    return None


async def get_average_color(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            image_data = await response.read()
            with Image.open(BytesIO(image_data)) as img:
                img = img.convert("RGB")
                img = img.resize((100, 100))
                pixel_data = img.load()
                width, height = img.size
                total_r, total_g, total_b = 0, 0, 0
                num_pixels = width * height

                for x in range(width):
                    for y in range(height):
                        r, g, b = pixel_data[x, y]
                        total_r += r
                        total_g += g
                        total_b += b

                avg_r = total_r // num_pixels
                avg_g = total_g // num_pixels
                avg_b = total_b // num_pixels

                return discord.Colour.from_rgb(avg_r, avg_g, avg_b)


async def generate_embed_color(member):
    embed_color = None
    if hasattr(member, "roles"):
        roles_with_color = [role for role in reversed(
            member.roles) if role.color != discord.Colour.default()]

        if roles_with_color:
            embed_color = roles_with_color[0].color

    if not embed_color and member.avatar:
        avatar_url = member.avatar.url
        avg_color = await get_average_color(avatar_url)
        return avg_color
    elif not embed_color and not member.avatar:
        return discord.Colour(random.randint(0, 0xFFFFFF))
    else:
        return embed_color


def calculate_level(user_xp):
    return math.floor(0.1 * math.sqrt(user_xp + xp_constant))


def calculate_remaining_xp(user_xp):
    current_level = calculate_level(user_xp)
    next_level = current_level + 1
    next_level_xp = ((next_level * 10) ** 2) - xp_constant  # Calculate the XP needed for the next level
    remaining_xp = next_level_xp - user_xp
    return remaining_xp, next_level_xp


def progress_percentage(remain, total):
    default_char = '◯'  # Define default_char here
    assert remain <= total, "remain should be less than or equal to total"
    max_bare_size = 10  # 10 units for 100%

    if total == 0:
        return f"0% {default_char * (max_bare_size - 1)}◯"

    remain_percent = min(100 * remain // total, 100) // max_bare_size
    icon = "⬤"
    bar = (default_char * max_bare_size)
    bar_done = (icon * remain_percent)
    bar_remain = bar[remain_percent:]
    return f"{bar_done}{bar_remain}"


def subtraction_percentage(bal, percentage_to_subtract):
    fraction = percentage_to_subtract / 100
    subtraction_amount = int(fraction * bal)
    result = bal - subtraction_amount
    return max(result, 0)


def search(s: str, substring: str) -> bool:
    """
    Searches ``s`` for ``substring``.
    ``substring`` can be an incomplete string with characters in a certain order,
    even with some missing in-between that can still yield a match.

    For example, if ``s`` is "test string", and ``substring`` is "ts sg", this will
    return True.
    """
    last_char_index = -1
    return not any((last_char_index := s.find(c, last_char_index + 1)) == -1 for c in substring)


class pagify(Iterator[str]):
    def __init__(
            self,
            text: str,
            delims: Sequence[str] = ("\n",),
            *,
            shorten_by: int = 8,
            page_length: int = 2000,
    ) -> None:
        self._text = text
        self._delims = delims
        self._shorten_by = shorten_by
        self._page_length = page_length - shorten_by
        self._start = 0
        self._end = len(text)

    def __repr__(self) -> str:
        text = self._text
        if len(text) > 20:
            text = f"{text[:19]}\N{HORIZONTAL ELLIPSIS}"
        return (
            "pagify("
            f"{text!r},"
            f" {self._delims!r},"
            f" shorten_by={self._shorten_by!r},"
            f" page_length={self._page_length + self._shorten_by!r}"
            ")"
        )

    def __length_hint__(self) -> int:
        return math.ceil((self._end - self._start) / self._page_length)

    def __iter__(self):
        return self

    def __next__(self) -> str:
        text = self._text
        page_length = self._page_length
        start = self._start
        end = self._end

        while (end - start) > page_length:
            stop = start + page_length
            closest_delim_it = (text.rfind(d, start + 1, stop) for d in self._delims)
            closest_delim = max(closest_delim_it)
            stop = closest_delim if closest_delim != -1 else stop
            to_send = text[start:stop]
            start = self._start = stop
            if len(to_send.strip()) > 0:
                return to_send

        if len(text[start:end].strip()) > 0:
            self._start = end
            return text[start:end]
        raise StopIteration
