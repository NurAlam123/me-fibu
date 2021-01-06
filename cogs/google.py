import discord
from datetime import datetime as time
from discord.ext import commands as c
import urllib.parse,urllib.request,re

class Google(c.Cog):
	def __init__(self,client):
		self.client = client
    
#youtube
	@c.group(aliases=["google","go"],case_insensitive=True)
	async def go(slef,ctx):
		if ctx.invoked_subcommand is None:
			pass
	@go.command()
	async def search(self,ctx,*,query):
		
		query = query.split()
     		search_word = "+".join(query)
		html = urllib.request.urlopen("https://www.google.com/search?q="+search_word)
    		goo = "https://www.google.com/search?q="+search_word
		try:
			
			await ctx.message.add_reaction("📺")
			await ctx.send("For viewing your results [Click here](goo))
		except:
			await ctx.message.add_reaction("❌")
			msg = discord.Embed(title="Error", description="Oops.. Your search was not found o..\nPlease search again by typing ```!fibu go search search_word ```")
			await ctx.send(embed=msg)


		
		
def setup(bot):
	bot.add_cog(Google(bot))
