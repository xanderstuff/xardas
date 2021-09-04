from datetime import datetime
from zoneinfo import ZoneInfo

from discord import Embed
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashCommandOptionType, SlashContext
from discord_slash.utils.manage_commands import create_option


class Timezones(Cog):
    def __init__(self, bot: Bot):
        self._bot = bot

    @cog_ext.cog_slash(
        name="unix",
        options=[
            create_option(
                name='time',
                description='The time to convert',
                option_type=SlashCommandOptionType.STRING,
                required=True
            ),
            create_option(
                name='tz',
                description='A timezone to use as a baseline (ie. US/Central)',
                option_type=SlashCommandOptionType.STRING,
                required=False
            ),
        ]
    )
    async def unix(self, ctx: SlashContext, time: str, tz: str = 'UTC'):
        """Convert a time of the format YYYY-MM-DD HH:MM[:SS] to a unix timestamp."""

        try:
            tz = ZoneInfo(tz)
        except Exception:
            await ctx.reply(embed=Embed(title=':x: Invalid invocation',
                                        description=f'Invalid timezone name: **{tz}**\n'
                                                    f'Use a timezone like this: **ETC/UTC-4**.'))
            return

        try:
            utc = datetime.strptime(time, '%Y-%d-%m %H:%M:%S')
        except ValueError:
            try:
                utc = datetime.strptime(time, '%Y-%d-%m %H:%M')
            except ValueError:
                await ctx.reply(embed=Embed(title=':x: Invalid invocation',
                                            description=f'Invalid time format: **{time}**\n'
                                                        f'Use the **YYYY-MM-DD HH:MM[:SS]** format.'))
                return

        local = utc.replace(tzinfo=tz)
        await ctx.reply(embed=Embed(title='Unix Timestamp',
                                    description=f'» **<t:{int(local.timestamp())}:F>**\n'
                                                f'_or as a raw unix timestamp:_ **{int(local.timestamp())}**'))


def load(bot: Bot):
    return Timezones(bot)


def unload(cog):
    pass
