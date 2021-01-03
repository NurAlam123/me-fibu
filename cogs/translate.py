 
import discord
from datetime import datetime as time
from discord.ext import commands as c
import wikipedia as wiki
import covid19_data
import urllib.parse,urllib.request,re
import translators as trans
import requests,json
import asyncio, typing

class Translate(c.Cog):
	def __init__(self,client):
		self.client = client

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

#echo

		
		
def setup(bot):
	bot.add_cog(Translate(bot))
