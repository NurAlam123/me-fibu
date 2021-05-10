import discord
from discord.ext import commands

import requests
import os
from datetime import datetime as time


class Compiler(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self.all_compilers = self.get_data()

### get compiler data
    def get_data(self):
        res = requests.get("https://wandbox.org/api/list.json")
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
        url = "https://wandbox.org/api/compile.json"
        data = {
            'code': code,
            'compiler': lang,
            'stdin': user_input 
            }
        res = requests.post(url, json=data)
        return res

## check message has user input or not    
    def has_user_input(self, message):
        if message.startswith("|"):
            return True
        elif message.startswith("`"):
            if len(message.split(r"`\n`")) <= 1:
                return True
        else:
            return False

## extract user input form message
    def get_user_input(self, stdin):
        if stdin.strip().startswith("|"):
            split_input = stdin.split("\n`")
            try:
                user_input = split_input[0]. replace("|", "", 1)
                code = split_input[1]
                return user_input, code
            except:
                return False
        elif stdin.strip().startswith("`"):
            try:
                user_input = stdin.split("```\n`")[0].lstrip("`\n")
                code = stdin.split(r"```\n`")[1]
                return user_input, code
            except:
                return False

## extract the code from message
    def get_code(self, code):
        all_code_lang = ['c', 'cpp', 'c++', 'c#', 'rill', 'erlang', 'elixir', 'haskell', 'd', 'java', 'rust', 'python', 'ruby', 'scala', 'groovy', 'javascript', 'coffeescript', 'swift', 'perl', 'php', 'lua', 'sql', 'pascal', 'lisp', 'vim script', 'ocaml', 'go', 'bash script', 'pony', 'crystal', 'nim', 'openssl', 'f#', 'cmake', 'r', 'typescript', 'julia', "py", "ts", "js", "vim"]
        code = code.lstrip("`\n").rstrip("\n`")

        if code.split("\n")[0] in all_code_lang:
            code = code.lstrip(i)
            return code
        else:
            return code

## compile command
    @commands.command()
    async def compile(self, ctx, lang, *, msg= None):
        lang_com = ["lang", "langs", "language", "languages"]
        lang = self.get_compiler(lang)
        
        if lang and lang not in lang_com:
            res = self.compiler(msg, lang)
            has_input = self.has_user_input(msg)
            if has_input:
                user_input, code = self.get_user_input(msg)
                code = self.get_code(code)
                compile_code = self.compiler(lang, code, user_input)
            else:
                code = self.get_code(code)
                compile_code = self.compiler(lang, code)
            
            status_code = compile_code.json()["status"]
            compile_output = compile_code.json()["compiler_message"]
            compile_embed = discord.Embed(title= "Result", color= 0xdbca32, timestamp= time.now())
            compile_embed.add_field(name= "Status", value= f"Program finished with exit code: {status}")
            compile_embed.add_field(name= "Program Output", value= f"```\n{compile_output}\n```")
            await ctx.send(embed= compile_embed)
            
            
        elif lang in lang_com:
            await ctx.invoke(self.client.get_command("_lang"))
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
        em_msg = discord.Embed(title= "Compiler Languages", description= all_langs[start: end], timestamp= time.now(), color= 0xffdf08)
        em_msg.set_footer(text= "Programming Hero")
        em_msg.set_author(name= self.client.user.name, icon_url= self.client.user.avatar_url)
        
        msg = await ctx.send(embed = em_msg)
        emojis = ["◀️", "▶️️"]
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
                reaction, user = await self.client.wait_for("reaction_add", check = lambda re, user: user.id == ctx.author.id and re.message.id == msg.id and re.emoji in emojis, timeout= 60)
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                break
            if reaction.emoji == emojis[1]:
                page += 1
                start = end
                end += n
                edit_em_msg = discord.Embed(title= "Compiler Languages", description= all_langs[start: end], timestamp= time.now(), color= 0xffdf08)
                edit_em_msg.set_author(name= self.client.user.name, icon_url= self.client.user.avatar_url)
                edit_em_msg.set_footer(text="Programming Hero")
                await msg.edit(embed= edit_em_msg)
                await msg.remove_reaction(reaction, user)
                
            elif reaction.emoji == emojis[0]:
                page -= 1
                end = start
                start -= n
                if page == pages-1:
                    last_page = True
                edit_em_msg = discord.Embed(title= "Compiler Languages", description= all_langs[start: end], timestamp= time.now(), color= 0xffdf08)
                edit_em_msg.set_footer(text= "Programming Hero")
                edit_em_msg.set_author(name= self.client.user.name, icon_url= self.client.user.avatar_url)

                await msg.edit(embed= edit_em_msg)
                await msg.remove_reaction(reaction, user)
            else:
                pass
        


def setup(bot):
    bot.add_cog(Compiler(bot))
    