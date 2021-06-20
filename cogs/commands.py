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
        files = None
        log_attach = ''
        if msg:
            if attachments:
                files = []
                for attachment in attachments:
                    file = await attachment.to_file()
                    log_attach += f'{attachment.url}\n'
                    files.append(file)
        elif attachments:
            files = []
            for attachment in attachments:
                file = await attachment.to_file()
                log_attach += f'{attachment.url}\n'
                files.append(file)
        await channel.send(msg, files= files)
        log_format = f"==========\nUser: `{ctx.author}`\nName: {ctx.author.name}\nID: {ctx.author.id}\nServer: {ctx.message.guild.name}\nChannel: {ctx.message.channel}\nMessage: {ctx.message.content}{log_attach}\n=========="
        log_channel = await self.bot.fetch_channel(802766376719876107)
        await log_channel.send(log_format, files= files)

    @commands.command()
    @has_permissions(administrator= True, manage_guild= True, manage_messages= True)
    async def echoin(self, ctx, guild = None, channel = None, *, msg= None):
        if isinstance(ctx.message.channel, discord.channel.DMChannel):
            attachments = ctx.message.attachments
            files = None
            log_attach = ''
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
                        files = []
                        for attachment in attachments:
                            file = await attachment.to_file()
                            log_attach += f'{attachment.url}\n'
                            files.append(file)
                except:
                    await ctx.send("Type the guild id that exists...🙄")
            elif attachments:
                files = []
                for attachment in attachments:
                    file = await attachment.to_file()
                    log_attach += f'{attachment.url}\n'
                    files.append(file)
            if msg or attachments:
                await channel.send(msg, files= files)
                log_format = f"==========\nUser: `{ctx.author}`\nName: {ctx.author.name}\nID: {ctx.author.id}\nServer: {ctx.message.guild.name}\nChannel: {ctx.message.channel}\nMessage: {ctx.message.content}{log_attach}\n=========="
                log_channel = await self.bot.fetch_channel(802766376719876107)
                await log_channel.send(log_format, files= files)
            
# edit message
    @commands.command()
    @has_permissions(administrator= True, manage_guild= True, manage_messages= True)
    async def edit(self, ctx, message: discord.Message):
        if message.author.id != self.bot.user.id:
            await ctx.send('This is not my message so I can\'t edit it')
        else:
            message_content = message.content
            attachments = message.attachments
            files = []
            for i in attachments:
                file = await i.to_file()
                files.append(file)
            original_message = await ctx.send(f'```\n{message_content}\n```', files= files)
            await original_message.reply('Here is the content of that message.\nCopy, edit and send it to replace you can also attachment files.**__Note:__ Write \'> \' at the beginning of the message**\nSend \'cancel\' to cancel the process!!\nYou have 5 minutes to response...')
            while True:
                try:
                    replace_message = await self.bot.wait_for('message', check= lambda msg: msg.author.id == ctx.author.id, timeout= 300)
                except asyncio.TimeoutError:
                    await ctx.send('Time out...\nYou took long time')
                    break
                else:
                    if len(replace_message.content) >=2000:
                        await ctx.send('Message character length is greater then 2000 or character limit\nTry again after reducing limit waiting for your messages for 5 min')
                    elif replace_message.content.lower().strip() == 'cancel':
                        await ctx.send('Process cancelled!!')
                        break
                    elif replace_message.content.startswith('>'):
                        message_content = replace_message.content.lstrip('> ')
                        attach = replace_message.attachments
                        for i in attach:
                            message_content += f'{i.url}'
                        update = await ctx.send('Wait... Editing message!!')
                        await message.edit(content= message_content)
                        await update.edit(content= '<:greentickbadge:852127602373951519> Message successfully edited!!')
                        break
                    else:
                        await ctx.send('Put > at the beginning of the message...')
        


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
    async def clean(self, ctx, limit: int= 10, member: discord.Member= None):
        await ctx.message.delete()
        if limit > 100 or limit < 1:
            await ctx.send(f"Can't delete {limit} messages! My limit is from 1 to 100.")
        else:
            if member:
                def check_msg(message):
                    return message.author.id == member.id
                check = check_msg
            else:
                check = None
            deleted = await ctx.channel.purge(limit= limit, check= check)
            count = len(deleted)
            msg = await ctx.send(f"{count} messages deleted!!")
            await asyncio.sleep(3)
            await msg.delete()
            ### log update ###
            log_format = f':warning: ️Clean command used by **{ctx.author}**\n**UserID:** {ctx.author.id}\nServer: {ctx.guild}\n**Limit:** {limit}\n**Deleted**: {count}'
            log_channel = await self.bot.fetch_channel(796371191837229098)
            await log_channel.send(log_format)


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