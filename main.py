from random import randint

import discord
from discord.ext import commands

from utils import make_scoreboard, super_users, get_teams, worst_list, make_tries, correct_list, wrong_list, teams

with open('secret.txt') as file:
    TOKEN = file.read().strip()

bot = commands.Bot(command_prefix='.')

tries = make_tries()
team_names = get_teams()

scoreboard = make_scoreboard()

answers = {}


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("Hasta la vista, baby"))


@bot.command(name="guide")
async def guide(ctx):
    embed = discord.Embed(title=f"__**Commands**__", description="Commands of Tyche", color=0x2e99dc,
                          timestamp=ctx.message.created_at)
    embed.set_thumbnail(url="https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg")
    embed.add_field(name="root", value=f'''```add - add options
        syntax:- .add <Question Number> <Answer>
        eg:- .add 1 answer

clear - clear options
        syntax:- .clear or .clear <q.no>
        eg:- .clear     #clears whole options
        eg:- .clears 1  #clear a option

score - view scoreboard
        eg:- .score

broadcast - .broadcast message

links - .links link```''', inline=False)
    # embed.add_field(name="user", value=f'''```answer - answer a question
    #     syntax:- .answer <Question Number> <Answer>
    #     eg:- .answer 1 answer```''', inline=False)
    await ctx.channel.send(embed=embed)


# mark - set marks for a question
#         syntax:- .mark <Question Number> <Mark>
#         eg:- .mark 1 45
#
# all - view all options
#         eg:- .all


@bot.command(name="add")
async def add(ctx, team_name: str, score):
    if ctx.message.author.id not in super_users:
        await ctx.channel.send("```[PERMISSION ERROR] Mrs. Robinson, you're trying to seduce me. Aren't you?```")
        return
    try:
        if team_name == "this":
            team_name = ctx.channel.name
        if team_name not in team_names.keys():
            r = randint(0, len(worst_list) - 1)
            await ctx.channel.send(f"```[NAME ERROR] {worst_list[r]}```")
            return
        score = int(score)
        if scoreboard[team_name]['points'] != 0:
            r = randint(0, len(worst_list) - 1)
            await ctx.channel.send(f"```[SCORE ONCE ADDED] {worst_list[r]}```")
            return
        scoreboard[team_name]['points'] = score
        await ctx.channel.send("```[PASSED] Score Added```")
    except Exception as e:
        print(e)
        raise commands.errors.BadArgument


@add.error
async def add_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.channel.send("```[MISSING ARGS] .add <team_name> <score>```")
    elif isinstance(error, commands.errors.BadArgument):
        await ctx.channel.send("```[INVALID ARGS TYPE] string int```")


@bot.command(name="clear")
async def clear(ctx):
    if ctx.message.author.id not in super_users:
        await ctx.channel.send("```[PERMISSION ERROR] Mrs. Robinson, you're trying to seduce me. Aren't you?```")
        return
    try:
        global scoreboard
        scoreboard = make_scoreboard()
        await ctx.channel.send("```[PASSED] Scoreboard Reset```")
    except:
        raise commands.errors.BadArgument


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.channel.send("```[MISSING ARGS] .clear```")


@bot.command(name="mark")
async def mark(ctx, x, y):
    if ctx.message.author.id not in super_users:
        await ctx.channel.send("```[PERMISSION ERROR] Mrs. Robinson, you're trying to seduce me. Aren't you?```")
        return
    try:
        answers[int(x)]['marks'] = int(y)
        await ctx.channel.send(f"```[PASSED] Mark -> {y}```")
    except:
        raise commands.errors.BadArgument


@mark.error
async def mark_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.channel.send("```[MISSING ARGS] .mark <Question Number> <Mark>```")
    elif isinstance(error, commands.errors.BadArgument):
        await ctx.channel.send("```[INVALID ARGS TYPE] int int```")


