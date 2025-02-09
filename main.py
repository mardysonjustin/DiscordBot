import discord 
import asyncio
import random
import time
import aiohttp
import os

from discord.ext import bridge
from dotenv import load_dotenv

load_dotenv()

class DcBot(bridge.Bot):
    TOKEN = os.getenv("DISCORD_TOKEN")
    intents = discord.Intents.all()

client = DcBot(intents=DcBot.intents, command_prefix="!")

@client.listen()
async def on_ready():
    print(f"Ready. Logged in as {client.user.name}")


@client.bridge_command(description="Check to see delay, nerd!")
async def ping(ctx): #ctx = context, what the command will do, how, and who ran it
    latency = (str(client.latency)).split('.')[1][1:3]
    await ctx.respond(f"Hello! Bot replied in {latency} ms")


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
