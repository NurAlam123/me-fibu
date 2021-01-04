import discord
from datetime import datetime as time
from discord.ext import commands as c
import pip
try:
	import pyjokes as j
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
		joke = j.get_joke()
		await ctx.send(joke)
		
def setup(bot):
	bot.add_cog(Joke(bot))
