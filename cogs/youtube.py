import discord
from datetime import datetime as time
from discord.ext import commands
from pyyoutube import Api
import re

API_KEY = "AIzaSyD-a3dlY_KYsKOiv1pIvQV44yPTQqKoJZk"

yt_api = Api(api_key=API_KEY)

class Youtube(commands.Cog):
    def __init__(self,client):
        self.client = client
#youtube
    @commands.group(aliases=["youtube","utube"],case_insensitive=True)
    async def yt(slef,ctx):
        if ctx.invoked_subcommand is None:
            pass
    @yt.command(aliases=["video", "vdo", "v", "srch", "search"])
    async def video(self,ctx,*,query):
        yt_video = yt_api.search_by_keywords(q = query, safe_search = "strict", search_type = "video")
        if yt_video != []:
            limit = 10
            yt_url = "https://youtube.com/watch?v="
            videos_urls = [yt_url+video["id"]["videoId"] for video in yt_video.items[:limit]]
            await ctx.message.add_reaction("📺")
            page = 0
            url_msg = await ctx.send(video_urls[0])
            pages = limit
            emojis = ["⏪","⏩️"]
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
                    user_react, user = await self.bot.wait_for("reaction_add", check = react_check, timeout=60)
                except asyncio.TimeoutError:
                        await url_msg.clear_reactions()
                        break
            				
                if user_react.emoji == emojis[1] and page != pages-1:
                    page += 1
                    await url_msg.edit(content = video_urls[page])
                    await url_msg.remove_reaction(user_react, user)	
                elif user_react.emoji == emojis[0] and page > 0:
                    page -= 1
                    if page==pages-1:
                        last_page = True
                        await url_msg.edit(content = video_urls[page])
                        await url_msg.remove_reaction(user_react, user)
            				
                    else:
                        await url_msg.remove_reaction(user_react,user)
            else:
                await ctx.message.add_reaction("❌")
                msg = discord.Embed(title="Error", description="Oops.. Not found the video..\nPlease search again by typing ```!fibu yt search <video name>```")
                await ctx.send(embed=msg)


    @yt.command(aliases=["chnl", "c"])
    async def channel(self,ctx,*,query):
        yt_video = yt_api.search_by_keywords(q = query, safe_search = "strict", search_type = "channel")
        if yt_video != []:
            limit = 10
            yt_url = "https://youtube.com/channel/"
            videos_urls = [yt_url+video["id"]["channelId"] for video in yt_video.items[:limit]]
            await ctx.message.add_reaction("✅")
            page = 0
            url_msg = await ctx.send(video_urls[0])
            pages = limit
            emojis = ["⏪","⏩️"]
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
                    user_react, user = await self.bot.wait_for("reaction_add", check = react_check, timeout=60)
                except asyncio.TimeoutError:
                        await url_msg.clear_reactions()
                        break
            				
                if user_react.emoji == emojis[1] and page != pages-1:
                    page += 1
                    await url_msg.edit(content = video_urls[page])
                    await url_msg.remove_reaction(user_react, user)	
                elif user_react.emoji == emojis[0] and page > 0:
                    page -= 1
                    if page==pages-1:
                        last_page = True
                        await url_msg.edit(content = video_urls[page])
                        await url_msg.remove_reaction(user_react, user)
            				
                    else:
                        await url_msg.remove_reaction(user_react,user)
            else:
                await ctx.message.add_reaction("❌")
                msg = discord.Embed(title="Error", description="Oops.. Not found the channel..\nPlease search again by typing ```!fibu yt channel <channel name>```")
                await ctx.send(embed=msg)




def setup(bot):
    bot.add_cog(Youtube(bot))
    
