import discord
from datetime import datetime as time
from discord.ext import commands as c
import pyjokes
import requests

class Twister(c.Cog):
	def __init__(self,client):
		self.client = client

	@c.command()
	async def twister(self,ctx):
		twis = pyjokes.get_joke(category = "twister")
		msg = discord.Embed(title="Tongue Twister", description=f"{twis}", color=0xffdf08, timestamp=time.now())
		msg.set_author(name = f"{self.client.user.name}" , icon_url = f"{self.client.user.avatar_url}")
		msg.set_footer(text = "Programming Hero ")
		
def setup(bot):
	bot.add_cog(Twister(bot))
