import discord,sqlite3
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.utils import get
import pymongo,os
	
class Greeting(commands.Cog):
	def __init__(self, client):
		self.client = client	
	
	@commands.command()
	@has_permissions(administrator=True,manage_roles=True,manage_messages=True)
	async def setWelcomeChannel(self,ctx,channel:discord.TextChannel):
		con_fibu = pymongo.MongoClient(os.getenv("DB"))
		db = con_fibu["fibu"] #database
		tb = db["guild_data"] #table
		get_guild = tb.find_one({"guild_id":ctx.guild.id})
		if get_guild!=None:
			new_value = {"welcome_channel": channel.id}
			tb.update_one({"guild_id":ctx.guild.id},{"$set":new_value})
			await ctx.send(f"Greeting channel has been updated to {channel}")
		else:
			data = {"guild_id":ctx.guild.id,"welcome_channel":channel.id}
			tb.insert_one(data)
			await ctx.send(f"Greeting channel has been set to {channel}")
			
		
#		get_guild = c_fibu.execute("select welcome_channel from guild_data where guild_id=?",(ctx.guild.id,)).fetchone()
#		if get_guild!=None:
#			c_fibu.execute("update guild_data set welcome_channel=? where guild_id=?",(channel.id,ctx.guild.id,))
#			con_fibu.commit()
#			await ctx.send(f"Greeting channel has been updated to {channel}")
#		else:
#			c_fibu.execute("insert into guild_data(guild_id,welcome_channel) values (?,?)",(ctx.guild.id,channel.id,))
#			con_fibu.commit()
#			await ctx.send(f"Greeting channel has been set to {channel}")
#			

	@commands.Cog.listener()
	async def on_member_join(self,member):
		await member.send(f"Hello {member.mention}! Welcome to **{member.guild}** server.\nI am Fibu. Your friend and a friendly bot. I am from Programming Hero.🙂\nMy prefix is ```!fibu ```\nFor help type ```!fibu help```")
#		welcomeChannel = c_fibu.execute("select welcome_channel from guild_data where guild_id=?",(member.guild.id,)).fetchone()
		con_fibu = pymongo.MongoClient(os.getenv("DB"))
		db = con_fibu["fibu"] #database
		tb = db["guild_data"] #table
		welcomeChannel = tb.find_one({"guild_id":member.guild.id})
		if welcomeChannel is None:
			sys_channel = member.guild.system_channel
			if sys_channel is None:
				channel = get(member.guild.channels,name="general")
				if channel is None:
					pass
				else:
					await channel.send(f"Hello, {member.mention}. Welcome to **{member.guild}**")
			else:
				await sys_channel.send(f"Hello, {member.mention}. Welcome to **{member.guild}**")
		else:
			welcomeChannel = get(member.guild.channels,id=welcomeChannel["welcome_channel"])
			if welcomeChannel is None:
				pass
			else:
				await welcomeChannel.send(f"Hello, {member.mention}. Welcome to **{member.guild}**")

	
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
			if member.id == self.client.id:
				pass
			else:
				await ctx.send(f"Check DM {member.mention}")
				await member.send(f"Hey {member.mention}!")
	
	@commands.Cog.listener("on_message")
	async def message(self,msg):
		if msg.content.lower() == "!fibu thank you":
			await msg.add_reaction("❤️")
		if msg.content.lower()=="!fibu ok":
			await msg.add_reaction("👌")
		if msg.content.lower() == "!fibu sorry":
			await msg.add_reaction("🙂")
			await msg.channel.send("Ok... I forgive you. But don't repeat it again!")

	@commands.command()
	async def showdb(self,ctx):
				db = c_fibu.execute("select * from guild_data")
				await ctx.send(db.fetchall())
				
				
def setup(bot):
	bot.add_cog(Greeting(bot))
