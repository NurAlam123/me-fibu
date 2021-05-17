import discord
from datetime import datetime as time
from discord.ext import commands
from pyyoutube import Api
import os
import asyncio

API_KEY = os.getenv("YT_API")

yt_api = Api(api_key=API_KEY)

class Youtube(commands.Cog):
    def __init__(self,client):
        self.bot = client

## YouTube video search
    @commands.group(aliases=["youtube","utube"],case_insensitive=True)
    async def yt(self,ctx):
        if ctx.invoked_subcommand is None:
            pass
    @yt.command(aliases=["vdo", "v"])
    async def video(self,ctx,*,query):
        yt_video = yt_api.search_by_keywords(q = query, safe_search = "strict", search_type = "video")
        if yt_video != []:
            limit = 10
            yt_url = "https://youtube.com/watch?v="
            video_urls = []
            for i in range(limit):
                video_id = yt_video.items[i].to_dict()['id']['videoId']
                video_url = yt_url+video_id
                video_urls.append(video_url)
            await ctx.message.add_reaction("\N{TELEVISION}")
            page = 0
            url_msg = await ctx.send(video_urls[0])
            pages = limit
            
            emojis = ["\N{Black Left-Pointing Triangle}", "\N{Black Right-Pointing Triangle}"]
            last_page = False
            while True:
                if page == 0 and pages == 1:
                    pass
                elif page <= 0:
                    await url_msg.clear_reactions()
                    await url_msg.add_reaction(emojis[1])     
                elif page >= pages-1:
                    await url_msg.clear_reactions()
    
                    await url_msg.add_reaction(emojis[0])
                        
                else:
                    if page-1<=0 or last_page:
                        await url_msg.clear_reactions()   
                        
                        for emoji in emojis:
                            await url_msg.add_reaction(emoji)
                        if last_page:
                            last_page = False
                try:
                    user_react, user = await self.bot.wait_for("reaction_add", check = lambda re, user: user.id == ctx.author.id and re.message.id == url_msg.id and re.emoji in emojis, timeout=60)
                except asyncio.TimeoutError:
                        await url_msg.clear_reactions()
                        break
            				
                if page <= 0 and user_react.emoji == emojis[0] and user.id!=self.bot.user.id:
                    await url_msg.remove_reaction(user_react, user)
                elif page >= pages and user_react.emoji == emojis[1] and user.id!=self.bot.user.id:
                    await url_msg.remove_reaction(user_react, user)
                    
                elif user_react.emoji == emojis[1]:
                    page += 1
                    await url_msg.edit(content = video_urls[page])
                    await url_msg.remove_reaction(user_react, user)	
                elif user_react.emoji == emojis[0]:
                    page -= 1
                    if page==pages-1:
                        last_page = True
                    await url_msg.edit(content = video_urls[page])
                    await url_msg.remove_reaction(user_react, user)
            				
                else:
                    await url_msg.remove_reaction(user_react, user)
            else:
                await ctx.message.add_reaction("\N{CROSS MARK}")
                msg = discord.Embed(title="Error", description="Oops.. Not found the video..\nPlease search again by typing ```!fibu yt search <video name>```")
                await ctx.send(embed=msg)

## YouTube channel search
    @yt.command(aliases=["chnl", "c"])
    async def channel(self,ctx,*,query):
        yt_channel = yt_api.search_by_keywords(q = query, safe_search = "strict", search_type = "channel")
        if yt_channel != []:
            limit = 10
            yt_url = "https://youtube.com/channel/"
            channel_urls = [yt_url+yt_channel.items[i].to_dict()["id"]["channelId"] for i in range(limit)]
            await ctx.message.add_reaction("\N{White Heavy Check Mark}")
            page = 0
            url_msg = await ctx.send(channel_urls[0])
            pages = limit
            emojis = ["\N{Black Left-Pointing Triangle}", "\N{Black Right-Pointing Triangle}"]
            last_page = False
            while True:
                if pages == 1 and page == 1:
                    pass
                elif page <= 1:
                    await msg.clear_reactions()
                    await msg.add_reaction(emojis[1])
                elif page >= pages:
                    await msg.clear_reactions()
                    await msg.add_reaction(emojis[0])
                else:
                    if page - 1 <=1 or last_page:
                        await msg.clear_reactions()
                        for i in emojis:
                            await msg.add_reaction(i)
                        if last_page:
                            last_page = False
                try:
                    user_react, user = await self.bot.wait_for("reaction_add", check = lambda re, user: user.id == ctx.author.id and re.message.id == url_msg.id and re.emoji in emojis, timeout=60)
                except asyncio.TimeoutError:
                        await url_msg.clear_reactions()
                        break
            				
                if user_react.emoji == emojis[1]:
                    page += 1
                    await msg.edit(content= channel_urls[page])
                    await msg.remove_reaction(reaction, user)
                    
                elif reaction.emoji == emojis[0]:
                    page -= 1
                    if page == pages-1:
                        last_page = True
                    await msg.edit(content= channel_urls[page])
                    await msg.remove_reaction(reaction, user)
                else:
                    pass
            else:
                await ctx.message.add_reaction("\N{CROSS MARK}")
                msg = discord.Embed(title="Error", description="Oops.. Not found the channel..\nPlease search again by typing ```!fibu yt channel <channel name>```")
                await ctx.send(embed=msg)




def setup(bot):
    bot.add_cog(Youtube(bot))