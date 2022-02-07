import discord
from discord.ext import commands
import os
import pymongo

import re
import asyncio

# class Chat(commands.Cog):
#     def __init__(self, client):
#         self.bot = client

#     @commands.command(name="chat_account")
#     @commands.has_permissions(administrator=True)
#     def chat_acc(self, member: discord.Member = None):
#         pass


#     @commands.command(name="chat")
#     def chat(self, *, message):
#         pass


# def setup(bot):
#     bot.add_cog(Chat(bot))

if __name__ == "__main__":
    # mclient = pymongo.MongoClient("mongodb+srv://fibu-ph:FibuProgrammingHero@fibu.vtsjw.mongodb.net/fibu?retryWrites=true&w=majority")
    # db
    con_fibu = pymongo.MongoClient(os.getenv("DB"))
    db = con_fibu["fibu"]  # database
    tb = db["other_data"]  # table
    print(dict(tb.find()))
