import discord
import requests
import re
import asyncio
from discord.ext import commands

class Google(commands.Cog):
    def __init__(self, client):
        self.bot = client
    
    @commands.command(description = "Search anything.. Example: @google Elon Musk", aliese=["g","search","srch","go"])
    async def google(self, ctx, *, query = None):
        if query is None:
            await ctx.send("You haven’t enter any word or sentence to search") # if user didn't send any word or sentence to search
        else:
            await ctx.message.add_reaction("🔍")
            url = f"https://www.google.com/search?q={query}" # google search url
            res = requests.get(url)
            html = res.text
            find_link = re.findall(r"<a href=\"(\S+[a-zA-Z])\"",html) # finding all link from html document
            all_working_link = [] # storing all working links
            remove_first_map_url = True
    	    
            for link in find_link: # here starts the sorting process
                if link.startswith("/search") or link.startswith("/advanced_search") or link.startswith("/?s"):
    				# there are many links that didn't work so we don't need them.
                    pass
                elif link.startswith("https://maps"): # to get google maps
                    if remove_first_map_url:
                        remove_first_map_url=False # removed the first map url which is not work
                    else:
                        all_working_link.append(link) # added the link in all_working_link list
    					
                elif "https://account.google" in link or "https://www.google.com/search" in link:
                    ''' eliminate all link which start with "https://account.google" or "https://www.google.com/search" to get all perfect link '''
                    pass
                else:
                    split_link = link.split("&")[0] # splitted the exact link. which is in index 0
                    if split_link.startswith("/url?q="):
                        exact_link = requests.utils.unquote(split_link[7:])
                        ''' omitted "/urls?q=" from splitted link to get perfect link and unquoted to get more perfect link '''
                        all_working_link.append(exact_link) # adding it in all_working_link list
                    else:
                        all_working_link.append(requests.utils.unquote(split_link)) 
                        ''' if the link didn't start with "/urls?q=" then do above same process but here not omitted "/urls?q=" '''
            try:
                link_msg = await ctx.send(all_working_link[0]) #send the link
            except:
                await ctx.send("Page Not Found")
            
            def react_check(reaction, user): #reaction check function
                return user.id == ctx.author.id and reaction.message.id == link_msg.id and str(reaction.emoji) in emojis
    
            page = 0
            pages = len(all_working_link)
            
            clean_emoji = True
    
            while True: # looping between pages
                '''
                    Handle page by emoji if page is 0 the can't go backward and if page is the last page then can't go forward
                '''
                if page == 0:
                    if not clean_emoji:
                        for i in emojis:
                            await link_msg.clear_reaction(i) # remove emoji if exists

                    emojis = ["🚫","➡️"]
                    for emoji in emojis:
                        await link_msg.add_reaction(emoji) # add emoji to link_msg
				
                    clean_emoji = True
                    
                elif page == pages-1:
                    if not clean_emoji:
                        for i in emojis:
                            await link_msg.clear_reaction(i) # remove emoji if exists

                    emojis = ["⬅️","🚫"]
                    for emoji in emojis:
                        await link_msg.add_reaction(emoji)
                    
                    clean_emoji = True
                else:
                    if clean_emoji:
                        for i in emojis:
                            await link_msg.clear_reaction(i) # remove emoji if exists

                    emojis = ["⬅️","➡️"]
                    for emoji in emojis:
                        await link_msg.add_reaction(emoji)
				
                    clean_emoji = False
                
                try: # to handle timeout error
                    user_react,user = await self.bot.wait_for("reaction_add", check = react_check, timeout=60)
    				
                    if user_react.emoji == "➡️" and page != pages-1:
                        page += 1
                        await link_msg.edit(content = all_working_link[page])
                        await link_msg.remove_reaction(user_react, user)
    				
                    elif user_react.emoji == "⬅️" and page > 0:
                        page -= 1
                        await link_msg.edit(content = all_working_link[page])
                        await link_msg.remove_reaction(user_react, user)
    				
                    else:
                        await link_msg.remove_reaction(user_react,user)
                
                except asyncio.TimeoutError:
                    try:
                        for emoji in emojis:
                            await link_msg.clear_reaction(emoji)
                    except:
                        pass

def setup(bot):
    bot.add_cog(Google(bot))