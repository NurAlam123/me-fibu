import discord
from datetime import datetime as time
from discord.ext import commands

class Help(commands.Cog):
	def __init__(self,client):
		self.client = client

#help
	@commands.command()
	async def help(self,ctx,arg=None):
		if arg==None:
			await ctx.message.add_reaction('''✅''')
			help_msg = discord.Embed(title='''Help on all features''',
					description='''My prefix is ```py
					!fibu ```''',
					color=0xffdf08,
					timestamp=time.now())
			help_msg.add_field(name="All Commands",
					value='''```py
					!fibu help commands```''')
			#help_msg.add_field(name='''QNA''',
			#		value='''```py 
			#!fibu help qna```''')
			help_msg.add_field(name='''Info''',
					value='''```py 
					!fibu help info```''')
			help_msg.add_field(name='''Others''', 	
					value='''```py 
					!fibu help others```''')
			help_msg.set_author(name=f'''{self.client.user.name}''',icon_url=f'''{self.client.user.avatar_url}''')
			help_msg.set_footer(text='''Programming Hero ''')
			await ctx.send(embed = help_msg)
#commands
		elif arg.lower()=='''commands''':
			await ctx.message.add_reaction('✅')
			msg = discord.Embed(title='''Help on commands''',
						color=0xffdf08,
						timestamp=time.now())
			msg.add_field(name='''```py 
			!fibu math equation```''',
						value='''Get the result of your math equation. i.e: **!fibu math 2+2**''')
						
			#msg.add_field(name='''```py 
			#!fibu wiki search search_word```''',
#						value='''Search any details on wikipedia''')
			
			msg.add_field(name='''```py 
			!fibu yt search search_word```''',
						value='''To seaech a video in youtube''')
			#msg.add_field(name='''```py 
			#!fibu translate from_language|to_language text```''',
#						value='''Translate your text to another language. Example: **!fibu translate en|fr Hello**\If you don't know from which language you are translating then put blank the from_language value. Example: **!fibu translate |fr Hello**''')
			msg.add_field(name='''```py 
			!fibu covid country_name```''',
						value='''Get statistics of coronavirus of specific country''')
			msg.set_author(name=f'''{self.client.user.name}''',icon_url=f'''{self.client.user.avatar_url}''')
			msg.set_footer(text='''Programming Hero ''')
			await ctx.send(embed=msg)

#qna
#		elif arg.lower()=='''qna''':
#			await ctx.message.add_reaction('✅')
#			msg = discord.Embed(title='''Help on qna commands''',color=0xffdf08,timestamp=time.now())
#			msg.add_field(name='''```py !fibu ans your_question```''', value='''Get the answer of your question''')
#			msg.set_author(name=f'''{self.client.user.name}''',icon_url=f'''{client.user.avatar_url}''')
#			msg.set_footer(text='''Programming Hero ''')
#			await ctx.send(embed=msg)

#info
		elif arg.lower()=='''info''':
			await ctx.message.add_reaction('✅')
			msg=discord.Embed(title='''Help on information commands''',
						color=0xffdf08,
						timestamp=time.now())
			msg.add_field(name='''```py 
			!fibu show server info```''',
						value='''Get information about the server''')
			msg.add_field(name='''```py 
			!fibu count members```''', 
						value='''Get the number of members in the server''')
			msg.add_field(name='''```py 
			!fibu show your team```''',
						value='''Get the information about my developers''')
			msg.add_field(name='''```py 
			!fibu show your info```''',value='''Get information about me''')
			msg.add_field(name='''```py 
			!fibu show my avatar```''',
						value='''To get or see your avatar''')
			msg.add_field(name='''```py 
			!fibu show avatar member id or mention```''',
						value='''To get the avatar of mentioned user.''')
			msg.add_field(name='''```py 
			!fibu show my info```''',
						value='''Get your information.''')
			msg.add_field(name='''```py 
			!fibu show info mention or member id```''',
						value='''Get information about mentioned user.''')
			msg.set_footer(text='''Programming Hero ''')
			msg.set_author(name=f'''{self.client.user.name}''',icon_url=f'''{self.client.user.avatar_url}''')
			await ctx.send(embed=msg)

#others
		elif arg.lower()=='''others''':
			await ctx.message.add_reaction('✅')
			msg = discord.Embed(title='''Help on other commands''',
						color=0xffdf08,
						timestamp=time.now())
			msg.add_field(name='''```py 
			!fibu hello```''', 
						value='''Greet you in server''')
			msg.add_field(name='''```py
			!fibu dm```''', 	
						value='''Greet you in DM.''')
			msg.add_field(name='''```py 
			!fibu ok```''',
						value='''If you want to say ok to me.''')
			msg.add_field(name='''```py 
			!fibu thank you```''', 
						value='''If you want to thanked me.''')
			msg.set_footer(text='''Programming Hero ''')
			msg.set_author(name=f'''{self.client.user.name}''',icon_url=f'''{self.client.user.avatar_url}''')
			await ctx.send(embed=msg)


def setup(bot):
	bot.add_cog(Help(bot))