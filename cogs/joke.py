import discord
from datetime import datetime as time
from discord.ext import commands as c
import pip
import pyjokes
try:
	import pyjokes
except:
	pip.main(["install","pyjokes"])
import asyncio, typing, random

class Joke(c.Cog):
	def __init__(self,client):
		self.client = client
    
    
 #joke
	"""@c.command()
	async def joke(self,ctx):
		joke = j.get_joke()
        	await ctx.send(joke)"""
	
	@c.command()
	async def joke(self,ctx):
		joke = pyjokes.get_joke()
		msg = discord.Embed(title = "Joke" ,description = joke, color = 0xffdf08 , timestamp = time.now())
		#msg.set_author(name = f"{client.user.name}" , icon_url = f"{client.user.avatar_url}")
		msg.set_footer(text = "Programming Hero ")
		await ctx.send(embed = msg)
		
		
def setup(bot):
	bot.add_cog(Joke(bot))
