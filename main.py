import discord
from discord.ext import commands
from discord.utils import get
import discord_components as d_c

import time
from datetime import datetime
import os
import asyncio
import logging

# from dotenv import load_dotenv

# load_dotenv()


#### logging [recommended]####
logging.basicConfig(level=logging.INFO)
#############################

token = os.getenv("TOKEN")

prefix_file = open("prefix.txt", "r")
prefixes = [i.replace("\n", " ") for i in prefix_file.readlines()]

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix=prefixes,
                   intents=intents, case_insensitive=True)
bot.remove_command("help")

d_c.DiscordComponents(bot)

# Team
bot.TEAM = [
    838836138537648149,  # Nur
    664550550527803405,  # Tamim
    728260210464129075,  # Rishikesh
    693375549686415381,  # Soren
    555452986885668886  # Karim
]  # our team's discord ids

bot.version = 'v0.4.1'

# on ready


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="!fibu help | Fibu | Programming Hero"))
    print(f"Logged in as {bot.user}")


# ping
@bot.command()
async def ping(ctx):
    msg = discord.Embed(title="Pong :ping_pong:",
                        description=f"{round(bot.latency*1000)} _ms_!", color=0xffdf08)
    await ctx.send(embed=msg)

# fibu


@bot.listen()
async def on_message(message):
    if message.content.lower().strip() == "!fibu" or message.content.lower().strip() == f"<@{bot.user.id}>":
        await message.channel.send(f"Type `!fibu help` to get help message!!")

# cogs load and unload


@bot.command()
async def on(ctx, file):
    if ctx.author.id in bot.TEAM:
        try:
            for files in os.listdir("./cogs"):
                if files == file.lower()+".py":
                    bot.load_extension(f"cogs.{files[:-3]}")
                    await ctx.send(f"{file} loaded!")
        except:
            await ctx.send(f"{file} is already loaded!")
    else:
        await ctx.send(f"You don't have the permission to do that!!")


@bot.command()
async def off(ctx, file):
    if ctx.author.id in bot.TEAM:
        try:
            bot.unload_extension(f"cogs.{file.lower()}")
            await ctx.send(f"{file} unloaded!")
        except:
            await ctx.send(f"{file} is already unloaded!")
    else:
        await ctx.send("You don't have the permission to do that!!")


for files in os.listdir("./cogs"):
    if files.endswith(".py") and files != "nqn.py":
        bot.load_extension(f"cogs.{files[:-3]}")

# bot.load_extension(f"cogs.commands")

bot.run(token)