@bot.command(name="answer")
async def answer(ctx, x, y):
    if ctx.channel.name in teams:
        try:
            q = int(x)
            if q in scoreboard[ctx.channel.name]['attended']:
                r = randint(0, len(worst_list) - 1)
                await ctx.channel.send(f"```[MULTIPLE ATTEMPTS ERROR] {worst_list[r]}!```")
                return
            if tries[ctx.channel.name]['tries'][q] == 0:
                r = randint(0, len(wrong_list) - 1)
                await ctx.channel.send(f"```[TRIES EXHAUSTED] {wrong_list[r]}!```")
                return
            if y.lower() in answers[q]['valid']:
                scoreboard[ctx.channel.name]['attended'].append(q)
                scoreboard[ctx.channel.name]['points'] += answers[q]['marks']
                r = randint(0, len(correct_list) - 1)
                await ctx.channel.send(f"```[CORRECT] {correct_list[r]}! +{answers[q]['marks']} Coins```")
            else:
                r = randint(0, len(wrong_list) - 1)
                await ctx.channel.send(f"```[WRONG] {wrong_list[r]}!```")
            tries[ctx.channel.name]['tries'][q] -= 1
        except:
            r = randint(0, len(wrong_list) - 1)
            await ctx.channel.send(f"```[INVALID QUESTION] {wrong_list[r]}!```")


@answer.error
async def answer_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.channel.send("```[MISSING ARGS] .answer <Question Number> <Answer>```")
    elif isinstance(error, commands.errors.BadArgument):
        await ctx.channel.send("```[INVALID ARGS TYPE] int string```")


@bot.command(name="all")
async def all(ctx):
    if ctx.message.author.id not in super_users:
        await ctx.channel.send("```[PERMISSION ERROR] Mrs. Robinson, you're trying to seduce me. Aren't you?```")
        return
    if len(answers) != 0:
        embed = discord.Embed(title=f"__**Answers**__", color=0x2e99dc,
                              timestamp=ctx.message.created_at)
        embed.set_thumbnail(url="https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg")
        for i in answers:
            embed.add_field(name=i, value=f'``` {",".join(answers[i]["valid"])} - {answers[i]["marks"]}```',
                            inline=False)
        await ctx.channel.send(embed=embed)
    else:
        await ctx.channel.send("```[EMPTY] Answer Set```")


@bot.command(name='score')
async def score(ctx, *args):
    if ctx.message.author.id not in super_users:
        await ctx.channel.send("```[PERMISSION ERROR] Mrs. Robinson, you're trying to seduce me. Aren't you?```")
        return
    placeholder = ''
    if len(args) != 0:
        placeholder = args[0] + ' '
    embed = discord.Embed(title=f"__**{placeholder}Scoreboard**__", description="Pretty Formatted", color=0x03f8fc,
                          timestamp=ctx.message.created_at)
    embed.set_thumbnail(url="https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg")
    for entry in scoreboard:
        embed.add_field(name=entry.upper(), value=f"``` Coins: {scoreboard[entry]['points']}```", inline=True)
    await ctx.channel.send(embed=embed)


@bot.command(name='links')
async def broadcast(ctx, *args):
    if ctx.message.author.id not in super_users:
        await ctx.channel.send("```[PERMISSION ERROR] Mrs. Robinson, you're trying to seduce me. Aren't you?```")
        return
    message = ' '.join(args)
    for i in team_names:
        await bot.get_channel(team_names[i]).send(
            f"```[LINK BROADCAST]  Author:- {ctx.message.author.name} ```{message}")


@bot.command(name='broadcast')
async def broadcast(ctx, *args):
    if ctx.message.author.id not in super_users:
        await ctx.channel.send("```[PERMISSION ERROR] Mrs. Robinson, you're trying to seduce me. Aren't you?```")
        return
    message = ' '.join(args)
    for i in team_names:
        embed = discord.Embed(title=f"__**Broadcast**__", color=0x03f8fc,
                              timestamp=ctx.message.created_at)
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Message", value=f"{message}", inline=False)
        await bot.get_channel(team_names[i]).send(embed=embed)


bot.run(TOKEN)
