import discord
import os
import pymongo
from discord.ext import commands
from discord.ext.commands import has_permissions

class Challenge(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.command()
    @has_permissions(administrator=True, manage_guild=True)
    async def addXp(self, ctx, xp: int, member: discord.Member, *, challenge = None):
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"] #database
        tb = db["all_about_challenge"] #table
        user = tb.find_one({
            "user_id": member.id,
            "guild_id": ctx.guild.id
        })
        if user:
            new_challenge = list(user["challenges"])
            if challenge:
                new_challenge.append(challenge)
                
            old_xp = user["xp"]
            total_xp = old_xp + xp
            old_need_xp = user["need_xp"]
            old_level = user["level"]
            if total_xp >= old_need_xp:
                level = int(total_xp/100)
                need_xp = (level+1)*100
                _xp = total_xp - ((level)*100)
            else:
                _xp = total_xp
                need_xp = old_need_xp
                level = old_level
            tb.update({
               "user_id": member.id,
                "guild_id": ctx.guild.id
            },
            {
                "$set": {
                    "xp": _xp, 
                    "need_xp": need_xp,
                    "level": level,
                    "challenges": new_challenge
                }
            })
            await ctx.reply(f"{member}'s Data Updated")
        else:
            level = int(xp/100)
            need_xp = (level+1)*100
            new_xp = xp - (level*100)
            if challenge:
                new_value = {
                    "user_id": member.id,
                    "guild_id": ctx.guild.id,
                    "xp": new_xp,
                    "need_xp": need_xp, 
                    "level": level,
                    "challenges": [challenge]
                }
            else:
                new_value = {
                    "user_id": member.id,
                    "guild_id": ctx.guild.id, 
                    "xp": new_xp,
                    "need_xp": need_xp,
                    "level": level,
                    "challenges": []
                }
            tb.insert(new_value)
            await ctx.reply("New Data Saved")
            
    @commands.command()
    @has_permissions(administrator=True,manage_guild=True)
    async def addChallenge(self, ctx, member: discord.Member, *, challenges):
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"] #database
        tb = db["all_about_challenge"] #table
        user = tb.find_one({
            "user_id": member.id,
            "guild_id": ctx.guild.id
        })
        if user:
            new_challenges = user["challenges"]
            for challenge in challenges.split(","):
                new_challenges.append(challenge.split())
            tb.update({
                "user_id": member.id,
                "guild_id": ctx.guild.id
           },
           {
               "$set": {
                   "challenges": new_challenges
               }
           })
            await ctx.send("Data Successfully Added!")
        else:
            await ctx.send("User not found in the database.")
    
    @commands.command(aliases=["rmData"])
    @has_permissions(administrator=True,manage_guild=True)
    async def removeData(self, ctx, member: discord.Member):
       con_fibu = pymongo.MongoClient(os.getenv("DB"))
       db = con_fibu["fibu"]
       tb = db["all_about_challenge"]
       tb.delete_one({
           "user_id": member.id,
           "guild_id": ctx.guild.id
       })
       await ctx.send("Data Deleted")
    
    @commands.command(aliases=["rmAllData"])
    @has_permissions(administrator=True,manage_guild=True)
    async def removeAllData(self, ctx):
       con_fibu = pymongo.MongoClient(os.getenv("DB"))
       db = con_fibu["fibu"]
       tb = db["all_about_challenge"]
       await ctx.send(':warning::warning: Do you really want to delete all challenges data of this server? :warning::warning:\nSend **\'Yes\'** to proceed or **\'No\'** to cancel the process\n**[!!Deleting data is very dangerous!!]**')
       confirm = await self.bot.wait_for('message', check= lambda message: message.author.id == ctx.author.id)
       if confirm.content.lower() == 'yes':
           tb.delete_one({"guild_id": ctx.guild.id})
           await ctx.send("Data Successfully Deleted!!!!")
       else:
           await ctx.send('Yeah.. That\'s a great choice!!')
     
    @commands.command(aliases=["rmxp", 'remxp'])
    @has_permissions(administrator=True, manage_guild=True)
    async def removeXp(self, ctx, xp: int, member: discord.Member):
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"]
        tb = db["all_about_challenge"]
        user = tb.find_one({
            "user_id": member.id,
            "guild_id": ctx.guild.id
        })
        if user:
            old_xp = user["xp"]
            old_need_xp = user["need_xp"]
            old_level = user["level"]
            insufficient = False
            if xp <= old_xp:
                level = old_level
                need_xp = old_need_xp
                _xp = old_xp - xp
                if _xp < 0:
                    insufficient = True
                else:
                    insufficient = False
            elif xp > old_xp:
                total_xp = old_xp + (old_level*100)
                _xp = total_xp - xp
                level = int(_xp/100)
                need_xp = (level+1)*100
                if _xp < 0:
                    insufficient = True
                else:
                    insufficient = False
            if not insufficient:
                tb.update({
                   "user_id": member.id,
                   "guild_id": ctx.guild.id
                },
                {
                    "$set": {
                        "xp": _xp, 
                        "need_xp": need_xp,
                        "level": level
                        }
                })
                await ctx.send("Done")
            else:
                await ctx.reply(f'This user don\'t have {xp} xp')
        else:
            await ctx.send("User not found!!") 
   
    @commands.command()
    @has_permissions(administrator=True,manage_guild=True)
    async def showAllData(self, ctx):
            con_fibu = pymongo.MongoClient(os.getenv("DB"))
            db = con_fibu["fibu"]
            tb = db["all_about_challenge"]
            all_data = list(tb.find({
                "guild_id": ctx.guild.id
            }))
            if all_data == []:
                await ctx.send("No data found of this server.")
            else:
                for data in all_data:
                    user = ctx.guild.get_member(data["user_id"])
                    challenges = ", ".join(i for i in data["challenges"])
                    await ctx.send(f"==========\n**User:** {user}\n**User Id:** {data['user_id']}\n**XP:** {data['xp']}\n**Level:** {data['level']}\n**Challenges:** ```{challenges}```\n==========")
    
    @commands.command()
    @has_permissions(administrator=True,manage_guild=True)
    async def showData(self, ctx, member: discord.Member=None):
            if member != None:
                con_fibu = pymongo.MongoClient(os.getenv("DB"))
                db = con_fibu["fibu"]
                tb = db["all_about_challenge"]
                member_data = tb.find_one({
                    "guild_id": ctx.guild.id,
                    "user_id": member.id
                })
                if not member_data:
                    await ctx.send("No data found!!")
                else:
                    user = ctx.guild.get_member(member_data["user_id"])
                    challenges = ", ".join(i for i in member_data["challenges"])
                    await ctx.send(f"==========\n**User:** {user}\n**User Id:** {member_data['user_id']}\n**XP:** {member_data['xp']}\n**Level:** {member_data['level']}\n**Challenges:** ```{challenges}```\n==========")
            else:
                await ctx.send("Provide user id or mention a user")
## swap challenges
    @commands.Cog.listener("on_message")
    async def _msg(self, message):
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"] #database
        tb = db["guild_data"] #table
        try:
            guild = tb.find_one({
                "guild_id":message.guild.id
            })
            from_channel_id = guild["swap_channels"]["from_channel"]
            to_channel_id = guild["swap_channels"]["to_channel"]
            if from_channel_id is not None:
                from_channel = await self.bot.fetch_channel(int(from_channel_id))
                to_channel = await self.bot.fetch_channel(int(to_channel_id))
                if message.channel.id == from_channel.id and message.author.id != self.bot.user.id:
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
