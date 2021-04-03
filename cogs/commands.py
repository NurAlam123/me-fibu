import discord
from datetime import datetime as time
from discord.ext import commands as c
from discord.ext.commands import has_permissions
import wikiquote as q
import asyncio
import typing
import random

class Command(c.Cog):
    def __init__(self,client):
        self.client = client

#echo
    @c.command()
    async def echo(self,ctx, channel: typing.Optional[discord.TextChannel]=None,*,msg):
        await ctx.message.delete()
        if channel == None:
            await ctx.send(msg)
        else:
            await channel.send(msg)
        log_format = f"==========\nUser: `{ctx.author}`\nName: {ctx.author.name}\nID: {ctx.author.id}\nServer: {ctx.message.guild.name}\nChannel: {ctx.message.channel}\nMessage: {ctx.message.content}\n=========="
        log_channel = await self.client.fetch_channel(802766376719876107)
        await log_channel.send(log_format)

    @c.command()
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
    @c.command()
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
    
    @c.command()
    @has_permissions(administrator=True,manage_roles=True, manage_messages=True)
    async def clean(self, ctx, limit: int):
        await ctx.message.delete()
        if limit > 100 and limit < 0:
            await ctx.send(f"Can't delete {limit} messages! My limit is from 1 to 100.")
        else:
            count = 0
            async for message in ctx.channel.history(limit=limit):
                await message.delete()
                count+=1
            msg = await ctx.send(f"{count} messages deleted!!")
            await asyncio.sleep(3)
            await msg.delete()



def setup(bot):
    bot.add_cog(Command(bot))
