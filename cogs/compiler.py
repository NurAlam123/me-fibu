import discord
from discord.ext import commands

import requests
import os
import asyncio
from datetime import datetime as time

API = os.getenv("WANDBOX_API")

class Compiler(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self.all_compilers = self.get_data()

### get compiler data
    def get_data(self):
        res = requests.get(f"{API}/list.json")
        json_data = res.json()
        compilers = {}
        for data in json_data:
           language = data["language"].lower()
           compiler = data["name"].lower()
           if language not in compilers:
               compilers[language] = [compiler]
           else:
               compilers[language].append(compiler)
        return compilers

## check it's compiler or not
    def check_compiler(self, compiler):
        for i in self.all_compilers.values():
            if compiler in i:
                return True
                break
            else:
                continue

## get compiler name    
    def get_compiler(self, lang):
        short_names = {"py": "python", "js": "javascript", "ts": "typescript", "vim": "vim script"}
        if lang in short_names:
            lang = short_names[lang]

        if lang in self.all_compilers:
            compiler = self.all_compilers[lang][0]
            return compiler
        else:
            is_compiler = self.check_compiler(lang)
            if is_compiler:
                return lang
            else:
                return None     
        
## the compiler   
    def compiler(self, lang, code, user_input=""): 
        url = f"{API}/compile.json"
        data = {
            'code': code,
            'compiler': lang,
            'stdin': user_input 
            }
        res = requests.post(url, json=data)
        return res

## check message has user input or not    
    def has_user_input(self, message):
        message = message.lower()
        if message.strip().startswith("-i") or "-i" in message:
            return True
        else:
            return False

## extract user input form message
    def get_user_input(self, stdin):
        if stdin.strip().startswith("-i"):
            user_input = stdin.strip().lstrip("-i ")
            code = user_input.split("-c ")[1]
        elif "-i" in stdin:
            user_input = stdin.split("-i ")[1]
            try:
                code = stdin.split("-c ")[1].split("-i ")[0]
            except:
                code = None
            
        if "```" in user_input:
            user_input = user_input.lstrip("`\n").rstrip("\n")[:-3].strip("\n")
            return user_input, code
        else:
            return user_input.strip("\n"), code

## extract the code from message
    def get_code(self, code):
        all_code_lang = ['c', 'cpp', 'c++', 'c#', 'rill', 'erlang', 'elixir', 'haskell', 'd', 'java', 'rust', 'python', 'ruby', 'scala', 'groovy', 'javascript', 'coffeescript', 'swift', 'perl', 'php', 'lua', 'sql', 'pascal', 'lisp', 'vim script', 'ocaml', 'go', 'bash script', 'pony', 'crystal', 'nim', 'openssl', 'f#', 'cmake', 'r', 'typescript', 'julia', "py", "ts", "js", "vim"]
        code = code.lstrip("\n-c ").lstrip("\n`").rstrip("\n`")
        if code.split("\n")[0] in all_code_lang:
            code = code.lstrip(code.split("\n")[0])
            return code
        else:
            return code

## compile command
    @commands.command()
    async def compile(self, ctx, lang, *, msg= None):
        lang_com = ["lang", "langs", "language", "languages"] # language commands
        compiler_lang = self.get_compiler(lang)
        
        error = False
        if compiler_lang and lang not in lang_com:
            if '-c ' not in msg or '-i ' not in msg:
                if "```" in msg:
                    code = self.get_code(msg)
                    compile_code = self.compiler(compiler_lang, code).json()
                else:
                    compile_code = self.compiler(compiler_lang, msg).json()
            else:
                has_input = self.has_user_input(msg)
                if has_input:
                    user_input, code = self.get_user_input(msg)
                    if code and user_input:
                        code = self.get_code(code)
                        compile_code = self.compiler(compiler_lang, code, user_input).json()
                    else:
                        error = True
                else:
                    code = self.get_code(msg)
                    compile_code = self.compiler(compiler_lang, code).json()
                
            if not error:
                json_keys = compile_code.keys()
                compile_embed = discord.Embed(title= "Result", color= 0xdbca32, timestamp= time.now())
                ######### Embed Part ########
                compile_embed.add_field(name= "Status", value= f"Program finished with exit code: {compile_code.get('status')}") if 'status' in json_keys else None
                compile_embed.add_field(name= "Signal", value= compile_code.get("signal")) if "signal" in json_keys else None
                compile_embed.add_field(name= "Compiler Message", value= f"```\n{compile_code.get('compiler_message')}\n```") if "compiler_message" in json_keys else None
                compile_embed.add_field(name= "Program Message", value= f"```\n{compile_code.get('program_message')}\n```") if "program_message" in json_keys else None
                compile_embed.set_footer(text=f"Requested by {ctx.author} | Programming Hero")
                await ctx.send(embed= compile_embed)
            else:
                msg = discord.Embed(title= ":warning: Compiler Error :warning:", description= "Code is a required argument which isn't provided. Provide code and try again", color= 0xC70039)
                await ctx.send(embed= msg)   
           
        elif lang in lang_com:
            await ctx.invoke(self.bot.get_command("_lang"))
        else:
            msg = discord.Embed(title= ":warning: Compiler Error :warning:", description= "Unsupported programming language.\nType ```!fibu compile languages``` to see all supported programming languages.", color= 0xC70039)
            await ctx.send(embed= msg)

## all supported programming language
    @commands.command()
    async def _lang(self, ctx):
        all_langs = [f"{i}. {j}" for i, j in enumerate(self.all_compilers, 1)]
        n = 10
        start = 0
        end = n
        em_msg = discord.Embed(title= "Compiler Languages", description= '\n'.join(i for i in all_langs[start: end]), timestamp= time.now(), color= 0xffdf08)
        em_msg.set_footer(text= "Programming Hero")
        em_msg.set_author(name= self.bot.user.name, icon_url= self.bot.user.avatar_url)
        
        msg = await ctx.send(embed = em_msg)
        emojis = ["⬅️", "➡️️️"]
        last_page = False # to control last page emoji reaction
        
        page = 1
        pages = round(len(self.all_compilers)/n)
        
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
                reaction, user = await self.bot.wait_for("reaction_add", check = lambda re, user: user.id == ctx.author.id and re.message.id == msg.id and re.emoji in emojis, timeout= 60)
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                break
            if reaction.emoji == emojis[1]:
                page += 1
                start = end
                end += n
                edit_em_msg = discord.Embed(title= "Compiler Languages", description= '\n'.join(i for i in all_langs[start: end]), timestamp= time.now(), color= 0xffdf08)
                edit_em_msg.set_author(name= self.bot.user.name, icon_url= self.bot.user.avatar_url)
                edit_em_msg.set_footer(text="Programming Hero")
                await msg.edit(embed= edit_em_msg)
                await msg.remove_reaction(reaction, user)
                
            elif reaction.emoji == emojis[0]:
                page -= 1
                end = start
                start -= n
                if page == pages-1:
                    last_page = True
                edit_em_msg = discord.Embed(title= "Compiler Languages", description= '\n'.join(i for i in all_langs[start: end]), timestamp= time.now(), color= 0xffdf08)
                edit_em_msg.set_footer(text= "Programming Hero")
                edit_em_msg.set_author(name= self.bot.user.name, icon_url= self.bot.user.avatar_url)

                await msg.edit(embed= edit_em_msg)
                await msg.remove_reaction(reaction, user)
            else:
                pass

##### get all compilers of that language
    @commands.command()
    async def compilers(self, ctx, lang=None):
        if lang:
            isCompiler = self.check_compiler(lang)
            if isCompiler:
                await ctx.send("It's a compiler. Write the programming language name to get all compilers list")
            else:
                short_names = {"py": "python", "js": "javascript", "ts": "typescript", "vim": "vim script"}
                if lang in short_names:
                    lang = short_names[lang]
                    if lang in self.all_compilers:
                        lang_compilers = self.all_compilers[lang]
                    else:
                        await ctx.send("Type language name correctly!")
                else:
                    if lang in self.all_compilers:
                        lang_compilers = self.all_compilers[lang]
                    else:
                        await ctx.send("Type language name correctly!!")
                        
                        
                format_compilers = [f"{i}. {j}" for i,j in enumerate(lang_compilers, 1)]
                n = 10
                start = 0
                end = n
                em_msg = discord.Embed(title= f"{lang.capitalize()} Compilers", description= '\n'.join(i for i in format_compilers[start: end]), timestamp= time.now(), color= 0xffdf08)
                em_msg.set_footer(text= "Programming Hero")
                em_msg.set_author(name= self.bot.user.name, icon_url= self.bot.user.avatar_url)
                
                msg = await ctx.send(embed = em_msg)
                emojis = ["⬅️", "➡️️️"]
                last_page = False # to control last page emoji reaction
                
                page = 1
                pages = round(len(self.all_compilers)/n)
                
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
                        reaction, user = await self.bot.wait_for("reaction_add", check = lambda re, user: user.id == ctx.author.id and re.message.id == msg.id and re.emoji in emojis, timeout= 60)
                    except asyncio.TimeoutError:
                        await msg.clear_reactions()
                        break
                    if reaction.emoji == emojis[1]:
                        page += 1
                        start = end
                        end += n
                        edit_em_msg = discord.Embed(title= f"{lang.capitalize()} Compilers", description= '\n'.join(i for i in format_compilers[start: end]), timestamp= time.now(), color= 0xffdf08)
                        edit_em_msg.set_author(name= self.bot.user.name, icon_url= self.bot.user.avatar_url)
                        edit_em_msg.set_footer(text="Programming Hero")
                        await msg.edit(embed= edit_em_msg)
                        await msg.remove_reaction(reaction, user)
                        
                    elif reaction.emoji == emojis[0]:
                        page -= 1
                        end = start
                        start -= n
                        if page == pages-1:
                            last_page = True
                        edit_em_msg = discord.Embed(title= f"{lang.capitalize()} Compilers", description= '\n'.join(i for i in format_compilers[start: end]), timestamp= time.now(), color= 0xffdf08)
                        edit_em_msg.set_footer(text= "Programming Hero")
                        edit_em_msg.set_author(name= self.bot.user.name, icon_url= self.bot.user.avatar_url)
        
                        await msg.edit(embed= edit_em_msg)
                        await msg.remove_reaction(reaction, user)
                    else:
                        pass

        else:
            await ctx.send("Language is an required argument. Type the programming language name to get all compilers.")



                 


def setup(bot):
    bot.add_cog(Compiler(bot))