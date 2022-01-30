import discord
from discord.ext import commands
import os
import re
import asyncio

class UsersDm(commands.Cog):
    def __init__(self, client):
        self.bot = client
        
    async def cog_check(self, ctx):
        return ctx.author.id in self.bot.TEAM

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.channel.DMChannel):
                if message.content.startswith("!"):
                    pass
                else:
                    if message.author.id == self.bot.user.id or message.author.id in self.bot.TEAM:
                        pass
                    else:
                        name = message.author
                        id = message.author.id
                        message_id = message.id
                        message_content = message.content
                         
                        receive_channel = await self.bot.fetch_channel(856057917705814056)
                        info_format = f"----------\n**Username:** {name}\n**UserId:** {id}\n**MessageId:** {message_id}\n----------"
                        #to_receiver = await receive_channel.send(info_format)
                        attachments = message.attachments
                        files = None
                        log_attach = ""
                        if attachments:
                            files = []
                            for attachment in attachments:
                                file = await attachment.to_file()
                                log_attach += f"\n{attachment.url}\n"
                                files.append(file)
                                
                        if len(message_content) >= 1500:
                            file = open("message.txt", "w")
                            message_content = f"{info_format}\n{message_content}\n--- Attachment ---\n{log_attach}\n----- ××× -----\n"
                            file.write(message_content)
                            file.close()
                            up_file = discord.File("message.txt")
                            if files:
                                files.append(up_file)
                            else:
                                files = [up_file]
                            message_format = f"{info_format}\nDownload the **message.txt** file as message length is more then the limit!!\n"
                            await receive_channel.send(message_format, files = files)
                            os.remove("message.txt")
                        else:
                            message_format = f"{info_format}\n`{name}::` {message_content}\n{log_attach}\n"
                            await receive_channel.send(message_format, files = files)

    @commands.Cog.listener()
    async def on_message_edit(self, before_msg, after_msg):
        if isinstance(before_msg.channel, discord.channel.DMChannel):
                receive_channel = await self.bot.fetch_channel(856057917705814056)
                id = before_msg.author.id
                name = before_msg.author.name
                if id != self.bot.user.id:
                    identity_format = f"----------\n**Username:** {name}\n**UserId:** {id}\n**MessageId:** {after_msg.id}\n----------"
                    
                    if (len(before_msg.content) + len(after_msg.content)) >= 1000:
                        file = open("message.txt", "w")
                        message = f"----- Old message -----\n{before_msg.content}\n\n----- New Message -----\n{after_msg.content}\n"
                        file.write(message)
                        file.close()
                        up_file = discord.File("message.txt")
                        message_format = f"{identity_format}\nDownload the **message.txt** file as message length is more then the limit!!\n"
                        await receive_channel.send(message_format, file = up_file)
                        os.remove("message.txt")
                    else:
                        edit_msg_format = f"{identity_format}\n++++ Message Edited ++++\n**From:** {before_msg.content}\n**To:** {after_msg.content}"
                        await receive_channel.send(edit_msg_format)
                

    @commands.command(name = "msg")
    async def _message(self, ctx, *, message=None):
        if ctx.author.id in self.bot.TEAM:
            if not message:
                await ctx.send("Send Message!!\n**__Note:__ Write '> ' at the beginning of the message!!**\nWaiting for 5 min.\n_Just send Exit to stop the process_")
                try:
                    user_message = await self.bot.wait_for("message", timeout = 300, check = lambda message: message.author.id in self.bot.TEAM)
                    if user_message.content.startswith(">"):
                        message = user_message.content.strip("> ")
                    elif user_message.content.lower() == "exit":
                        await ctx.send("Process stopped!!")
                        message = None
                    
                except asyncio.TimeoutError:
                    await ctx.send(":warning: Timeout!!")
            
            if message:
                receive_channel = await self.bot.fetch_channel(856057917705814056)
                ##### reference message finder ####
                ref_message_id = ctx.message.reference.message_id
                ref_message_obj = await ctx.channel.fetch_message(ref_message_id)
                ref_message_content = ref_message_obj.content
                ########
                user_id = int(re.findall(r"\d+", ref_message_content)[1])
                
                files= None
                user = await self.bot.fetch_user(user_id)
                
                if ctx.message.attachments:
                    files = []
                    for attachment in ctx.message.attachments:
                        file = await attachment.to_file()
                        files.append(file)
                            
                msg = await user.send(f"{message}", files= files)
                
                await ctx.message.add_reaction("<:greentickbadge:852127602373951519>")
                await ctx.reply(f"Message ID: {msg.id}")
                
#    @commands.command()
#    async def reply(self, ctx, *, reply_message = None):
#        if ctx.author.id in self.bot.TEAM:
#            if not reply_message:
#                await ctx.send("Send Message!!\n**__Note:__ Write '> ' at the beginning of the message!!**\nWaiting for 5 min.\n_Just send Exit to stop the process_")
#                try:
#                    user_message = await self.bot.wait_for("message", timeout = 300, check = lambda message: message.author.id in self.bot.TEAM)
#                    if user_message.content.startswith(">"):
#                        reply_message = user_message.content.strip("> ")
#                    elif user_message.content.lower() == "exit":
#                        await ctx.send("Process stopped!!")
#                        reply_message = None
#                    
#                except asyncio.TimeoutError:
#                    await ctx.send(":warning: Timeout!!")
#            
#            if reply_message:
#                receive_channel = await self.bot.fetch_channel(856057917705814056)
#                ##### reference message finder ####
#                ref_message_id = ctx.message.reference.message_id
#                ref_message_obj = await ctx.channel.fetch_message(ref_message_id)
#                ref_message_content = ref_message_obj.content
#                ########
#                ids = re.findall(r"\d+", ref_message_content)
#                user_id = int(ids[1])
#                message_id = int(ids[2])

