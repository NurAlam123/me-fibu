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
    async def addXp(self, ctx, xp: int, member: discord.Member, *, challenge = None):
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"] #database
        tb = db["all_about_challenge"] #table
        user = tb.find_one({"user_id": member.id, "guild_id": ctx.guild.id})
        if user is not None:
            new_challenge = list(user["challenges"])
            if challenge != None:
                new_challenge.append(challenge)
            else:
                pass
            old_xp = user["xp"]
            total_xp = xp + old_xp
            old_need_xp = user["need_xp"]
            old_level = user["level"]
            if total_xp >= old_need_xp:
                level = old_level + 1
                need_xp = old_need_xp + 100
                _xp = total_xp - old_need_xp
            else:
                _xp = total_xp
                need_xp = old_need_xp
                level = old_level
            tb.update({"user_id": member.id, "guild_id": ctx.guild.id}, {"$set": {"xp": _xp, "need_xp": need_xp, "level": level, "challenges": new_challenge}})
            await ctx.send("Data Updated")
        else:
            level = int(xp/100)
            need_xp = (level+1)*100
            new_xp = xp - (level*100)
            if challenge != None:
                new_value = {"user_id": member.id, "guild_id": ctx.guild.id, "xp": new_xp, "need_xp": need_xp, "level": level, "challenges": [challenge]}
            else:
                new_value = {"user_id": member.id, "guild_id": ctx.guild.id, "xp": new_xp, "need_xp": need_xp, "level": level, "challenges": []}
                
            tb.insert(new_value)
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
    
    @commands.command(aliases=["rmData"])
    @has_permissions(administrator=True,manage_guild=True)
    async def removeData(self, ctx, member: discord.Member):
       con_fibu = pymongo.MongoClient(os.getenv("DB"))
       db = con_fibu["fibu"]
       tb = db["all_about_challenge"]
       tb.delete_one({"user_id": member.id, "guild_id": ctx.guild.id})
       await ctx.send("Data Deleted")
    
    @commands.command(aliases=["rmAllData"])
    @has_permissions(administrator=True,manage_guild=True)
    async def removeAllData(self, ctx):
       con_fibu = pymongo.MongoClient(os.getenv("DB"))
       db = con_fibu["fibu"]
       tb = db["all_about_challenge"]
       tb.delete_one({"guild_id": ctx.guild.id})
       await ctx.send("Data Deleted")
     
    @commands.command(aliases=["rmxp"])
    @has_permissions(administrator=True,manage_guild=True)
    async def removeXp(self, ctx, xp: int, member: discord.Member):
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"]
        tb = db["all_about_challenge"]
        user = tb.find_one({"user_id": member.id, "guild_id": ctx.guild.id})
        if user is not None:
            old_xp = user["xp"]
            old_need_xp = user["need_xp"]
            old_level = user["level"]
            if xp > old_xp:
                remain_xp = xp - old_xp
                level = old_level-1
                need_xp = (level+1)*100
                _xp = need_xp - remain_xp
                tb.update({"user_id": member.id, "guild_id": ctx.guild.id}, {"$set": {"xp": _xp, "need_xp": need_xp, "level": level}})
            elif xp == old_xp:
                tb.update({"user_id": member.id, "guild_id": ctx.guild.id}, {"$set": {"xp": 0, "need_xp": old_need_xp, "level": old_level}})
            else:
                _xp = old_xp - xp
                tb.update({"user_id": member.id, "guild_id": ctx.guild.id}, {"$set": {"xp": _xp, "need_xp": old_need_xp, "level": old_level}})
            await ctx.send("Done")
        else:
            await ctx.send("User not found!!") 
   
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
    
    @commands.command()
    @has_permissions(administrator=True,manage_guild=True)
    async def showData(self, ctx, member: discord.Member):
            con_fibu = pymongo.MongoClient(os.getenv("DB"))
            db = con_fibu["fibu"]
            tb = db["all_about_challenge"]
            member_data = tb.find_one({"guild_id": ctx.guild.id, "user_id": member.id})
            if member_data is None:
                await ctx.send("No data found!!")
            else:
                user = ctx.guild.get_member(member_data["user_id"])
                challenges = ", ".join(i for i in member_data["challenges"])
                await ctx.send(f"==========\n**User:** {user}\n**User Id:** {member_data['user_id']}\n**XP:** {member_data['xp']}\n**Level:** {member_data['level']}\n**Challenges:** ```{challenges}```\n==========")

    ## Permissions Handling
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
    @removeData.error
    async def _error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
    @addChallenge.error
    async def _error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
    @removeXp.error
    async def _error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
    @showData.error
    async def _error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
            
            
def setup(bot):
    bot.add_cog(Challenge(bot))