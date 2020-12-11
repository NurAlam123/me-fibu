import discord
from discord.ext import commands

class Greeting(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_member_join(self,member):
		await member.send(f"Hello {member.mention}! Welcome to **{member.guild}** server.\nI am Fibu. Your friend and a friendly bot. I am from Programming Hero.🙂\nMy prefix is ```!fibu ```")
	
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
			await ctx.send(f"Check DM {member.mention}")
			await member.send(f"Hey {member.mention}!")
	
	@commands.Cog.listener("on_message")
	async def message(self,msg):
		if msg.content.lower() == "!fibu thank you":
			await msg.add_reaction("❤️")
		if msg.content.lower()=="!fibu ok":
			await msg.add_reaction("👌")#
		if msg.content.lower() == "!fibu sorry":
			await msg.add_reaction("🙂")
			await msg.channel.send("Ok... I forgive you. But don't repeat it again!")

				
				
def setup(bot):
	bot.add_cog(Greeting(bot))