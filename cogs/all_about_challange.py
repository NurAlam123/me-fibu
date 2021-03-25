import discord
import os
import pymongo
from discord.ext import commands
from discord.ext.commands import has_permissions

class Challenge(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @has_permissions(administrator=True,manage_guild=True)
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
    @has_permissions(administrator=True,manage_guild=True)
    async def removeSwap(self, ctx):
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"] #database
        tb = db["guild_data"] #table
        #guild = tb.find_one({"guild_id":ctx.guild.id})
        new_value = {"swap_channels": {"from_channel": None, "to_channel": None}}
        tb.update_one({"guild_id":ctx.guild.id},{"$set":new_value})
        await ctx.message.add_reaction("✅")
    
    @commands.command()
    @has_permissions(administrator=True,manage_guild=True)
    async def addXp(self, ctx, xp: int, member: discord.Member, *, challenge):
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"] #database
        tb = db["all_about_challenge"] #table
        user = tb.find_one({"user_id": member.id, "guild_id": ctx.guild.id})
        if user is not None:
            new_challenge = user["challenges"]
            print(new_challenge)
            print(challenge)
            new_challenge.append(challenge)
            print(3)
            old_xp = user["xp"]
            print(4)
            total_xp = xp + old_xp
            print(5)
            old_need_xp = user["need_xp"]
            print(6)
            old_level = user["level"]
            print(7)
            if total_xp >= need_xp:
                print(8)
                level = old_level + 1
                print(9)
                need_xp = old_need_xp + 100
                print(10)
                _xp = total_xp - old_need_xp
                print(11)
            else:
                print(12)
                _xp = total_xp
                print(13)
                need_xp = old_need_xp
                print(14)
                level = old_level
                print(16)
            tb.update({"user_id": member.id, "guild_id": ctx.guild.id}, {"$set": {"xp": _xp, "need_xp": need_xp, "level": level, "challenges": new_challenge}})
            print(17)
            await ctx.send("Data Updated")
        else:
            print(18)
            level = int(xp/100)
            print(19)
            need_xp = (level+1)*100
            print (20)
            new_xp = xp - (level*100)
            print(21)
            new_value = {"user_id": member.id, "guild_id": ctx.guild.id, "xp": new_xp, "need_xp": need_xp, "level": level, "challenges": challenge}
            print(22)
            tb.insert(new_value)
            print(23)
            await ctx.send("New Data Saved")
            
    @commands.command()
    @has_permissions(administrator=True,manage_guild=True)
    async def addChallenge(self, ctx, member: discord.Member, *, challenges):
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"] #database
        tb = db["all_about_challenge"] #table
        user = tb.find_one({"user_id": member.id, "guild_id": ctx.guild.id})
        if user is not None:
            new_challenges = user["challenges"]
            for challenge in challenges.split(","):
                new_challenges.append(challenge.split())
            tb.update({"user_id": member.id, "guild_id": ctx.guild.id}, {"$set": {"challenges": new_challenges}})
            await ctx.send("Data Successfully Added!")
        else:
            await ctx.send("User not found in the database.")
    
    @commands.command(aliases=["rmAllData"])
    @has_permissions(administrator=True,manage_guild=True)
    async def removeAllData(self, ctx, member: discord.Member):
       con_fibu = pymongo.MongoClient(os.getenv("DB"))
       db = con_fibu["fibu"]
       tb = db["all_about_challenge"]
#       all_data = tb.find_one({"user_id": member.id, "guild_id": ctx.guild.id})
       tb.delete_one({"user_id": member.id, "guild_id": ctx.guild.id})
       await ctx.send("Data Deleted")
       
       
    @commands.command()
    @has_permissions(administrator=True,manage_guild=True)
    async def showAllData(self, ctx):
            con_fibu = pymongo.MongoClient(os.getenv("DB"))
            db = con_fibu["fibu"]
            tb = db["all_about_challenge"]
            all_data = list(tb.find({"guild_id": ctx.guild.id}))
            if all_data == []:
                await ctx.send("No data found of this server.")
            else:
                for data in all_data:
                    user = ctx.guild.get_member(data["user_id"])
                    challenges = ", ".join(i for i in data["challenges"])
                    await ctx.send(f"==========\n**User:** {user}\n**User Id:** {data['user_id']}\n**XP:** {data['xp']}\n**Level:** {data['level']}\n**Challenges:** ```{challenges}```\n==========")
            
    @commands.Cog.listener("on_message")
    async def _msg(self, message):
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"] #database
        tb = db["guild_data"] #table
        try:
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
                        await to_channel.send(f"**Submitted By:** `{message.author}`\n**ID:** {message.author.id}\n**__Code:__**\n{message.content}")
            else:
                pass
        except:
            pass

    ## Permissions Handling
    @swap.error
    async def _error(self,ctx,error):
            if isinstance(error,commands.MissingPermissions):
                await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
    @removeSwap.error
    async def _error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
    @addXp.error
    async def _error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
    @showAllData.error
    async def _error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
    @removeAllData.error
    async def _error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
    @addChallenge.error
    async def _error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")       
            
            
def setup(bot):
    bot.add_cog(Challenge(bot))