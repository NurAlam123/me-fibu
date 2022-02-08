import discord
from discord.ext import commands
import os
import pymongo

import re
import asyncio


class Chat(commands.Cog):
    def __init__(self, client):
        self.bot = client

    def database():
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"]  # database
        tb = db["other_data"]  # table
        return db, tb

    @commands.command(name="chat_account")
    @commands.has_permissions(administrator=True)
    async def chat_account(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author

        db, tb = Chat.database()
        info = tb.find_one({"name": "chat_info"})
        fibu_acc = info.get("fibu")
        if fibu_acc:
            await ctx.send("Do you really want to change the chat account? (y/n)")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            try:
                msg = await self.bot.wait_for('message', check=check, timeout=60)
            except asyncio.TimeoutError:
                await ctx.send("Timeout!!\nTry again.")
            else:
                if msg.content.lower() == "y":
                    tb.update_one({"name": "chat_info"}, {
                                  "$set": {"fibu": member.id}})
                    await ctx.send(f"Chat account changed to: {member.mention}")
                else:
                    await ctx.send("Canceled.")
        else:
            tb.update_one({"name": "chat_info"}, {"$set": {"fibu": member.id}})
            await ctx.send(f"Chat account set to: {member.mention}")

    @commands.command(name="chat_channel")
    @commands.has_permissions(administrator=True)
    async def chat_channel(self, ctx, channel: discord.TextChannel):
        db, tb = Chat.database()
        info = tb.find_one({"name": "chat_info"})
        chat_channel = info.get("channel")
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
                    tb.update_one({"name": "chat_info"}, {
                                    "$set": {"channel": channel.id}})
                    await ctx.send(f"Chat channel changed to: {channel.mention}")
                else:
                    await ctx.send("Canceled.")
        else:
            tb.update_one({"name": "chat_info"}, {
                            "$set": {"channel": channel.id}})
            await ctx.send(f"Chat channel set to: {channel.mention}")

    @commands.command(name="chat")
    async def chat(self, ctx, *, message):
        db, tb = Chat.database()
        info = tb.find_one({"name": "chat_info"})
        fibu_acc_id = info.get("fibu")
        chat_channel_id = info.get("channel")
        if not fibu_acc_id:
            await ctx.send("First link your account with me by typing\n```\n!fibu chat_account [member]\n```")
        elif not chat_channel_id:
            await ctx.send("First link a channel where I should chat. Type\n```\n!fibu chat_channel <channel>\n```")
        else:
            if fibu_acc_id == ctx.author.id:
                ref_message = ctx.message.reference
                if ref_message:
                    ref_message_id = ref_message.message_id
                    ref_message_obj = await ctx.channel.fetch_message(ref_message_id)
                    ref_message_content = ref_message_obj.content.replace("!fibu chat ", "")
                    chat_channel = ctx.guild.get_channel(chat_channel_id)
                    channel_messages = await chat_channel.history(limit=100).flatten()
                    for channel_message in channel_messages:
                        print(channel_message.content, ref_message_content)
                        if channel_message.content == ref_message_content:
                            await channel_message.reply(message)
                            break
                else:
                    chat_channel = ctx.guild.get_channel(chat_channel_id)
                    await chat_channel.send(message)
    
    ###### Error handling ######
    @chat.error
    async def _chat_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Message is missing!!\n```\n!fibu chat <message>\n```")
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
