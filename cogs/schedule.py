import discord
from discord.ext import commands
from discord.ext import tasks

from datetime import datetime
import asyncio
import os


class Schedule(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        Schedule.db()
        
    def db(self):
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"] #database
        tb = db["other_data"]
        self.bot.scheduleData = tb.find({"name": "scheduleTask"})
        print(f"\n\n----------------\n{self.bot.scheduleData}\n------------\n\n")
    
    
    @commands.group(case_insensitive = True)
    async def schedule(self, ctx):
        pass
    
    @schedule.command()
    async def add(self, ctx, channel: discord.TextChannel = None):
        if not channel:
            channel = ctx.channel
            
        def user_check(message):
            return message.author.id == ctx.author.id and message.channel.id == ctx.channel.id
        
        while True:
            await ctx.send("<:yellow_dot:896045640168120370> Send time!!\nFormat: dd-mm-yy HH:MM:SS\n**__Note:__Time should be in 24h format**\nFor Example:\n```\n04-12-21 13:30:00\n```\n_Send **exit** to stop this process!!_")
            try:
                userDateTime = await self.bot.wait_for("message", check = user_check, timeout = 300)
            except asyncio.TimeoutError:
                await ctx.send(":warning: **Time out** :warning:\nTry agin!!")
                break
            else:
                if userDateTime.content.strip().lower() != "exit":
                    dateTime = userDateTime.content.strip()
                    timeFormat = "%d-%m-%y %H:%M:%S"
                    try:
                        userTime = datetime.strptime(dateTime, timeFormat).strftime(timeFormat)
                    except:
                        await ctx.send("<:redtickbadge:854250345113714688> **Wrong format!!**\nSend time in correct format...")
                    else:
                        await ctx.send("<:yellow_dot:896045640168120370> Send the message!!\nYou have 5 minutes!!")
                        try:
                            userMessage = await self.bot.wait_for("message", check = user_check, timeout = 300)
                        except asyncio.TimeoutError:
                            await ctx.send(":warning: **Timeout!!!** :slight_smile::warning:")
                            break
                        else:
                            guild_id = ctx.guild.id
                            channel_id = channel.id
                            message = userMessage
                            time = userTime
                            dataFormat = {
                                "guild_id": guild_id,
                                "channel_id": channel_id,
                                "message": userMessage
                            }
                            if time in self.bot.scheduleData:
                                timeData = scheduleData.get(time)
                                timeData.append(dataFormat)
                            else:
                                scheduleData[time] = [dataFormat]
                                
                            await ctx.send("**<:greentickbadge:852127602373951519> Schedule message added successfully!!**")
                            break
                else:
                    await ctx.send("Process stopped!!")
                    break
    
    @schedule.command()
    async def view(self, ctx):
        data = self.bot.scheduleData
        if len(data):
            for time in data:
                for scheduleData in data[time]:
                    guild_id = scheduleData.get("guild_id")
                    if guild_id == ctx.guild.id:
                        channel_id = scheduleData.get("channel_id")
                        message = scheduleData.get("message")
                        dataFormat = f"Time: {time}\nGuild: {guild_id}\nChannel: {channel_id}\nMessage: {message}"
                        await ctx.send(dataFormat)
    
    @tasks.loop(seconds = 1)
    async def timeCheck(self):
        if self.bot.scheduleData.__len__():
            timeFormat = "%d-%m-%y %H:%M:%S"
            timeFormat_2 = "%d-%m-%y %H:%M"
            
            now = datetime.now()
            
            dateTimeNow = now.strftime(timeFormat)
            nowSec = now.second + 1
            dateTimeNowSec = str(nowSec) if nowSec != 60 else "00"
            dateTimeNowCheck = f"{now.strftime(timeFormat_2)}:{dateTimeNowSec}"
            dateTimeNowCheck = datetime.strptime(dateTimeNowCheck, timeFormat).strftime(timeFormat)
        
            if self.bot.scheduleDone and dateTimeNowCheck in self.scheduleData:
                self.bot.scheduleDone = False
        
            if dateTimeNow in self.bot.scheduleData and not self.bot.scheduleDone:
                for scheduleData in self.bot.scheduleData[dateTimeNow]:
                    guild_id = scheduleData.get("guild_id")
                    channel_id = scheduleData.get("channel_id")
                    message = scheduleData.get("message")
                        
                    guild = self.bot.get_guild(guild_id)
                    channel = guild.get_channel(channel_id)
                        
                    await channel.send(message)
                    self.bot.scheduleDone = True
                self.bot.scheduleData.pop(dateTimeNow)


def setup(bot):
    bot.add_cog(Schedule(bot))
        