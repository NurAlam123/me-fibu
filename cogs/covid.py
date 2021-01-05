import discord
from datetime import datetime as time
from discord.ext import commands as c
import covid_daily

class Corona(c.Cog):
	def __init__(self,client):
		self.client = client

#covid19	
	@c.command()
	async def covid(self,ctx,*,country_name=None):
			covid = covid_daily.overview(as_json=True)
			is_done = False
			if country_name != None:
				for i in covid:
					if i["Country,Other"].lower()==country_name.lower():
						await ctx.message.add_reaction("😷")
						msg = discord.Embed(title="Coronavirus", description="Protect yourself and others from *COVID-19*.\nStay safe by taking some simple precautions, such as physical distancing, wearing a mask, keeping rooms well ventilated, avoiding crowds, cleaning your hands, and coughing into a bent elbow or tissue.\nFor more details... [click here](https://is.gd/XQfmI2)",color=0xffdf08,timestamp=time.now())
						msg.add_field(name="Name",value=f"{i['Country,Other']}")
						msg.add_field(name="New Cases",value=f"{i['NewCases']:,}")
						msg.add_field(name="Total Cases",value=f"{i['TotalCases']:,}")
						msg.add_field(name="New Deaths",value=f"{i['NewDeaths']:,}")
						msg.add_field(name="Total Deaths",value=f"{i['TotalDeaths']:,}")
						msg.add_field(name="New Recovered",value=f"{i['NewRecovered']:,}")
						msg.add_field(name="Total Recovered",value=f"{i['TotalRecovered']:,}")
						await ctx.send(embed=msg)
						is_done = True
						break
			else:
				await ctx.message.add_reaction("😷")
				world = covid[0]
				msg = discord.Embed(title="Coronavirus", description="Protect yourself and others from *COVID-19*.\nStay safe by taking some simple precautions, such as physical distancing, wearing a mask, keeping rooms well ventilated, avoiding crowds, cleaning your hands, and coughing into a bent elbow or tissue.\nFor more details... [click here](https://is.gd/XQfmI2)",color=0xffdf08,timestamp=time.now())
				msg.add_field(name="Name",value=f"World")
				msg.add_field(name="New Cases",value=f"{world['NewCases']:,}")
				msg.add_field(name="Total Cases",value=f"{world['TotalCases']:,}")
				msg.add_field(name="New Deaths",value=f"{world['NewDeaths']:,}")
				msg.add_field(name="Total Deaths",value=f"{world['TotalDeaths']:,}")
				msg.add_field(name="New Recovered",value=f"{world['NewRecovered']:,}")
				msg.add_field(name="Total Recovered",value=f"{world['TotalRecovered']:,}")
				await ctx.send(embed=msg)
				is_done=True
			if not is_done:
				await ctx.message.add_reaction("❌")
				msg = discord.Embed(title="Error", description="**Oops!** Not Found!\nTry again by typing ```!fibu covid country_name```")
				msg.set_thumbnail(url="https://is.gd/TTTW35")
				msg.set_author(name=f"{self.client.user.name}",url="https://www.programming-hero.com/",icon_url=f"{self.client.user.avatar_url}")
				msg.set_footer(text="Programming Hero ")
				await ctx.send(embed=msg)

		
def setup(bot):
	bot.add_cog(Corona(bot))
