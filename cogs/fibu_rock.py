import discord
from discord.ext import commands
import pymongo
import os

class UsersDm(commands.Cog):
    
    DEVS = [680360098836906004]#,728260210464129075,664550550527803405,693375549686415381]
    
    def __init__(self, client):
        self.bot = client

    async def cog_check(self, ctx):
        return ctx.author.id in UsersDm.DEVS
    
    con_fibu = pymongo.MongoClient(os.getenv("DB"))
    db = con_fibu["fibu"] #database
    tb = db["DmUsers"] #table
    all_users = tb.find()
    users = [user["user_id"] for user in all_users]
    Msg = {user["user_id"]: user["msg_ids"] for user in all_users}

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
                    if id not in UsersDm.users:
                        UsersDm.users.append(id)
                        UsersDm.Msg[id] = [message.id]
                        new_value = {"user_id":  id, "msg_ids": [message.id]}
                        UsersDm.tb.insert_one(new_value)
                    elif message.id not in Msg[id]:
                        msg_id = message.id
                        UsersDm.Msg[id].append(msg_id)
                        new_value = {"msg_ids": UsersDm.Msg[id]}
                        tb.update_one({"user_id": id}, {"$set": new_value})
                        
                    name = message.author.name
                    for dev in UsersDm.DEVS:
                        receiver = await self.bot.fetch_user(dev)
                        info_format = f"----------\n**Username:** {name}\n**UserIndex:** {UsersDm.users.index(id)}\n**UserId:** {id}\n**MessageId:** {message.id}\n**MessageIndex**: {UsersDm.Msg.index(after_msg.id)}\n----------"
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
            if len(UsersDm.users) >= 20:
                removed_user_id = UsersDm.users.pop(0)
                tb.delete_one({"user_id": removed_user_id})
            elif UsersDm.Msg.get(message.author.id):
                all_msg_id = UsersDm.Msg[message.author.id]
                if len(all_msg_id) >= 5:
                    all_msg_id.pop(0)
                    UsersDm.Msg[message.author.id] = all_msg_id
                    new_value = {"msg_ids": all_msg_id}
                    tb.update_one({"user_id": message.author.id}, {"$set":new_value})
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
                        identity_format = f"----------\n**Username:** {name}\n**UserIndex:** {UsersDm.users.index(id)}\n**UserId:** {id}\n**MessageId:** {after_msg.id}\n**MessageIndex**: {UsersDm.Msg.index(after_msg.id)}\n----------"
                        await receiver.send(identity_format)
                        edit_msg_format = f"++++ Message Edited ++++\n**From:** {before_msg.content}\n**To:** {after_msg.content}"
                        await receiver.send(edit_msg_format)
                    else: pass

    @commands.command()

    async def msg(self, ctx, index_no: int, *, message):

        if ctx.author.id in UsersDm.DEVS:

            receivers = [i for i in UsersDm.DEVS if i != ctx.author.id]

            try:

                id = UsersDm.users[index_no]

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

                user_id = UsersDm.users[index_no]

                try:

                    msg_id = UsersDm.Msg[user_id][msg_index]

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
            for user_id in UsersDm.users:
                user = await self.bot.fetch_user(user_id)
                data += f"{UsersDm.users.index(user_id)} - {user.name} - {user_id}\n"
            if UsersDm.users == []:
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
                if user.id not in UsersDm.users:
                    UsersDm.users.append(user.id)
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
                users.pop(int(index_no))
                tb.update_one({"field_id": 1}, {"$set": {"Users": UsersDm.users}})
                await ctx.send("{user.name} removed!!")
                
            else:
                tb.update_one({"field_id": 1}, {"$set": {"Users": []}})
                await ctx.send("Data Successfully Deleted!!")


def setup(bot):
    bot.add_cog(UsersDm(bot))
