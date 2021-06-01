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
        self.bot = client

#echo
    @commands.command()
    @has_permissions(administrator= True, manage_guild= True, manage_messages= True)
    async def echo(self, ctx, channel: typing.Optional[discord.TextChannel] = None, *, msg= None):
        await ctx.message.delete()
        if not channel:
            channel = ctx.channel
        
        attachments = ctx.message.attachments
        files = []
        if msg:
            if attachments:
                for attachment in attachments:
                    file = await attachment.to_file()
                    files.append(file)
                await channel.send(msg, files= files)
                log_format = f"==========\nUser: `{ctx.author}`\nName: {ctx.author.name}\nID: {ctx.author.id}\nServer: {ctx.message.guild.name}\nChannel: {ctx.message.channel}\nMessage: {ctx.message.content}\n=========="
                log_channel = await self.bot.fetch_channel(802766376719876107)
                await log_channel.send(log_format, files= files)
            else:
                await channel.send(msg)
                log_format = f"==========\nUser: `{ctx.author}`\nName: {ctx.author.name}\nID: {ctx.author.id}\nServer: {ctx.message.guild.name}\nChannel: {ctx.message.channel}\nMessage: {ctx.message.content}\n=========="
                log_channel = await self.bot.fetch_channel(802766376719876107)
                await log_channel.send(log_format)
        elif attachments:
            for attachment in attachments:
                file = await attachment.to_file()
                files.append(file)
            await channel.send(msg, files= files)
            log_format = f"==========\nUser: `{ctx.author}`\nName: {ctx.author.name}\nID: {ctx.author.id}\nServer: {ctx.message.guild.name}\nChannel: {ctx.message.channel}\nMessage: {ctx.message.content}\n=========="
            log_channel = await self.bot.fetch_channel(802766376719876107)
            await log_channel.send(log_format, files= files)

    @commands.command()
    @has_permissions(administrator= True, manage_guild= True, manage_messages= True)
    async def echoin(self, ctx, guild = None, channel = None, *, msg= None):
        if isinstance(ctx.message.channel, discord.channel.DMChannel):
            attachments = ctx.message.attachments
            files = []
            if not guild:
                await ctx.send("Put a guild id...😑")
            elif not channel:
                await ctx.send("Put a channel id...😪")
            elif not msg:
                await ctx.send('Provide message 😩')
            elif msg:
                try:
                    find_guild = await self.bot.fetch_guild(int(guild))
                    channel = await self.bot.fetch_channel(int(channel))
                    if attachments:
                        for attachment in attachments:
                            file = await attachment.to_file()
                            files.append(file)
                        await channel.send(msg, files= files)
                        log_format = f"==========\nUser: `{ctx.author}`\nName: {ctx.author.name}\nID: {ctx.author.id}\nServer: {ctx.message.guild.name}\nChannel: {ctx.message.channel}\nMessage: {ctx.message.content}\n=========="
                        log_channel = await self.bot.fetch_channel(802766376719876107)
                        await log_channel.send(log_format, files= files)
                    else:
                        await channel.send(msg)
                        log_format = f"==========\nUser: `{ctx.author}`\nName: {ctx.author.name}\nID: {ctx.author.id}\nServer: {ctx.message.guild.name}\nChannel: {ctx.message.channel}\nMessage: {ctx.message.content}\n=========="
                        log_channel = await self.bot.fetch_channel(802766376719876107)
                        await log_channel.send(log_format)
                except:
                    await ctx.send("Type the guild id that exists...🙄")
            elif attachments:
                for attachment in attachments:
                    file = await attachment.to_file()
                    files.append(file)
                await channel.send(msg, files= files)
                log_format = f"==========\nUser: `{ctx.author}`\nName: {ctx.author.name}\nID: {ctx.author.id}\nServer: {ctx.message.guild.name}\nChannel: {ctx.message.channel}\nMessage: {ctx.message.content}\n=========="
                log_channel = await self.bot.fetch_channel(802766376719876107)
                await log_channel.send(log_format, files= files)
            
       


#quotes
    @commands.command()
    async def quote(self, ctx, *, arg = None):
        if not arg:
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
# delete message
    @commands.command()
    @has_permissions(administrator= True, manage_guild= True, manage_roles= True, manage_messages= True)
    async def clean(self, ctx, limit: int= 100, member: discord.Member= None):
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

# add swap channels
#    @commands.command()
#    @has_permissions(administrator=True,manage_guild=True)
#    async def swap(self, ctx, from_channel: discord.TextChannel = None, to_channel: discord.TextChannel = None):
#        if from_channel is None or to_channel is None:
#            await ctx.send("Provide channel correctly!!")
#        else:
#            con_fibu = pymongo.MongoClient(os.getenv("DB"))
#            db = con_fibu["fibu"] #database
#            tb = db["guild_data"] #table
#            get_guild = tb.find_one({"guild_id":ctx.guild.id})
#            if get_guild!=None:
#                new_value = {"swap_channels": {"from_channel": from_channel.id, "to_channel": to_channel.id}}
#                tb.update_one({"guild_id":ctx.guild.id},{"$set":new_value})
#                await ctx.message.add_reaction("✅")
#            else:
#                value = {"guild_id": ctx.guild.id, "swap_channels": {"from_channel": from_channel.id, "to_channel": to_channel.id}}
#                tb.insert_one(value)
#                await ctx.message.add_reaction("✅")
# remove swap channels
#    @commands.command()
#    @has_permissions(administrator=True,manage_guild=True)
#    async def removeSwap(self, ctx):
#        con_fibu = pymongo.MongoClient(os.getenv("DB"))
#        db = con_fibu["fibu"] #database
#        tb = db["guild_data"] #table
#        #guild = tb.find_one({"guild_id":ctx.guild.id})
#        new_value = {"swap_channels": {"from_channel": None, "to_channel": None}}
#        tb.update_one({"guild_id":ctx.guild.id},{"$set":new_value})
#        await ctx.message.add_reaction("✅")

######### permission Handling #########
   # @swap.error
#    async def _error(self,ctx,error):
#        if isinstance(error,commands.MissingPermissions):
#            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
#    
#    @removeSwap.error
#    async def _error(self,ctx,error):
#        if isinstance(error,commands.MissingPermissions):
#            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")

### Error Handling ###
    @clean.error
    async def _error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
    @echo.error
    async def _error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
    @echoin.error
    async def _error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")

def setup(bot):
    bot.add_cog(Command(bot))