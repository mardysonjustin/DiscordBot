import discord 
import asyncio
import random
import time
import aiohttp
import os

from discord.ext.pages import Paginator, Page
from discord.ext import bridge
from dotenv import load_dotenv

load_dotenv()

class DcBot(bridge.Bot):
    TOKEN = os.getenv("DISCORD_TOKEN")
    intents = discord.Intents.all()
    help_command=None

client = DcBot(intents=DcBot.intents, command_prefix="!",help_command=DcBot.help_command)

@client.listen()
async def on_ready():
    print(f"Ready. Logged in as {client.user.name}")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/help"))


@client.bridge_command(description="Check to see delay, nerd!")
async def ping(ctx): #ctx = context, what the command will do, how, and who ran it
    latency = (str(client.latency)).split('.')[1][1:3]
    await ctx.respond(f"Hello! Bot replied in {latency} ms")

pages =  [
    Page(
        embeds=[
            discord.Embed(title="PyCord Bot", description="A discord bot I made for general purposes with some fun stuffs!")
        ],
    ),
    Page(
        embeds=[
            discord.Embed(title="Moderation", description="**/ban\n/kick\n/timeout\n/purge**")
        ],
    ),
    Page(
        embeds=[
            discord.Embed(title="Utilities", description="**/lucky number\n/lucky color\n/check avatar**")
        ],
    ),
]

@client.bridge_command(description="Bot Information")
async def help(ctx):
    paginator= Paginator(pages=pages)
    try: await paginator.respond(ctx.interaction)
    except: await paginator.send(ctx)


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")
        print(f"Loaded {filename}")


async def main_bot(): #how the bot will run and start
    print("Bot starting . . .")
    await client.start(DcBot().TOKEN)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(main_bot()))
