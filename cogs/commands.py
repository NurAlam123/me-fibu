import discord
from datetime import datetime as time
from discord.ext import commands as c
import pip
try:
	import wikiquote as q
except:
	pip.main(["install","wikiquote"])
import asyncio, typing, random

class Command(c.Cog):
	def __init__(self,client):
		self.client = client
#math	
	@c.command()
	async def math(self,ctx,eq=""):
		if eq=="":
			msg = discord.Embed(title="Calculator",
						description="Try again by typing ```!fibu math equation```",
						color=0xffdf08,timestamp=time.now())
			msg.set_author(name=f"{selt.client.user.name}",icon_url=f"{self.client.user.avatar_url}")
			msg.set_footer(text="Programming Hero ")
			await message.channel.send(embed=msg)
		else:
			if "^" in eq:
				eq = eq.replace("^","**")
			if "×" in eq:
				eq = eq.replace("×","*")
			if "÷" in eq:
				eq = eq.replace("÷","/")
			if 'x' in eq.lower():
				eq = eq.replace('x','*')
			result = eval(eq)
			msg = discord.Embed(title="Calculator",
													color=0xffdf08,
													timestamp=time.now())
			msg.add_field(name="Math",value=eq)
			msg.add_field(name="Result",value=result)
			msg.set_author(name=f"{self.client.user.name}",icon_url=f"{self.client.user.avatar_url}")
			msg.set_footer(text="Programming Hero ")
			await ctx.send(embed=msg)

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
