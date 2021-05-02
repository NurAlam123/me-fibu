import discord
from discord.ext import commands
import pymongo
import os

class UsersDm(commands.Cog):
    
    DEVS = [680360098836906004]#,728260210464129075,664550550527803405,693375549686415381]
    con_fibu = pymongo.MongoClient(os.getenv("DB"))
    db = con_fibu["fibu"] #database
    tb = db["DmUsers"] #table
    
    def __init__(self, client):
        self.bot = client
        all_users = UsersDm.tb.find()
        
        if all_users != None:
            print(all_user['msg_ids'])
            self.users = [user["user_id"] for user in all_users]
            self.Msg = {user['user_id']: user['msg_ids'] for user in all_users}
            print(self.Msg)
        else:
            self.users = []
            self.Msg = {}
        
    async def cog_check(self, ctx):
        return ctx.author.id in UsersDm.DEVS

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.channel.DMChannel):
            if message.content.startswith("!"):
                pass
            else:
                if message.author.id == self.bot.user.id or message.author.id in UsersDm.DEVS:
                    pass
                else:
                    id = message.author.id
                    if id not in self.users:
                        self.users.append(id)
                        self.Msg[id] = [message.id]
                        new_value = {"user_id":  id, "msg_ids": [message.id]}
                        UsersDm.tb.insert_one(new_value)
                    elif id not in self.Msg and id in self.users:
                        self.Msg[id] = [message.id]
                        new_value = {"msg_ids": message.id}
                        UsersDm.tb.update_one({"user_id": id}, {"$set": new_value})
                    elif id in self.Msg:
                        if message.id not in self.Msg[id]:
                            self.Msg[id].append(message.id)
                            UsersDm.tb.update_one({"user_id": id}, {"$set": {"msg_ids": self.Msg[id]}})
                       
                    name = message.author.name
                    for dev in UsersDm.DEVS:
                        receiver = await self.bot.fetch_user(dev)
                        info_format = f"----------\n**Username:** {name}\n**UserIndex:** {self.users.index(id)}\n**UserId:** {id}\n**MessageId:** {message.id}\n**MessageIndex**: {self.Msg[id].index(message.id)}\n----------"
                        await receiver.send(info_format)
                        if message.attachments:
                            attach_format = f"`{name}::` {message.content}\n--- Attachment!! ---"
                            await receiver.send(attach_format)
                            for attachment in message.attachments:
                                await receiver.send(attachment.url)
                        else:
                            message_format = f"`{name}::` {message.content}\n"
                            await receiver.send(message_format)

 ###################
            receivers = [i for i in UsersDm.DEVS if i != message.author.id]
            if len(self.users) >= 20:
                removed_user_id = self.users.pop(0)
                user = await self.bot.fetch_user(removed_user_id)
                UsersDm.tb.delete_one({"user_id": removed_user_id})
                for receiver in receivers:
                        receiver = await self.bot.fetch_user(receiver)
                        await receiver.send(f"{user} remove from list.")
                    
                    
            elif self.Msg.get(message.author.id):
                all_msg_id = self.Msg[message.author.id]
                if len(all_msg_id) >= 5:
                    all_msg_id.pop(0)
                    self.Msg[message.author.id] = all_msg_id
                    new_value = {"msg_ids": all_msg_id}
                    UsersDm.tb.update_one({"user_id": message.author.id}, {"$set":new_value})
                else: pass
            else: pass
 ##################
    		
    @commands.Cog.listener()
    async def on_message_edit(self, before_msg, after_msg):
        if isinstance(before_msg.channel, discord.channel.DMChannel):
                for dev in UsersDm.DEVS:
                    receiver = await self.bot.fetch_user(dev)
                    id = before_msg.author.id
                    name = before_msg.author.name
                    if id != self.bot.user.id:
                        identity_format = f"----------\n**Username:** {name}\n**UserIndex:** {self.users.index(id)}\n**UserId:** {id}\n**MessageId:** {after_msg.id}\n**MessageIndex**: {self.Msg[id].index(after_msg.id)}\n----------"
                        await receiver.send(identity_format)
                        edit_msg_format = f"++++ Message Edited ++++\n**From:** {before_msg.content}\n**To:** {after_msg.content}"
                        await receiver.send(edit_msg_format)
                    else: pass

    @commands.command()
    async def msg(self, ctx, index_no: int, *, message):
        if ctx.author.id in UsersDm.DEVS:
            receivers = [i for i in UsersDm.DEVS if i != ctx.author.id]
            try:
                id = self.users[index_no]
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
            receivers = [i for i in UsersDm.DEVS if i != ctx.author.id]
            try:
                user_id = self.users[user_index]
                try:
                    msg_id = self.Msg[user_id][msg_index]
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
            data = ""
            for user_id in self.users:
                user = await self.bot.fetch_user(user_id)
                data += f"{self.users.index(user_id)} - {user.name} - {user_id}\n"
            if self.users == []:
               await ctx.send("Empty List")
            else:
                await ctx.send(data)
    
    @commands.command()
    async def new_dm(self, ctx, user_id: int, *, msg = None):
        if msg is None:
            await ctx.send("Give a message!!")
        if ctx.author.id not in UsersDm.DEVS:
            pass
        else:
            try:
                user = await self.bot.fetch_user(user_id)
                if user.id not in self.users:
                    self.users.append(user.id)
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
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"] #database
        tb = db["DmUsers"] #table
        if ctx.author.id in UsersDm.DEVS:
            if index_no != None:
                user = await self.bot.fetch_user(user_id)
                self.users.pop(int(index_no))
                tb.delete_one({"user_id": user.id})
                receivers = [i for i in UsersDm.DEVS if i != ctx.author.id]
                for receiver in receivers:
                        receiver = await self.bot.fetch_user(receiver)
                        await receiver.send(f"{user} removed from list.")
                await ctx.send("{user.name} removed!!")
                
            else:
                tb.delete()
                receivers = [i for i in UsersDm.DEVS if i != ctx.author.id]
                for receiver in receivers:
                        receiver = await self.bot.fetch_user(receiver)
                        await receiver.send(f"Users list fully cleared by `{ctx.author.name}`")
                await ctx.send("Data Successfully Deleted!!")


def setup(bot):
    bot.add_cog(UsersDm(bot))
