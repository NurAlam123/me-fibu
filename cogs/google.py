import discord
import requests
import re
import asyncio
from discord.ext import commands
from bs4 import BeautifulSoup

class Google(commands.Cog):
    def __init__(self, client):
        self.bot = client
    
    @commands.command(aliases=["g","search","srch","go"])
    async def google(self, ctx, *, query = None):
        if query is None:
            await ctx.send("You haven’t enter any word or sentence to search") # if user didn't send any word or sentence to search
        else:
            await ctx.message.add_reaction("🔍")
            url = f"https://www.google.com/search?q={query}&safe=active" # google search url
            res = requests.get(url)
            html = res.text
            soup = BeautifulSoup(html, "lxml")
            all_anchor_tag = soup.find_all("a") # finding all anchor tag from html
            links = []    	    
            for a in all_anchor_tag: # here starts the sorting process
                link = a["href"]
                if link.startswith("/url?q="):
    				# omitting /url?q= from link to get working link
                    link = link.split("/url?q=")[1].split("&")[0] # working link
                    if "https://" in link and ".google" not in link: #finding perfect link
                        link = link.split("&")[0]
                        links.append(link)
                    else:
                        split_link = link.split("&")[0] # splitted the exact link. which is in index 0
                        if split_link.startswith("/url?q="):
                            exact_link = requests.utils.unquote(split_link[7:])
                            ''' omitted "/urls?q=" from splitted link to get perfect link and unquoted to get more perfect link '''
                            links.append(exact_link) # adding it in links list
                        else:
                            links.append(requests.utils.unquote(split_link)) 
                            ''' if the link didn't start with "/urls?q=" then do above same process but here not omitted "/urls?q=" '''
            try:
                link_msg = await ctx.send(links[0]) #send the link
            
                def react_check(reaction, user): #reaction check function
                    return user.id == ctx.author.id and reaction.message.id == link_msg.id
        
                page = 0
                pages = len(links)
                
                emojis = ["\N{Black Left-Pointing Triangle}\ufe0f", "\N{Black Right-Pointing Triangle}\ufe0f"]
                last_page = False # to control last page emoji reaction
                reverse = False # to control page that goes reverse
                out_emoji = False # to control emojis which is not in emojis

                while True: # looping between pages
                    '''
                        Handle page by emoji if page is 0 then can't go backward and if page is the last page then can't go forward
                    '''
                    if out_emoji:
                        pass
                    elif page <= 1 or page <= 0:
                        await link_msg.clear_reactions()
                        await link_msg.add_reaction(emojis[1])
                    elif page >= pages:
                        await link_msg.clear_reactions()
                        await link_msg.add_reaction(emojis[0])
                    else:
                        if not reverse:
                            if (page-1)<=1 or last_page:
                                await link_msg.clear_reactions()
                                for emoji in emojis:
                                    await link_msg.add_reaction(emoji)
                        else:
                            if last_page:
                                await link_msg.clear_reactions()
                                for emoji in emojis:
                                    await link_msg.add_reaction(emoji)
                        if last_page:
                            last_page = False
                    try: # to handle timeout error
                        reaction, user = await self.bot.wait_for("reaction_add", check = react_check, timeout=60)
                    except asyncio.TimeoutError:
                        await link_msg.clear_reactions()
                        break
        				
                    if reaction.emoji == emojis[1] and page!=pages:
                        page += 1
                        reverse = False
                        out_emoji = False
                        await link_msg.edit(content= links[page])
                        await link_msg.remove_reaction(reaction, user)
                        
                    elif reaction.emoji == emojis[0] and page > 1:
                        page -= 1
                        reverse = True
                        out_emoji = False
                        await link_msg.edit(content= links[page])
                        await link_msg.remove_reaction(reaction, user)
                        if page == pages-1:
                            last_page = True
                     else:
                        out_emoji = True
                        await msg.remove_reaction(reaction, user)
            except:
                await ctx.send("404 Page Not Found!!")

def setup(bot):
    bot.add_cog(Google(bot))