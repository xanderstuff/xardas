from typing import Optional

from discord import Embed
from discord.ext.commands import Cog
from discord_slash import cog_ext, SlashContext, SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option
from pydantic import ValidationError

from xardas import Xardas


class XardasBuiltin(Cog):
    def __init__(self, bot: Xardas):
        self.bot = bot

    @cog_ext.cog_slash(
        name="reload",
        description='Reloads the entire bot\'s configuration or a single module.',
        options=[
            create_option(
                name='module',
                description='The module to reload',
                option_type=SlashCommandOptionType.STRING,
                required=False
            )
        ]
    )
    async def reload(self, ctx: SlashContext, module: Optional[str] = None):
        if not await self.bot.is_owner(ctx.author):
            await ctx.reply(embed=Embed(title=':x: Insufficient Permission',
                                        description=f'Only the bot\'s owner may reload it.'))
            return

        await ctx.defer()

        try:
            await self.bot.reload(module)

            if module is None:
                await ctx.reply(embed=Embed(title=':white_check_mark: Reloaded', description='» Bot reloaded.'))
            else:
                await ctx.reply(embed=Embed(title=':white_check_mark: Reloaded',
                                            description=f'» Module **\'{module}\'** reloaded.'))
        except KeyError:
            await ctx.reply(embed=Embed(title=':x: Invalid Invocation',
                                        description=f'Module **\'{module}\'** does not exist.'))
        except ValidationError as e:
            await ctx.reply(embed=Embed(title=':x: Configuration Error',
                                        description=f'Your configuration file is invalid.\n'
                                                    f'I\'ve sent you a DM with the details.'))

            chan = await ctx.author.create_dm()
            await chan.send(f'Here\'s what you did wrong:\n```{e}```')
        except Exception as e:
            await ctx.reply(embed=Embed(title=':x: Internal Error',
                                        description=f'An unexpected error occurred.\n'
                                                    f'I\'ve sent you a DM with the details.'))

            chan = await ctx.author.create_dm()
            await chan.send(f'Here\'s what happened:\n```{type(e)}:\n{e}```')

    @cog_ext.cog_slash(
        name="modules",
        description='Lists all modules currently loaded.',
    )
    async def modules(self, ctx: SlashContext):
        embed = Embed(title='Currently Loaded Modules', description='\n'.join(
            [f'» **{mod}**: {cfg.description}' for mod, cfg in self.bot.get_loaded_modules()]))
        await ctx.reply(embed=embed)

    @cog_ext.cog_slash(
        name="info",
        description='Get some information about the bot.',
    )
    async def info(self, ctx: SlashContext):
        embed = Embed(title='About Me',
                      description='Hey there, I\'m _Xardas_ and I was written by <@686669430930931791>.\n'
                                  '» GitHub ')
        await ctx.reply(embed=embed)


def load(bot: Xardas) -> Cog:
    return XardasBuiltin(bot)
