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
    def __init__(self, client):
        self.bot = client

# echo
    @commands.command()
    @has_permissions(administrator=True, manage_guild=True, manage_messages=True)
    async def echo(self, ctx, channel: typing.Optional[discord.TextChannel] = None, *, msg=None):
        await ctx.message.delete()
        if not channel:
            channel = ctx.channel

        attachments = ctx.message.attachments
        files = None
        log_attach = ''
#        if msg:
#            if attachments:
#                files = []
#                for attachment in attachments:
#                    file = await attachment.to_file()
#                    log_attach += f'\n{attachment.url}\n'
#                    files.append(file)
        if attachments:
            files = []
            for attachment in attachments:
                file = await attachment.to_file()
                log_attach += f'\n{attachment.url}\n'
                files.append(file)

        await channel.send(msg, files=files)
        log_format = f"==========\nUser: `{ctx.author}`\nName: {ctx.author.name}\nID: {ctx.author.id}\nServer: {ctx.message.guild.name}\nChannel: {ctx.message.channel}\nMessage: {ctx.message.content}{log_attach}\n=========="
        log_channel = await self.bot.fetch_channel(802766376719876107)
        await log_channel.send(log_format)

    @commands.command()
    @has_permissions(administrator=True, manage_guild=True, manage_messages=True)
    async def echoin(self, ctx, guild=None, channel=None, *, msg=None):
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
                await channel.send(msg, files=files)
                log_format = f"==========\nUser: `{ctx.author}`\nName: {ctx.author.name}\nID: {ctx.author.id}\nServer: {ctx.message.guild.name}\nChannel: {ctx.message.channel}\nMessage: {ctx.message.content}{log_attach}\n=========="
                log_channel = await self.bot.fetch_channel(802766376719876107)
                await log_channel.send(log_format, files=files)

# edit message
    @commands.command()
    @has_permissions(administrator=True, manage_guild=True)
    async def edit(self, ctx, channel: typing.Optional[discord.TextChannel], message_id: int):
        if not channel:
            channel = ctx.channel
        message = await channel.fetch_message(message_id)
        if message.author.id != self.bot.user.id:
            await ctx.send('This is not my message so I can\'t edit it')
        else:
            message_content = message.content
            message_content = discord.utils.escape_markdown(
                message_content, as_needed=True)  # escape markdown
            message_content = discord.utils.escape_mentions(
                message_content)  # escape mentions
            attachments = message.attachments
            files = []
            for i in attachments:
                file = await i.to_file()
                files.append(file)
            original_message = await ctx.send(f'{message_content}', files=files)
            await original_message.reply('Here is the content of that message.\nCopy, edit and send it to replace you can also attachment files.\n**__Note:__ Write \'> \' at the beginning of the message**\nSend \'cancel\' to cancel the process!!\nYou have 5 minutes to response...')
            while True:
                try:
                    replace_message = await self.bot.wait_for('message', check=lambda msg: msg.author.id == ctx.author.id, timeout=300)
                except asyncio.TimeoutError:
                    await ctx.send('Time out...\nYou took long time')
                    break
                else:
                    if len(replace_message.content) >= 2000:
                        await ctx.send('Message character length is greater then 2000 or character limit\nTry again after reducing limit waiting for your messages for 5 min')
                    elif replace_message.content.lower().strip() == 'cancel':
                        await ctx.send('Process cancelled!!')
                        break
                    elif replace_message.content.startswith('>'):
                        message_content = replace_message.content.lstrip('> ')
                        attach = replace_message.attachments
                        for i in attach:
                            message_content += f'\n{i.url}'
                        update = await ctx.send('Wait... Editing message!!')
                        await message.edit(content=message_content)
                        await update.edit(content='<:greentickbadge:852127602373951519> Message successfully edited!!')
                        break
                    else:
                        await ctx.send('Put > at the beginning of the message...')


