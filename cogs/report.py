import discord
from discord.ext import commands
from discord.utils import get
from datetime import datetime as time

import asyncio
import pymongo

class Bug(commands.Cog):
    def __init__(self,client):
        self.bot = client
    
    @commands.command()
    async def bug(self, ctx):
        #### connect with database ####
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"] #database
        tb = db['guild_data']
        other_tb = db["other_data"] #table
        other_data = tb.find_one({'name': 'ignore_dm'})
        guild_data = tb.find_one({'guild_id': ctx.guild.id})
        if guild_data:
            questions = guild_data.get('report_questions')
            if questions:
                #### check function ####
                def message_check(message):
                    return message.author.id == ctx.author.id and isinstance(message.channel, discord.channel.DMChannel)
                if other_data:
                    ids = other_data.get('user_ids')
                    if ids:
                        ids.append(ctx.author.id)
                    else:
                        ids = [ctx.author.id]
                    other_tb.update_one({'name': 'ignore_dm'}, {'$set': {'user_ids': ids}})
                else:
                    other_tb.insert_one({'name': 'ignore_dm', 'user_ids': [ctx.author.id]})
                
                await ctx.message.add_reaction('\N{Lady Beetle}')
                await ctx.author.send("Thank you {ctx.author.mention} for informing a bug.\nPlease provide some extra information to make it easier for the developer to fix.\nSend 'Ok' to continue.")
                try:
                    ok = await self.bot.wait_for("message", check= message_check, timeout=60)
                except asyncio.TimeoutError:
                    await ctx.author.send('Time out!!\nYou didn\'t respond in time')
                    ids= other_data.get('user_ids')
                    if ctx.author.id in ids:
                        ids.remove(ctx.author.id)
                    other_tb.update_one({'name': 'ignore_dm'}, {'$set': {'user_ids': ids}})
                else:
                    if ok.content.lower() == 'ok':
                        await asyncio.sleep(2)
                        answers = {}
                        for no, question in enumerate(questions, 1):
                            ques_em = discord.Embed(title= f'Question-{no}', description= f'{question}', color= 0xFDB706)
    		                await ctx.author.send(embed= ques_em)
    		                try:
    		                    ans = await self.bot.wait_for('message', check= message_check, timeout= 180)
    		                except asyncio.TimeoutError:
    		                    await ctx.send('Time out!!\nYou didn\'t respond in time')
    		                    break
                            else:
                                if ans.attachments:
                                    for attachment in ans.attachments:
                                        ans.content += f'\n{attachment.url}'
                                user_ans = answers.get(ctx.author.id)
                                if user_ans:
                                    user_answers = answers[ctx.author.id]
                                    user_answers.append(ans.content)
                                else:
                                    user_ans[ctx.author.id] = [ans.content]
                        await ctx.author.send('Do you want to submit this bug?\nSend \'Yes\' or \'Done\' to **continue** or \'No\' to **cancel**!!')
                        done = await self.bot.wait_for('reaction_add', check= message_check, timeout= 60)
                        if done.content.lower() in ['done', 'yes']:
                            report_channel = guild_data.get('bug_channel')
                            if report_channel:
                                channel = await bot.fetch_channel(int(report_channel))
                            else:
                                channel = ctx.channel
                            report_em = discord.Embed(title= f'Bug Reported', description= 'A bug reported by **{ctx.author}**\n**User ID:** {ctx.author.id}', timestamp= time.now(), color= 0xFDB706)
                            for question in enumerate(questions, 1):
                                the_ans = user_answers.get(ctx.author.id)[no-1]
                                report_em.add_field(name= f'Question-{no}', value= f'**Answer:** {the_answer}')
                            await channel.send(embed= report_em)
                            await done.add_reaction('\N{green heavy check mark}')
                            await ctx.author.send('Your report successfully submitted!!')
                        else:
                            await ctx.author.send('Ok.. No problem.')
                                    
                            
		                
		                    
	
	
	'''questions = ["Where did you find the bug? Forums, Settings, Profiles, or in the content?","If the bug is in the content, please write the Galaxy name > Module name > Lesson name (if applicable) > and the Page Name (For eg: Fundamentals > Functions > function usage > 2/9)","What we need to do to see the bug? (how to reproduce the bug/issue?)","What is the expected behaviour? What should we change?","Please take a screenshot and post it in the #🕸bugs-or-issues channel... Appreciated your support!"]
	reports = []
	channel = None
	submit = "no"
	@commands.command()
	async def apply(self,ctx):
		await ctx.message.add_reaction("🐞")
		await ctx.author.send("Thank you for informing this bug. Please provide some extra information to make it easier for the developer to fix. Send 'Ok' to continue.")
		try:
			ok = await self.bot.wait_for("message",check=lambda msg: msg.author.id==ctx.author.id,timeout=60)
			await asyncio.sleep(2)
			if ok.content.lower()=="ok":
				for i in range(len(self.questions)):
					ques = discord.Embed(title="Question", description=f"{self.questions[i]}",color=0xffdf08, timestamp=time.now())
					ques.set_author(name=self.bot.user.name,icon_url=self.bot.user.avatar_url)
					ques.set_footer(text="Programming Hero")
					await ctx.author.send(embed=ques)
					ans = await self.bot.wait_for("message",check=lambda msg: msg.author.id==ctx.author.id)
					ques_with_ans = f"**Question:** {self.questions[i]}\n**Answer:** {ans.content.capitalize()}"
					self.reports.append(ques_with_ans)
					if i >= len(self.questions)-1:
						await ctx.author.send("Send 'Done' to submit.")
						done = await self.bot.wait_for("message",check=lambda msg:msg.author.id==ctx.author.id)
						if done.content.lower()=="done":
							await ctx.author.send("Submitted successfully!")
							self.submit = "yes"
							self.i = 0
							break
			else:
				await ctx.author.send("Oops.. Try again!")
		except asyncio.TimeoutError:
						await ctx.author.send("Time Out!!\nYou haven't responds in time!\nTry again.")
						pass
		if self.submit== "yes":
			if self.channel is None:
				channel = ctx.guild.system_channel
				if channel is not None:
					self.channel = channel.id
				else:
					self.channel = get(ctx.guild.channels,name="general").id
		else:
			self.channel = ctx.message.channel.id

			em = discord.Embed(title=f"New Bug Reported | Repoter: {ctx.author}", description="\n".join(self.reports),color=0xffdf08, timestamp=time.now())
			em.set_author(name=self.bot.user.name,icon_url=self.bot.user.avatar_url)
			em.set_footer(text="Programming Hero")
			await get(ctx.guild.channels,id=self.channel).send(embed=em)
			self.reports = []
			self.submit = "no"
#set channel	
	@commands.command()
	async def setBugReportChannel(self,ctx,channel:discord.TextChannel):
			self.channel = channel.id
			await ctx.send("Bug reports update channel has been set!")'''
			
def setup(bot):
	bot.add_cog(Bug(bot))