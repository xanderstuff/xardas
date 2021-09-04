import random

from discord import Embed
from discord.ext.commands import Cog, Bot
from discord_slash import SlashContext, SlashCommandOptionType, cog_ext
from discord_slash.utils.manage_commands import create_option


class DnD(Cog):
    def __init__(self, bot: Bot):
        self._bot = bot

    @cog_ext.cog_slash(
        name="roll",
        description='Roll some dice.',
        options=[
            create_option(
                name='throw',
                description='A string denoting the number of dice to throw (ie. 2d5).',
                option_type=SlashCommandOptionType.STRING,
                required=True
            ),
        ]
    )
    async def roll(self, ctx: SlashContext, throw: str):
        """Roll some dice. Usage: #d$ where # is the number of dice to roll and $ is the number of sides to the dice."""
        rolls = []

        a, b = throw.lower().split('d')
        try:
            a = int(a)
            b = int(b)
        except ValueError:
            await ctx.reply(embed=Embed(title=':x: Invalid Roll',
                                        description='Please provide a number followed by a _d_ followed by a number.'))
            return

        if a > 100:
            await ctx.reply(embed=Embed(title=':x: Invalid Roll',
                                        description=f'I\'m sorry, where am I supposed to get **{a}** dice from?'))
            return

        if a == 0 or b == 0:
            await ctx.reply(embed=Embed(title=':x: Invalid Roll',
                                        description=f'You get nothing! You LOSE! Good day sir!'))
            return

        if a < 0 or b < 0:
            await ctx.reply(embed=Embed(title=':x: Invalid Roll',
                                        description=f'You wake up in the depths of hell. You have been banished\n'
                                                    f'to eternal pain and suffering.'))

            return

        for i in range(a):
            rolls.append(random.randint(1, b))

        summed = sum(rolls)

        rolls_str = ", ".join([f'**{x}**' for x in rolls[:-1]]) + f', and **{rolls[-1]}**'
        embed = Embed(title=f'{ctx.author.display_name}\'s Roll',
                      description=f'You rolled:\n\n» {rolls_str}\n_Sum:_ **{summed}**')

        await ctx.reply(embed=embed)


def load(bot: Bot):
    return DnD(bot)


def unload(cog):
    pass
