import discord
import time,os
from discord.ext import commands
from discord.utils import get
import sqlite3
import asyncio
import pymongo

token = os.getenv("TOKEN")

dev = [680360098836906004,728260210464129075,664550550527803405,693375549686415381,555452986885668886]

prefix_file = open("prefix.txt","r")
prefixes = [i.replace("\n"," ") for i in prefix_file.readlines()]

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=prefixes,
										intents=intents,
										case_insensitive=True)
bot.remove_command("help")

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game(name="!fibu help | Fibu | Programming Hero"))
	print(f"Logged in as {bot.user}")
#ping
@bot.command()
async def ping(ctx):
	msg = discord.Embed(title="Pong 🏓", description=f"{round(bot.latency*1000)} _ms_!",color=0xffdf08)
	await ctx.send(embed=msg)

#cogs

@bot.command()
async def on(ctx,file):
	if ctx.author.id in dev:
		try:
			for files in os.listdir("./cogs"):
				if files==file.lower()+".py":
					bot.load_extension(f"cogs.{files[:-3]}")
					await ctx.send(f"{file} loaded!")
		except:
			await ctx.send(f"{file} is already loaded!")
	else:
		await ctx.send(f"You don't have the permission to do that!!")
@bot.command()
async def off(ctx,file):
		if ctx.author.id in dev:
			try:
				bot.unload_extension(f"cogs.{file.lower()}")
				await ctx.send(f"{file} unloaded!")
			except:
				await ctx.send(f"{file} is already unloaded!")
		else:
			await ctx.send("You don't have the permission to do that!!")
			

for files in os.listdir("./cogs"):
		if files.endswith(".py"):
			bot.load_extension(f"cogs.{files[:-3]}")


client = pymongo.MongoClient("mongodb+srv://fibu-ph:FibuProgrammingHero@fibu.vtsjw.mongodb.net/fibu?retryWrites=true&w=majority")			
db = client["fibu"]
	
##testing mongodb
@bot.command()
async def show_db(ctx,*,name):
	col = db["guild_data"]
	data = {"name":f"{name}"}
	show_data = col.find_one(data)
#	print(show_data)
	try:
		await ctx.send(f"Name: {show_data['name']}\nDev: {show_data['dev']}")
	except:
		pass

@bot.command()
async def add_db(ctx,*,name):
		col = db["guild_data"]
		data = {"name":f"{name}"}
		add = col.insert_one(data)
		await ctx.send(f"{name} added to database")
@bot.command()
async def del_db(ctx,*,name):
		col = db.guild_data
		data = {"name":f"{name}"}
		del_data = col.delete_one(data)
		await ctx.send(f"{name} deleted!")
		
		

bot.run(token)
