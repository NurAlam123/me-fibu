import discord
from datetime import datetime as time
from discord.ext import commands

class Info(commands.Cog):
	def __init__(self,client):
		self.client = client

	@commands.group(case_insensitive=True)
	async def show(self,ctx):
		if ctx.invoked_subcommand is None:
			pass
	@show.command()
	async def my(self,ctx,arg):
#my av
			if arg.lower()=="av" or arg.lower()=="avatar":
					avatar = discord.Embed(title="Avatar", 
							description=f"{ctx.author.mention}",
							color=0xffdf08)
					avatar.set_image(url=f"{ctx.author.avatar_url}")
					await ctx.send(embed=avatar)
#my info
			elif arg.lower()=="info":
				roles = [i.mention for i in ctx.message.author.roles if i.name!="@everyone"]
				if roles==[]:
					roles = ["No roles!"]
				msg = discord.Embed(title="User information", 
							description=f"{ctx.author.mention}",
							color=0xffdf08,
							timestamp=time.now())
				msg.add_field(name="Name",value=f"{ctx.author.name}")
				msg.set_thumbnail(url=ctx.author.avatar_url)
				msg.add_field(name="Created at",value=f"{(ctx.author.created_at).strftime('%a, %d-%b-%Y %I:%M %p')}")
				msg.add_field(name="Joined at",value=f"{(ctx.author.joined_at).strftime('%a, %d-%b-%Y %I:%M %p')}")
				msg.add_field(name=f"Roles [{len(roles)-1}]",value=f"{', '.join(roles)}")
				msg.set_author(name=f"{self.client.user.name}",icon_url=f"{self.client.user.avatar_url}")
				msg.set_footer(text="Programming Hero ")
				await ctx.send(embed=msg)
			
#server info
	@show.command()
	async def server(self,ctx,arg):
			if arg.lower()=="info":
				roles_name = [i.name for i in ctx.guild.roles]
				if roles_name==[]:
					roles_name =["No roles!"]
				bots=(ctx.guild.member_count)-len([m for m in ctx.guild.members if not m.bot])
				guild = ctx.guild
				text = len(guild.text_channels)
				voice = len(guild.voice_channels)
				total = text + voice
				owner = self.client.get_user(ctx.guild.owner_id)
				
				msg = discord.Embed(title="Information about",
							color=0xffdf08,
							timestamp=time.now(), 
							description=f"```{guild}```")
				msg.set_thumbnail(url=f"{ctx.guild.icon_url}")
				msg.add_field(name="Region",value=f"{guild.region}")
				msg.add_field(name="Owner",value=owner)
				msg.add_field(name="Members",value=f"{guild.member_count}")
				msg.add_field(name="Bots",value=bots)
				msg.add_field(name=f"Roles [{len(ctx.guild.roles)}]",value=f"{', '.join(roles_name)}")
				msg.add_field(name="Channels",value=total)
				msg.add_field(name="Text channels",value=text)
				msg.add_field(name="Voice channels",value=voice)
				msg.set_author(name=f"{self.client.user.name}",icon_url=f"{self.client.user.avatar_url}")
				msg.set_footer(text=f"Programming Hero ")
				await ctx.send(embed=msg)

#our team **need more improvement**
	@show.command()
	async def your(self,ctx,arg):
			if arg.lower()=="team":
				await ctx.message.add_reaction("⚒️")
				msg = discord.Embed(title="Developer information",
							description="Here are my developers:",
							color=0xffdf08,
							timestamp=time.now())
				msg.add_field(name="Nur Alam [NurAlam#6519]",value="Worked on my designing and development.")
				msg.add_field(name="Tamim Vaiya [Tamim Vaiya#2029]",value="Gave suggestions to my developers.")
				msg.add_field(name="Rishikesh [Rishikesh#2034]",value="Worked on my development.")
				msg.add_field(name="Soren_Blank [Soren_Blank#4853]",value="Worked on my development.")
				msg.set_author(name=f"{self.client.user.name}",url="https://www.programming-hero.com/",icon_url=f"{self.client.user.avatar_url}")
				msg.set_footer(text=f"Programming Hero ")
				await ctx.send(embed=msg)
