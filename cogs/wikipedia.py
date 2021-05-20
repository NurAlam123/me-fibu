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
#wiki
    @commands.group(case_insensitive = True)
    async def wiki(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    wiki_content = {}

    @wiki.command()
    async def search(self, ctx, *, query):
        wikipedia = wikiapi.Wikipedia("en")
        page = wikipedia.page(query)
        result = page.summary[:450]
        if "may refer to" in result.lower():
            try:
                result = wiki.summary(query)
            except wiki.exceptions.DisambiguationError as e:
                self.wiki_content[ctx.author.id] = e.options # storing options and author id to execute select command
                options = [f"{i+1} • {e.options[i]}" for i in range(len(e.options))]
                from_no = 0
                to_no = 10
                need_no = 10
                pages = math.ceil(len(options)/10)
                page_no = 1
                
                show = discord.Embed(title=f"Wikipedia | Page: {page_no}/{pages}", description="**Not found the page you are looking for. See the below list.**\n"+"\n".join(options[from_no:to_no]),color=0xffdf08, timestamp=time.now())
                show.add_field(name="Pick a number and send below command to search!",value="Example: ```!fibu wiki select 1```")
                show.set_author(name=self.client.user.name,icon_url=self.client.user.avatar_url)
                show.set_footer(text="Programming Hero")
                msg = await ctx.send(embed = show)
                # reaction check 
                def re_check(reaction,user):
                    return user==ctx.author and (str(reaction.emoji)) in emojis and reaction.message.id == msg.id
                emojis = ["◀️","▶️"]
                last_page = False
                while True:
                    if page_no <= 1:
                        await msg.clear_reactions() # remove reactions if exists
                        await msg.add_reaction(emojis[1]) # adding :arrow_forword:
                    elif page_no >= pages:
                        await msg.clear_reactions() # remove reactions if exists
                        await msg.add_reaction(emojis[0]) # adding :arrow_backword:
                    
                    else:
                        if page_no-1<=1 or last_page:
                            await msg.clear_reactions() # remove emoji if exists

                            for i in emojis:
                                await msg.add_reaction(i)
                            if last_page:
                                last_page = False
                    try:
                        reaction, user = await self.client.wait_for("reaction_add",check=re_check, timeout=60)
                    except asyncio.TimeoutError:
                        options=[]
                        await msg.clear_reactions()
                        break
                    if str(reaction.emoji)=="▶️" and page_no!=pages:
                        page_no += 1
                        from_no += need_no
                        to_no +=need_no
                        options_msg = discord.Embed(title=f"Wikipedia | Page: {page_no}/{pages}", description="\n".join(options[from_no:to_no]),color=0xffdf08, timestamp=time.now())
                        options_msg.add_field(name="Pick a number and send below command to search!",value="```!fibu wiki select [the number]```\nExample: ```!fibu wiki select 1```")
                        options_msg.set_author(name=self.client.user.name,icon_url=self.client.user.avatar_url)
                        options_msg.set_footer(text="Programming Hero")
                        await msg.edit(embed=options_msg)
                        await msg.remove_reaction(reaction,user)
                    elif str(reaction.emoji)=="◀️" and page_no > 1:
                        page_no -= 1
                        if page_no == pages-1:
                            last_page = True
                        from_no -= need_no
                        to_no -= need_no
                        options_msg = discord.Embed(title=f"Wikipedia | Page: {page_no}/{pages}", description="\n".join(options[from_no:to_no]),color=0xffdf08, timestamp=time.now())
                        options_msg.add_field(name="Pick a number and send below command to select that title!",value="```!fibu wiki select [the number]```\nExample: ```!fibu wiki select 1```")
                        options_msg.set_author(name=self.client.user.name,icon_url=self.client.user.avatar_url)
                        options_msg.set_footer(text="Programming Hero")
                        await msg.edit(embed=options_msg)
                        await msg.remove_reaction(reaction,user)
                        
                    else:
                        await msg.remove_reaction(reaction, user)
                        
        elif result.strip() == "":
            await ctx.message.add_reaction("🚫")
            await ctx.send("No Page Found!!")
        else:
            await ctx.message.add_reaction("🔍")
            wiki_msg = discord.Embed(title="Wikipedia", description=f"Showing result of **{page.title}**",color=0xffdf08,timestamp=time.now())
            try:
                wiki_msg.add_field(name=page.title,value=f"{result} ... [Read More]({page.fullurl})")
            except:
                wiki_msg.add_field(name=page.title,value=f"{result} ... [Read More]({page.canonicalurl})")
            wiki_msg.set_author(name=self.client.user.name,icon_url=self.client.user.avatar_url)
            wiki_msg.set_footer(text="Programming Hero")
            await ctx.send(embed=wiki_msg)



#select options
    @wiki.command()
    async def select(self, ctx, index_no):
        if ctx.author.id in self.wiki_content.keys() and index_no.isnumeric():
            await ctx.message.add_reaction("🆗")
            query = self.wiki_content[ctx.author.id][int(index_no) - 1]
            await ctx.invoke(self.client.get_command("wiki search"), query = query)
            
            


def setup(bot):
    bot.add_cog(Wiki(bot))