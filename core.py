import asyncio
import functools
import itertools
import math
import random
import discord
import sqlite3
from discord.ext import commands,tasks
import youtube_dl
from async_timeout import timeout
import praw
import datetime
from discord import Webhook, RequestsWebhookAdapter, File
#import giphy_client
#from giphy_client.rest import ApiException
from pprint import pprint
from music import *
from myanimelistdaily import *
from db_handler import eventmanager

NSFW_ID=712204655517499403
GENERAL_ID = 692648658210127956
WEBHOOK_TOKEN="BGrajX2DkzfexjfXN3WbTtuf--MdkSyYOGHyHyngRkfmpS6f4YPadOC3kPiEbGK3a-dS"
WEBHOOK_ID=768470281286451200
Announcement=768467811521134632
webhook = Webhook.partial(WEBHOOK_ID, WEBHOOK_TOKEN,adapter=RequestsWebhookAdapter())
TOKEN="NzY3ODA5MDczMDg1MDIyMjgw.X43T7A.DO7Efb5uK-OjHbBRvcajweJoSmE"
client = commands.Bot(command_prefix = '.')
reddit = praw.Reddit(client_id="Fl7RhNqbtCme_g",
    client_secret="UVCPCvFKnlQvXw5mV1Us1qPGxJo",
    username="heckorb0t",
    password="heckorb0t",
    user_agent="b0t")
client.remove_command('help')

discord_token = TOKEN
giphy_token = 'sCil6JxMoSLi7gPSyaUZ5n0cwvLtZ0Xb'

"""
api_instance = giphy_client.DefaultApi()
def search_gifs(query):
    try:
        return api_instance.gifs_search_get(giphy_token, query, limit=5, rating = 'g')

    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e

def gif_response(emotion):
    gifs = search_gifs(emotion)
    lst = list(gifs.data)
    gif = random.choices(lst)
    return gif[0].url

@client.command()

async def gif(ctx, *args):

    await ctx.channel.send(gif_response(args))
"""
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round (client.latency * 1000)}ms ')

@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(colour=discord.Colour.green())
    embed.set_author(name='Help : list of commands available')
    embed.add_field(name='.ping', value='Returns bot respond time in milliseconds', inline=False)
    embed.add_field(name='.hpic', value='hentai pics', inline=False)
    embed.add_field(name='.hgif', value='hentai gifs', inline=False)
    embed.add_field(name='.gif arg', value='sends agif basedon your arg', inline=False)
    embed.add_field(name='.p song', value='play song', inline=False)
    embed.add_field(name='.dc', value='disconnect', inline=False)
    embed.add_field(name='.s', value='skip', inline=False)
    embed.add_field(name='.queue', value='queue', inline=False)
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
    if (ctx.channel.id ==NSFW_ID): 
        await ctx.send(embed=em)
    else:
        await ctx.send("Use NSFW channel you pervert")
        
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
    if (ctx.channel.id ==NSFW_ID): 
        await ctx.send(embed=em)
    else:
        await ctx.send("Use NSFW channel you pervert")

@client.event
async def on_message(ctx):
    if 'gay' in ctx.content or 'gey' in ctx.content:
        emoji = '\N{EYES}'
        await ctx.add_reaction(emoji)
    if 'anda' in ctx.content or 'egg' in ctx.content:
        emoji = '\N{EGG}'
        await ctx.add_reaction(emoji)
    if 'ded' in ctx.content:
        await ctx.channel.send("Omae Wa Mou Shinderu!")
    if 'nani' in ctx.content:
        await ctx.channel.send("Ora! Ora! Ora!")
    if client.user in ctx.mentions:
        await ctx.channel.send("Kya re bhadwe !?")
    await client.process_commands(ctx)

time_day = 24*60*60

@tasks.loop(seconds = time_day)
async def time_check():
    await client.wait_until_ready()
    channel = client.get_channel(int(Announcement))
    now = datetime.datetime.now()
    month=now.strftime("%m")
    date=now.strftime("%d")
    if now.hour == 0 and now.minute == 0 and month=='10' and date=='12':
        await channel.send("@here Happy Ungli Diwas")

@tasks.loop(seconds = time_day)
async def csgo_check():
    await client.wait_until_ready()
    channel = client.get_channel(int(Announcement))
    now = datetime.datetime.now()
    if now.hour == 15 and now.minute == 25:
        await channel.send("@here CS:GO Time bous")

@tasks.loop(seconds = time_day)
async def stream_check():
    await client.wait_until_ready()
    channel = client.get_channel(int(Announcement))
    now = datetime.datetime.now()
    if now.hour == 22 and now.minute == 0:
        await channel.send("@here Stream/AmongUs Time bous")



@tasks.loop(seconds = time_day)
async def anime_check():
    await client.wait_until_ready()
    channel = client.get_channel(int(Announcement))
    now = datetime.datetime.now()
    print(now)
    if now.hour == 0 and now.minute == 0:
        data=animeschedule()
        embedlist=[]
        for i in range(len(data)):
            embed = discord.Embed(colour=discord.Colour.blue())
            embed.set_author(name=data[i][0])
            embed.set_image(url=data[i][1])
            embedlist.append(embed)
            if i==10:
                break
        webhook.send(embeds=embedlist)
        await channel.send("@here Enjoy ;)")    
              

@client.event
async def on_ready():
    time_check.start()
    anime_check.start()
    csgo_check.start()
    stream_check.start()
    activity = discord.Game(name = "Hentai ",type = 2)
    await client.change_presence(status=discord.Status.idle, activity=activity)
    print("Bot is ready!")



client.add_cog(Music(client))
client.add_cog(eventmanager(client))

client.run(TOKEN)
