import discord
from discord.ext import commands
from discord.utils import get
from datetime import datetime as time

import asyncio
import pymongo
import os

class Bug(commands.Cog):
    def __init__(self,client):
        self.bot = client
    
    def guild_check(self, ctx):
        return ctx.guild.id == 550676428040044574
    
    @commands.command()
    @commads.guild_only()
    @commands.check(self.guild_check)
    async def report(self, ctx):
        #### connect with database ####
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"] #database
        tb = db['guild_data']
        other_tb = db["other_data"] #table
        other_data = other_tb.find_one({'name': 'ignore_dm'})
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
                        if not ctx.author.id in ids:
                            ids.append(ctx.author.id)
                    else:
                        ids = [ctx.author.id]
                    other_tb.update_one({'name': 'ignore_dm'}, {'$set': {'user_ids': ids}})
                else:
                    other_tb.insert_one({'name': 'ignore_dm', 'user_ids': [ctx.author.id]})
                
                await ctx.message.add_reaction('\N{Lady Beetle}')
                await ctx.send(f'Thank you {ctx.author.mention} for informing a bug.\nCheck DM!!')
                await ctx.author.send(f"Please provide some extra information to make it easier for the developer to fix.\nSend 'Ok' to continue.")
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
                        await ok.add_reaction('\N{white heavy check mark}')
                        await asyncio.sleep(2)
                        answers = {ctx.author.id: []}
                        done = True
                        for no, question in enumerate(questions, 1):
                            ques_em = discord.Embed(title= f'Question-{no}', description= f'{question}', color= 0xFDB706)
                            await ctx.author.send(embed= ques_em)
                            try:
                                ans = await self.bot.wait_for('message', check= message_check, timeout= 180)
                            except asyncio.TimeoutError:
                                await ctx.author.send('Time out!!\nYou didn\'t respond in time')
                                ## remove user
                                ids= other_data.get('user_ids')
                                if ctx.author.id in ids:
                                    ids.remove(ctx.author.id)
                                other_tb.update_one({'name': 'ignore_dm'}, {'$set': {'user_ids': ids}})
                                done = False
                                break
                            else:
                                if ans.attachments:
                                    for attachment in ans.attachments:
                                        ans.content += f'\n{attachment.url}'
                                answers[ctx.author.id].append(ans.content)
                        if done:
                            submit = await ctx.author.send('Do you want to submit this bug?\n**React below:**\n\N{white heavy check mark} = \'Yes\'\n\N{cross mark} = \'No\'')
                            
                            emojis = ['\N{white heavy check mark}', '\N{cross mark}']
                            for emoji in emojis:
                                await submit.add_reaction(emoji)
                            ## reaction check
                            def reaction_check(reaction, user):
                                return user.id == ctx.author.id and reaction.message.id == submit.id and reaction.emoji in emojis
            
                            try:
                                reaction,user = await self.bot.wait_for('reaction_add', check= reaction_check, timeout= 60)
                            except:
                                await ctx.author.send('Oops!! You didn\'t respond in time :(')
                                ## remove user
                                ids= other_data.get('user_ids')
                                if ctx.author.id in ids:
                                    ids.remove(ctx.author.id)
                                other_tb.update_one({'name': 'ignore_dm'}, {'$set': {'user_ids': ids}})
                            else:
                                if str(reaction.emoji) == emojis[0]:
                                    report_channel = guild_data.get('bug_channel')
                                    if report_channel:
                                        channel = await bot.fetch_channel(int(report_channel))
                                    else:
                                        channel = ctx.channel
                                    
                                    report_em = discord.Embed(title= f'Bug Reported', description= f'A bug reported by **{ctx.author}**\n**User ID:** {ctx.author.id}', timestamp= time.now(), color= 0xFDB706)
                                    for no, question in enumerate(questions, 1):
                                        the_answer = answers.get(ctx.author.id)[no-1]
                                        report_em.add_field(name= f'Question-{no}', value= f'**Question:** {question}\n**Answer:** {the_answer}', inline= False)
                                    report_em.set_thumbnail(url= f'{ctx.author.avatar_url}')
                                    await channel.send(embed= report_em)
                                    await ctx.author.send('Your report successfully submitted!!')
                                    ## remove user
                                    ids= other_data.get('user_ids')
                                    if ctx.author.id in ids:
                                        ids.remove(ctx.author.id)
                                    other_tb.update_one({'name': 'ignore_dm'}, {'$set': {'user_ids': ids}})
                                elif str(reaction.emoji) == emojis[1]:
                                    await ctx.author.send('Ok.. No problem.')
                                    ## remove user
                                    ids= other_data.get('user_ids')
                                    if ctx.author.id in ids:
                                        ids.remove(ctx.author.id)
                                    other_tb.update_one({'name': 'ignore_dm'}, {'$set': {'user_ids': ids}})
                            
            else:
                await ctx.send('No question provided from the server')
        else:
            await ctx.send('This server doesn\'t enabled this feature')




def setup(bot):
	bot.add_cog(Bug(bot))