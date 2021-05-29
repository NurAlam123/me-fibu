import discord
from discord.ext import commands

import requests
#import json
import os
import asyncio
import re
from datetime import datetime as time

API = os.getenv("COMPILER_API")

class Compiler(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self.all_languages = {}
        self.all_sup_lang = []
        self.data = {}
        self.need_edit = False
        self.find_code = re.compile(r'(?s)(?:edit_last_)?compile(?: +(?P<language>\S*)\s*|\s*)(?:\n'
    r'(?P<args>(?:[^\n\r\f\v]*\n)*?)\s*|\s*)'
    r'```(?:(?P<syntax>\S+)\n\s*|\s*)(?P<source>.*)```'
    r'(?:\n?(?P<stdin>(?:[^\n\r\f\v]\n?)+)+|)')
        self.get_data()

### get compiler data
    def get_data(self):
        res = requests.get(f"{API}/runtimes")
        json_data = res.json()
        for data in json_data:
           language = data["language"]
           version = data["version"]
           aliases = data["aliases"]
           if language.capitalize() not in self.all_sup_lang or language!="cpp":
               self.all_sup_lang.append(language.capitalize())
           self.all_languages[language] = language
           for alias in aliases:
               self.all_languages[alias] = language

        
## the compiler   
    def compiler(self, lang, code, args, user_input=""): 
        url = f"{API}/execute"
        data = {
            'language': lang,
            'version': '*',
            'args': args,
            'files':[{'content': code}],
            'stdin': user_input,
            'log': 0
            }
        try:
            res = requests.post(url, json=data)
            return res
        except:
            return

## compile command
    @commands.group()
    async def compile(self, ctx):
        if ctx.invoked_subcommand is None:
            msg = None
        ### loading gif reaction ####
            await ctx.message.clear_reactions()
            await ctx.message.add_reaction("<:loading:846416824903270420>")
            await asyncio.sleep(2)
            
            match = self.find_code.search(ctx.message.content)
            if not match:
                pass
            lang_error = False
            code_error = False
            try:
                lang, args, syntax, code, stdin = match.groups()
            except Exception as e:
                #receiver = await self.bot.fetch_user(838836138537648149)
                #await receiver.send(f'Exception in compile command: {e}')
                code_error = True
            if not code_error:
                if not lang:
                    lang = syntax
                if lang:
                    lang = lang.lower()
                if lang not in self.all_languages:
                    lang_error = True
                if code=="" or code==None:
                    code_error = True
    
            if not lang_error and not code_error:
                    lang = self.all_languages[lang]
                    compile_response = self.compiler(lang, code, args, stdin)
                    if compile_response:
                        
            ########## Embed Part #########
                        output = None
                        error = None
                        status_code = None
                        if compile_response.status_code == 200:
                            compile_code = compile_response.json().get('run')
                            compile_embed = discord.Embed(title= f"{lang.capitalize()} Compilation Results", color= 0xdbca32, timestamp= time.now())
                            if len(compile_code.get('stderr')) != 0:
                                await ctx.message.clear_reactions()
                                await ctx.message.add_reaction("<:wrong:846424916404207636>")
                                if compile_response.json().get("compile"):
                                    compiler = compile_response.json()['compile']
                                    error = compiler['output']
                                    status_code = compiler.get("code") if compiler.get("code") else None
                                else:
                                    error = compile_code.get('stderr')
                                
                            elif compile_code.get('output')!=None:
                                await ctx.message.clear_reactions()
                                await ctx.message.add_reaction("\N{White Heavy Check Mark}")
                                if compile_code.get("code"):
                                    status_code = compile_code.get('code')
                                else:
                                    status_code = None
                                output = compile_code.get('output')
                                output = discord.utils.escape_mentions(output)
                                output = output.replace("`", "`\u200b")
                                if output.__len__() >= 2000:
                                    output = output[:1000]
                                elif output.__len__() <= 0:
                                    output = 'No output found'
                            else:
                                pass
                            if self.need_edit and ctx.author.id in self.data:
                                self.need_edit = False
                                compile_embed.add_field(name= f"Status Code", value=f"```\nPrograme finished with status code {status_code}\n```") if (status_code or status_code == 0) else None
                                compile_embed.add_field(name= f"Output", value=f"```\n{output}\n```") if output else None
                                compile_embed.add_field(name= f"Error", value=f"```\n{error}\n```") if error else None
                                compile_embed.set_footer(text=f"{ctx.author} |")
                                embed_message = await ctx.fetch_message(self.data.get(ctx.author.id))
                                compile_msg = await embed_message.edit(embed= compile_embed)
                            else:
                                compile_embed.add_field(name= f"Status Code", value=f"```\nPrograme finished with status code {status_code}\n```") if (status_code or status_code == 0) else None
                                compile_embed.add_field(name= f"Output", value=f"```\n{output}\n```") if output else None
                                compile_embed.add_field(name= f"Error", value=f"```\n{error}\n```") if error else None
                                compile_embed.set_footer(text=f"{ctx.author} |")
                                compile_msg = await ctx.reply(embed= compile_embed, mention_author=True)
           
           ########## Error Part ############
                        else:
                            await ctx.message.clear_reactions()
                            await ctx.message.add_reaction("<:wrong:846424916404207636>")
                            msg = discord.Embed(title= ":warning: Compiler Error :warning:", description= f"Something went wrong!:(\nStatus: {compile_response.json()['message']}", color= 0xC70039)
                            await ctx.reply(embed= msg, mention_author=True)
                    else:
                        await ctx.message.clear_reactions()
                        await ctx.message.add_reaction("<:wrong:846424916404207636>")
                        msg = discord.Embed(title= ":warning: Compiler Error :warning:", description= "Something went wrong\nType ```!fibu help compile``` for help or try again after sometime.", color= 0xC70039)
                        await ctx.reply(embed= msg, mention_author=True)
                        
            elif code_error:
                        await ctx.message.clear_reactions()
                        await ctx.message.add_reaction("<:wrong:846424916404207636>")
                        msg = discord.Embed(title= ":warning: Compiler Error [Code block not found] :warning:", description= "Write your code inside code block.\nUse **```** before and after your code.\n__For Example:__\n", color= 0xC70039)
                        msg.set_image(url="https://is.gd/ea7N4q")
                        await ctx.reply(embed= msg, mention_author=True)
            elif lang_error:
                await ctx.message.clear_reactions()
                await ctx.message.add_reaction("<:wrong:846424916404207636>")
                msg = discord.Embed(title= ":warning: Compiler Error :warning:", description= "Unsupported programming language.\nType ```!fibu compile languages``` to see all supported programming languages.", color= 0xC70039)
                await ctx.reply(embed= msg, mention_author=True)
            else:
                await ctx.message.clear_reactions()
                await ctx.message.add_reaction("<:wrong:846424916404207636>")
                msg = discord.Embed(title= ":warning: Compiler Error :warning:", description= "Something went wrong\nType ```!fibu help compile``` for help or try again after sometime.", color= 0xC70039)
                await ctx.reply(embed= msg, mention_author=True)
            
            ########## message data store #########
            if msg:
                try:
                    self.data[ctx.author.id] = msg.id
                except Exception as e:
                    #receiver = await self.bot.fetch_user(838836138537648149)
                    #await receiver.send(f'Exception in compile msg: {e}')
                    pass
            elif compile_msg:
                try:
                    self.data[ctx.author.id] = compile_msg.id
                except:
                    pass
                
            
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.bot:
            return
        if before.author.id in self.data:
            prefixes = await self.bot.get_prefix(after)
            if isinstance(prefixes, str):
                prefixes = [prefixes, ]
            for prefix in prefixes:
                if after.content.lower().startswith(f'{prefix}compile'):
                    after.content = after.content.replace(f'{prefix}compile', f'{prefix}compile')
                    self.need_edit = True
                    await self.bot.process_commands(after)
                    break

## all supported programming language
    @compile.command(aliases=["language", "languages", "langs"])
    async def lang(self, ctx):
        message_content = []
        for i, j in enumerate(sorted(self.all_sup_lang), 1):
            page_format = f"{i}. {j}"
            message_content.append(page_format)
        per_page = 10
        start = 0
        end = per_page
        page = 1
        pages = round(len(message_content)/per_page)

        em_msg = discord.Embed(title= "Compiler Languages", description= '\n'.join(i for i in message_content[start: end]), timestamp= time.now(), color= 0xffdf08)
        em_msg.set_footer(text= f"Page: {page}/{pages} | Programming Hero")
        em_msg.set_author(name= self.bot.user.name, icon_url= self.bot.user.avatar_url)
        
        msg = await ctx.send(embed = em_msg)
       ####### Paginator ######### 
        emojis = ["\N{Black Left-Pointing Triangle}\ufe0f", "\N{Black Right-Pointing Triangle}\ufe0f"]
        last_page = False # to control last page emoji reaction
        reverse = False # to control page that goes reverse
        out_emoji = False # to control emojis which is not in emojis
        
        def reaction_check(reaction, user):
            return user.id == ctx.author.id and reaction.message.id == msg.id
        
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
                reaction, user = await self.bot.wait_for("reaction_add", check = reaction_check, timeout= 60)
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                break
            
            if reaction.emoji == emojis[1] and page!=pages:
                page += 1
                start = end
                end += per_page
                reverse = False
                out_emoji = False
                edit_em_msg = discord.Embed(title= "Compiler Languages", description= '\n'.join(i for i in message_content[start: end]), timestamp= time.now(), color= 0xffdf08)
                edit_em_msg.set_author(name= self.bot.user.name, icon_url= self.bot.user.avatar_url)
                edit_em_msg.set_footer(text= f"Page: {page}/{pages} | Programming Hero")
                await msg.edit(embed= edit_em_msg)
                await msg.remove_reaction(reaction, user)
                
            elif reaction.emoji == emojis[0] and page > 1:
                page -= 1
                end = start
                start -= per_page
                reverse = True
                out_emoji = False
                if page == pages-1:
                    last_page = True
                edit_em_msg = discord.Embed(title= "Compiler Languages", description= '\n'.join(i for i in message_content[start: end]), timestamp= time.now(), color= 0xffdf08)
                edit_em_msg.set_footer(text= f"Page: {page}/{pages} | Programming Hero")
                edit_em_msg.set_author(name= self.bot.user.name, icon_url= self.bot.user.avatar_url)

                await msg.edit(embed= edit_em_msg)
                await msg.remove_reaction(reaction, user)
            else:
                out_emoji = True
                await msg.remove_reaction(reaction, user)

def setup(bot):
    bot.add_cog(Compiler(bot))