# quotes


    @commands.command()
    async def quote(self, ctx, *, arg=None):
        if not arg:
            random_q = q.random_titles(max_titles=1)[0]
            quote_text = random.choice(q.quotes(random_q))
            await ctx.send(f">>> {quote_text}\n	- *{random_q}*")
        else:
            try:
                search = q.search(arg)[0]
                quote = random.choice(q.quotes(search))
                await ctx.send(f">>> {quote}\n	- *{search}*")
            except:
                pass

    @commands.command(name="dm")
    @commands.has_permissions(administrator=True)
    async def dm(self, ctx, member: int = None, *, msg=None):
        if not member:
            await ctx.send('Please mention a member...')
        elif not msg:
            await ctx.send('Please provide a message...')
        else:
            try:
                member = await self.bot.fetch_user(member)
            except:
                await ctx.send('Member Not Found!\nPlease provide a valid user id...')
            else:
                attachments = ctx.message.attachments
                files = None
                log_attach = ''
                if attachments:
                    files = []
                    for attachment in attachments:
                        file = await attachment.to_file()
                        log_attach += f'\n{attachment.url}\n'
                        files.append(file)

                await ctx.message.delete()
                await member.send(msg, files=files)
                await ctx.send('Message sent successfully...')
                log_format = f"========== DM Message Log ==========\n**From:** `{ctx.author}`\n**UserID:** {ctx.author.id}\n**Server:** {ctx.message.guild.name}\n**Channel:** {ctx.message.channel}\n**To:** {member}\n**UserID:** {member.id}\nMessage: {msg}{log_attach}\n===================="
                log_channel = await self.bot.fetch_channel(938085689772355594)
                await log_channel.send(log_format)

    @commands.command(name="bndm")
    @commands.has_permissions(administrator=True)
    async def bndm(self, ctx, member: int = None, *, msg=None):
        if not member:
            await ctx.send('Please mention a member...')
        elif not msg:
            await ctx.send('Please provide a message...')
        else:
            try:
                member = await self.bot.fetch_user(member)
            except:
                await ctx.send('Member Not Found!\nPlease provide a valid user id...')
            else:
                embed_msg = discord.Embed(
                    title="Underage Ban from Hero Programmers", description=msg, color=0xfdb706)
                embed_msg.set_image(
                    url="https://media.discordapp.net/attachments/938133816097263686/938134127100702780/Under_Age_Ban_Message.png")
                embed_msg.set_footer(
                    text=f"{ctx.author.name}", icon_url=ctx.author.avatar_url)
                await ctx.message.delete()
                await member.send(embed=embed_msg)
                await ctx.send('Message sent successfully...')
                log_format = f"========== Under Age Ban DM Message Log ==========\n**From:** `{ctx.author}`\n**UserID:** {ctx.author.id}\n**Server:** {ctx.message.guild.name}\n**Channel:** {ctx.message.channel}\n**To:** {member}\n**UserID:** {member.id}\nMessage: {msg}\n===================="
                log_channel = await self.bot.fetch_channel(938085689772355594)
                await log_channel.send(log_format)


# delete message


    @commands.command()
    @has_permissions(administrator=True, manage_guild=True, manage_roles=True, manage_messages=True)
    async def clean(self, ctx, limit: int = 10, member: discord.Member = None):
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
            deleted = await ctx.channel.purge(limit=limit, check=check)
            count = len(deleted)
            msg = await ctx.send(f"{count} messages deleted!!")
            await asyncio.sleep(3)
            await msg.delete()
            ### log update ###
            log_format = f':warning: Clean command used by **{ctx.author}**\n**UserID:** {ctx.author.id}\nServer: {ctx.guild}\n**Limit:** {limit}\n**Deleted**: {count}'
            log_channel = await self.bot.fetch_channel(796371191837229098)
            await log_channel.send(log_format)

# revive ping command
    @commands.command(name="revive")
    @has_permissions(manage_messages=True)
    async def revive(self, ctx):
        await ctx.message.delete()
        role_id = None
        if ctx.guild.id == 720365448809545742:
            role_id = 874979840741244959
        elif ctx.guild.id == 550676428040044574:
            role_id = 867668660247592980

        if role_id:
            await ctx.send(f"<@&{role_id}>")
            log_format = f"========== Revive Ping Log ==========\nUser: `{ctx.author}`\nName: {ctx.author.name}\nID: {ctx.author.id}\nServer: {ctx.message.guild.name}\nChannel: {ctx.message.channel}\n===================="
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
    async def _clean_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")

    @echo.error
    async def _echo_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")

    @echoin.error
    async def _echoin_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")

    @edit.error
    async def _edit_error(self, ctx, error):
        if isinstance(error, commands.MessageNotFound):
            await ctx.send(f'Not found any message that associated with the message id in this server!')
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send(error)
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
        elif isinstance(error, commands.MissingRequiredArgument):
            arg_name = error.param.name
            if arg_name == 'message':
                await ctx.send(f'Please provide a message id that I have to edit!!')
            if arg_name == 'channel':
                await ctx.send(f'Please provide a channel where the message is!!')

        log = await self.bot.fetch_channel(855048645174755358)
        await log.send(f'Error in **Edit** command:\n{error}')
        raise error

    @revive.error
    async def _revive_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")

    @dm.error
    async def _dm_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
        # if isinstance():
        #     pass


def setup(bot):
    bot.add_cog(Command(bot))
