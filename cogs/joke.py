import discord
from datetime import datetime as time
from discord.ext import commands as c
#import pyjokes
import requests

class Joke(c.Cog):
	def __init__(self,client):
		self.client = client

	@c.command()
	async def joke(self,ctx,*,type=None):
		if type==None:
			url="https://official-joke-api.appspot.com/random_joke"
			get_joke = requests.get(url).json()
			msg = discord.Embed(title="Joke", description=f"{get_joke['setup']}\n{get_joke['punchline']}",color=0xffdf08)
			msg.set_author(name = f"{self.client.user.name}" , icon_url = f"{self.client.user.avatar_url}")
			msg.set_footer(text = "Programming Hero ")
			await ctx.send(embed = msg)
		else:
			try:
				url = f"https://official-joke-api.appspot.com/jokes/{type}/random"
				get_joke = requests.get(url).json()[0]
				msg = discord.Embed(title="Joke", description=f"{get_joke['setup']}\n{get_joke['punchline']}", color=0xffdf08, timestamp=time.now())
				msg.set_author(name = f"{self.client.user.name}" , icon_url = f"{self.client.user.avatar_url}")
				msg.set_footer(text = "Programming Hero ")
				await ctx.send(embed = msg)
			except:
				await ctx.send(f"{type} is not a valid type!")		
		
def setup(bot):
	bot.add_cog(Joke(bot))
