import discord
from datetime import datetime as time
from discord.ext import commands
from pyyoutube import Api
import os
import asyncio

API_KEY = os.getenv("YT_API")

yt_api = Api(api_key=API_KEY)


class Youtube(commands.Cog):
    def __init__(self, client):
        self.bot = client

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
                    #page += 1
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


def setup(bot):
    bot.add_cog(Youtube(bot))
