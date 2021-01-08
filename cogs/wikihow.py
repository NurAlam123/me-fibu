import discord
from discord.ext import commands
from datetime import datetime as time
import whapi

class WikiHow(commands.Cog):
	def __init__(self,client):
		self.client = client
	
##Search article
	@commands.command()
	async def how(self,ctx,*, query):
		search = whapi.search(query,max_results=1)
		if search == []:
			await ctx.send("No result found!")
		else:
			article_id = search[0]["article_id"]
			url = search[0]["url"]
			main = whapi.parse_intro(article_id)[:500]
			msg = discord.Embed(title=f"{search[0]['title']}", description=f"{main} ...[more info]({url})",color=0xffdf08, timestamp=time.now())
			try:
				all_step = whapi.parse_steps(article_id)
				steps = []
				for i, step in enumerate(all_step,1):
					str = f"{i} - {all_step[step]['summary']}"
					steps.append(str)
				msg.add_field(name="Steps",value="\n".join(steps))
			except:
				msg.add_field(name="Steps",value="Opps.. Not found\nClick on **more info** to get all steps and information.")
			try:
				get_image = whapi.get_images(article_id)
				thumb_image = get_image[len(get_image)-1]
				msg.set_thumbnail(url=thumb_image)
			except:
				pass
			msg.set_author(name = f"{self.client.user.name}" , icon_url = f"{self.client.user.avatar_url}")
			msg.set_footer(text = "Programming Hero ")
			await ctx.send(embed=msg)

##Random article
	@commands.command()
	async def randomHow(self,ctx):
				article_id = whapi.random_article()
				article_title = whapi.return_details(article_id)["title"]
				article_url = whapi.return_details(article_id)["url"]
				main = whapi.parse_intro(article_id)[:500]
				msg = discord.Embed(title=f"{article_title}", description=f"{main} ...[more info]({article_url})",color=0xffdf08, timestamp=time.now())
				try:
					all_step = whapi.parse_steps(article_id)
					steps = []
					for i, step in enumerate(all_step,1):
						str = f"{i} - {all_step[step]['summary']}"
						steps.append(str)
						msg.add_field(name="Steps",value="\n".join(steps))
				except:
					msg.add_field(name="Steps",value="Opps.. Not found\nClick on **more info** to get all steps and information.")
				try:
					get_image = whapi.get_images(article_id)
					thumb_image = get_image[len(get_image)-1]
					msg.set_thumbnail(url=thumb_image)
				except:
					pass
				msg.set_author(name = f"{self.client.user.name}" , icon_url = f"{self.client.user.avatar_url}")
				msg.set_footer(text = "Programming Hero ")
				await ctx.send(embed=msg)
				
			
def setup(bot):
	bot.add_cog(WikiHow(bot)) 