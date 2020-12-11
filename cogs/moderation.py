import discord,sqlite3
from datetime import datetime as time
from discord.ext import commands
from discord.utils import get
import asyncio
from discord.ext.commands import has_permissions

con_fibu = sqlite3.connect("./data/fibu.db")
c_fibu = con_fibu.cursor()

dev = [680360098836906004,728260210464129075,664550550527803405,693375549686415381,555452986885668886]

class Mod(commands.Cog):

#abuse word
	warns = 0
	def __init__(self,client):
		self.client = client

	@commands.Cog.listener("on_message")
	async def message(self,msg):
		fetch_users = c_fibu.execute("select * from warnings").fetchall()
		users = [i[0] for i in fetch_users]
		if msg.author.id == self.client.user.id:
			return 
		user = msg.author.id
		if msg.author.id not in users:
			c_fibu.execute("insert into warnings(id) values(?)",(msg.author.id,))
			con_fibu.commit()
			self.warns = 0
		elif msg.author.id in users:
			self.warns = c_fibu.execute("select * from warnings where id=?",(user,)).fetchone()[1]
		words = c_fibu.execute("select * from abuse_words").fetchall()
		words = [i[0] for i in words]
		for word in words:
			if word in msg.content.lower().split():
				await msg.delete()
				self.warns+=1
				await msg.author.send(f"Hey, {msg.author.mention}!\nYou have been warned for using bad words from {msg.guild}\nWarnings no: {self.warns}")
				c_fibu.execute("update warnings set warning=? where id=?",(self.warns,user,))
				con_fibu.commit()
			if self.warns>=5:
				c_fibu.execute("update warnings set warning=0 where id=?",(user,))
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

#warn

	channel = None
	warning = 1
	@commands.command()
	@has_permissions(administrator=True,manage_roles=True,manage_messages=True)
	async def warn(self,ctx,member:discord.Member,*,reason="No reason!"):
				guilds = c_fibu.execute("select * from guild_data").fetchall()
				guilds = [i[0] for i in guilds]
				print(guilds)
				
				if member.id==ctx.author.id:
					await ctx.send("You can't warn yourself!!")
				elif member.id == self.client.user.id:
					pass
				else:
			#fetch reason
					fetch_user = c_fibu.execute("select * from other_warning").fetchall()
					all_user = [i[0] for i in fetch_user]
					if member.id in all_user:
						self.warning = c_fibu.execute("select warning from other_warning where id =?",(member.id,)).fetchone()[0]+1
						fetch_reasons = c_fibu.execute("select reason from other_warning where id=?",(member.id,)).fetchone()[0]
						reasons = fetch_reasons +","+reason
						c_fibu.execute("update other_warning set reason=?,warning=? where id=?",(reasons,self.warning,member.id))
						con_fibu.commit()
					elif member.id not in all_user:
						self.warning+=1
						c_fibu.execute("insert into other_warning values(?,?,?)",(member.id,self.warning,reason,))
						con_fibu.commit()
					await ctx.message.delete()
					
					await ctx.send(f"{member.mention} has been warned for {reason}")
					await member.send(f"You have been warned from {ctx.guild.name} for {reason}!\nWarning no: {self.warning}")
			
					if ctx.guild.id in guilds:
						fetch_channel = c_fibu.execute("select warn_channel from guild_data where guild_id = ?",(ctx.guild.id,)).fetchone()[0]
						print(fetch_channel)
						if fetch_channel is None:
							pass
						else:
							self.channel = fetch_channel
					else:
							if self.channel is None:
								channel = ctx.guild.system_channel
								if channel is not None:
									self.channel = channel.id
								else:
									self.channel = get(ctx.guild.channels,name="general").id
							else:
								self.channel = ctx.message.channel.id

					warn_em = discord.Embed(title="Warning", description=f"{member.mention} warned!",color=0xffdf08, timestamp=time.now())
					warn_em.add_field(name="Warned By",value=f"**__Name:__** {ctx.author.name}\n**__Username:__** {ctx.author}\n**__Id:__** {ctx.author.id}")
					warn_em.add_field(name="User",value=f"**__Name:__** {member.name}\n**__Username:__** {member}\n**__Id:__** {member.id}\n**__Joined_at:__** {member.joined_at.strftime('%A, %d-%m-%y %I:%M:%S %p')}")
					warn_em.add_field(name="Reason",value=f"{reason}")
					await get(ctx.guild.channels,id=self.channel).send(embed=warn_em)
					self.warning=0

#error handling
	@warn.error
	async def warn_error(self,ctx,error):
		if isinstance(error,commands.MissingPermissions):
			await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
			
			
#set channel
	@commands.command()
	@has_permissions(administrator=True,manage_roles=True,manage_messages=True)
	async def setWarningsChannel(self,ctx,channel:discord.TextChannel=None):
			guilds = c_fibu.execute("select * from guild_data").fetchall()
			guilds = [i[0] for i in guilds]
			if channel is not None:
				if ctx.guild.id in guilds:
					c_fibu.execute("update guild_data set warn_channel=? where guild_id=?",(channel.id,ctx.guild.id))
					con_fibu.commit()
				else:
					c_fibu.execute("insert into guild_data(guild_id,warn_channel) values(?,?)",(ctx.guild.id,channel.id,))
					con_fibu.commit()
				await ctx.send("Warnings update channel has been set!")
			else:
				await ctx.send("You haven't set any channel!!")
	@setWarningsChannel.error
	async def warn_channel_error(self,ctx,error):
				if isinstance(error,commands.MissingPermission):
					await ctx.send(f"Hey {ctx.author.mention}, you haven't any permission to do that!")
				
		
#show warnings			
	@commands.command()
	@has_permissions(administrator=True,manage_roles=True,manage_messages=True)
	async def warnings(self,ctx, member: discord.Member=None):
		if member is None:
			fetch_all = c_fibu.execute("select * from other_warning").fetchall()
			all = []
			for i in range(len(fetch_all)):
				format_sys = f"{i+1} - 	{get(ctx.guild.members,id=fetch_all[i][0])} 	- 	{fetch_all[i][1]}"
				all.append(format_sys)

			show_em = discord.Embed(title="No - 	Name	 - 	Warnings", description="\n".join(all),color=0xffdf08)
			await ctx.send(embed=show_em)
		else:
				fetch_one = c_fibu.execute("select * from other_warning where id=?",(member.id,)).fetchone()
				show_em = discord.Embed(title="Warnings", description=f"Showing all warnings of {member.mention}",color=0xffdf08, timestamp=time.now())
				show_em.add_field(name="Name",value=f"{member.name}")
				show_em.add_field(name="Username",value=f"{member}")
				show_em.add_field(name="ID",value=f"{member.id}")
				show_em.add_field(name="Warnings no",value=f"{fetch_one[1]}")
				reasons = fetch_one[2].split(",")
				reasons = list(set([i for i in reasons]))
				show_em.add_field(name="Reasons",value=",".join(reasons))
				show_em.set_author(name=f"{self.client.user.name}",icon_url=f"{self.client.user.avatar_url}")
				show_em.set_footer(text="Programming Hero ")
				await ctx.send(embed=show_em)
				
	@warnings.error
	async def warn_error(self,ctx,error):
		if isinstance(error,commands.MissingPermissions):
			await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
				

def setup(bot):
	bot.add_cog(Mod(bot))