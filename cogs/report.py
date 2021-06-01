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
                            await done.add_reaction('\N{white heavy check mark}')
                            await ctx.author.send('Your report successfully submitted!!')
                        else:
                            await ctx.author.send('Ok.. No problem.')
            else:
                await ctx.send('No question found')
        else:
            await ctx.send('This server doesn\'t allow report command')

def setup(bot):
	bot.add_cog(Bug(bot))