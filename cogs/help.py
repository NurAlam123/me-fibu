import discord
from datetime import datetime as time
from discord.ext import commands

#commands =======================
def com_help(client,ctx):
			msg = discord.Embed(title='Help on commands',
						color=0xffdf08,
						timestamp=time.now())
			msg.add_field(name='```!fibu math equation```',
						value='Get the result of your math equation. i.e: **!fibu math 2+2**')
			msg.add_field(name='```!fibu quote```', value="Get a random quote")
			msg.add_field(name="```!fibu echo [channel] (message)```",value="To echo a message by Fibu.\n[channel] is optional but (message) is required")
			msg.add_field(name='```!fibu yt search search_word```',
						value='To seaech a video in youtube')
			msg.add_field(name='```!fibu covid country_name```',
						value='Get statistics of coronavirus of specific country')
			'''msg.add_field(name='```!fibu wiki search search_word```',
						value='Search any details on wikipedia')
			msg.add_field(name='```!fibu translate from_language|to_language text```',
						value='Translate your text to another language. Example: **!fibu translate en|fr Hello**\If you don't know from which language you are translating then put blank the from_language value. Example: **!fibu translate |fr Hello**')'''
			msg.set_author(name=f'{client.user.name}',icon_url=f'{client.user.avatar_url}')
			msg.set_footer(text='Programming Hero ')
			return ctx.send(embed=msg)

#info ============================
def info_help(client,ctx):
			msg=discord.Embed(title='Help on information commands',
						color=0xffdf08,
						timestamp=time.now())
			msg.add_field(name='```!fibu show server info```',
						value='Get information about the server')
			msg.add_field(name='```!fibu count members```', 
						value='Get the number of members in the server')
			msg.add_field(name='```!fibu show your team```',
						value='Get the information about my developers')
			msg.add_field(name='```!fibu show your info```',value='Get information about me')
			msg.add_field(name='```!fibu show my avatar```',
						value='To get or see your avatar')
			msg.add_field(name='```!fibu show avatar member id or mention```',
						value='To get the avatar of mentioned user.')
			msg.add_field(name='```!fibu show my info```',
						value='Get your information.')
			msg.add_field(name='```!fibu show info mention or member id```',
						value='Get information about mentioned user.')
			msg.set_footer(text='Programming Hero ')
			msg.set_author(name=f'{client.user.name}',icon_url=f'{client.user.avatar_url}')
			return ctx.send(embed=msg)

#others =======================
def others_help(client,ctx):
			msg = discord.Embed(title='Help on other commands',
						color=0xffdf08,
						timestamp=time.now())
			msg.add_field(name='```!fibu hello```', 
						value='Greet you in server')
			msg.add_field(name='```!fibu dm```', 	
						value='Greet you in DM.')
			msg.add_field(name='```!fibu ok```',
						value='If you want to say ok to me.')
			msg.add_field(name='```!fibu thank you```', 
						value='If you want to thanked me.')
			msg.set_footer(text='Programming Hero ')
			msg.set_author(name=f'{client.user.name}',icon_url=f'{client.user.avatar_url}')
			return ctx.send(embed=msg)

#qna ==========================
def qna_help(client,ctx):
			msg = discord.Embed(title='Help on qna commands',color=0xffdf08,timestamp=time.now())
			msg.add_field(name='``` !fibu ans your_question```', value='Get the answer of your question')
			msg.set_author(name=f'{client.user.name}',icon_url=f'{client.user.avatar_url}')
			msg.set_footer(text='Programming Hero ')
			return ctx.send(embed=msg)
	

	
class Help(commands.Cog):
	def __init__(self,client):
		self.client = client

#help
	@commands.group(case_insensitive=True)
	async def help(self,ctx):
		if ctx.invoked_subcommand is None:
			await ctx.message.add_reaction('✅')
			help_msg = discord.Embed(title='Help on all features',
					description='My prefix is ```!fibu ```',
					color=0xffdf08,
					timestamp=time.now())
			help_msg.add_field(name="All Commands",
					value='```!fibu help commands```')
			#help_msg.add_field(name='QNA',
			#		value='``` 
			#!fibu help qna```')
			help_msg.add_field(name='Info',
					value='```!fibu help info```')
			help_msg.add_field(name='Others', 	
					value='```!fibu help others```')
			help_msg.set_author(name=f'{self.client.user.name}',icon_url=f'{self.client.user.avatar_url}')
			help_msg.set_footer(text='Programming Hero ')
			await ctx.send(embed = help_msg)

#commands_help
	@help.command()
	async def commands(self,ctx):
		await ctx.message.add_reaction("✅")
		await com_help(self.client,ctx)

#qna_help
	@help.command()
	async def qna(self,ctx):
		await ctx.message.add_reaction('✅')
		await qna_help(self.client,ctx)

#info_help
	@help.command()
	async def info(self,ctx):
		await ctx.message.add_reaction('✅')
		await info_help(self.client,ctx)

#others_help
	@help.command()
	async def others(self,ctx):
		await ctx.message.add_reaction('✅')
		await others_help(self.client,ctx)


def setup(bot):
	bot.add_cog(Help(bot))
