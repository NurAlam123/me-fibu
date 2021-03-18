import discord
import os
import pymongo
from discord.ext import commands

class Challenge(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.command()
    async def swap(self, ctx, from_channel: discord.TextChannel = None, to_channel: discord.TextChannel = None):
        if from_channel is None or to_channel is None:
            await ctx.send("Provide channel correctly!!")
        else:
            con_fibu = pymongo.MongoClient(os.getenv("DB"))
            db = con_fibu["fibu"] #database
            tb = db["guild_data"] #table
            get_guild = tb.find_one({"guild_id":ctx.guild.id})
            if get_guild!=None:
                new_value = {"swap_channels": {"from_channel": from_channel.id, "to_channel": to_channel.id}}
                tb.update_one({"guild_id":ctx.guild.id},{"$set":new_value})
                await ctx.message.add_reaction("✅")
            else:
                value = {"guild_id": ctx.guild.id, "swap_channels": {"from_channel": from_channel.id, "to_channel": to_channel.id}}
                tb.insert_one(value)
                await ctx.message.add_reaction("✅")
    
    @commands.Cog.listener("on_message")
    async def _msg(self, message):
        if message.channel.id == Challenge.channel1.id and message.author.id != self.client.user.id:
            con_fibu = pymongo.MongoClient(os.getenv("DB"))
            db = con_fibu["fibu"] #database
            tb = db["guild_data"] #table
            guild = tb.find_one({"guild_id":ctx.guild.id})
            from_channel = await self.client.fetch_channel(int(guild["swap_channels"]["from_channel"]))
            to_channel = await self.client.fetch_channel(int(guild["swap_channels"]["to_channel"]))
            await message.delete()
            await from_channel.send(f"{message.author.mention}, your code has been submitted!!")
            if message.content.__len__() >= 1990:
                await to_channel.send(f"**Submitted By:** `{message.author}`\n**__Code:__**\n")
                await to_channel.send(message.content)
            else:
                await to_channel.send(f"**Submitted By:** `{message.author}`\n**__Code:__**\n{message.content}")
            

def setup(bot):
    bot.add_cog(Challenge(bot))   