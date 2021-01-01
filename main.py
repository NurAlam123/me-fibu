import discord
import time,os
from discord.ext import commands
from discord.utils import get
import sqlite3
import asyncio

token = os.getenv("TOKEN")

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
	msg = discord.Embed(title="Pong 🏓", description=f"{round(bot.latency*1000)} _ms_!")
	await ctx.send(embed=msg)

#cogs
@bot.command()
async def on(ctx,file):
		try:
			for files in os.listdir("./cogs"):
				if files==file+".py":
					bot.load_extension(f"cogs.{files[:-3]}")
					await ctx.send(f"{file} loaded!")
		except:
			await ctx.send(f"{file} is already loaded!")
@bot.command()
async def off(ctx,file):
		bot.unload_extension(f"cogs.{file}")
		await ctx.send(f"{file} unloaded!")

for files in os.listdir("./cogs"):
		if files.endswith(".py"):
			bot.load_extension(f"cogs.{files[:-3]}")
		

bot.run(token)