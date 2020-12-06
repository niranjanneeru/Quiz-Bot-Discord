from random import randint

import discord
from discord.ext import commands

from utils import make_tries, make_scoreboard, super_users, wrong_list, worst_list, correct_list, teams

with open('secret.txt') as file:
    TOKEN = file.read().strip()

bot = commands.Bot(command_prefix='.')

tries = make_tries()

scoreboard = make_scoreboard()

answers = {}


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("Hasta la vista, baby"))


@bot.command(name="help")
async def guide(ctx):
    embed = discord.Embed(title=f"__**Commands**__", color=0x03f8fc,
                          timestamp=ctx.message.created_at)
    embed.add_field(name="root", value=f"```add - add options"
                                       f"   syntax:- .add <Question Number> <Answer>"
                                       f"   eg:- add 1 answer"
                                       f"clear - clear options"
                                       f"   syntax:- .clear or .clear <q.no>"
                                       f"   eg:- .clear     #clears whole options"
                                       f"   eg:- .clears 1  #clears for a specific option"
                                       f"mark - set marks for a question"
                                       f"   syntax:- .mark <Question Number> <Mark>"
                                       f"   eg:- .mark 1 45"
                                       f"all - view all options"
                                       f"   eg:- .all"
                                       f"score - view scoreboard"
                                       f"   eg:- .all```", inline=False)
    embed.add_field(name="user", value=f"```answer - answer a question"
                                       f"   syntax:- .answer <Question Number> <Answer>"
                                       f"   eg:- .answer 1 answer```", inline=False)
    await ctx.channel.send(embed=embed)


@bot.command(name="add")
async def add(ctx, x, y):
    if ctx.message.author.id not in super_users:
        await ctx.channel.send("```[PERMISSION ERROR] Mrs. Robinson, you're trying to seduce me. Aren't you?```")
        return
    try:
        q = int(x)
        if q in answers:
            answers[q]['valid'].append(y.lower())
        else:
            answers[q] = {"valid": [y.lower(), ], "marks": 20}
        for i in tries:
            tries[i]['tries'][q] = 3
        await ctx.channel.send("```[PASSED] Answer Added```")
    except:
        raise commands.errors.BadArgument


@add.error
async def add_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.channel.send("```[MISSING ARGS] .add <Question Number> <Answer>```")
    elif isinstance(error, commands.errors.BadArgument):
        await ctx.channel.send("```[INVALID ARGS TYPE] int string```")


@bot.command(name="clear")
async def clear(ctx, *args):
    if ctx.message.author.id not in super_users:
        await ctx.channel.send("```[PERMISSION ERROR] Mrs. Robinson, you're trying to seduce me. Aren't you?```")
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
        await ctx.channel.send("```[INVALID ARGS TYPE] int```")


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
                await ctx.channel.send(f"```[CORRECT] {correct_list[r]}! +{answers[q]['marks']} points```")
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
        embed = discord.Embed(title=f"__**Answers**__", color=0x03f8fc,
                              timestamp=ctx.message.created_at)
        for i in answers:
            embed.add_field(name=i, value=f'>{",".join(answers[i]["valid"])} - {answers[i]["marks"]}', inline=False)
        await ctx.channel.send(embed=embed)
    else:
        await ctx.channel.send("```[EMPTY] Answer Set```")


@bot.command(name='score')
async def score(ctx):
    if ctx.message.author.id not in super_users:
        await ctx.channel.send("```[PERMISSION ERROR] Mrs. Robinson, you're trying to seduce me. Aren't you?```")
        return
    embed = discord.Embed(title=f"__**Scoreboard**__", color=0x03f8fc,
                          timestamp=ctx.message.created_at)
    for entry in scoreboard:
        embed.add_field(name=entry.upper(), value=f"points: {scoreboard[entry]['points']}", inline=False)
    await ctx.channel.send(embed=embed)


bot.run(TOKEN)
