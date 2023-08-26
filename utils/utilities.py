import discord
import random
import aiohttp
from PIL import Image
from io import BytesIO


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
    roles_with_color = [role for role in reversed(member.roles) if role.color != discord.Colour.default()]

    if roles_with_color:
        embed_color = roles_with_color[0].color
    else:
        embed_color = None

    if not embed_color and member.avatar:
        avatar_url = member.avatar.url
        avg_color = await get_average_color(avatar_url)
        return avg_color
    elif not embed_color and not member.avatar:
        return discord.Colour(random.randint(0, 0xFFFFFF))
    else:
        return embed_color


def progress_percentage(remain, total):
    assert remain <= total
    max_bare_size = 10  # 10 units for 100%
    remain_percent = 100 * remain // total // max_bare_size
    default_char = '◯'
    icon = "⬤"
    bar = (default_char * max_bare_size) + "]"
    bar_done = "[" + (icon * remain_percent)
    bar_remain = bar[remain_percent:]
    return f"\r{bar_done}{bar_remain} {remain_percent * 10}%"


def subtraction_percentage(bal, percentage_to_subtract):
    fraction = percentage_to_subtract / 100
    subtraction_amount = int(fraction * bal)
    result = bal - subtraction_amount
    return max(result, 0)
