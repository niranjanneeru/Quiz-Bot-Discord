import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='.')

mark = 30
qn = 1
teams = [
    "arnold",
    "bergman",
    "brad",
    "cameron",
    "chadwick",
    "connery",
    "leonardo",
    "nolan",
    "spielberg",
    "stan",
    "sylvestor",
    "tarantino",
]

super_users = [755703395989585942, 743472398896070657]


def make_scoreboard():
    scoreboard = {}
    for i in teams:
        scoreboard[i] = {"points": 0, "attended": []}
    return scoreboard


scoreboard = make_scoreboard()

answers = {}


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("Let's Informals"))


@bot.command(name="add")
async def add(ctx, x, y):
    if ctx.message.author.id not in super_users:
        await ctx.channel.send("[Error] Super User Command")
        return
    try:
        q = int(x)
        if q in answers:
            answers[q]['valid'].append(y)
        else:
            answers[q] = {"valid": [y, ], "marks": 20}
        await ctx.channel.send("Answer Added")
    except:
        raise commands.errors.BadArgument


@add.error
async def add_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.channel.send("[Error] Missing Arguments")
        await ctx.channel.send('''```.add <Question Number> <Answer>```''')
    elif isinstance(error, commands.errors.BadArgument):
        await ctx.channel.send("[Error] Argument Types Don't Match")


@bot.command(name="clear")
async def clear(ctx, *args):
    if ctx.message.author.id not in super_users:
        await ctx.channel.send("[Error] Super User Command")
        return
    global answers
    try:
        q = int(args[0])
        del answers[q]
    except IndexError:
        answers = {}
    except:
        raise commands.errors.BadArgument


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.errors.BadArgument):
        await ctx.channel.send("[Error] Argument Types Don't Match")


@bot.command(name="mark")
async def mark(ctx, x, y):
    if ctx.message.author.id not in super_users:
        await ctx.channel.send("[Error] Super User Command")
        return
    try:
        answers[int(x)]['marks'] = int(y)
        await ctx.channel.send(f"[Success] Mark Set to {y}")
    except:
        raise commands.errors.BadArgument


@mark.error
async def mark_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.channel.send("[Error] Missing Arguments")
        await ctx.channel.send('''```.mark <Question Number> <Mark>```''')
    elif isinstance(error, commands.errors.BadArgument):
        await ctx.channel.send("[Error] Argument Types Don't Match")


@bot.command(name="answer")
async def answer(ctx, x, y):
    if ctx.channel.name in teams:
        try:
            q = int(x)
            if q in scoreboard[ctx.channel.name]['attended']:
                await ctx.channel.send("[Error] Naughty Naughty! You have done it once")
                return
            if y in answers[q]['valid']:
                scoreboard[ctx.channel.name]['attended'].append(q)
                scoreboard[ctx.channel.name]['points'] += answers[q]['marks']
                await ctx.channel.send(f"[Success] Kumbayaa Kumbayaa! +{answers[q]['marks']} points")
            else:
                await ctx.channel.send(f"[Oops] Try Again!")
        except:
            await ctx.channel.send("[Error] Invalid Question Number")


@answer.error
async def answer_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.channel.send("[Error] Missing Arguments")
        await ctx.channel.send('''```.answer <Question Number> <Answer>```''')
    elif isinstance(error, commands.errors.BadArgument):
        await ctx.channel.send("[Error] Argument Types Don't Match")


@bot.command(name="all")
async def all(ctx):
    if ctx.message.author.id not in super_users:
        await ctx.channel.send("[Error] Super User Command")
        return
    if len(answers) != 0:
        embed = discord.Embed(title=f"__**Answers**__", color=0x03f8fc,
                              timestamp=ctx.message.created_at)
        for i in answers:
            embed.add_field(name=i, value=f'>{",".join(answers[i]["valid"])} - {answers[i]["marks"]}', inline=False)
        await ctx.channel.send(embed=embed)
    else:
        await ctx.channel.send("Empty Answer Set")


@bot.command(name='score')
async def score(ctx):
    if ctx.message.author.id not in super_users:
        await ctx.channel.send("[Error] Super User Command")
        return
    embed = discord.Embed(title=f"__**Scoreboard**__", color=0x03f8fc,
                          timestamp=ctx.message.created_at)
    for entry in scoreboard:
        embed.add_field(name=entry.upper(), value=f"points: {scoreboard[entry]['points']}", inline=False)
    await ctx.channel.send(embed=embed)


bot.run("TOKEN")
