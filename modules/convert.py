import string

from discord import Embed
from discord.ext.commands import Cog, Bot, Context
from discord_slash import cog_ext, SlashCommandOptionType, SlashContext
from discord_slash.utils.manage_commands import create_option

full_name = {
    # length
    'mm': 'Millimetre',
    'cm': 'Centimetre',
    'dm': 'Decimetre',
    'm': 'Metre',
    'km': 'Kilometre',
    'in': 'Inch',
    'ft': 'Foot',
    'yd': 'Yard',
    'mi': 'Mile',
    'au': 'Astronomical Unit',
    'ly': 'Light Year',
    'pc': 'Parsec',

    # mass
    'mg': 'Milligram',
    'g': 'Gram',
    'kg': 'Kilogram',
    't': 'Metric Tonne',
    'oz': 'Ounce',
    'lb': 'Pound',

    # volume
    'ml': 'Millilitre',
    'cl': 'Centilitre',
    'l': 'Litre',
    'floz': 'Fluid Ounce [US]',
    'gi': 'Gill',
    'pt': 'Pint [US]',
    'qt': 'Quart [US]',
    'gal': 'Gallon [US]',

    # temperature
    '°F': 'Degrees Fahrenheit',
    '°C': 'Degrees Celsius',
    '°K': 'Degrees Kelvin'
}

to_si = {
    # length
    'mm': lambda x: x / 1000,
    'cm': lambda x: x / 100,
    'dm': lambda x: x / 10,
    'm': lambda x: x,
    'km': lambda x: x * 1000,
    'in': lambda x: x * 0.0254,
    'ft': lambda x: x * 0.3048,
    'yd': lambda x: x * 0.9144,
    'mi': lambda x: x * 1609.344,
    'au': lambda x: x * 149597870700,
    'ly': lambda x: x * 9460730472580.8 * 1000,
    'pc': lambda x: x * 30856775814671.9 * 1000,

    # mass
    'mg': lambda x: x / 1000,
    'g': lambda x: x,
    'kg': lambda x: x * 1000,
    't': lambda x: x * 1000 * 1000,
    'oz': lambda x: x * 28.34952,
    'lb': lambda x: x * 453.5924,

    # volume
    'ml': lambda x: x / 1000,
    'cl': lambda x: x / 100,
    'l': lambda x: x,
    'floz': lambda x: x * 0.02957344,
    'gi': lambda x: x * 0.11829411005,
    'pt': lambda x: x * 0.473175,
    'qt': lambda x: x * 0.94635,
    'gal': lambda x: x * 3.7854,

    # temperature
    '°f': lambda x: (x - 32) / 1.8 + 273.15,
    '°k': lambda x: x,
    '°c': lambda x: x + 273.15,
}

from_si = {
    # length
    'mm': lambda x: x * 1000,
    'cm': lambda x: x * 100,
    'dm': lambda x: x * 10,
    'm': lambda x: x,
    'km': lambda x: x / 1000,
    'in': lambda x: x / 0.0254,
    'ft': lambda x: x / 0.3048,
    'yd': lambda x: x / 0.9144,
    'mi': lambda x: x / 1609.344,
    'au': lambda x: x / 149597870700,
    'ly': lambda x: x / (9460730472580.8 * 1000),
    'pc': lambda x: x / (30856775814671.9 * 1000),

    # mass
    'mg': lambda x: x * 1000,
    'g': lambda x: x,
    'kg': lambda x: x / 1000,
    't': lambda x: x / (1000 * 1000),
    'oz': lambda x: x / 28.34952,
    'lb': lambda x: x / 453.5924,

    # volume
    'ml': lambda x: x * 1000,
    'cl': lambda x: x * 100,
    'l': lambda x: x,
    'floz': lambda x: x / 0.02957344,
    'gi': lambda x: x / 0.11829411005,
    'pt': lambda x: x / 0.473175,
    'qt': lambda x: x / 0.94635,
    'gal': lambda x: x / 3.7854,

    # temperature
    '°f': lambda x: x * 1.8 - 459.67,
    '°k': lambda x: x,
    '°c': lambda x: x - 273.15,
}


class Convert(Cog):
    def __init__(self, bot: Bot):
        self._bot = bot

    @cog_ext.cog_slash(
        name='cvlist',
        description='List all supported conversion units'
    )
    async def cvlist(self, ctx: Context):
        embed = Embed(title='Supported Units', description='\n'.join(
            [f'» **{name}**: {abbr}' for abbr, name in full_name.items()]))
        await ctx.reply(embed=embed)

    @cog_ext.cog_slash(
        name="cv",
        description='Converts a value from one unit to another.',
        options=[
            create_option(
                name='value',
                description='The value and unit to convert (ie. 10ml)',
                option_type=SlashCommandOptionType.STRING,
                required=True
            ),
            create_option(
                name='other',
                description='The unit to convert to (ie. pt)',
                option_type=SlashCommandOptionType.STRING,
                required=True
            ),
        ]
    )
    async def cv(self, ctx: SlashContext, value: str, other: str):
        val = ''
        unit = None

        for i, c in enumerate(value):
            if c in string.digits:
                val += c
            else:
                unit = value[i:].lower()
                break

        if unit is None:
            await ctx.reply(embed=Embed(title=':x: Invalid Invocation',
                                        description='No unit provided. Please attach the unit\'s\n'
                                                    'abbreviation to it\'s value (ie. _10ml_)'))
            return

        from_unit = unit

        try:
            val = float(val)
        except ValueError:
            await ctx.reply(embed=Embed(title=':x: Invalid Invocation',
                                        description=f'**{val}** is not a decimal value.'))
            return

        try:
            cv_to_m = to_si[from_unit]
            cv_from_m = from_si[other.lower()]
        except KeyError as e:
            await ctx.reply(embed=Embed(title=':x: Unsupported Unit',
                                        description=f'Unit **{e}** is not supported. Check _!cvlist_'))
            return

        res = cv_from_m(cv_to_m(val))
        await ctx.reply(
            embed=Embed(title='Unit Conversion', description=f'» **{val}{from_unit}** is **{round(res, 4)}{other}**.'))


def load(bot: Bot):
    return Convert(bot)


def unload(cog):
    pass
