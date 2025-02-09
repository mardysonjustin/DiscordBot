import discord
from discord.ext import commands, bridge
from datetime import timedelta

class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @bridge.bridge_group()
    async def automod():
        pass

    @automod.command(description="Set up the automoderation system")
    @bridge.has_permissions(administrator=True)
    async def enable(self, ctx):
        await ctx.defer()
        try:
            metadata = discord.AutoModActionMetadata(custom_message="This message was blocked.")
            await ctx.guild.create_auto_moderation_rule(name="Anti-Spam", reason="Automoderation rule by this bot", enabled=True, event_type=discord.AutoModEventType.message_send, trigger_type=discord.AutoModTriggerType.spam, trigger_metadata=discord.AutoModTriggerMetadata(), actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)]) 
            await ctx.guild.create_auto_moderation_rule(name="Censor Words", reason="Automoderation rule by this bot", enabled=True, event_type=discord.AutoModEventType.message_send, trigger_type=discord.AutoModTriggerType.keyword_preset, trigger_metadata=discord.AutoModTriggerMetadata(presets=[discord.AutoModKeywordPresetType.profanity,discord.AutoModKeywordPresetType.sexual_content,discord.AutoModKeywordPresetType.slurs]), actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)]) 
            await ctx.guild.create_auto_moderation_rule(name="Anti-mention", reason="Automoderation rule by this bot", enabled=True, event_type=discord.AutoModEventType.message_send, trigger_type=discord.AutoModTriggerType.mention_spam, trigger_metadata=discord.AutoModTriggerMetadata(mention_total_limit=3), actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)]) 
            await ctx.respond("Automoderation enabling is a success!", ephemeral=True)
        except:
            try:
                rulelist = await ctx.guild.fetch_auto_moderation_rules()
                for rules in rulelist:
                    await rules.delete()
                metadata = discord.AutoModActionMetadata("This message was blocked")
                await ctx.guild.create_auto_moderation_rule(name="Anti-Spam", reason="Automoderation rule by this bot", enabled=True, event_type=discord.AutoModEventType.message_send, trigger_type=discord.AutoModTriggerType.spam, trigger_metadata=discord.AutoModTriggerMetadata(), actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)]) 
                await ctx.guild.create_auto_moderation_rule(name="Censor Words", reason="Automoderation rule by this bot", enabled=True, event_type=discord.AutoModEventType.message_send, trigger_type=discord.AutoModTriggerType.keyword_preset, trigger_metadata=discord.AutoModTriggerMetadata(presets=[discord.AutoModKeywordPresetType.profanity,discord.AutoModKeywordPresetType.sexual_content,discord.AutoModKeywordPresetType.slurs]), actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)]) 
                await ctx.guild.create_auto_moderation_rule(name="Anti-mention", reason="Automoderation rule by this bot", enabled=True, event_type=discord.AutoModEventType.message_send, trigger_type=discord.AutoModTriggerType.mention_spam, trigger_metadata=discord.AutoModTriggerMetadata(mention_total_limit=3), actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)]) 
            except Exception as e:
                await ctx.respond(f"Automoderation enabling failed: {e}", ephemeral=True)
                return



    @automod.command(description="Turn off the automoderation system")
    @bridge.has_permissions(administrator=True)
    async def disable(self, ctx):
        await ctx.defer() 

        rulelist = await ctx.guild.fetch_auto_moderation_rules()
        
        if not rulelist:
            return await ctx.respond("No automoderation rules found.", ephemeral=True)

        try:
            for rule in rulelist:
                await rule.delete()
            
            await ctx.respond("Automoderation has been disabled!", ephemeral=True)
        
        except Exception as e:
            await ctx.respond(f"Failed to disable automoderation: {e}", ephemeral=True)


def setup(bot):
    bot.add_cog(Automod(bot))
    