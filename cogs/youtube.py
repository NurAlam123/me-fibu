import discord
from datetime import datetime as time
from discord.ext import commands
from pyyoutube import Api
import re

class Youtube(commands.Cog):
	def __init__(self,client):
		self.client = client
    
#youtube
	@commands.group(aliases=["youtube","utube"],case_insensitive=True)
	async def yt(slef,ctx):
		if ctx.invoked_subcommand is None:
			pass
	@yt.command()
	async def search(self,ctx,*,query):
		query = query.split()
		search_word = "+".join(query)
		html = urllib.request.urlopen("https://www.youtube.com/results?search_query="+search_word)
		results = re.findall("watch\?v=(\S{11})",html.read().decode())
		try:
			await ctx.message.add_reaction("📺")
			await ctx.send("https://youtube.com/watch?v="+results[0])
		except:
			await ctx.message.add_reaction("❌")
			msg = discord.Embed(title="Error", description="Oops.. Not found the video..\nPlease search again by typing ```!fibu yt search <search_word>```")
			await ctx.send(embed=msg)


		
		
def setup(bot):
	bot.add_cog(Youtube(bot))
