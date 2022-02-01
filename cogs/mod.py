import discord
from datetime import datetime as time
from discord.ext import commands as c
import pyjokes
import random
import requests


class Mod(c.Cog):
    def __init__(self, client):
        self.client = client

    @c.command()
    @c.has_role("Admin In Command")
    @c.cooldown(1, 86400, c.BucketType.user)
    async def mod(self, ctx):
        try:
            mods = []
            for member in ctx.guild.members:
                for role in member.roles:
                    if role.name == "Moderator":
                        await ctx.send(f"NAME : {member.name}")
                        mods.append(f"{member.mention}")

            await ctx.send(f"{random.choice(mods)} youl'll manage the PH forum for today..")
            await ctx.send("Daily one new mod will be choosen..")
        except Exception as e:
            await ctx.send(f"{e}")


def setup(bot):
    bot.add_cog(Mod(bot))
