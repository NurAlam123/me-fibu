import discord
from datetime import datetime as time
from discord.ext import commands as c
import wikipedia as wiki
import covid19_data
import urllib.parse,urllib.request,re
import translators as trans
import asyncio

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

#covid19	
	@c.command()
	async def covid(self,ctx,*,country_name="total"):
			try:
				country = covid19_data.dataByName(country_name)
				await ctx.message.add_reaction("😷")
				msg = discord.Embed(title="Coronavirus", description="Protect yourself and others from *COVID-19*.\nStay safe by taking some simple precautions, such as physical distancing, wearing a mask, keeping rooms well ventilated, avoiding crowds, cleaning your hands, and coughing into a bent elbow or tissue.\nFor more details... [click here](https://is.gd/XQfmI2)",color=0xffdf08,timestamp=time.now())
				if country_name !="total":
					msg.add_field(name="Name",value=f"{country_name.capitalize()}")
				else:
					msg.add_field(name="Name",value="Global")
				msg.add_field(name="Cases",value=f"{country.cases:,}")
				msg.add_field(name="Deaths",value=f"{country.deaths:,}")
				msg.add_field(name="Recoverd",value=f"{country.recovered:,}")
			except:
				await ctx.message.add_reaction("❌")
				msg = discord.Embed(title="Error", description="**Oops!** Not Found!\nTry again by typing ```!fibu covid country_name```",color=0xffdf08)

			msg.set_thumbnail(url="https://is.gd/TTTW35")
			msg.set_author(name=f"{self.client.user.name}",url="https://www.programming-hero.com/",icon_url=f"{self.client.user.avatar_url}")
			msg.set_footer(text="Programming Hero ")
			await ctx.send(embed=msg)
#youtube
	@c.group(aliases=["youtube","utube"],case_insensitive=True)
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
			msg = discord.Embed(title="Error", description="Oops.. Not found the video..\nPlease search again by typing ```!fibu yt search search_word ```")
			await ctx.send(embed=msg)

#translate			
	@c.command(aliases=["translate"])
	async def ts(self,ctx,lang,*,text):
			lang = lang.split("|")
			if lang[0]=="":
				translation = trans.bing(text,to_language=lang[1])
			else:
				translation = trans.bing(text,from_language=lang[0],to_language=lang[1])
			msg = discord.Embed(title="Translator", color=0xffdf08)
			msg.add_field(name="Word",value=f"{text.capitalize()}")
			msg.add_field(name="Translation",value=f"{translation}")
			await ctx.send(embed=msg)
	@c.command()
	async def echo(self,ctx, channel: discord.TextChannel,*,msg):
		await channel.send(msg)
		
		
def setup(bot):
	bot.add_cog(Command(bot))