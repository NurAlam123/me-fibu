import discord
from discord.ext import commands
from discord.ext import tasks

from datetime import datetime
import asyncio
import os
import pymongo

class Schedule(commands.Cog):
    
    con_fibu = pymongo.MongoClient(os.getenv("DB"))
    db = con_fibu["fibu"] #database
    tb = db["other_data"]
    
    def __init__(self, bot):
        self.bot = bot
        self.db()
        self.timeCheck.start()
        
    def db(self):
        data = Schedule.tb.find_one({"name": "scheduleTask"})
        task = data.get("task")
        if not task:
            self.bot.scheduleData = {}
        else:
            self.bot.scheduleData = task   
    
    
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
                        userTime = datetime.strptime(dateTime, timeFormat).timestamp()
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
                            message = userMessage.content
                            time = str(int(userTime) - 21600)
                            dataFormat = {
                                "guild_id": guild_id,
                                "channel_id": channel_id,
                                "message": message
                            }
                            if time in self.bot.scheduleData:
                                timeData = self.bot.scheduleData.get(time)
                                timeData.append(dataFormat)
                            else:
                                self.bot.scheduleData[time] = [dataFormat]
                                
                            Schedule.tb.update_one({"name": "scheduleTask"}, {"$set": self.bot.scheduleData})
                            await ctx.send("<:greentickbadge:852127602373951519> **Schedule message added successfully!!**")
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
        else:
            await ctx.send("Empty!!")
    
    @tasks.loop(seconds = 1)
    async def timeCheck(self):
        if len(self.bot.scheduleData) >= 1:
            
            timeFormat = "%d-%m-%y %H:%M:%S"
            
            now = datetime.now()
            
            dateTimeNow = str(int(now.timestamp()))


            if dateTimeNow in self.bot.scheduleData:
                for scheduleData in self.bot.scheduleData[dateTimeNow]:
                    guild_id = scheduleData.get("guild_id")
                    channel_id = scheduleData.get("channel_id")
                    message = scheduleData.get("message")
                        
                    guild = self.bot.get_guild(guild_id)
                    channel = guild.get_channel(channel_id)
                        
                    await channel.send(message)
                    
                self.bot.scheduleData.pop(dateTimeNow)
                Schedule.tb.update_one({"name": "scheduleTask"}, {"$set": self.bot.scheduleData})


def setup(bot):
    bot.add_cog(Schedule(bot))  