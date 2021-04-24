import discord
from datetime import datetime as time
from discord.ext import commands
from discord.ext.commands import has_permissions
import wikiquote as q
import asyncio
import typing
import random
import pymongo
import os

class Command(commands.Cog):
    def __init__(self,client):
        self.client = client

#echo
    @commands.command()
    async def echo(self,ctx, channel: typing.Optional[discord.TextChannel]=None,*,msg):
        await ctx.message.delete()
        if channel == None:
            await ctx.send(msg)
        else:
            await channel.send(msg)
        log_format = f"==========\nUser: `{ctx.author}`\nName: {ctx.author.name}\nID: {ctx.author.id}\nServer: {ctx.message.guild.name}\nChannel: {ctx.message.channel}\nMessage: {ctx.message.content}\n=========="
        log_channel = await self.client.fetch_channel(802766376719876107)
        await log_channel.send(log_format)

    @commands.command()
    async def echoin(self, ctx, guild = None, channel = None, *, msg):
        if isinstance(ctx.message.channel, discord.channel.DMChannel):
            if guild == None:
                await ctx.send("Put a guild id...😑")
            elif channel == None:
                await ctx.send("Put a channel id...😪")
            else:
                try:
                    find_guild = await self.client.fetch_guild(int(guild))
                    find_channel = await self.client.fetch_channel(int(channel))
                    await find_channel.send(msg)
                    log_format = f"==========\nUser: `{ctx.author}`\nName: {ctx.author.name}\nID: {ctx.author.id}\nServer: {find_guild.name}\nChannel: {find_channel}\nMessage: {msg}\n=========="
                    log_channel = await self.client.fetch_channel(802766376719876107)
                    await log_channel.send(log_format) 
                except:
                    await ctx.send("Type the guild id that exists...🙄")
            
       


#quotes
    @commands.command()
    async def quote(self, ctx,*,arg = None):
        if arg == None:
            random_q = q.random_titles(max_titles = 1)[0]
            quote_text = random.choice(q.quotes(random_q))
            await ctx.send(f">>> {quote_text}\n	- *{random_q}*")
        else:
            try:
                search = q.search(arg)[0]
                quote = random.choice(q.quotes(search))
                await ctx.send(f">>> {quote}\n	- *{search}*")
            except:
                pass
    
    @commands.command()
    @has_permissions(administrator=True,manage_roles=True, manage_messages=True)
    async def clean(self, ctx, limit: int=100, member: discord.Member=None):
        await ctx.message.delete()
        if limit > 100 or limit < 1:
            await ctx.send(f"Can't delete {limit} messages! My limit is from 1 to 100.")
        else:
            count = 0
            async for message in ctx.channel.history(limit=limit):
                if member is None:
                    await message.delete()
                    count+=1
                else:
                    if message.author.id==member.id:
                        await message.delete()
                        count+=1
                    else:
                        pass
            
            msg = await ctx.send(f"{count} messages deleted!!")
            await asyncio.sleep(3)
            await msg.delete()
    
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

######### permission Handling #########
    @swap.error
    async def _error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
    
    @removeSwap.error
    async def _error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
    @clean.error
    async def _error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")


def setup(bot):
    bot.add_cog(Command(bot))