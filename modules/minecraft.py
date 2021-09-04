import httpx
from discord import Embed
from discord.ext.commands import Cog, Bot
from discord_slash import cog_ext, SlashCommandOptionType, SlashContext
from discord_slash.utils.manage_commands import create_option

WIKI_URL = 'https://minecraft.fandom.com/wiki/%s'
WIKI_SEARCH = WIKI_URL % 'Special:Search?search=%s&go=Go'


class Minecraft(Cog):
    def __init__(self, bot: Bot):
        self._bot = bot

    @cog_ext.cog_slash(
        name="mcwiki",
        description='Searches the minecraft wiki for a term.',
        options=[
            create_option(
                name='term',
                description='The time to convert',
                option_type=SlashCommandOptionType.STRING,
                required=True
            ),
        ]
    )
    async def mcwiki(self, ctx: SlashContext, term: str):
        async with httpx.AsyncClient() as client:
            await ctx.defer()
            url = WIKI_URL % term.replace(' ', '_')
            result = await client.get(url)

            if result.status_code >= 400:
                url = WIKI_SEARCH % term.replace(' ', '+')
            else:
                url = result.headers.get('Location') if result.is_redirect else url

            await ctx.reply(content=url)

    @cog_ext.cog_slash(
        name="overworld",
        description='Converts Nether coordinates into Overworld coordinates.',
        options=[
            create_option(
                name='x',
                description='The x-coordinate',
                option_type=SlashCommandOptionType.INTEGER,
                required=True
            ),
            create_option(
                name='z',
                description='The z-coordinate',
                option_type=SlashCommandOptionType.INTEGER,
                required=True
            ),
        ]
    )
    async def overworld(self, ctx: SlashContext, x: int, z: int):
        await ctx.reply(embed=Embed(title='Overworld Coordinates', description=f'» **x = {x * 8}**\n» **z = {z * 8}**'))

    @cog_ext.cog_slash(
        name="nether",
        description='Converts nether Overworld into Nether coordinates.',
        options=[
            create_option(
                name='x',
                description='The x-coordinate',
                option_type=SlashCommandOptionType.INTEGER,
                required=True
            ),
            create_option(
                name='z',
                description='The z-coordinate',
                option_type=SlashCommandOptionType.INTEGER,
                required=True
            ),
        ]
    )
    async def nether(self, ctx: SlashContext, x: int, z: int):
        await ctx.reply(embed=Embed(title='Nether Coordinates', description=f'» **x = {int(x / 8)}**\n» **z = {int(z / 8)}**'))


def load(bot):
    return Minecraft(bot)


def unload(cog):
    pass
