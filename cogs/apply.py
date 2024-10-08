import discord
from discord.ext import commands
from discord.utils import get
from datetime import datetime as time

import asyncio
import pymongo
import os


class Application(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.command()
    @commands.guild_only()
    async def apply(self, ctx):
        #### connect with database ####
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"]  # database
        tb = db['guild_data']
        other_tb = db["other_data"]  # table
        other_data = other_tb.find_one({'name': 'ignore_dm'})
        guild_data = tb.find_one({'guild_id': ctx.guild.id})
        if guild_data:
            questions = guild_data.get('report_questions')
            if questions:
                #### check function ####
                def message_check(message):
                    return message.author.id == ctx.author.id and isinstance(message.channel, discord.channel.DMChannel)
                ########
                if other_data:
                    ids = other_data.get('user_ids')
                    if ids:
                        if not ctx.author.id in ids:
                            ids.append(ctx.author.id)
                    else:
                        ids = [ctx.author.id]
                    other_tb.update_one({'name': 'ignore_dm'}, {
                                        '$set': {'user_ids': ids}})
                else:
                    other_tb.insert_one(
                        {'name': 'ignore_dm', 'user_ids': [ctx.author.id]})

                await ctx.message.add_reaction('\N{Lady Beetle}')
                await ctx.send(f'Thank you {ctx.author.mention} for informing a bug.\nCheck DM!!')
                em = discord.Embed(
                    description='Please provide some extra information to make it easier for the developer to fix.\nSend \'Ok\' to continue.', color=0x7700FE)
                await ctx.author.send(embed=em)
                try:
                    ok = await self.bot.wait_for("message", check=message_check, timeout=60)
                except asyncio.TimeoutError:
                    await ctx.author.send('Time out!!\nYou didn\'t respond in time')
                    ids = other_data.get('user_ids')
                    if ctx.author.id in ids:
                        ids.remove(ctx.author.id)
                    other_tb.update_one({'name': 'ignore_dm'}, {
                                        '$set': {'user_ids': ids}})
                else:
                    if ok.content.lower() == 'ok':
                        await ok.add_reaction('<:greentickbadge:852127602373951519>')
                        await asyncio.sleep(2)
                        answers = {ctx.author.id: []}
                        done = True
                        for no, question in enumerate(questions, 1):
                            ques_em = discord.Embed(
                                title=f'Question-{no}', description=f'{question}', color=0xFDB706)
                            await ctx.author.send(embed=ques_em)
                            try:
                                ans = await self.bot.wait_for('message', check=message_check, timeout=180)
                            except asyncio.TimeoutError:
                                await ctx.author.send('Time out!!\nYou didn\'t respond in time')
                                # remove user
                                ids = other_data.get('user_ids')
                                if ctx.author.id in ids:
                                    ids.remove(ctx.author.id)
                                other_tb.update_one({'name': 'ignore_dm'}, {
                                                    '$set': {'user_ids': ids}})
                                done = False
                                break
                            else:
                                if ans.attachments:
                                    for attachment in ans.attachments:
                                        ans.content += f'\n{attachment.url}'
                                answers[ctx.author.id].append(ans.content)
                        if done:
                            submit_em = discord.Embed(
                                title='Do you want to submit this bug?', description='**React below:**\n<:greentickbadge:852127602373951519> = \'Yes\'\n<:redtickbadge:854250345113714688> = \'No\'', color=0x7700FE)
                            submit = await ctx.author.send(embed=submit_em)

                            emojis = ['<:greentickbadge:852127602373951519>',
                                      '<:redtickbadge:854250345113714688>']
                            for emoji in emojis:
                                await submit.add_reaction(emoji)
                            # reaction check

                            def reaction_check(reaction, user):
                                return user.id == ctx.author.id and reaction.message.id == submit.id

                            try:
                                reaction, user = await self.bot.wait_for('reaction_add', check=reaction_check, timeout=60)
                            except:
                                await ctx.author.send('Oops!! You didn\'t respond in time :(')
                                # remove user
                                ids = other_data.get('user_ids')
                                if ctx.author.id in ids:
                                    ids.remove(ctx.author.id)
                                other_tb.update_one({'name': 'ignore_dm'}, {
                                                    '$set': {'user_ids': ids}})

                            else:
                                if str(reaction.emoji) == emojis[0]:
                                    report_channels = guild_data.get(
                                        'report_channels')

                                    report_em = discord.Embed(
                                        title=f'Bug Reported', description=f'A bug reported by **{ctx.author}**\n**User ID:** {ctx.author.id}', color=0xFDB706)
                                    for no, question in enumerate(questions, 1):
                                        the_answer = answers.get(
                                            ctx.author.id)[no-1]
                                        report_em.add_field(
                                            name=f'Question-{no}', value=f'**Question:** {question}\n**Answer:** {the_answer}', inline=False)
                                    report_em.set_thumbnail(
                                        url=f'{ctx.author.avatar_url}')
                                    if report_channels:
                                        for channel in report_channels:
                                            channel = await self.bot.fetch_channel(int(channel))
                                            await channel.send(embed=report_em)
                                    else:
                                        await ctx.send(embed=report_em)
                                    await ctx.author.send('Your report successfully submitted!!')
                                    # remove user
                                    ids = other_data.get('user_ids')
                                    if ctx.author.id in ids:
                                        ids.remove(ctx.author.id)
                                    other_tb.update_one({'name': 'ignore_dm'}, {
                                                        '$set': {'user_ids': ids}})

                                elif str(reaction.emoji) == emojis[1]:
                                    await ctx.author.send('Ok.. No problem.')
                                    # remove user
                                    ids = other_data.get('user_ids')
                                    if ctx.author.id in ids:
                                        ids.remove(ctx.author.id)
                                    other_tb.update_one({'name': 'ignore_dm'}, {
                                                        '$set': {'user_ids': ids}})

            else:
                await ctx.send('No question provided from the server')
        else:
            await ctx.send('This server doesn\'t enabled this feature')

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def addQuestion(self, ctx):
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"]  # database
        tb = db['guild_data']  # table
        guild_data = tb.find_one({'guild_id': ctx.guild.id})
        if not guild_data:
            tb.insert_one({'guild_id': ctx.guild.id, 'report_questions': []})

        questions = guild_data.get('report_questions')
        if questions:
            await ctx.send('Seems like I found some report questions of this server in my database.\n**__Note:__ You can send \'cancel\' anytime to cancel the process.**')
        else:
            questions = []

        def check(message):
            return message.author.id == ctx.author.id
        no = 1
        ques_len = len(questions)
        while True:

            if questions and no <= ques_len:
                q_em = discord.Embed(color=0xFDB706)
                q_em.title = f'Question-{no}'
                q_em.description = f'**Old question:** {questions[no-1]}'
                await ctx.send(embed=q_em)
                await ctx.send('Send the question.\nTo cancel send \'cancel\' or \'skip\' to skip to the next question this question will not change if you skip!!')
            else:
                await ctx.send(f'Question-{no}')
                await ctx.send('Send the question.\nTo cancel send \'cancel\' or \'Done\' if you are done!!')

            try:
                question = await self.bot.wait_for('message', check=check, timeout=300)
            except asyncio.TimeoutError:
                await ctx.send(f'Time out!!\n{ctx.author.mention}, you took a long time...\nNow the process has been cancelled.')
                break
            if question.content.lower().strip() == 'cancel':
                await ctx.send('The process has been cancelled!!')
                break
            elif question.content.lower().strip() == 'done':
                update_msg = await ctx.send('Wait... Your questions are saving!!')
                tb.update_one({
                    'guild_id': ctx.guild.id
                },
                    {
                    '$set': {
                        'report_questions': questions
                    }
                })
                await update_msg.edit(content='<:greentickbadge:852127602373951519>Data Successfully Saved!!')
                break
            elif question.content.lower().strip() == 'skip' and no <= ques_len:
                await ctx.send(f'Question-{no} skipped!!')
                no += 1
            elif question.content.lower().strip() == 'skip' and no > ques_len:
                await ctx.send(f'You can\'t skip questions now!!')
            else:
                if questions and no <= ques_len:
                    questions[no-1] = question.content
                else:
                    questions.append(question.content)
                no += 1

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def addChannel(self, ctx):
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"]  # database
        tb = db['guild_data']  # table
        guild_data = tb.find_one({'guild_id': ctx.guild.id})

        if not guild_data:
            tb.insert_one({'guild_id': ctx.guild.id, 'report_channels': {}})
        channels = guild_data.get('report_channels')
        if not channels:
            channels = []

        def check(message):
            return message.author.id == ctx.author.id

        channel_len = len(channels)
        if channels:
            await ctx.send('Seems like I found some channels to send report.\n**__Note:__ You can send \'cancel\' anytime to cancel the process.**')

        no = 1
        invalid_channel = False
        while True:
            if channels and no <= channel_len and not invalid_channel:
                old_channel_id = int(channels[no-1])
                old_channel = discord.utils.get(
                    old_guild.channels, id=old_channel)
                await ctx.send(f'Old Channel: {old_channel}')
                await ctx.send('Send the channel id.\nTo cancel send \'cancel\' or \'skip\' to skip to the next channel!!')
            else:
                await ctx.send('Send the channel id.\nType and send \'done\' if you are done.')
            try:
                channel = await self.bot.wait_for('message', check=check, timeout=120)
            except asyncio.TimeoutError:
                await ctx.send(f'Time out..!\n{ctx.author.mention}, you took a long time.')
                break
            if channel.content.lower().strip() == 'skip' and no <= channel_len:
                await ctx.send('Skipping!!')
                no += 1
            elif channel.content.lower().strip() == 'skip' and no > channel_len:
                await ctx.send('You can\'t skip now!!')
            elif channel.content.lower().strip() == 'cancle':
                await ctx.send('The process has been cancelled!!')
                break
            elif channel.content.lower().strip() == 'done':
                update_msg = await ctx.send('Wait... Data saving in database!!')
                tb.update_one({
                    'guild_id': ctx.guild.id
                },
                    {
                    '$set': {
                        'report_channels': channels
                    }
                })
                await update_msg.edit(content='<:greentickbadge:852127602373951519>Data Successfully Saved!!')
                break
            elif channel.content.isnumeric():
                is_channel = await self.bot.fetch_channel(int(channel.content))
                if is_channel and no <= channel_len:
                    channel[no-1] = int(channel.content)
                    no += 1
                elif is_channel and no > channel_len:
                    channels.append(int(channel.content))
                    no += 1
                else:
                    await ctx.send('Invaild channel!!\nDidn\'t find any channel with that id -_-')
                    invalid_channel = True

            else:
                await ctx.send('Need an integer value!!')

    @commands.command(aliases=['rmReportChannel'])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def removeChannel(self, ctx):
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"]  # database
        tb = db['guild_data']  # table
        guild_data = tb.find_one({'guild_id': ctx.guild.id})

        def check(message):
            return message.author.id == ctx.author.id

        if guild_data:
            channel_ids = guild_data.get('report_channels')
            if channel_ids:
                channels = []
                indx = []
                no = 0
                for i in channel_ids:
                    ch = await self.bot.fetch_channel(int(i))
                    channels.append(ch)
                msg = ''
                for i, j in enumerate(channels, 1):
                    msg += f'{i:^5} - {j.guild.name:^20} - {j.name:^20}\n'

                ch_msg = await ctx.send(f'Here are all channels\n```\n{"Index":^5} - {"Guild Name":^20} - {"Channel Name":^20}\n{msg}\n```')
                await ch_msg.reply('Send the index number of the channel you want to remove or send \'cancel\' anytime if you want to cancel')
                while True:
                    if no != len(channel_ids):
                        await ctx.send('Send the index number or send \'Done\' if you are done!!\n(send \'all\' to remove all channel)')
                    try:
                        if no != len(channel_ids):
                            choice = await self.bot.wait_for('message', check=check, timeout=120)
                    except asyncio.TimeoutError:
                        await ctx.send(f'Time Out!!\n{ctx.author.mention}, You took long time so the process is cancelled...')
                        break

                    else:
                        if choice.content.lower().strip() == 'done' or no == len(channel_ids):
                            update_msg = await ctx.send('Wait... Data saving in database!!')
                            for j in indx:
                                channel_ids.remove(j)
                            tb.update_one({
                                'guild_id': ctx.guild.id
                            },
                                {
                                '$set': {
                                    'report_channels': channel_ids
                                }
                            })
                            await update_msg.edit(content='<:greentickbadge:852127602373951519> Data Successfully Saved!!')
                            break
                        elif choice.content.lower().strip() == 'all':
                            update_msg = await ctx.send('Wait... Data saving in database!!')
                            tb.update_one({
                                'guild_id': ctx.guild.id
                            },
                                {
                                '$set': {
                                    'report_channels': []
                                }
                            })
                            await update_msg.edit(content='<:greentickbadge:852127602373951519> Data Successfully Saved!!')
                            break
                        elif choice.content.lower().strip() == 'cancle':
                            await ctx.send('<:greentickbadge:852127602373951519> Process cancelled!!')
                            break
                        elif choice.content.isnumeric():
                            ind = int(choice.content)
                            if ind > len(channel_ids):
                                await ctx.send('<:redtickbadge:854250345113714688> Index out of range!!\nSee the list of channels and try again!!')
                            else:
                                ind_no = int(choice.content)-1
                                id = channel_ids[ind_no]
                                indx.append(id)
                                no += 1

                        else:
                            await ctx.send('Give an integer value...')
            else:
                await ctx.send('No report channels found of this server in my database...')

        else:
            await ctx.send('This server hasn\'t enabled report command!!')

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def showChannels(self, ctx):
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"]  # database
        tb = db['guild_data']  # table
        guild_data = tb.find_one({'guild_id': ctx.guild.id})
        if guild_data:
            channel_ids = guild_data.get('report_channels')
            if channel_ids:
                channels = []
                for i in channel_ids:
                    ch = await self.bot.fetch_channel(int(i))
                    channels.append(ch)
                msg = ''
                for i, j in enumerate(channels, 1):
                    msg += f'{i:^5} - {j.guild.name:^20} - {j.name:^20}\n'
                await ctx.send(f'Here are all channels\n```\n{"Index":^5} - {"Guild Name":^20} - {"Channel Name":^20}\n{msg}\n```')

            else:
                await ctx.send('No report channels found of this server in my database...')
        else:
            await ctx.send('This server hasn\'t enabled report command!!')

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def showQuestions(self, ctx):
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"]  # database
        tb = db['guild_data']  # table
        guild_data = tb.find_one({'guild_id': ctx.guild.id})
        if guild_data:
            questions = guild_data.get('report_questions')
            if questions:
                msg = ''
                for i, j in enumerate(questions, 1):
                    msg += f'{i:^5} - {j:>5}\n'
                await ctx.send(f'Here are all questions\n```\n{"No":^5} - {"Question":>5}\n{msg}\n```')

            else:
                await ctx.send('No questions found of this server in my database...')
        else:
            await ctx.send('This server hasn\'t enabled report command!!')

    @commands.command(aliases=['rmReportQuestions'])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def removeQuestion(self, ctx):
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"]  # database
        tb = db['guild_data']  # table
        guild_data = tb.find_one({'guild_id': ctx.guild.id})

        def check(message):
            return message.author.id == ctx.author.id

        if guild_data:
            questions = guild_data.get('report_questions')
            if questions:
                indx = []
                no = 0

                msg = ''
                for i, j in enumerate(questions, 1):
                    msg += f'{i:^5} - {j:>5}\n'
                ques_msg = await ctx.send(f'Here are all questions\n```\n{"No":^5} - {"Question":>5}\n{msg}\n```')

                await ques_msg.reply('Send the index number of the question you want to remove or send \'cancel\' anytime if you want to cancel')
                while True:
                    if no != len(questions):
                        await ctx.send('Send the index number or send \'Done\' if you are done!!\n(send \'all\' to remove all question)')
                    try:
                        if no != len(questions):
                            choice = await self.bot.wait_for('message', check=check, timeout=120)
                    except asyncio.TimeoutError:
                        await ctx.send(f'Time Out!!\n{ctx.author.mention}, You took long time so the process is cancelled...')
                        break

                    else:
                        if choice.content.lower().strip() == 'done' or no == len(questions):
                            update_msg = await ctx.send('Wait... Data saving in database!!')
                            for j in indx:
                                questions.remove(j)
                            tb.update_one({
                                'guild_id': ctx.guild.id
                            },
                                {
                                '$set': {
                                    'report_questions': questions
                                }
                            })
                            await update_msg.edit(content='<:greentickbadge:852127602373951519> Data Successfully Saved!!')
                            break
                        elif choice.content.lower().strip() == 'all':
                            update_msg = await ctx.send('Wait... Data saving in database!!')
                            tb.update_one({
                                'guild_id': ctx.guild.id
                            },
                                {
                                '$set': {
                                    'report_questions': []
                                }
                            })
                            await update_msg.edit(content='<:greentickbadge:852127602373951519> Data Successfully Saved!!')
                            break
                        elif choice.content.lower().strip() == 'cancle':
                            await ctx.send('<:greentickbadge:852127602373951519> Process cancelled!!')
                            break
                        elif choice.content.isnumeric():
                            ind = int(choice.content)
                            if ind > len(questions):
                                await ctx.send('<:redtickbadge:854250345113714688> Index out of range!!\nSee the list of questions carefully and try again!!')
                            else:
                                ind_no = int(choice.content)-1
                                q = questions[ind_no]
                                indx.append(q)
                                no += 1

                        else:
                            await ctx.send('Give an integer value...')
            else:
                await ctx.send('No questions found of this server in my database...')

        else:
            await ctx.send('This server hasn\'t enabled report command!!')

    ###### Error Handling ######

    @apply.error
    async def _error(self, ctx, error):
        log = await self.bot.fetch_channel(855048645174755358)
        await log.send(f'Exception in **apply command** > apply: {error}')
        raise error

    @addQuestion.error
    async def _error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send('This command only work in server!!')
        else:
            log = await self.bot.fetch_channel(855048645174755358)
            await log.send(f'Exception in **apply command** > addQuestion: {error}')
            raise error

    @addChannel.error
    async def _error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send('This command only work in server!!')
        else:
            log = await self.bot.fetch_channel(855048645174755358)
            await log.send(f'Exception in **apply command** > addChannel: {error}')
            raise error

    @removeChannel.error
    async def _error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send('This command only work in server!!')
        else:
            log = await self.bot.fetch_channel(855048645174755358)
            await log.send(f'Exception in **apply comamnd** > removeChannel: {error}')
            raise error

    @removeQuestion.error
    async def _error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send('This command only work in server!!')
        else:
            log = await self.bot.fetch_channel(855048645174755358)
            await log.send(f'Exception in **apply command** > removeQuestion: {error}')
            raise error

    @showQuestions.error
    async def _error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send('This command only work in server!!')
        else:
            log = await self.bot.fetch_channel(855048645174755358)
            await log.send(f'Exception in **apply command** > showQuestions: {error}')
            raise error

    @showChannels.error
    async def _error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send('This command only work in server!!')
        else:
            log = await self.bot.fetch_channel(855048645174755358)
            await log.send(f'Exception in **apply command** > showChannels: {error}')
            raise error


def setup(bot):
    bot.add_cog(Application(bot))
