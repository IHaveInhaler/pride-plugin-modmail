import io

import aiohttp
import cairosvg
import discord
from discord import app_commands
from discord.ext import commands

from core import checks
from core.models import PermissionLevel


TABLE = {
    "Agender": "agender_2014",
    "Aroace": "aroace_2018",
    "Aromantic": "aromantic_2014",
    "Asexual": "asexual_2010",
    "Bigender": "bigender_2014",
    "Bisexual": "bisexual_1998",
    "Gay Men": "gay_men_2019",
    "Genderfluid": "genderfluid_2012",
    "Genderqueer": "genderqueer_2011",
    "Intersex": "intersex_2013",
    "Intersex Inclusive Pride": "intersexInclusive_2021",
    "Labrys Lesbian": "labrysLesbian_1999",
    "Lesbian": "lesbian_2019",
    "Nonbinary": "nonbinary_2014",
    "Omnisexual": "omnisexual_2015",
    "Pangender": "pangender_2015",
    "Pansexual": "pansexual_2010",
    "Pink Union Jack": "pinkUnionJack_2009",
    "Polysexual": "polysexual_2012",
    "Pride": "pride_1979",
    "Progress Pride": "progressPride_2018",
    "Sapphic": "sapphic_2015",
    "South African Pride": "southAfricaPride_2010",
    "Transgender": "transgender_1999",
}

# Case-insensitive lookup so users don't have to match capitalisation exactly.
LOOKUP = {k.lower(): k for k in TABLE}

# Discord allows up to 25 choices per option — we have 24, so they all fit.
FLAG_CHOICES = [
    app_commands.Choice(name=name, value=name) for name in TABLE
]


class Pride(commands.Cog):
    """Show your pride with a beautiful flag! 🏳️‍🌈"""

    def __init__(self, bot):
        self.bot = bot

    async def generate_flag(self, flag_id: str) -> bytes:
        url = f"https://pride-flag.dev/api/flags/{flag_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                resp.raise_for_status()
                data = await resp.json()

        svg = data["svg"]
        return cairosvg.svg2png(
            bytestring=svg.encode("utf-8"),
            output_width=800,
            output_height=500,
        )

    @commands.hybrid_command(
        name="pride",
        description="Show your pride with a beautiful flag! 🏳️‍🌈",
    )
    @app_commands.describe(flag="Choose your pride flag")
    @app_commands.choices(flag=FLAG_CHOICES)
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def pride(self, ctx, *, flag: str = None):
        """Show your pride with a beautiful flag! 🏳️‍🌈"""
        await ctx.defer(ephemeral=False)

        if flag is None or flag.lower() not in LOOKUP:
            choices = ", ".join(f"`{name}`" for name in TABLE)
            await ctx.send(
                f"Please choose a flag. Available flags:\n{choices}",
                ephemeral=False,
            )
            return

        canonical = LOOKUP[flag.lower()]
        flag_id = TABLE[canonical]

        try:
            png_bytes = await self.generate_flag(flag_id)
        except Exception as error:
            print(f"Error in pride command: {error}")  # ERROR?!!??!? MARCH ASAP
            await ctx.send(
                "Sorry, there was an error generating the flag. Please try again!",
                ephemeral=False,
            )
            return

        filename = f"{flag_id}.png"
        file = discord.File(io.BytesIO(png_bytes), filename=filename)

        embed = discord.Embed(
            title=f"{canonical} Pride Flag",
            description=(
                "🏳️‍🌈 Pride is about love, acceptance, and being true to yourself! 💖"
            ),
            color=discord.Color.from_rgb(255, 105, 180),
        )
        embed.set_image(url=f"attachment://{filename}")

        await ctx.send(embed=embed, file=file, ephemeral=False)


async def setup(bot):
    await bot.add_cog(Pride(bot))
