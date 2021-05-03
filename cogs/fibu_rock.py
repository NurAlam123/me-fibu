import discord
from discord.ext import commands
import pymongo
import os

class UsersDm(commands.Cog):
    
    DEVS = [680360098836906004,728260210464129075,664550550527803405,693375549686415381]
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
        return ctx.author.id in UsersDm.DEVS

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.channel.DMChannel):
            users, Msg = self.db()
        ###################
            receivers = [i for i in UsersDm.DEVS if i != message.author.id]
            if len(users) >= 20:
                removed_user_id = users.pop(0)
                user = await self.bot.fetch_user(removed_user_id)
                UsersDm.tb.delete_one({"user_id": removed_user_id})
                for receiver in receivers:
                        receiver = await self.bot.fetch_user(receiver)
                        await receiver.send(f"{user} remove from list.")
                    
                    
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
                if message.author.id == self.bot.user.id or message.author.id in UsersDm.DEVS:
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
                        
                    name = message.author.name
                    for dev in UsersDm.DEVS:
                        receiver = await self.bot.fetch_user(dev)
                        info_format = f"----------\n**Username:** {name}\n**UserIndex:** {users.index(id)}\n**MessageIndex**: {Msg[id].index(message.id)}\n**UserId:** {id}\n**MessageId:** {message.id}\n----------"
                        await receiver.send(info_format)
                        if message.attachments:
                            attach_format = f"`{name}::` {message.content}\n--- Attachment!! ---"
                            await receiver.send(attach_format)
                            for attachment in message.attachments:
                                await receiver.send(attachment.url)
                        else:
                            message_format = f"`{name}::` {message.content}\n"
                            await receiver.send(message_format)

    @commands.Cog.listener()
    async def on_message_edit(self, before_msg, after_msg):
        if isinstance(before_msg.channel, discord.channel.DMChannel):
                users, Msg = self.db()
                for dev in UsersDm.DEVS:
                    receiver = await self.bot.fetch_user(dev)
                    id = before_msg.author.id
                    name = before_msg.author.name
                    if id != self.bot.user.id:
                        identity_format = f"----------\n**Username:** {name}\n**UserIndex:** {users.index(id)}\n**MessageIndex**: {Msg[id].index(after_msg.id)}\n**UserId:** {id}\n**MessageId:** {after_msg.id}\n----------"
                        await receiver.send(identity_format)
                        edit_msg_format = f"++++ Message Edited ++++\n**From:** {before_msg.content}\n**To:** {after_msg.content}"
                        await receiver.send(edit_msg_format)
                    else: pass

    @commands.command()
    async def msg(self, ctx, index_no: int, *, message):
        if ctx.author.id in UsersDm.DEVS:
            users, Msg = self.db()
            receivers = [i for i in UsersDm.DEVS if i != ctx.author.id]
            try:
                id = users[index_no]
                user = await self.bot.fetch_user(id)
                 # async with ctx.channel.typing():
                await user.send(f"{message}")
                await ctx.message.add_reaction("✅")
                for receiver in receivers:
                    receiver = await self.bot.fetch_user(receiver)
                    await receiver.send(f"`{ctx.author.name} to {user}::` {message}")
            except:
                await ctx.send("User not in list.\nTry `new_dm` command to continue!!")
                
    @commands.command()
    async def reply(self, ctx, user_index: int, msg_index: int, *, message):
        if ctx.author.id in UsersDm.DEVS:
            users, Msg = self.db()
            receivers = [i for i in UsersDm.DEVS if i != ctx.author.id]
            try:
                user_id = users[user_index]
                try:
                    msg_id = Msg[user_id][msg_index]
                    user = await self.bot.fetch_user(user_id)
                    msg = await user.fetch_message(msg_id)
                    # async with ctx.channel.typing():
                    await msg.reply(f"{message}")
                    await ctx.message.add_reaction("✅")
                    for receiver in receivers:
                        receiver = await self.bot.fetch_user(receiver)
                        await receiver.send(f"`{ctx.author.name} to {user}::` {message}")
                except:
                    await ctx.send("Oops!! Message not found..\nTry `msg` command!!")
            except:
                await ctx.send("User not in list.\nTry `new_dm` command to continue!!")                

    @commands.command()
    async def show_all_dm(self, ctx):
        if ctx.author.id not in UsersDm.DEVS:
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
        if msg is None:
            await ctx.send("Give a message!!")
        if ctx.author.id not in UsersDm.DEVS:
            pass
        else:
            try:
                user = await self.bot.fetch_user(user_id)
                if user.id not in users:
                    users.append(user.id)
                    new_value = {"user_id": user.id, "msg_ids": []}
                    UsersDm.tb.insert_one(new_value)
                else:
                    pass
                receivers = [i for i in UsersDm.DEVS if i != ctx.author.id]
                await user.send(f"{msg}")
                for receiver in receivers:
                    receiver = await self.bot.fetch_user(receiver)
                    await receiver.send(f"`{ctx.author.name}`:: {msg}")
                await ctx.message.add_reaction("✅")
            except:
                await ctx.send("Not found this user")

    @commands.command()
    async def clean_dm(self, ctx, index_no = None):
        if ctx.author.id in UsersDm.DEVS:
            users, Msg = self.db()
            if index_no != None:
                user_id = users[int(index_no)]
                user = await self.bot.fetch_user(user_id)
                users.pop(int(index_no))
                UsersDm.tb.delete_one({"user_id": user.id})
                receivers = [i for i in UsersDm.DEVS if i != ctx.author.id]
                for receiver in receivers:
                        receiver = await self.bot.fetch_user(receiver)
                        await receiver.send(f"{user} removed from list.")
                await ctx.send(f"{user.name} removed from db!!")
                
            else:
                UsersDm.tb.delete_many({})
                receivers = [i for i in UsersDm.DEVS if i != ctx.author.id]
                for receiver in receivers:
                        receiver = await self.bot.fetch_user(receiver)
                        await receiver.send(f"Users list fully cleared by `{ctx.author.name}`")
                await ctx.send("Data Successfully Deleted!!")


def setup(bot):
    bot.add_cog(UsersDm(bot))
