import discord
from discord.ext import commands
from datetime import datetime as time
import whapi

class WikiHow(commands.Cog):
	def __init__(self,client):
		self.client = client
	
	@commands.command()
	async def how(self,ctx,*, query):
		search = whapi.search(query,max_results=1)
		if search == []:
			await ctx.send("No result found!")
		else:
			article_id = search[0]["article_id"]
			url = search[0]["url"]
			main = whapi.parse_intro(article_id)[:500]
			all_step = whapi.parse_steps(article_id)
			steps = []
			for i, step in enumerate(all_step,1):
				str = f"{i} - {all_step[step]['summary']}"
				steps.append(str)
			msg = discord.Embed(title=f"{search[0]['title']}", description=f"{main} ...[more info]({url})",color=0xffdf08, timestamp=time.now())
			msg.add_field(name="Steps",value="\n".join(steps))
			msg.set_author(name = f"{self.client.user.name}" , icon_url = f"{self.client.user.avatar_url}")
			msg.set_footer(text = "Programming Hero ")
			await ctx.send(embed=msg)
			
def setup(bot):
	bot.add_cog(WikiHow(bot)) 