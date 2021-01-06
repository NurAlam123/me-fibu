import discord
from datetime import datetime as time
from discord.ext import commands as c

class Math(c.Cog):
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
			try:
				result = eval(eq)
				await ctx.send(f"**__Your Input:__**\n```{eq}```\n**__Result:__**\n```{result}```")
			except:
				await ctx.send("Invalid Input")
					
		
def setup(bot):
	bot.add_cog(Math(bot))
