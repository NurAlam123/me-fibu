import discord
from discord.ext import commands


class UsersDm(commands.Cog):
    
    DEVS = [680360098836906004,728260210464129075,664550550527803405,693375549686415381,555452986885668886]
    
    def __init__(self, client):
        self.bot = client

    async def cog_check(self, ctx):
        return ctx.author.id in UserDm.DEVS
    
    users = []

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.channel.DMChannel):
            if message.content.startswith("@"):
                pass
            else:
                if message.author.id == self.bot.user.id or message.author.id in UserDm.DEVS:
                    pass
                else:
                    id = message.author.id
                    if id not in self.users:
                        self.users.append(id)
                    name = message.author.name
                    for dev in UserDm.DEVS:
                        receiver = await self.bot.fetch_user(dev)
                        info_format = f"----------\n**{id} - {name} > {self.users.index(id)}**\n----------"
                        await receiver.send(info_format)
                        if message.attachments:
                            attach_format = f"`{name}::` {message.content}\n--- Attachment!! ---"
                            await receiver.send(attach_format)
                            for attachment in message.attachments:
                                await receiver.send(attachment.url)
                            await receiver.send("------ End Attachment ------")
                        else:
                            message_format = f"`{name}::` {message.content}\n---- End ----"
                            await receiver.send(message_format)

    @commands.Cog.listener()
    async def on_message_edit(self, before_msg, after_msg):
        if isinstance(before_msg.channel, discord.channel.DMChannel):
                for dev in UserDm.DEVS:
                    receiver = await self.bot.fetch_user(dev)
                    id = before_msg.author.id
                    name = before_msg.author.name
                    if id != self.bot.user.id:
                        identity_format = f"----------\n**{id} - {name} > {self.users.index(id)}**\n----------"
                        await receiver.send(identity_format)
                        edit_msg_format = f"++++ Message Edited ++++\n**From:** {before_msg}\n**To:** {after_msg}"
                        await receiver.send(edit_msg_format)
                    else: pass

    @commands.command()
    async def msg(self, ctx, index_no: int, *, message):
        if ctx.author.id in UserDm.DEVS:
            receivers = [i for i in UserDm.DEVS if i != ctx.author.id]
            id = self.users[index_no]
            user = await self.bot.fetch_user(id)
            await user.send(f"`{ctx.author.name}` - {message}")
            for receiver in receivers:
                receiver = await self.bot.fetch_user(receiver)
                await receiver.send(f"`{ctx.author.name}`:: {message}")

    @commands.command()
    async def show_all(self, ctx):
        if ctx.author.id not in UserDm.DEVS:
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
    async def new_dm(self, ctx, user_id: int, *, msg):
        if ctx.author.id not in UserDm.DEVS:
            pass
        else:
            try:
                await ctx.message.add_reaction("✅")
                user = await self.bot.fetch_user(user_id)
                if user.id not in self.users:
                    self.users.append(user.id)
                else:
                    pass
                receivers = [i for i in UserDm.DEVS if i != ctx.author.id]
                await user.send(f"`{ctx.author.name}` - {msg}")
                for receiver in receivers:
                    receiver = await self.bot.fetch_user(receiver)
                    await receiver.send(f"`{ctx.author.name}`:: {msg}")
            except:
                await ctx.send("Not found this user")

    @commands.command()
    async def clean_msg(self, ctx, index_no = None):
        if ctx.author.id in UserDm.DEVS:
            if index_no != None:
                self.users.pop(int(index_no))
            else:
                self.users = []


def setup(bot):
    bot.add_cog(UsersDm(bot))