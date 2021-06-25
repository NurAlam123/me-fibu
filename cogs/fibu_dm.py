import discord
from discord.ext import commands
import pymongo
import os

class UsersDm(commands.Cog):

    con_fibu = pymongo.MongoClient(os.getenv("DB"))
    db = con_fibu["fibu"] #database
    tb = db["DmUsers"] #table
    def __init__(self, client):
        self.bot = client
        
    def db(self):
        all_users = UsersDm.tb.find()
        if all_users != None:
            users = []
            Msg = {}
            for user in all_users:
                user_id = user['user_id']
                user_msg_ids = user['msg_ids']
                Msg[user_id] = user_msg_ids
                users.append(user_id)

        else:
            users = []
            Msg = {}
        return users, Msg
        
    async def cog_check(self, ctx):
        return ctx.author.id in self.bot.TEAM

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.channel.DMChannel):
            con_fibu = pymongo.MongoClient(os.getenv("DB"))
            db = con_fibu["fibu"] #database
            other_tb = db["other_data"] #table
            field =  other_tb.find_one({'name': 'ignore_dm'})
            if field:
                user_ids = field.get('user_ids')
                if not user_ids:
                    user_ids = []
            else:
                user_ids = []
            if message.author.id not in user_ids:
                users, Msg = self.db()
                ###################
                receivers = [i for i in self.bot.TEAM if i != message.author.id]
                if len(users) >= 20:
                    removed_user_id = users.pop(0)
                    user = await self.bot.fetch_user(removed_user_id)
                    UsersDm.tb.delete_one({"user_id": removed_user_id})
                    for receiver in receivers:
                            receiver = await self.bot.fetch_user(receiver)
                            await receiver.send(f":warning: {user} remove from list.:warning:", mention_author= True)
                        
                        
                elif Msg.get(message.author.id):
                    all_msg_id = Msg[message.author.id]
                    if len(all_msg_id) >= 5:
                        all_msg_id.pop(0)
                        Msg[message.author.id] = all_msg_id
                        new_value = {"msg_ids": all_msg_id}
                        UsersDm.tb.update_one({"user_id": message.author.id}, {"$set":new_value})
                    else: pass
                else: pass
            ##################
                if message.content.startswith("!"):
                    pass
                else:
                    if message.author.id == self.bot.user.id or message.author.id in self.bot.TEAM:
                        pass
                    else:
                        id = message.author.id
                        if id not in users:
                            users.append(id)
                            Msg[id] = [message.id]
                            new_value = {"user_id":  id, "msg_ids": [message.id]}
                            UsersDm.tb.insert_one(new_value)
                        elif id not in Msg and id in users:
                            Msg[id] = [message.id]
                            new_value = {"msg_ids": message.id}
                            UsersDm.tb.update_one({"user_id": id}, {"$set": new_value})
                        elif id in Msg:
                            if message.id not in Msg[id]:
                                Msg[id].append(message.id)
                                UsersDm.tb.update_one({"user_id": id}, {"$set": {"msg_ids": Msg[id]}})
                            
                        name = message.author
                        for dev in self.bot.TEAM:
                            receiver = await self.bot.fetch_user(dev)
                            info_format = f"----------\n**Username:** {name}\n**UserIndex:** {users.index(id)}\n**MessageIndex**: {Msg[id].index(message.id)}\n**UserId:** {id}\n**MessageId:** {message.id}\n----------"
                            to_receiver = await receiver.send(info_format)
                            if message.attachments:
                                attach_format = f"`{name}::` {message.content}\n--- Attachment!! ---"
                                await to_receiver.reply(attach_format)
                                for attachment in message.attachments:
                                    await to_receiver.reply(attachment.url)
                            else:
                                message_format = f"`{name}::` {message.content}\n"
                                await to_receiver.reply(message_format)

    @commands.Cog.listener()
    async def on_message_edit(self, before_msg, after_msg):
        if isinstance(before_msg.channel, discord.channel.DMChannel):
                users, Msg = self.db()
                for dev in self.bot.TEAM:
                    receiver = await self.bot.fetch_user(dev)
                    id = before_msg.author.id
                    name = before_msg.author.name
                    if id != self.bot.user.id:
                        identity_format = f"----------\n**Username:** {name}\n**UserIndex:** {users.index(id)}\n**MessageIndex**: {Msg[id].index(after_msg.id)}\n**UserId:** {id}\n**MessageId:** {after_msg.id}\n----------"
                        to_receiver = await receiver.send(identity_format)
                        edit_msg_format = f"++++ Message Edited ++++\n**From:** {before_msg.content}\n**To:** {after_msg.content}"
                        await to_receiver.reply(edit_msg_format)
                    else: pass

    @commands.command()
    @commands.dm_only()
    async def msg(self, ctx, index_no: int, *, message):
        if ctx.author.id in self.bot.TEAM:
            users, Msg = self.db()
            receivers = [i for i in self.bot.TEAM if i != ctx.author.id]
            try:
                id = users[index_no]
            except Exception as e:
                receiver = await self.bot.fetch_user(self.bot.TEAM[0])
                await receiver.send(f'Exception in msg: {e}')
                await ctx.send("User not in list.\nTry `new_dm` command to continue!!")
            else:
                files= None
                user = await self.bot.fetch_user(id)
                # async with ctx.channel.typing():
                if ctx.message.attachments:
                    files = []
                    for attachment in ctx.message.attachments:
                        file = await attachment.to_file()
                        files.append(file)
                        
                msg = await user.send(f"{message}", files= files)
                for receiver in receivers:
                    receiver = await self.bot.fetch_user(receiver)
                    to_receiver = await receiver.send(f"`{ctx.author.name} to {user}::` {message}", files= files)
                    await to_receiver.reply(f'Message ID: {msg.id}')
                
                await ctx.message.add_reaction("✅")
                await ctx.send(f'Message sent to {user}..\nUse bellow message id to **edit or delete** message next time')
                await ctx.reply(f'Message ID: {msg.id}')
                
    @commands.command()
    async def reply(self, ctx, user_index: int, msg_index: int, *, message):
        if ctx.author.id in self.bot.TEAM:
            users, Msg = self.db()
            receivers = [i for i in self.bot.TEAM if i != ctx.author.id]
            try:
                user_id = users[user_index]
            except Exception as e:
                receiver = await self.bot.fetch_user(self.bot.TEAM[0])
                await receiver.send(f'Exception in reply: {e}')
                await ctx.send("User not in list.\nTry `new_dm` command to continue!!")
            else:
                try:
                    msg_id = Msg[user_id][msg_index]
                except Exception as e:
                    receiver = await self.bot.fetch_user(self.bot.TEAM[0])
                    await receiver.send(f'Exception in reply: {e}')
                    await ctx.send("Oops!! Message not found..\nTry `msg` command!!")
                else:
                    files= None
                    user = await self.bot.fetch_user(user_id)
                    msg = await user.fetch_message(msg_id)
                    # async with ctx.channel.typing():
                    if ctx.message.attachments:
                        files = []
                        for attachment in ctx.message.attachments:
                            file = attachment.to_file()
                            files.append(file)
                    reply_msg = await msg.reply(f"{message}", files= files)
                    for receiver in receivers:
                        receiver = await self.bot.fetch_user(receiver)
                        to_receiver = await receiver.send(f"`{ctx.author.name} replied to {user}::` {message}", files= files)
                        await to_receiver.reply(f'Message ID: {reply_msg.id}')
                    await ctx.message.add_reaction("✅")
                    await ctx.send(f'You replied a message of {user}..\nUse bellow message id to **edit or delete** message next time')
                    await ctx.reply(f'Message ID: {reply_msg.id}')
                

    @commands.command()
    async def show_all_dm(self, ctx):
        if ctx.author.id not in self.bot.TEAM:
            pass
        else:
            users, Msg = self.db()
            data = ""
            for user_id in users:
                user = await self.bot.fetch_user(user_id)
                data += f"{users.index(user_id)} - {user.name} - {user_id}\n"
            if users == []:
               await ctx.send("Empty List")
            else:
                await ctx.send(data)
    
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
                await ctx.message.add_reaction('❌')
                await ctx.send("You didn't gave a message!!")
        elif ctx.author.id not in self.bot.TEAM:
            pass
        else:
            try:
                user = await self.bot.fetch_user(user_id)
            except Exception as e:
                receiver = await self.bot.fetch_user(self.bot.TEAM[0])
                await receiver.send(f'Exception in new_dm: {e}')
                await ctx.reply("\N{NO ENTRY SIGN} Not found this user or user might be disabled direct messages form server members!!!")
            else:
                if user.id not in users:
                    users.append(user.id)
                    new_value = {"user_id": user.id, "msg_ids": []}
                    UsersDm.tb.insert_one(new_value)
                else:
                    pass
                receivers = [i for i in self.bot.TEAM if i != ctx.author.id]
                files= None
                if ctx.message.attachments:
                    files = []
                    for attachment in ctx.message.attachments:
                        file = await attachment.to_file()
                        files.append(file)
                sent_msg = await user.send(f"{msg}", files= files)
                
                for receiver in receivers:
                    receiver = await self.bot.fetch_user(receiver)
                    to_receiver = await receiver.send(f"`{ctx.author.name} to {user}`:: {msg}", files= files)
                    await to_receiver.reply(f'Message ID: {sent_msg.id}')
                await ctx.message.add_reaction("✅")
                await ctx.author.send(f'Message sent to {user}..\nTo Check **UserIndex** use ```!fibu show_all_dm```\nUse bellow message id to **edit or delete** message next time')
                await ctx.reply(f'Message ID: {sent_msg.id}')

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
                    receivers = [i for i in self.bot.TEAM if i != ctx.author.id]
                    for receiver in receivers:
                            receiver = await self.bot.fetch_user(receiver)
                            await receiver.send(f"Message Edited by {ctx.author}::\nMessageID: {msg_id.id}\nFrom: {from_msg}\nTo: {message}")
                    await ctx.send(f"Message Edited::\nFrom: {from_msg}\nTo: {message}")
                    await ctx.message.add_reaction('✅')
                else:
                    await ctx.send('Provide message')
            else:
                await ctx.send('Provid message id')
    
    ### message delete
    @commands.command()
    async def delmsg(self, ctx, msg_id: discord.Message= None):
        if ctx.author.id not in self.bot.TEAM:
            pass
        else:
                if msg_id:
                    msg_content = msg_id.content
                    await msg_id.delete()
                    receivers = [i for i in self.bot.TEAM if i != ctx.author.id]
                    for receiver in receivers:
                            receiver = await self.bot.fetch_user(receiver)
                            await receiver.send(f"Message Deleted by {ctx.author}::\nMessageID: {msg_id.id}\nMessage: {msg_content}")
                    await ctx.send(f"Message Deleted::\nMessage: {msg_content}")
                    await ctx.message.add_reaction('✅')
                    
                
    
    
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
                    data+= f'{i} - {j}\n'
                await ctx.send(f'Username: {user}\nUserId: {user.id}\nUserIndex: {index}\nMessagesIDs:\n```\nindex - message ID\n{data}\n```')
            except Exception as e:
                receiver = await self.bot.fetch_user(self.bot.TEAM[0])
                await receiver.send(f'Exception in show_dm: {e}')
    
    @commands.command()
    async def clean_dm(self, ctx, index_no = None):
        if ctx.author.id in self.bot.TEAM:
            users, Msg = self.db()
            if index_no != None:
                user_id = users[int(index_no)]
                user = await self.bot.fetch_user(user_id)
                users.pop(int(index_no))
                UsersDm.tb.delete_one({"user_id": user.id})
                receivers = [i for i in self.bot.TEAM if i != ctx.author.id]
                for receiver in receivers:
                        receiver = await self.bot.fetch_user(receiver)
                        await receiver.send(f":warning: {user} removed from list. :warning:", mention_author= True)
                await ctx.message.add_reaction('✅')
                await ctx.send(f"{user.name} removed from db!!")
                
            else:
                UsersDm.tb.delete_many({})
                receivers = [i for i in self.bot.TEAM if i != ctx.author.id]
                for receiver in receivers:
                        receiver = await self.bot.fetch_user(receiver)
                        await receiver.send(f":warning::warning: Users list fully cleared by `{ctx.author.name}` :warning::warning:", mention_author= True)
                await ctx.message.add_reaction('✅')
                await ctx.send("Data Successfully Deleted!!")


def setup(bot):
    bot.add_cog(UsersDm(bot))