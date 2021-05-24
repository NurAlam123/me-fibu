import discord
from discord.ext import commands
from datetime import datetime as time
import wikipedia as wiki
import wikipediaapi as wikiapi
import asyncio
import math

class Wiki(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.wiki_content = {}
#wiki
    @commands.command(aliases=["wikipedia"])
    async def wiki(self, ctx, *, query):
        wikipedia = wikiapi.Wikipedia("en")
        page = wikipedia.page(query)
        result = page.summary[:450]
        if "may refer to" in result.lower():
            try:
                result = wiki.summary(query)
            except wiki.exceptions.DisambiguationError as e:
                self.wiki_content[ctx.author.id] = e.options # storing options and author id to execute select command
                options = [f"{i+1} • {e.options[i]}" for i in range(len(e.options))]
                await ctx.message.add_reaction("<:wrong:846424916404207636>")
                start = 0
                end = 10
                n = 10
                page = 1
                pages = math.ceil(len(options)/10)
                
                show = discord.Embed(title=f"Wikipedia | Page: {page}/{pages}", description="**Not found the page you are looking for. See the below list.**\n"+"\n".join(options[start:end]), color=0xffdf08, timestamp= time.now())
                show.add_field(name="Pick a index number reference to that title and send below command to search again!",value="Example: ```!fibu wiki select <index no>```")
                show.set_author(name=self.client.user.name, icon_url= self.client.user.avatar_url)
                show.set_footer(text="Programming Hero")
                msg = await ctx.send(embed = show)
                
                # reaction check 
                def re_check(reaction,user):
                    return user==ctx.author and reaction.message.id == msg.id
                
                emojis = ["\N{Black Left-Pointing Triangle}\ufe0f", "\N{Black Right-Pointing Triangle}\ufe0f"]
                last_page = False
                out_emoji = False
                reverse = False
                
                while True:
                    if out_emoji:
                        pass
                    elif page <= 1 or page <= 0:
                        await msg.clear_reactions()
                        await msg.add_reaction(emojis[1])
                    elif page >= pages:
                        await msg.clear_reactions()
                        await msg.add_reaction(emojis[0])
                    else:
                        if not reverse:
                            if (page-1)<=1 or last_page:
                                await msg.clear_reactions()
                                for emoji in emojis:
                                    await msg.add_reaction(emoji)
                        else:
                            if last_page:
                                await msg.clear_reactions()
                                for emoji in emojis:
                                    await msg.add_reaction(emoji)
                        if last_page:
                            last_page = False

                    try:
                        reaction, user = await self.client.wait_for("reaction_add", check=re_check, timeout=60)
                    except asyncio.TimeoutError:
                        options=[]
                        await msg.clear_reactions()
                        break
                    
                    if str(reaction.emoji)== emoji[1] and page!=pages:
                        page += 1
                        start = end
                        end += n

                        reverse = True
                        out_emoji = False

                        options_msg = discord.Embed(title=f"Wikipedia | Page: {page}/{pages}", description="\n".join(options[start:end]),color=0xffdf08, timestamp=time.now())
                        options_msg.add_field(name="Pick a number and send below command to search!",value="```!fibu wiki select [the number]```\nExample: ```!fibu wiki select 1```")
                        options_msg.set_author(name=self.client.user.name,icon_url=self.client.user.avatar_url)
                        options_msg.set_footer(text="Programming Hero")
                        await msg.edit(embed=options_msg)
                        await msg.remove_reaction(reaction,user)
                    
                    elif str(reaction.emoji)==emoji[0] and page > 1:
                        page -= 1
                        start = end
                        end -= n

                        reverse = False
                        out_emoji = False
                        if page == pages-1:
                            last_page = True

                        options_msg = discord.Embed(title=f"Wikipedia | Page: {page}/{pages}", description="\n".join(options[start:end]),color=0xffdf08, timestamp=time.now())
                        options_msg.add_field(name="Pick a number and send below command to select that title!",value="```!fibu wiki select [the number]```\nExample: ```!fibu wiki select 1```")
                        options_msg.set_author(name=self.client.user.name,icon_url=self.client.user.avatar_url)
                        options_msg.set_footer(text="Programming Hero")
                        await msg.edit(embed=options_msg)
                        await msg.remove_reaction(reaction,user)
                        
                    else:
                        out_emoji = True
                        await msg.remove_reaction(reaction, user)
                        
        elif result.strip() == "":
            await ctx.message.add_reaction("<:wrong:846424916404207636>")
            await ctx.send("No Page Found!!")
        else:
            await ctx.message.add_reaction("🔍")
            wiki_msg = discord.Embed(title= "Wikipedia", description=f"Showing result of **{page.title}**",color=0xffdf08,timestamp=time.now())
            try:
                wiki_msg.add_field(name= page.title, value=f"{result} ... [Read More]({page.fullurl})")
            except:
                wiki_msg.add_field(name= page.title, value=f"{result} ... [Read More]({page.canonicalurl})")
            wiki_msg.set_author(name= self.client.user.name,icon_url=self.client.user.avatar_url)
            wiki_msg.set_footer(text= "Programming Hero")
            await ctx.send(embed= wiki_msg)



#select options
    @wiki.command()
    async def select(self, ctx, index_no):
        if ctx.author.id in self.wiki_content.keys() and index_no.isnumeric():
            await ctx.message.add_reaction("🆗")
            query = self.wiki_content[ctx.author.id][int(index_no) - 1]
            await ctx.invoke(self.client.get_command("wiki"), query = query)
            
            


def setup(bot):
    bot.add_cog(Wiki(bot))