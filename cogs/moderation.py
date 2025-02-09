import discord
from discord.ext import bridge, commands
from datetime import timedelta

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(description="Kick someone")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason: str = "No reason provided"):
        await ctx.defer()
        if member.guild_permissions.administrator and not member.bot:
            return await ctx.respond(embed=discord.Embed(
                title="Failed", description="You can't kick another admin", color=discord.Color.red()
            ))

        try:
            try:
                kick_embed = discord.Embed(
                    title="Kick", description=f"You have been kicked from {ctx.guild.name}", color=discord.Color.red()
                )
                await member.send(embed=kick_embed)
            except discord.HTTPException:
                pass  # ignore errors if the user cannot receive DMs

            await member.kick(reason=reason)
            embed = discord.Embed(
                title="Success", description=f"'{member.name}' has been successfully kicked", color=discord.Color.green()
            )
            await ctx.respond(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="Failed", description=f"Failed to kick '{member.name}': {e}", color=discord.Color.red()
            )
            await ctx.respond(embed=embed)

    @bridge.bridge_command(description="Ban someone")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason: str = "No reason provided"):
        await ctx.defer()
        if member.guild_permissions.administrator and not member.bot:
            return await ctx.respond(embed=discord.Embed(
                title="Failed", description="You can't ban another admin", color=discord.Color.red()
            ))

        try:
            try:
                ban_embed = discord.Embed(
                    title="Ban", description=f"You have been banned from {ctx.guild.name}", color=discord.Color.red()
                )
                await member.send(embed=ban_embed)
            except discord.HTTPException:
                pass  

            await member.ban(reason=reason)
            embed = discord.Embed(
                title="Success", description=f"'{member.name}' has been successfully banned", color=discord.Color.green()
            )
            await ctx.respond(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="Failed", description=f"Failed to ban '{member.name}': {e}", color=discord.Color.red()
            )
            await ctx.respond(embed=embed)

    @bridge.bridge_command(description="Timeout a member")
    @bridge.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member:discord.Member, minutes:int=0, hours:int=0):
        duration = timedelta(minutes=minutes, hours=hours)
        if minutes==0 and hours==0:
            return await ctx.respond("Duration can't be 0 hours, 0 minutes!", ephemeral=True)  
        await member.timeout_for(duration)
        embed = discord.Embed(title="Success!", color=discord.Color.green(), description=f"{member.mention} succesfully timed out for {hours} hours {minutes} minutes.")
        await ctx.respond(embed=embed, ephemeral=True)
        embed2 = discord.Embed(title= "Timed out", description=f"You have been timed out for {hours}m {minutes}m in {ctx.guild.name}", color=discord.Colour.red())
        try:
            await member.send(embed=embed)
        except: 
            pass
    
    @bridge.bridge_command(description="Delete messages")
    @bridge.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount:int, member:discord.Member=None):
        if member != None:
            msg=[]
            async for m in ctx.channel.history():
                if len(msg) == amount:
                    break
                if m.author.id == member.id:
                    msg.append(m)
                await ctx.channel.delete_messages(msg)
                return await ctx.respond(f"Messages from {member.mention} has been removed." , ephemeral=True)    
        await ctx.respond("Hang on, purging messages . . .", ephemeral=True)    
        await ctx.channel.purge(limit=amount)

        
def setup(bot):
    bot.add_cog(Moderation(bot))
