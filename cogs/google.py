import discord
from datetime import datetime as time
from discord.ext import commands as c
import urllib.parse,urllib.request,re

class Google(c.Cog):
	def __init__(self,client):
		self.client = client
    
#youtube
	@c.group(aliases=["google","gog"],case_insensitive=True)
	async def go(slef,ctx):
		if ctx.invoked_subcommand is None:
			pass

	
	@go.command()
	async def search(self,ctx,*,query):
		query = query.split()
		search_word = "+".join(query)
		goo = "https://www.google.com/search?q="+search_word
		try:
			await ctx.message.add_reaction("✔")
			#await ctx.send(f"For viewing your results [Click here]({goo})")
			msg = discord.Embed(title="Google Search", description=f"For viewing your results [Click here]({goo})" , color=0xffdf08)
			await ctx.send(embed = msg)
			#await ctx.send(f"https://google.com/search?q={search_word}")
		except:
			await ctx.message.add_reaction("❌")
			msg = discord.Embed(title="Error", description="Oops.. Your search was not found o..\nPlease search again by typing ```!fibu go search search_word ```" , color=0xffdf08)
			await ctx.send(embed = msg)


		
		
def setup(bot):
	bot.add_cog(Google(bot))
