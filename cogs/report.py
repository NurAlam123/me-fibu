import discord
from discord.ext import commands
import discord_components as d_c

import pymongo
import os
import asyncio
import pygsheets

g_user = pygsheets.authorize(service_file= 'keys.json')

ID = '1XuQL65cSJR4oGbvWADF-DpEkIIdycEcVw3C9U8oZoic'

class Report(commands.Cog):
    def __init__(self, client):
        self.bot = client

    def build_embed(self, question, no = None):
        em = discord.Embed(color= 0xFDDD0B)
        em.title = f"Question-{no}" if no else None
        em.description = question
        return em
    
    def store_data(self, user, answers):
        ### open sheet
        spreadsheet = g_user.open_by_key(ID)
        sheet = spreadsheet[0]
        
        all_reports = sheet.get_all_values(include_tailing_empty=False, include_tailing_empty_rows=False)
        
        length = len(all_reports)
        sl = length
        
        row = length+1
        cols = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
        
        ### collect data
        data = []
        
        ### user info
        _user = user["user"]
        user_id = user["id"]
        platform = user["platform"]
        device = user["device"]
        
        ## store user data
        data.append(sl)
        data.append(_user)
        data.append(user_id)
        data.append(platform)
        data.append(device)
        
        ### answers
        bug_in = answers["bug_in"]
        live_bug = answers["see_bug"]
        screenshots = answers["screenshots"]
        
        if bug_in != "App Crash":
            bug_location = answers["location"]   
        else:
            bug_location = ""
        
        if "app_crash_details" in answers:
            crash_details = answers["app_crash_details"]
        else:
            crash_details = ""
        
        if "bug_details" in answers.keys():
            bug_details = answers["bug_details"]
        else:
            bug_details = ""
        
        ## store bug data
        data.append(bug_in)
        data.append(bug_location)
        data.append(bug_details)
        data.append(live_bug)
        data.append(crash_details)
        data.append(screenshots)
        
        for i in range(len(cols)):
            cell = f"{cols[i]}{row}"
            sheet.update_value(cell, data[i])
            
            
    def hv_embed(self, user, answers):
        ### open sheet
        spreadsheet = g_user.open_by_key(ID)
        sheet = spreadsheet[0]
        
        all_reports = sheet.get_all_values(include_tailing_empty=False, include_tailing_empty_rows=False)
        
        sl = len(all_reports)
        ### user info
        _user = user["user"]
        user_name = user["name"]
        user_id = user["id"]
        
        ### answers
        bug_in = answers["bug_in"]
        live_bug = answers["see_bug"]
        screenshots = answers["screenshots"]
        
        embed = discord.Embed(title= "Bug Report-{sl}", description= f"A bug reported by <@{user_id}>\n**User**: {_user}\n**Name:** {user_name}\n**User ID:** {user_id}", color = 0xFDDD0B)
    
        embed.add_field(name = "Bug Found in?", value = f"{bug_in}", inline = False)
        
        if bug_in != "App Crash":
            bug_location = answers["location"] # questions 2.1
            embed.add_field(name = "Bug Location?", value = f"{bug_location}", inline = False)
            
        
        if "bug_details" in answers.keys():
            bug_details = answers["bug_details"]
            embed.add_field(name = "Extra Details", value = f"{bug_details}", inline = False)
        else:
            embed.add_field(name = "Extra Details", value = f"Not Provided!!", inline = False)
        
        embed.add_field(name = "How to reproduce the bug/issue?", value = f"{live_bug}", inline = False)
        if screenshots.strip() != "":
            embed.add_field(name = "Screenshots", value = f"{screenshots}", inline = False)
        embed.set_thumbnail(url = f"{_user.avatar_url}")
        
        return embed
    
    def full_report_embed(self, user, answers):
        embed = hv_embed(user, answers)
        platform = user["platform"]
        device = user["device"]
        embed_1 = embed.copy()
        embed_1.insert_field_at(0, name = "Device information", value = f"Operating system: {platform}\n{device}", inline = False)
        if "app_crash_details" in answers:
            crash_details = answers["app_crash_details"] # app crash details
            embed_1.insert_field_at(2, name = "App Crash Details", value = f"{crash_details}", inline = False)
        else:
            embed_1.insert_field_at(2, name = "App Crash Details", value = f"Not Provided!!", inline = False)
            
            return embed_1
    
    @commands.command()
    @commands.guild_only()
    async def report(self, ctx):
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"] #database
        other_tb = db["other_data"] #table
        other_data = other_tb.find_one({"name": "ignore_dm"})
        if ctx.guild.id != 839126064621027329:
            pass
        else:
            if other_data:
                ids = other_data.get("user_ids")
                if ids:
                    if not ctx.author.id in ids:
                        ids.append(ctx.author.id)
                else:
                    ids = [ctx.author.id]
                other_tb.update_one({"name": "ignore_dm"}, {"$set": {"user_ids": ids}})
            else:
                other_tb.insert_one({"name": "ignore_dm", "user_ids": [ctx.author.id]})
                    
            ids = other_data.get('user_ids')
            
            #### check functions ####
            def message_check(message):
                 return message.author.id == ctx.author.id and isinstance(message.channel, discord.channel.DMChannel)
            ########
            
            await ctx.message.add_reaction("\N{Lady Beetle}")
            await ctx.send(f"Thank you {ctx.author.mention} for informing a bug.\nCheck DM!!")
            
            confirm_msg = "Your one message hurts bugs but doesn't kill them. We'll need a little extra information so developers can wear the Flash suit. \N{winking face}\nClick 'Continue' to continue.\nClick 'Cancel' to cancel the process!!"
            options = [
                [
                    d_c.Button(
                        label = "Continue",
                        id = "yes",
                        style = 3
                    ),
                    d_c.Button(
                        label = "Cancel",
                        id = "cancel",
                        style = 4
                    )
                ]
            ]
            em = self.build_embed(confirm_msg)
            msg = await ctx.author.send(embed= em, components = options)
            try:
                confirm = await self.bot.wait_for("button_click", timeout= 180)
            except asyncio.TimeoutError:
                await msg.edit(components = [])
                await ctx.author.send("Time out!!\nYou didn\'t respond in time")
                if ctx.author.id in ids:
                    ids.remove(ctx.author.id)
                other_tb.update_one({'name': 'ignore_dm'}, {'$set': {'user_ids': ids}})
            else:
                user_info = {}
                answers = {}
                option_value = confirm.component.id
                if option_value == "cancel":
                   await ctx.author.send("The process has been cancelled!!")
                   await msg.edit(components = [])
                   if ctx.author.id in ids:
                        ids.remove(ctx.author.id)
                   other_tb.update_one({'name': 'ignore_dm'}, {'$set': {'user_ids': ids}})
                elif option_value == "yes":
                    await msg.edit(components = [])
                    ## question 1
                    question_1 = "Which operating system you are using?"
                    embed = self.build_embed(question_1, 1)
                    options = [
                        [
                            d_c.Button(
                                label = "Android",
                                emoji = self.bot.get_emoji(860566286069268521),
                                style = 3,
                                id = "android"
                            ),
                            d_c.Button(
                                label = "iOS",
                                emoji = self.bot.get_emoji(860566067201441793),
                                style = 1,
                                id = "ios"
                            )
                        ]
                    ]
                    
                    platform_msg = await ctx.author.send(embed = embed, components = options)
                    try:
                        platform_select = await self.bot.wait_for("button_click", timeout = 180)
                    except asyncio.TimeoutError:
                        await platform_msg.edit(components = [])
                        await ctx.author.send("You didn't respond in time!!")
                        if ctx.author.id in ids:
                            ids.remove(ctx.author.id)
                        other_tb.update_one({'name': 'ignore_dm'}, {'$set': {'user_ids': ids}})
                    else:
                        user_info["user"] = ctx.author # store user
                        user_info["name"] = f"{ctx.author.name}" # store user name 
                        user_info["id"] = f"{ctx.author.id}" # store user id
                        user_info["tag"] = f"{ctx.author.discriminator}" # store user tag
                        
                        option_value = platform_select.component.id
                        await platform_msg.edit(components = [])
                        user_info["platform"] = "Android" if option_value == "android" else "iOS" # store user operating system name
                        if option_value == "android":
                            format = "Device Name: \nModel Number: \nAndroid Version: \nApp Version: \nRam (Optional): \nRom (Optional): "
                        else:
                            format = "Device Name: \nModel Number: \niOS Version: \nApp Version: \nRam (Optional): \nRom (Optional): "
                        
                        text = "Please provide us some information about your device such as device name, model number, system version and our app version.\nCopy below text, fill up properly and send it here!!"
                        embed = self.build_embed(text)
                        device_info_msg = await ctx.author.send(embed = embed)
                        await device_info_msg.reply(f"```\n{format}\n```")
                        try:
                            device_info = await self.bot.wait_for("message", check = message_check, timeout = 180)
                        except asyncio.TimeoutError:
                            await ctx.author.send("You didn't respond in time!!")
                            if ctx.author.id in ids:
                                ids.remove(ctx.author.id)
                            other_tb.update_one({'name': 'ignore_dm'}, {'$set': {'user_ids': ids}})
                        else:
                            user_info["device"] = device_info.content # store user device information
                            
                            ## question 2
                            question_2 = "Where was this bug sucking your happiness?"
                            embed = self.build_embed(question_2, 2)
                            options = [
                                d_c.Select(
                                    placeholder = "Select from here!!",
                                    id = "bug_in",
                                    options = [
                                       d_c.SelectOption(
                                              label = "Forums",
                                              value = "forums"
                                       ),
                                       d_c.SelectOption(
                                               label = "Settings",
                                                value = "settings"
                                        ),
                                        d_c.SelectOption(
                                                label = "Profile",
                                                value = "profile"
                                        ),
                                        d_c.SelectOption(
                                                label = "Content",
                                                value = "content"
                                        ),
                                        d_c.SelectOption(
                                                label = "App Crash",
                                                value = "app_crash"
                                        )
                                    ]
                                )
                            ]
                            options_msg = await ctx.author.send(embed = embed, components= options)
                            try:
                                option = await self.bot.wait_for("select_option", timeout = 180)
                            except asyncio.TimeoutError:
                                await ctx.author.send("You didn't respond in time!!")
                                await options_msg.edit(components = [])
                                if ctx.author.id in ids:
                                    ids.remove(ctx.author.id)
                                other_tb.update_one({'name': 'ignore_dm'}, {'$set': {'user_ids': ids}})
                            else:
                                option_value = option.component[0].value
                                answers["bug_in"] = option.component[0].label # store bug location
                                await options_msg.edit(components= [])
                                if option_value == "content":
                                    ## question 2.1
                                    location = "Seems like, bug was trying to learn programming from the contents. You have to give us the location of that bug to kill it properly.\n**__For Example:__**\n```\nGalaxy Name > Fundamentals\nModule Name > Functions\nLesson Name > function usage\nPage Number > 2/9\n```\nNow, copy below text, fill up properly like that given example and send it here!!"
                                    embed = build_embed(location)
                                    location_format = "Galaxy name > \nModule name > \nLesson name> \nPage Number > "
                                    loc_msg = await ctx.author.send(embed = embed)
                                    await loc_msg.reply(f"```\n{location_format}\n```")
                                    try:
                                        location_msg = await self.bot.wait_for("message", check = message_check, timeout = 180)
                                    except asyncio.TimeoutError:
                                        await ctx.author.send("You didn't respond in time!!")
                                        await options_msg.edit(components = [])
                                        bug_found = False
                                        if ctx.author.id in ids:
                                            ids.remove(ctx.author.id)
                                        other_tb.update_one({'name': 'ignore_dm'}, {'$set': {'user_ids': ids}})
                                    else:
                                        answers["location"] = location_msg.content
                                        bug_found = True
                                elif option_value == "settings":
                                    ## question 2.1
                                    ques = "Where did you find the bug in settings?"
                                    embed = self.build_embed(ques, 2.1)
                                    await ctx.author.send(embed = embed)
                                    try:
                                        location_msg = await self.bot.wait_for("message", check = message_check, timeout = 180)
                                    except asyncio.TimeoutError:
                                        await ctx.author.send("You didn't respond in time!!")
                                        await options_msg.edit(components = [])
                                        bug_found = False
                                        if ctx.author.id in ids:
                                            ids.remove(ctx.author.id)
                                        other_tb.update_one({'name': 'ignore_dm'}, {'$set': {'user_ids': ids}})
                                    else:
                                        answers["location"] = location_msg.content
                                        bug_found = True
                                elif option_value == "profile":
                                    ## question 2.1
                                    ques = "Where did you find the bug in profile?"
                                    embed = self.build_embed(lques, 2.1)
                                    await ctx.author.send(embed = embed)
                                    try:
                                        location_msg = await self.bot.wait_for("message", check = message_check, timeout = 180)
                                    except asyncio.TimeoutError:
                                        await ctx.author.send("You didn't respond in time!!")
                                        await options_msg.edit(components = [])
                                        bug_found = False
                                        if ctx.author.id in ids:
                                            ids.remove(ctx.author.id)
                                        other_tb.update_one({'name': 'ignore_dm'}, {'$set': {'user_ids': ids}})
                                    else:
                                        answers["location"] = location_msg.content
                                        bug_found = True
                                elif option_value == "forums":
                                    ## question 2.1
                                    ques = "Where did you find the bug in forums?"
                                    embed = self.build_embed(ques, 2.1)
                                    await ctx.author.send(embed = embed)
                                    try:
                                        location_msg = await self.bot.wait_for("message", check = message_check, timeout = 180)
                                    except asyncio.TimeoutError:
                                        await ctx.author.send("You didn't respond in time!!")
                                        await options_msg.edit(components = [])
                                        bug_found = False
                                        if ctx.author.id in ids:
                                            ids.remove(ctx.author.id)
                                        other_tb.update_one({'name': 'ignore_dm'}, {'$set': {'user_ids': ids}})
                                    else:
                                        answers["location"] = location_msg.content
                                        bug_found = True
                                elif option_value == "app_crash":
                                    ## question 2.1
                                    ques = "If you can give us the crash report by clicking on 'View Details' option then send it here (you can provide screen shot) or type 'No' to skip!!"
                                    embed = self.build_embed(ques)
                                    await ctx.author.send(embed = embed)
                                    try:
                                        location_msg = await self.bot.wait_for("message", check = message_check, timeout = 180)
                                    except asyncio.TimeoutError:
                                        await ctx.author.send("You didn't respond in time!!")
                                        await options_msg.edit(components = [])
                                        bug_found = False
                                        if ctx.author.id in ids:
                                            ids.remove(ctx.author.id)
                                        other_tb.update_one({'name': 'ignore_dm'}, {'$set': {'user_ids': ids}})
                                    else:
                                        if location_msg.content.lower().strip() == "no":
                                            bug_found = True
                                        else:
                                            if location_msg.attachments:
                                                for i in location_msg.attachments:
                                                    location_msg.content += f"\n{i.url}"
                                            
                                            answers["app_crash_details"] = location_msg.content
                                            bug_found = True
                                
                                if bug_found:
                                    ## question 3
                                    question_3 = "Do you want to describe the bug?\nIf yes then type 'Yes'\nIf no then type 'No' to skip!!"
                                    embed = self.build_embed(question_3, 3)
                                    await ctx.author.send(embed = embed)
                                    try:
                                        yes_no = await self.bot.wait_for("message", check = message_check, timeout = 180)
                                    except asyncio.TimeoutError:
                                        await ctx.author.send("You didn't respond in time!!")
                                        if ctx.author.id in ids:
                                            ids.remove(ctx.author.id)
                                        other_tb.update_one({'name': 'ignore_dm'}, {'$set': {'user_ids': ids}})
                                    else:
                                        if yes_no.content.lower().strip() == "yes":
                                            await ctx.author.send("Send the details here... \nYou have 5 minutes.")
                                            try:
                                                details = await self.bot.wait_for("message", check = message_check, timeout = 300)
                                            except asyncio.TimeoutError:
                                                await ctx.author.send("You didn't respond in time!!\nSo the process skipped...")
                                                
                                            else:
                                                answers["bug_details"] = details.content
                                        elif yes_no.content.lower().strip() in ["no", "skip"]:
                                            pass
                                    
                                    ## question 4
                                    question_4 = "How do we see the bug sucking our happiness LIVE? (how to reproduce the bug/issue?)\n(You can attach some screenshots or screen record too)"
                                    embed = self.build_embed(question_4, 4)
                                    await ctx.author.send(embed = embed)
                                    try:
                                        user_ans = await self.bot.wait_for("message", check = message_check, timeout = 180)
                                    except asyncio.TimeoutError:
                                        await ctx.author.send("You didn't respond in time!!")
                                        if ctx.author.id in ids:
                                            ids.remove(ctx.author.id)
                                        other_tb.update_one({'name': 'ignore_dm'}, {'$set': {'user_ids': ids}})
                                    else:
                                        if user_ans.attachments:
                                            for i in user_ans.attachments:
                                                user_ans.content += f"\n{i.url}"
                                        
                                        answers["see_bug"] = user_ans.content
                                        
                                        ## last
                                        text = "If you want to send some screenshots or screen record then send send all so that we can upgrade our Sword to Level 69.\nType 'Done' if you are done..."
                                        embed = self.build_embed(text)
                                        await ctx.author.send(embed = embed)
                                        content = ""
                                        while True:
                                            try:
                                                user_ans = await self.bot.wait_for("message", check = message_check, timeout = 180)
                                            except asyncio.TimeoutError:
                                                await ctx.author.send("You didn't respond in time!!")
                                                if ctx.author.id in ids:
                                                    ids.remove(ctx.author.id)
                                                other_tb.update_one({'name': 'ignore_dm'}, {'$set': {'user_ids': ids}})
                                                break
                                            else:
                                                
                                                if user_ans.content.lower().strip() == "done":
                                                    answers["screenshots"] = content
                                                    break
                                                else:
                                                    if user_ans.content:
                                                        content += user_ans.content
                                                    if user_ans.attachments:
                                                        for i in user_ans.attachments:
                                                            content += f"\n{i.url}"
                                                   
                                        options = [
                                            [
                                                d_c.Button(
                                                    label = "Yes",
                                                    id = "yes",
                                                    style = 3
                                                ),
                                                d_c.Button(
                                                    label = "No",
                                                    id = "no",
                                                    style = 4
                                                )
                                            ]
                                        ]
                                        
                                        ### preview
                                        preview_embed = full_report_embed(user_info, answers)
                                        preview = await ctx.author.send(content = "Here is the preview of your report!!", embed = preview_embed)
                                        
                                        ### submit
                                        text = "Do you want to submit this bug?"
                                        
                                        embed = self.build_embed(text)
                                        sub_msg = await ctx.author.send(embed = embed, components = options)
                                        try:
                                            submit = await self.bot.wait_for("button_click", timeout = 180)
                                        except asyncio.TimeoutError:
                                            await ctx.send("Time out!!\nYou didn't respond in time!!")
                                            await sub_msg.edit(components = [])
                                            if ctx.author.id in ids:
                                                ids.remove(ctx.author.id)
                                            other_tb.update_one({'name': 'ignore_dm'}, {'$set': {'user_ids': ids}})
                                        else:
                                            value = submit.component.id
                                            await sub_msg.edit(components = [])
                                            if value == "yes":
                                                self.store_data(user_info, answers) ## storing data
                                                main_ch = await self.bot.fetch_channel(848863022905688074)
                                                normal_em = self.hv_embed(user_info, answers)
                                                main_em = self.full_report_embed(user_info, answers)
                                                if answers["bug_in"] != "Content":
                                                    #content_ch = [557639363807150092, 826686813103587341]
                                                    content_ch = [846398100447821824, 843870747331526708]
                                                    for i in bug_ch:
                                                        channel = await self.bot.fetch_channel(i)
                                                        await channel.send(embed = normal_em)
                                                else:
                                                    #bug_ch = [634995781404983296, 826683797377384448]
                                                    bug_ch = [856964979667501066, 856549332286570507]
                                                    for i in content_ch:
                                                        channel = await self.bot.fetch_channel(i)
                                                        await channel.send(embed = normal_em)
                                                
                                                await main_ch.send(embed = main_em)
                                                
                                                if ctx.author.id in ids:
                                                    ids.remove(ctx.author.id)
                                                other_tb.update_one({'name': 'ignore_dm'}, {'$set': {'user_ids': ids}})

    @report.error
    async def _error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send('This command only work in server!!')
        else:
            log = await self.bot.fetch_channel(855048645174755358)
            await log.send(f'Exception in **report command** > report: {error}')
            raise error
            
    
def setup(bot):
    bot.add_cog(Report(bot))