import discord
from discord.ext import commands
from datetime import datetime as time
import wikipedia as wiki
import asyncio

class Wiki(commands.Cog):
	def __init__(self, client):
		self.client=client
#wiki
	@commands.group(case_insensitive=True)
	async def wiki(self,ctx):
		if ctx.invoked_subcommand is None:
			pass

	@wiki.command()
	@commands.cooldown(1,30,commands.BucketType.user)
	async def search(self,ctx,*,query):
		await ctx.message.add_reaction("🔍")
		try:
			page = wiki.page(query)
			result = wiki.summary(query,sentences=4)
			wiki_msg = discord.Embed(title="Wikipedia", description=f"Showing result of **{page.title}**",color=0xffdf08,timestamp=time.now())
			wiki_msg.add_field(name=page.title,value=result)
			wiki_msg.set_author(name=self.client.user.name,icon_url=self.client.user.avatar_url)
			wiki_msg.set_footer(text="Programming Hero")
			await ctx.send(embed=wiki_msg)
		
		except wiki.exceptions.DisambiguationError as e:
			opt = e.options
			options = []
			no = 0
			no_need = 0
			page_no,pages = 1,6
			for i in range(len(opt)):
				options.append(f"{i+1}• {opt[i]}")
			need_no = round(len(options)/6)
			no_need = need_no
			options_msg = discord.Embed(title=f"Wikipedia | Page: {page_no}/{pages}", description="**Not found the page you are looking for. See the below list.**\n"+"\n".join(options[no:no_need]),color=0xffdf08, timestamp=time.now())
			options_msg.add_field(name="Rewrite the title from the above list!",value="Example: ```!fibu wiki search android (robot)```")
			options_msg.set_author(name=self.client.user.name,icon_url=self.client.user.avatar_url)
			options_msg.set_footer(text="Programming Hero")
			msg = await ctx.send(embed=options_msg)
			emojis = ["◀️","▶️"]
			for i in emojis:
				await msg.add_reaction(i)
			def re_check(reaction,user):
				return user==ctx.author and (str(reaction.emoji)) in emojis
			while True:
				try:
					reaction,user = await self.client.wait_for("reaction_add",check=re_check,timeout=60)
					if str(reaction.emoji)=="▶️" and page_no!=pages:
						page_no+=1
						no += need_no
						no_need += need_no
						options_msg = discord.Embed(title=f"Wikipedia | Page: {page_no}/{pages}", description="\n".join(options[no:no_need]),color=0xffdf08, timestamp=time.now())
						options_msg.add_field(name="Rewrite the title from the above list!",value="Example: ```!fibu wiki search android (robot)```")
						options_msg.set_author(name=self.client.user.name,icon_url=self.client.user.avatar_url)
						options_msg.set_footer(text="Programming Hero")
						await msg.edit(embed=options_msg)
						await msg.remove_reaction(reaction,user)
					elif str(reaction.emoji)=="◀️" and page_no > 1:
						page_no -= 1
						no -= need_no
						no_need -= need_no
						options_msg = discord.Embed(title=f"Wikipedia | Page: {page_no}/{pages}", description="\n".join(options[no:no_need]),color=0xffdf08, timestamp=time.now())
						options_msg.add_field(name="Rewrite the title from the above list!",value="Example: ```!fibu wiki search android (robot)```")
						options_msg.set_author(name=self.client.user.name,icon_url=self.client.user.avatar_url)
						options_msg.set_footer(text="Programming Hero")
						await msg.edit(embed=options_msg)
						await msg.remove_reaction(reaction,user)
					else:
						await msg.remove_reaction(reaction,user)
				except asyncio.TimeoutError:
					options=[]
					break
		
#select options
#	@commands.Cog.listener("on_message")
#	async def _message(self,msg):
#				if self.author == msg.author.id:
#					if msg.content.lower().startswith("select"):
#						await msg.add_reaction("🆗")
#						ind = msg.content.lower().split("select ")[1]
#						query = self.options[int(ind)-1]
#						page = wiki.page(query)
#						result = wiki.summary(query,sentences=4)
#						wiki_msg = discord.Embed(title="Wikipedia", description=f"Showing result of **{page.title}**",color=0xffdf08,timestamp=time.now())
#						wiki_msg.add_field(name=page.title,value=result)
#						wiki_msg.set_author(name=self.client.user.name,icon_url=self.client.user.avatar_url)
#						wiki_msg.set_footer(text="Programming Hero ")
#						await msg.channel.send(embed=wiki_msg)
#						self.author = 0
#						self.no = 0
#						self.no_need = 0
#						self.options=[]

				
def setup(bot):
	bot.add_cog(Wiki(bot))