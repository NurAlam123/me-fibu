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
    @commands.command()
    async def removeSwap(self, ctx):
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"] #database
        tb = db["guild_data"] #table
        #guild = tb.find_one({"guild_id":ctx.guild.id})
        new_value = {"swap_channels": {"from_channel": None, "to_channel": None}}
        tb.update_one({"guild_id":ctx.guild.id},{"$set":new_value})
        await ctx.message.add_reaction("✅")
    
    @commands.command()
    async def addXp(self, ctx, xp: int, *, members):
        ids_list = [int(i) for i in members.split(",")]
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"] #database
        tb = db["all_about_challenge"] #table
        for id in ids_list:
            user = tb.find_one({"user_id": id})
            guild = user["guild_id"]
            if user is not None and guild == ctx.guild.id:
                old_xp = user["xp"]
                total_xp = xp + old_xp
                new_level = int(total_xp/100)
                new_need_xp = (new_level+1)*100
                new_xp = total_xp - (new_level*100)
                tb.update({"user_id": id, "guild_id": ctx.guild.id}, {"$set": {"xp": new_xp, "need_xp": new_need_xp, "level": new_level}})
                await ctx.send("Data Updated")
            else:
                level = int(xp/100)
                need_xp = (level+1)*100
                new_xp = xp - (level*100)
                new_value = {"user_id": id, "guild_id": ctx.guild.id, "xp": new_xp, "need_xp": need_xp, "level": level, "challenges": []}
                tb.insert(new_value)
                await ctx.send("New Data Saved")
       
    @commands.command()
    async def showAllData(self, ctx):
            con_fibu = pymongo.MongoClient(os.getenv("DB"))
            db = con_fibu["fibu"]
            tb = db["all_about_challenge"]
            all_data = tb.find({"guild_id": ctx.guild.id})
            for data in all_data:
                await ctx.send(f"==========\n**User Id:** {data['user_id']}\n**XP:** {data['xp']}\n**Level:** {data['level']}\n**Challenges:** ```{', '.join(i for i in data['challenges'])}```\n==========")
            
    @commands.Cog.listener("on_message")
    async def _msg(self, message):
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"] #database
        tb = db["guild_data"] #table
        guild = tb.find_one({"guild_id":message.guild.id})
        from_channel_id = guild["swap_channels"]["from_channel"]
        to_channel_id = guild["swap_channels"]["to_channel"]
        if from_channel_id is not None:
            from_channel = await self.client.fetch_channel(int(from_channel_id))
            to_channel = await self.client.fetch_channel(int(to_channel_id))
            if message.channel.id == from_channel.id and message.author.id != self.client.user.id:
                await message.delete()
                await message.author.send(f"{message.author.mention}, your code has been submitted!!")
                if message.content.__len__() >= 1990:
                    await to_channel.send(f"**Submitted By:** `{message.author}`\n**ID:** {message.author.id}\n**__Code:__**\n")
                    await to_channel.send(message.content)
                else:
                    await to_channel.send(f"**Submitted By:** `{message.author}`\n**__Code:__**\n{message.content}")
        else:
            pass
            

def setup(bot):
    bot.add_cog(Challenge(bot))   