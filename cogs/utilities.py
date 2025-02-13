import discord
from discord.ext import commands, bridge
import random
from urllib.request import urlopen

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_group()
    async def random(self,ctx):
        pass 

    @random.command(description="Generate a lucky number!")
    async def number(self,ctx, lowernumber:int, uppernumber:int):
        number = random.randrange(lowernumber,uppernumber)
        await ctx.respond(f"Your lucky number from {lowernumber} to {uppernumber} is {number} !")

    @discord.message_command()
    async def getmessageid(self, ctx, message:discord.Message):
        await ctx.respond(f"{message.id}", ephemeral=True)

    @discord.user_command()
    async def getuserid(self,ctx, user:discord.User):
        await ctx.respond(f"{user.id}", ephemeral=True)

    
    @random.command(description="Generate a lucky color!")
    async def color(self, ctx):
        await ctx.defer()
        rcolor = lambda: random.randint(0, 255)
        color = "#%02X%02X%02X" % (rcolor(), rcolor(), rcolor())
        color = color.replace("#", "")
        crgblink = f"https://some-random-api.ml/canvas/misc/rgb?hex={color}"
        crgbpage = urlopen(crgblink)
        crgbbytes = crgbpage.read()
        crgbdecode = crgbbytes.decode("utf-8")
        crgb0 = crgbdecode.replace("{\"r\":", "")
        crgb1 = crgb0.replace("\"g\":","")
        crgb2 = crgb1.replace("\"\":","")
        crgb3 = crgb2.replace("}", "")
        crgb = crgb3.replace(",",", ")
        embed = discord.Embed(title=f"#{color}", description=f"Lucky Color")
        embed.add_field(name=f"RGB", value=f"{crgb}")
        embed.set_image(url="https://some-random-api.ml/canvas/misc/colorviewer?hex={color}")
        await ctx.respond(embed=embed)
    
    @bridge.bridge_command(description="See someone's avatar!")
    async def avatar(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author
        embed = discord.Embed(title=f"{str(member)}'s avatar: ", color=random.randrange(0,0xffffff))
        embed.set_image(url=member.avatar.url)
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Utilities(bot))