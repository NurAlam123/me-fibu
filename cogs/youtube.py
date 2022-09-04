import discord
from datetime import datetime as time
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from pyyoutube import Api
import os
import asyncio
import pymongo
from pytube import Channel

API_KEY = os.getenv("YT_API")

yt_api = Api(api_key=API_KEY)


class Youtube(commands.Cog):

    con_fibu = pymongo.MongoClient(os.getenv("DB"))
    db = con_fibu["fibu"]  # database
    tb = db["other_data"]

    def __init__(self, client):
        self.bot = client
        self.db()

        # self.yt_ch = "https://www.youtube.com/channel/UCfzA2NPW1UUm-Q6kpVkbN5w"
        # self.last_video_id = None
        self.check_video.start()

    # database
    def db(self):
        yt_db = Youtube.tb.find_one({"name": "youtube_notify"})
        data = yt_db.get("data")
        if not data:
            self.ytData = {}
        else:
            self.ytData = data

    # YouTube video search
    @commands.group(aliases=["youtube", "utube"], case_insensitive=True)
    async def yt(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    @yt.command(aliases=["vdo", "v"])
    async def video(self, ctx, *, query):
        yt_video = yt_api.search_by_keywords(
            q=query, safe_search="strict", search_type="video")
        if yt_video.items != []:
            limit = 10
            yt_url = "https://youtube.com/watch?v="
            video_urls = []
            for i in range(limit):
                video_id = yt_video.items[i].to_dict()['id']['videoId']
                video_url = yt_url+video_id
                video_urls.append(video_url)
            await ctx.message.add_reaction("\N{TELEVISION}")
            url_msg = await ctx.send(video_urls[0])
            page = 1
            pages = limit

            emojis = ["\N{Black Left-Pointing Triangle}",
                      "\N{Black Right-Pointing Triangle}"]

            last_page = False
            reverse = False
            out_emoji = False

            def reaction_check(reaction, user):
                return user.id == ctx.author.id and reaction.message.id == url_msg.id

            while True:
                if out_emoji:
                    pass
                elif page <= 1:
                    await url_msg.clear_reactions()
                    await url_msg.add_reaction(emojis[1])
                elif page >= pages:
                    await url_msg.clear_reactions()
                    await url_msg.add_reaction(emojis[0])
                else:
                    if not reverse:
                        if (page-1) <= 1 or last_page:
                            await url_msg.clear_reactions()
                            for emoji in emojis:
                                await url_msg.add_reaction(emoji)
                    else:
                        if last_page:
                            await url_msg.clear_reactions()
                            for emoji in emojis:
                                await url_msg.add_reaction(emoji)
                    if last_page:
                        last_page = False

                try:
                    reaction, user = await self.bot.wait_for("reaction_add", check=reaction_check, timeout=60)
                except asyncio.TimeoutError:
                    await url_msg.clear_reactions()
                    break

                if reaction.emoji == emojis[1] and page != pages:
                    page += 1
                    await url_msg.edit(content=video_urls[page-1])
                    await url_msg.remove_reaction(reaction, user)
                    reverse = False
                    out_emoji = False
                elif reaction.emoji == emojis[0] and page > 1:
                    page -= 1
                    await url_msg.edit(content=video_urls[page-1])
                    await url_msg.remove_reaction(reaction, user)
                    reverse = True
                    out_emoji = False
                    if page == pages-1:
                        last_page = True
                else:
                    out_emoji = True
                    await url_msg.remove_reaction(reaction, user)
        else:
            await ctx.message.add_reaction("<:wrong:846424916404207636>")
            msg = discord.Embed(title=":warning: Error :warning:",
                                description="Oops.. Not found any video..\nPlease search again by typing ```!fibu yt search <video name>```")
            await ctx.send(embed=msg)

# YouTube channel search
    @yt.command(aliases=["chnl", "c"])
    async def channel(self, ctx, *, query):
        yt_channel = yt_api.search_by_keywords(
            q=query, safe_search="strict", search_type="channel")
        if yt_channel.items != []:
            limit = 10
            yt_url = "https://youtube.com/channel/"
            channel_urls = [yt_url+yt_channel.items[i].to_dict()["id"]["channelId"]
                            for i in range(limit)]
            await ctx.message.add_reaction("\N{White Heavy Check Mark}")
            url_msg = await ctx.send(channel_urls[0])
            page = 1
            pages = limit

            emojis = ["\N{Black Left-Pointing Triangle}",
                      "\N{Black Right-Pointing Triangle}"]

            last_page = False
            reverse = False
            out_emoji = False

            def reaction_check(reaction, user):
                return user.id == ctx.author.id and reaction.message.id == url_msg.id

            while True:
                if out_emoji:
                    pass
                elif page <= 1:
                    await url_msg.clear_reactions()
                    await url_msg.add_reaction(emojis[1])
                elif page >= pages:
                    await url_msg.clear_reactions()
                    await url_msg.add_reaction(emojis[0])
                else:
                    if not reverse:
                        if (page-1) <= 1 or last_page:
                            await url_msg.clear_reactions()
                            for emoji in emojis:
                                await url_msg.add_reaction(emoji)
                    else:
                        if last_page:
                            await url_msg.clear_reactions()
                            for emoji in emojis:
                                await url_msg.add_reaction(emoji)
                    if last_page:
                        last_page = False

                try:
                    reaction, user = await self.bot.wait_for("reaction_add", check=reaction_check, timeout=60)
                except asyncio.TimeoutError:
                    await url_msg.clear_reactions()
                    break

                if reaction.emoji == emojis[1] and page != pages:
                    page = + 1
                    await url_msg.edit(content=channel_urls[page-1])
                    await url_msg.remove_reaction(reaction, user)
                    # page += 1
                    reverse = False
                    out_emoji = False
                elif reaction.emoji == emojis[0] and page > 1:
                    page -= 1
                    await url_msg.edit(content=channel_urls[page-1])
                    await url_msg.remove_reaction(reaction, user)
                    reverse = True
                    out_emoji = False
                    if page == pages-1:
                        last_page = True
                else:
                    out_emoji = True
                    await url_msg.remove_reaction(reaction, user)
        else:
            await ctx.message.add_reaction("<:wrong:846424916404207636>")
            msg = discord.Embed(title=":warning: Error :warning:",
                                description="Oops.. Not found the channel..\nPlease search again by typing ```!fibu yt channel <channel name>```")
            await ctx.send(embed=msg)
# YouTube channel notification

    @yt.group(aliases=["alert"], case_insensitive=True)
    async def notification(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    @notification.command()
    @has_permissions(administrator=True, manage_roles=True, manage_messages=True)
    async def add(self, ctx, channel_link: str = None, post_channel: discord.TextChannel = None, *, text: str = ""):

        # arguments error => channel_link and post_channel are require
        if not channel_link:
            await ctx.send("Provide the youtube channel link!")
        elif not post_channel:
            await ctx.send("Mention the discord channel where you want to get the notification message!")
        else:
            # get recent video
            channel_videos = Channel(channel_link).url_generator()
            try:
                first_video_id = str(
                    channel_videos.__next__()).split("?v=")[-1]
            except:
                first_video_id = None

            dataFormat = {
                "ytChannel": channel_link,
                "postChannel": str(post_channel.id),
                "textFormat": text,
                "lastVideoID": first_video_id
            }

            get_guild_data = self.ytData.get(f"{ctx.guild.id}")

            if not get_guild_data:
                self.ytData[f"{ctx.guild.id}"] = [dataFormat]
                self.tb.update_one({"name": "youtube_notify"}, {
                                   "$set": {"data": self.ytData}})

            else:
                self.ytData[f"{ctx.guild.id}"].append(dataFormat)
                self.tb.update_one({"name": "youtube_notify"}, {
                                   "$set": {"data": self.ytData}})

    async def send_message(self, ytLink: str, guildId: int, channelId: int, text: str):
        # guild = await self.bot.fetch_channel(guildId)
        channel = await self.bot.fetch_channel(channelId)
        await channel.send(f"{text}\n{ytLink}")

    @tasks.loop(seconds=600.0)
    async def check_video(self):
        guilds_data = self.ytData
        for guild_id in guilds_data:
            guild_data = guilds_data[guild_id]
            i = 0
            for data in guild_data:
                yt_channel = data.get("ytChannel")
                lastVideoID = data.get("lastVideoID")
                postChannel = data.get("postChannel")
                text = data.get("text")
                # get all videos of that channel
                channel_videos = Channel(yt_channel).url_generator()
                # get first videos of that channel and store video id
                try:
                    first_video_id = str(
                        channel_videos.__next__()).split("?v=")[-1]
                except:
                    first_video_id = None

                if not lastVideoID:
                    self.ytData[guild_id][i]["lastVideoID"] = first_video_id
                    self.tb.update_one({"name": "youtube_notify"}, {
                        "$set": {"data": self.ytData}})

                if (lastVideoID != first_video_id) and first_video_id:
                    ytLink = f"https://youtube.com/watch?v={first_video_id}"
                    await self.send_message(ytLink, guild_id, postChannel, text)

                    self.ytData[guild_id][i]["lastVideoID"] = first_video_id
                    self.tb.update_one({"name": "youtube_notify"}, {
                        "$set": {"data": self.ytData}})
                i += 1


def setup(bot):
    bot.add_cog(Youtube(bot))
