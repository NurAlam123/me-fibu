import discord,sqlite3
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.utils import get
import pymongo
import os
import re

class Greeting(commands.Cog):
    def __init__(self, client):
            self.client = client
    
    @commands.command()
    @has_permissions(administrator=True,manage_roles=True,manage_messages=True)
    async def setWelcomeChannel(self,ctx,channel:discord.TextChannel, *, welcome_text=None):
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"] #database
        tb = db["guild_data"] #table
        get_guild = tb.find_one({"guild_id":ctx.guild.id})
        if get_guild != None:
            if welcome_text == None:
                welcome_text = "Hello, {member.mention}. Welcome to **{member.guild}**"
            new_value = {"welcome_channel": channel.id, "welcome_msg": welcome_text}
            tb.update_one({"guild_id":ctx.guild.id},{"$set":new_value})
            await ctx.send(f"Greeting channel has been updated to {channel}")
        else:
            if welcome_text == None:
                welcome_text = "Hello, {member.mention}. Welcome to **{member.guild}**"
                data = {"guild_id":ctx.guild.id,"welcome_channel":channel.id, "welcome_msg": welcome_text}
                tb.insert_one(data)
                await ctx.send(f"Greeting channel has been set to {channel}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.send(f"Hello {member.mention}! Welcome to **{member.guild}** server.\nI am Fibu. Your friend and a friendly bot. I am from **Programming Hero**.🙂\nMy prefix is ```!fibu ```\nFor help type ```!fibu help```")
#		welcomeChannel = c_fibu.execute("select welcome_channel from guild_data where guild_id=?",(member.guild.id,)).fetchone()
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"] #database
        tb = db["guild_data"] #table
        welcomeChannel = tb.find_one({"guild_id":member.guild.id})
        
        ## message customization part
        welcome_msg = welcomeChannel["welcome_msg"]
        if welcome_msg != None:
            find_attributes = re.findall("{[a-z]+\.[a-z]+}"[1:-1], welcome_msg) # finding all attributes that are between { and } and removing the curly braces
            for attribute in find_attributes:
                split_attribute = attribute.split(".")
                first = split_attribute[0]. lower()
                last = split_attribute[1].lower()
                if first == "user" or first == "member":
                    if last == "name":
                        welcome_msg = welcome_msg.replace("{"+first+".name}", member.name)
                    elif last == "id":
                        welcome_msg = welcome_msg.replace("{"+first+".id}", member.id)
                    elif last == "mention":
                        welcome_msg = welcome_msg.replace("{"+first+".mention}", member.mention)
                    elif last == "user":
                        welcome_msg = welcome_msg.replace("{"+first+".user}", member)
                elif first == "server" or first == "guild":
                    if last == "name":
                        welcome_msg = welcome_msg.replace("{"+first+".name}", member.guild.name)
                    elif last == "id":
                        welcome_msg = welcome_msg.replace("{"+first+".id}", member.guild.id)
                    elif last == "mention":
                        welcome_msg = welcome_msg.replace("{"+first+".mention}", member.guild)
                    #elif last == "user":
#                        welcome_msg = welcome_msg.replace("{"+first+".user}", member)
        ## End
        else:
            welcome_msg = "Hello, {member.mention}. Welcome to **{member.guild}**"
        if welcomeChannel is None:
            sys_channel = member.guild.system_channel
            if sys_channel is None:
                channel = get(member.guild.channels,name="general")
                if channel is None:
                    pass
                else:
                    await channel.send(welcome_msg)
            else:
                await sys_channel.send(welcome_mag)
        else:
            welcomeChannel = get(member.guild.channels,id=welcomeChannel["welcome_channel"])
            if welcomeChannel is None:
                pass
            else:
                await welcomeChannel.send(welcome_msg)
    
    @commands.command()
    async def hello(self,ctx):
        await ctx.message.add_reaction("🙂")
        await ctx.send(f"Hello {ctx.author.mention}! How are you?")
    @commands.command()
    async def dm(self,ctx,member: discord.Member=None):
        await ctx.message.add_reaction("👍")
        if member==None:
            await ctx.send(f"Check DM {ctx.author.mention}")
            await ctx.author.send(f"Hey {ctx.author.mention}!")
        else:
            if member.id == self.client.user.id:
                await ctx.send("Hey it's me. I can't DM myself.")
            elif member.bot:
                await ctx.send(f"{member.mention} is a bot. I can't DM a bot.")
            else:
                await ctx.send(f"Check DM {member.mention}")
                await member.send(f"Hey {member.mention}!")
	
    @commands.Cog.listener("on_message")
    async def message(self,msg):
        if msg.content.lower() == "!fibu thank you" or msg.content.lower() == "!fibu thanks" or msg.content.lower() == "!fibu thnx" or msg.content.lower() == "!fibu tnx" or msg.content.lower() == "!fibu tnq":
            await msg.add_reaction("❤️")
        if msg.content.lower()=="!fibu ok":
            await msg.add_reaction("👌")
        if msg.content.lower() == "!fibu sorry" or msg.content.lower() == "!fibu sry" or msg.content.lower() == "!fibu forgive me" or msg.content.lower() == "!fibu forgive":
            await msg.add_reaction("🙂")
            await msg.channel.send("Ok... I forgive you. But don't repeat it again!")

    #permission error handling
    @setWelcomeChannel.error
    async def perm_error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have the permissions to do that!")

				
def setup(bot):
    bot.add_cog(Greeting(bot))