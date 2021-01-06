import discord
from datetime import datetime as time
from discord.ext import commands as c
import wikiquote as q
import asyncio, typing, random

class Command(c.Cog):
	def __init__(self,client):
		self.client = client

#echo
	@c.command()
	async def echo(self,ctx, channel: typing.Optional[discord.TextChannel]=None,*,msg):
		if channel==None:
			await ctx.message.delete()
			await ctx.send(msg)
		else:
			await ctx.message.delete()
			await channel.send(msg)

#quotes
	@c.command()
	async def quote(self, ctx,*,arg=None):
		if arg==None:
			random_q = q.random_titles(max_titles=1)[0]
			quote_text= random.choice(q.quotes(random_q))
			await ctx.send(f">>> {quote_text}\n	- *{random_q}*")
		else:
			try:
				search = q.search(arg)[0]
				quote = random.choice(q.quotes(search))
				await ctx.send(f">>> {quote}\n	- *{search}*")
			except:
				pass
		
		
		
def setup(bot):
	bot.add_cog(Command(bot))