#                files= None
#                user = await self.bot.fetch_user(user_id)
#                ###### Stuck here #####
#                message = await user.dm_channel.fetch_message(923485994156703815)
#                ##########
#                if ctx.message.attachments:
#                    files = []
#                    for attachment in ctx.message.attachments:
#                        file = await attachment.to_file()
#                        files.append(file)
#                print(1)         
#                msg = await message.reply(f"{reply_message}", files= files)
#                print(2)
#                await ctx.message.add_reaction("<:greentickbadge:852127602373951519>")
#                await ctx.reply(f"Message ID: {msg.id}")
#                
    
    @commands.command()
    async def new_dm(self, ctx, user_id: int, *, msg = None):
        users, Msg = self.db()
        if not msg:
            user = await self.bot.fetch_user(user_id)
            files= None
            if ctx.message.attachments:
                    files = []
                    for attachment in ctx.message.attachments:
                        file = await attachment.to_file()
                        files.append(file)
                    await user.send(files= files)
            else:
                await ctx.message.add_reaction("❌")
                await ctx.send("You didn't gave a message!!")
        elif ctx.author.id not in self.bot.TEAM:
            pass
        else:
            try:
                user = await self.bot.fetch_user(user_id)
            except Exception as e:
                receiver = await self.bot.fetch_channel(855048645174755358)
                await receiver.send(f"Exception in **fibu_dm**: __new_dm__ >\n {e}")
                await ctx.reply("\N{NO ENTRY SIGN} Not found this user or user might be disabled direct messages form server members!!!")
            else:
                if user.id not in users:
                    users.append(user.id)
                    new_value = {"user_id": user.id, "msg_ids": []}
                    UsersDm.tb.insert_one(new_value)
                else:
                    pass
                receive_channel = await self.bot.fetch_channel(856057917705814056)
                files= None
                if ctx.message.attachments:
                    files = []
                    for attachment in ctx.message.attachments:
                        file = await attachment.to_file()
                        files.append(file)
                sent_msg = await user.send(f"{msg}", files= files)

                to_receiver = await receive_channel.send(f"`{ctx.author.name} to {user}`:: {msg}", files= files)
                await to_receiver.reply(f"Message ID: {sent_msg.id}")
                await ctx.message.add_reaction("✅")
                await ctx.author.send(f"Message sent to {user}..\nTo Check **UserIndex** use ```!fibu show_all_dm```\nUse bellow message id to **edit or delete** message next time")
                await ctx.reply(f"Message ID: {sent_msg.id}")

    ### message edit
    @commands.command()
    async def editmsg(self, ctx, msg_id: discord.Message= None, message= None):
        if ctx.author.id not in self.bot.TEAM:
            pass
        else:
            if msg_id:
                if message:
                    from_msg = msg_id.content
                    await msg_id.edit(content= message)
                    receive_channel = await self.bot.fetch_channel(856057917705814056)
                    await receive_channel.send(f"Message Edited by {ctx.author}::\nMessageID: {msg_id.id}\nFrom: {from_msg}\nTo: {message}")
                    await ctx.send(f"Message Edited::\nFrom: {from_msg}\nTo: {message}")
                    await ctx.message.add_reaction("✅")
                else:
                    await ctx.send("Provide message")
            else:
                await ctx.send("Provid message id")
    
    ### message delete
    @commands.command()
    async def delmsg(self, ctx, msg_id: discord.Message= None):
        if ctx.author.id not in self.bot.TEAM:
            pass
        else:
                if msg_id:
                    msg_content = msg_id.content
                    await msg_id.delete()
                    receive_channel = await self.bot.fetch_channel(856057917705814056)
                    await receive_channel.send(f"Message Deleted by {ctx.author}::\nMessageID: {msg_id.id}\nMessage: {msg_content}")
                    await ctx.send(f"Message Deleted::\nMessage: {msg_content}")
                    await ctx.message.add_reaction("✅")
                    
                
    
    
    @commands.command()
    async def show_dm(self, ctx, index):
        if ctx.author.id not in self.bot.TEAM:
            pass
        else:
            users, Msg = self.db()
            data = ""
            try:
                user = users[int(index)]
                user = await self.bot.fetch_user(user)
                for i, j in enumerate(Msg[user.id]):
                    data+= f"{i} - {j}\n"
                await ctx.send(f"Username: {user}\nUserId: {user.id}\nUserIndex: {index}\nMessagesIDs:\n```\nindex - message ID\n{data}\n```")
            except Exception as e:
                receiver = await self.bot.fetch_channel(855048645174755358)
                await receiver.send(f"Exception in **fibu_dm**: __show_dm__ > {e}")
    
    @commands.command()
    async def clean_dm(self, ctx, index_no = None):
        if ctx.author.id in self.bot.TEAM:
            users, Msg = self.db()
            if index_no != None:
                user_id = users[int(index_no)]
                user = await self.bot.fetch_user(user_id)
                users.pop(int(index_no))
                UsersDm.tb.delete_one({"user_id": user.id})
                receive_channel = await self.bot.fetch_channel(856057917705814056)
                await receive_channel.send(f":warning: {user} removed from list. :warning:")
                await ctx.message.add_reaction("✅")
                await ctx.send(f"{user.name} removed from db!!")
                
            else:
                UsersDm.tb.delete_many({})
                receive_channel = await self.bot.fetch_channel(856057917705814056)
                await receive_channel.send(f":warning::warning: Users list fully cleared by `{ctx.author.name}` :warning::warning:", mention_author= True)
                await ctx.message.add_reaction("✅")
                await ctx.send("Data Successfully Deleted!!")


def setup(bot):
    bot.add_cog(UsersDm(bot))