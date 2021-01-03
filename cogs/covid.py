import discord
from datetime import datetime as time
from discord.ext import commands as c
import wikipedia as wiki
import covid19_data
import urllib.parse,urllib.request,re
import translators as trans
import requests,json
import asyncio, typing

class Command(c.Cog):
	def __init__(self,client):
		self.client = client

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