#fibu info
			elif arg.lower()=="info":
				msg = discord.Embed(title="My information", 
							description="Hey there! I am Fibu. Your friend and a friendly bot. I am from Programming Hero",
							color=0xffdf08,
							timestamp=time.now())
				msg.set_thumbnail(url=f"{self.client.user.avatar_url}")
				msg.add_field(name="Version",value="0.0.1")
				msg.add_field(name="Prefix",value="```!fibu```")
				msg.add_field(name="Released on",value="Jan 1, 2020 4:00 pm")
				msg.add_field(name="Website",value="[Programming Hero](https://www.programming-hero.com/)")
				msg.add_field(name="Application",value="[Android App](https://is.gd/z11RUg)\n[Iphone Version](https://is.gd/eVH92i)")
				msg.add_field(name="Social Media",value="[Facebook](https://m.facebook.com/programmingHero/)\n[Instagram](https://is.gd/6m3hgd)\n[Twitter](https://twitter.com/ProgrammingHero?s=09)\n[Youtube](https://is.gd/EulQLJ)\n[Pinterest](https://www.pinterest.com/programminghero1/)")
				msg.add_field(name="Team",value="**1. Nur Alam,\n2. Tamim Vaiya,\n3. Rishikesh,\n4.Soren_blank**\nFor more info type ```!fibu show your team```")
				msg.set_author(name=f"{self.client.user.name}",url="https://www.programming-hero.com/",icon_url=f"{self.client.user.avatar_url}")
				msg.set_footer(text=f"Programming Hero ")
				await ctx.send(embed=msg)
#user info
	@show.command()
	async def info(self,ctx,member: discord.Member):
		print(member)
		roles = [i.mention for i in member.roles if i.name!="@everyone"]
		if roles==[]:
			roles =["No roles!"]
		msg = discord.Embed(title="User information", description=f"{member.mention}",color=0xffdf08,timestamp=time.now())
		msg.add_field(name="Name",value=f"{member.name}")
		msg.set_thumbnail(url=member.avatar_url)
		msg.add_field(name="Created at",value=f"{(member.created_at).strftime('%a, %d-%b-%Y %I:%M %p')}")
		msg.add_field(name="Joined at",value=f"{(member.joined_at).strftime('%a, %d-%b-%Y %I:%M %p')}")
		msg.add_field(name=f"Roles [{len(member.roles)-1}]",value=f"{', '.join(roles)}")
		msg.set_author(name=f"{self.client.user.name}",url="https://www.programming-hero.com/",icon_url=f"{self.client.user.avatar_url}")
		msg.set_footer(text="Programming Hero ")
		await ctx.send(embed=msg)
#user av	
	@show.command(aliases=["av","avatar"])
	async def _av(self,ctx,member: discord.Member):
		avatar = discord.Embed(title="Avatar",
						color=0xffdf08,
						timestamp=time.now())
		avatar.set_author(name=f"{self.client.user.name}",
						icon_url=self.client.user.avatar_url)
		avatar.set_footer(text="Programming Hero ")
		avatar.set_image(url=member.avatar_url)
		await ctx.send(embed=avatar)

#member count	
	@commands.command()
	async def count(self,ctx,arg=None):
		if arg==None:
			pass
		elif arg.lower()=="members":
			bots=(ctx.guild.member_count)-len([m for m in ctx.guild.members if not m.bot])
			msg=discord.Embed(title="Members",
						color=0xffdf08,
						timestamp=time.now())
			msg.add_field(name="Server Name",value=f"{ctx.guild.name}")
			msg.add_field(name="Members",value=f"{ctx.guild.member_count}")
			msg.add_field(name="Humans",value=f"{(ctx.guild.member_count)-bots}")
			msg.add_field(name="Bots",value=f"{bots}")
			msg.set_author(name=f"{self.client.user.name}",icon_url=f"{self.client.user.avatar_url}")
			msg.set_footer(text=f"Programming Hero ")
			await ctx.send(embed=msg)
		

def setup(bot):
	bot.add_cog(Info(bot))
