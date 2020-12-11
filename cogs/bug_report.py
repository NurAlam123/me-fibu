import discord
from discord.ext import commands
from discord.utils import get
import sqlite3
from datetime import datetime as time
import asyncio

class Bug(commands.Cog):
	def __init__(self,client):
		self.client = client
	
	questions = ["Where did you find the bug? Forums, Settings, Profiles, or in the content?","If the bug is in the content, please write the Galaxy name > Module name > Lesson name (if applicable) > and the Page Name (For eg: Fundamentals > Functions > function usage > 2/9)","What we need to do to see the bug? (how to reproduce the bug/issue?)","What is the expected behaviour? What should we change?","Please take a screenshot and post it in the #🕸bugs-or-issues channel... Appreciated your support!"]
	reports = []
	channel = None
	submit = "no"
	@commands.command()
	async def apply(self,ctx):
		await ctx.message.add_reaction("🐞")
		await ctx.author.send("Thank you for informing this bug. Please provide some extra information to make it easier for the developer to fix. Send 'Ok' to continue.")
		try:
			ok = await self.client.wait_for("message",check=lambda msg: msg.author.id==ctx.author.id,timeout=60)
			await asyncio.sleep(2)
			if ok.content.lower()=="ok":
				for i in range(len(self.questions)):
					ques = discord.Embed(title="Question", description=f"{self.questions[i]}",color=0xffdf08, timestamp=time.now())
					ques.set_author(name=self.client.user.name,icon_url=self.client.user.avatar_url)
					ques.set_footer(text="Programming Hero")
					await ctx.author.send(embed=ques)
					ans = await self.client.wait_for("message",check=lambda msg: msg.author.id==ctx.author.id)
					ques_with_ans = f"**Question:** {self.questions[i]}\n**Answer:** {ans.content.capitalize()}"
					self.reports.append(ques_with_ans)
					if i >= len(self.questions)-1:
						await ctx.author.send("Send 'Done' to submit.")
						done = await self.client.wait_for("message",check=lambda msg:msg.author.id==ctx.author.id)
						if done.content.lower()=="done":
							await ctx.author.send("Submitted successfully!")
							self.submit = "yes"
							self.i = 0
							break
			else:
				await ctx.author.send("Oops.. Try again!")
		except asyncio.TimeoutError:
						await ctx.author.send("Time Out!!\nYou haven't responds in time!\nTry again.")
						pass
		if self.submit== "yes":
			if self.channel is None:
				channel = ctx.guild.system_channel
				if channel is not None:
					self.channel = channel.id
				else:
					self.channel = get(ctx.guild.channels,name="general").id
		else:
			self.channel = ctx.message.channel.id

			em = discord.Embed(title=f"New Bug Reported | Repoter: {ctx.author}", description="\n".join(self.reports),color=0xffdf08, timestamp=time.now())
			em.set_author(name=self.client.user.name,icon_url=self.client.user.avatar_url)
			em.set_footer(text="Programming Hero")
			await get(ctx.guild.channels,id=self.channel).send(embed=em)
			self.reports = []
			self.submit = "no"
#set channel	
	@commands.command()
	async def setBugReportChannel(self,ctx,channel:discord.TextChannel):
			self.channel = channel.id
			await ctx.send("Bug reports update channel has been set!")
			
def setup(bot):
	bot.add_cog(Bug(bot))