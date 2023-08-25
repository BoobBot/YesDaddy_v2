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


async def generate_embed_color(user):
    top_role = user.top_role
    embed_color = top_role.color if top_role.color != discord.Colour.default() else None
    if not embed_color and user.avatar:
        avatar_url = user.avatar_url_as(format='png')
        avg_color = await get_average_color(avatar_url)
    elif not embed_color and not user.avatar:
        avg_color = discord.Colour(random.randint(0, 0xFFFFFF))
    else:
        avg_color = embed_color

    return avg_color


