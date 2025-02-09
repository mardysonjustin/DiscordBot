import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
my_id = os.getenv("MY_ID")

class AutoReply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
       
        if ("ily" in message.content.lower() or "i love you" in message.content.lower()) and message.author.id != my_id:
            await message.channel.send("This is me nung cinocode 'to and I made this autoreply for you hehe I love you too :>")

        if "dionela" in message.content.lower():
            await message.channel.send("BINIBINING MAY SALAMANDER")

        if "avo" in message.content.lower():
            await message.channel.send("HALLO AVOOOO !! ")  

def setup(bot):
    bot.add_cog(AutoReply(bot))
