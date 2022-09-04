import discord
from discord.ext import commands
import os
import pymongo

import asyncio


class Chat(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self.data = Chat.offline_database()

    def online_database():
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"]  # database
        tb = db["other_data"]  # table
        return tb

    def offline_database():
        tb = Chat.online_database()
        data = tb.find_one({"name": "chat_info"})
        return data

    @commands.command(name="chat_account")
    @commands.has_permissions(administrator=True)
    async def chat_account(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author

        tb = Chat.online_database()
        info = tb.find_one({"name": "chat_info"})
        guild_data = info.get(str(ctx.guild.id))
        if guild_data:
            chat_account = guild_data.get("fibu")
            if chat_account:
                await ctx.send("Do you really want to change the chat acoount? (y/n)")

                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel
                try:
                    msg = await self.bot.wait_for('message', check=check, timeout=60)
                except asyncio.TimeoutError:
                    await ctx.send("Timeout!!\nTry again.")
                else:
                    if msg.content.lower() == "y":
                        guild_data["fibu"] = member.id
                        data = {
                            str(ctx.guild.id): guild_data
                        }
                        tb.update_one({"name": "chat_info"}, {
                            "$set": data})
                        await ctx.send(f"Chat account changed to: {member.mention}")
                        self.data = Chat.offline_database()
                    else:
                        await ctx.send("Canceled.")
            else:
                guild_data["fibu"] = member.id
                data = {
                    str(ctx.guild.id): guild_data
                }
                tb.update_one({"name": "chat_info"}, {
                    "$set": data})
                await ctx.send(f"Chat account set to: {member.mention}")
                self.data = Chat.offline_database()
        else:
            data = {
                str(ctx.guild.id): {
                    "fibu": member.id
                }
            }
            tb.update_one({"name": "chat_info"}, {
                "$set": data})
            await ctx.send(f"Chat account set to: {member.mention}")
            self.data = Chat.offline_database()

    @commands.command(name="chat_channel")
    @commands.has_permissions(administrator=True)
    async def chat_channel(self, ctx, channel: discord.TextChannel):
        tb = Chat.online_database()
        info = tb.find_one({"name": "chat_info"})
        guild_data = info.get(str(ctx.guild.id))
        if guild_data:
            chat_channel = guild_data.get("channel")
            if chat_channel:
                await ctx.send("Do you really want to change the chat channel? (y/n)")

                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel
                try:
                    msg = await self.bot.wait_for('message', check=check, timeout=60)
                except asyncio.TimeoutError:
                    await ctx.send("Timeout!!\nTry again.")
                else:
                    if msg.content.lower() == "y":
                        guild_data["channel"] = channel.id
                        data = {
                            str(ctx.guild.id): guild_data
                        }
                        tb.update_one({"name": "chat_info"}, {
                            "$set": data})
                        await ctx.send(f"Chat channel changed to: {channel.mention}")
                        self.data = Chat.offline_database()
                    else:
                        await ctx.send("Canceled.")
            else:
                guild_data["channel"] = channel.id
                data = {
                    str(ctx.guild.id): guild_data
                }
                tb.update_one({"name": "chat_info"}, {
                    "$set": data})
                await ctx.send(f"Chat channel set to: {channel.mention}")
                self.data = Chat.offline_database()
        else:
            data = {
                str(ctx.guild.id): {
                    "channel": channel.id
                }
            }
            tb.update_one({"name": "chat_info"}, {
                "$set": data})
            await ctx.send(f"Chat channel set to: {channel.mention}")
            self.data = Chat.offline_database()

    @commands.command(name="chat_command")
    @commands.has_permissions(administrator=True)
    async def chat_command(self, ctx, channel: discord.TextChannel):
        tb = Chat.online_database()
        info = tb.find_one({"name": "chat_info"})
        guild_data = info.get(str(ctx.guild.id))
        if guild_data:
            chat_channel = guild_data.get("command")
            if chat_channel:
                await ctx.send("Do you really want to change the chat command channel? (y/n)")

                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel
                try:
                    msg = await self.bot.wait_for('message', check=check, timeout=60)
                except asyncio.TimeoutError:
                    await ctx.send("Timeout!!\nTry again.")
                else:
                    if msg.content.lower() == "y":
                        guild_data["command"] = channel.id
                        data = {
                            str(ctx.guild.id): guild_data
                        }
                        tb.update_one({"name": "chat_info"}, {
                            "$set": data})
                        await ctx.send(f"Chat command channel changed to: {channel.mention}")
                        self.data = Chat.offline_database()
                    else:
                        await ctx.send("Canceled.")
            else:
                guild_data["command"] = channel.id
                data = {
                    str(ctx.guild.id): guild_data
                }
                tb.update_one({"name": "chat_info"}, {
                    "$set": data})
                await ctx.send(f"Chat command channel set to: {channel.mention}")
                self.data = Chat.offline_database()
        else:
            data = {
                str(ctx.guild.id): {
                    "command": channel.id
                }
            }
            tb.update_one({"name": "chat_info"}, {
                "$set": data})
            await ctx.send(f"Chat command channel set to: {channel.mention}")
            self.data = Chat.offline_database()

    @commands.Cog.listener()
    async def on_message(self, message):
        data = self.data
        try:
            guild_data = data.get(f"{message.guild.id}")
        except:
            pass
        if guild_data:
            fibu_account = guild_data.get("fibu")
            chat_channel_id = guild_data.get("channel")
            command_channel = guild_data.get("command")
            if command_channel == message.channel.id:
                if fibu_account == message.author.id:
                    if message.content.lower().startswith("!fibu ") or message.content.lower().startswith("!f "):
                        return

                    ref_message = message.reference
                    if ref_message:
                        ref_message_id = ref_message.message_id
                        ref_message_obj = await message.channel.fetch_message(ref_message_id)
                        ref_message_content = ref_message_obj.content
                        chat_channel = message.guild.get_channel(
                            chat_channel_id)
                        channel_messages = await chat_channel.history(limit=100).flatten()
                        for channel_message in channel_messages:
                            if channel_message.content == ref_message_content:
                                await channel_message.reply(message.content)
                                break
                    else:
                        chat_channel = message.guild.get_channel(
                            chat_channel_id)
                        await chat_channel.send(message.content)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        data = self.data
        guild_data = data.get(f"{before.guild.id}")
        if guild_data:
            fibu_account = guild_data.get("fibu")
            chat_channel_id = guild_data.get("channel")
            command_channel = guild_data.get("command")
            if command_channel == before.channel.id:
                if fibu_account == before.author.id:
                    chat_channel = before.guild.get_channel(
                        chat_channel_id)
                    channel_messages = await chat_channel.history(limit=100).flatten()
                    for channel_message in channel_messages:
                        if channel_message.content == before.content:
                            await channel_message.edit(content=after.content)
                            break

####### on_raw_message_edit ######
        # data = self.data
        # message_data = playload.data
        # guild_id = message_data.get("guild_id")
        # guild = self.bot.get_guild(guild_id)
        # guild_data = data.get(guild_id)
        # if guild_data:
        #     fibu_account = guild_data.get("fibu")
        #     chat_channel_id = guild_data.get("channel")
        #     command_channel = guild_data.get("command")
        #     channel_id = int(message_data.get("channel_id"))
        #     if command_channel == channel_id:
        #         print(7)
        #         author_id = int(message_data.get("author").get("id"))
        #         print(8)
        #         print(message_data)
        #         print()
        #         print(playload.cached_message)
        #         # before_content = message_data.get(
        #         #     "referenced_message").get("content")
        #         # print(9)
        #         # after_content = message_data.get("content")
        #         # print(10)
        #         # if fibu_account == author_id:
        #         #     print(11)
        #         #     chat_channel = guild.get_channel(
        #         #         chat_channel_id)
        #         #     print(12)
        #         #     channel_messages = await chat_channel.history(limit=100).flatten()
        #         #     print(13)
        #         #     for channel_message in channel_messages:
        #         #         print(14, "loop")
        #         #         if channel_message.content == before_content:
        #         #             print(15)
        #         #             await channel_message.edit(content=after_content)
        #         #             print(16)
        #         #             break

    ###### Error handling ######

    @chat_account.error
    async def _chat_account_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You don't have the permissions to do that!!")

    @chat_channel.error
    async def _chat_channel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You don't have the permissions to do that!!")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Channel is missing!!\n```\n!fibu chat_channel <channel>\n```")


def setup(bot):
    bot.add_cog(Chat(bot))
