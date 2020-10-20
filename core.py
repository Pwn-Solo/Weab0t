import asyncio
import functools
import itertools
import math
import random
import discord
import sqlite3
from discord.ext import commands
import youtube_dl
from async_timeout import timeout
import praw
from music import *
from animesearch import *
from mangasearch import *

TOKEN="NzY3ODA5MDczMDg1MDIyMjgw.X43T7A.DO7Efb5uK-OjHbBRvcajweJoSmE"
client = commands.Bot(command_prefix = '.')
reddit = praw.Reddit(client_id="Fl7RhNqbtCme_g",
    client_secret="UVCPCvFKnlQvXw5mV1Us1qPGxJo",
    username="heckorb0t",
    password="heckorb0t",
    user_agent="b0t")
client.remove_command('help')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round (client.latency * 1000)}ms ')

@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(colour=discord.Colour.green())
    embed.set_author(name='Help : list of commands available')
    embed.add_field(
        name='.ping', value='Returns bot respond time in milliseconds', inline=False)
    embed.add_field(name='.hentai', value='You pervert', inline=False)
    await ctx.send(embed=embed)

@client.command()
async def hpic(ctx):
    subreddit = reddit.subreddit("hentai")
    subtype = ['hot', 'new', 'top']
    choice = random.choice(subtype)
    if choice == 'top':
        submission = subreddit.top(limit=100)
    elif choice == 'hot':
        submission = subreddit.hot(limit=100)
    elif choice == 'new':
        submission = subreddit.new(limit=100)

    urls = []
    for submissions in submission:
        print(submissions.url)
        if submissions.url.endswith(('jpg', 'jpeg', 'png')):
            urls.append(submissions.url)
    url = random.choice(urls)
    em = discord.Embed()
    em.set_image(url=url)
    await ctx.send(embed=em)

@client.command()
async def hgif(ctx):
    subreddit = reddit.subreddit("HENTAI_GIF")
    subtype = ['hot', 'new', 'top']
    choice = random.choice(subtype)

    if choice == 'top':
        submission = subreddit.top(limit=100)
    elif choice == 'hot':
        submission = subreddit.hot(limit=100)
    elif choice == 'new':
        submission = subreddit.new(limit=100)

    urls = []
    for submissions in submission:
        print(submissions.url)
        if 'gif' in submissions.url:
            urls.append(submissions.url)

    url = random.choice(urls)
    em = discord.Embed()
    em.set_image(url=url)
    await ctx.send(embed=em)

@client.command(aliases=["ANIME"])
async def anime(ctx, *, title):
    embed = animeSearch(title)
    await ctx.send(embed=embed)

@client.command(aliases=["MANGA"])
async def manga(ctx, *, title):
    embed = mangaSearch(title)
    await ctx.send(embed=embed)

@client.event
async def on_message(ctx):
    if 'gay' in ctx.content:
        emoji = '\N{EYES}'
        await ctx.add_reaction(emoji)
    if 'gey' in ctx.content:
        emoji = '\N{EYES}'
        await ctx.add_reaction(emoji)
    if 'anda' in ctx.content:
        emoji = '\N{EGG}'
        await ctx.add_reaction(emoji)
    if 'egg' in ctx.content:
        emoji = '\N{EGG}'
        await ctx.add_reaction(emoji)
    if client.user in ctx.mentions:
        await ctx.channel.send("Kya re bhadwe !?")
    await client.process_commands(ctx)

client.add_cog(Music(client))

print("Bot is ready!")
client.run(TOKEN)