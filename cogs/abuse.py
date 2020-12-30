import discord,sqlite3
from datetime import datetime as time
from discord.ext import commands
from discord.utils import get
import asyncio

con_fibu = sqlite3.connect("data/fibu.db")
c_fibu = con_fibu.cursor()

dev = [680360098836906004,728260210464129075,664550550527803405,693375549686415381,555452986885668886]

class Abuse(commands.Cog):
  
  def __init__(self,client):
    self.client=client
  
  warns = 0
  
  @commands.Cog.listener("on_message")
  async def message(self,msg):
    user = msg.author.id
    server = msg.guild.id
    fetch_warns = c_fibu.execute("select warnings from warnings where guild_id=? and user_id=?",(server,user,)).fetchone()

    if fetch_warns is None:
      c_fibu.execute("insert into warnings(guild_id,user_id) values(?,?)",(server,user,))
      con_fibu.commit()
      self.warns=0
    
    else:
      self.warns = int(fetch_warns[0])
    
    words = c_fibu.execute("select * from abuse_words").fetchall()
    words = [i[0] for i in words]
    for word in words:
      if word.lower() in msg.content.lower().split():
        await msg.delete()
        self.warns+=1
        await msg.author.send(f"Hey, {msg.author.mention}!\nYou have been warned for using bad words from {msg.guild}\nWarnings no: {self.warns}")
        
        c_fibu.execute("update warnings set warnings=? where guild_id=? and user_id=?",(self.warns,server,user,))
        con_fibu.commit()
      
      if self.warns>=5:
        c_fibu.execute("update warnings set warnings=0 where guild_id=? and user_id=?",(server,user,))
        con_fibu.commit()
        try:
          await msg.author.send(f"{msg.author.mention}!! You have banned from {msg.guild} for using bad words!")
        except:
          pass
        await asyncio.sleep(2)
        await msg.guild.ban(msg.author,reason="For using bad words")

#add abuse word				
  @commands.command()
  async def addWord(self,ctx,*,words):
    word = words.lower().split(",")
    if ctx.author.id in dev:
      for i in word:
        c_fibu.execute("insert into abuse_words values(?)",(i,))
        con_fibu.commit()
        await ctx.send("Words added!!")
    else:
      await ctx.send("Sorry... You haven't any permission to fo this!")


def setup(bot):
  bot.add_cog(Abuse(bot))