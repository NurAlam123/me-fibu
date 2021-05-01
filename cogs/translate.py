import discord
from datetime import datetime as time
from discord.ext import commands
import translators as trans

class Translate(commands.Cog):
    def __init__(self,client):
        self.client = client
## Languages data
        self.supp_langs = {'Afrikaans': 'af', 'Albanian': 'sq', 'Amharic': 'am', 'Arabic': 'ar', 'Armenian': 'hy', 'Azerbaijani': 'az', 'Basque': 'eu', 'Belarusian': 'be', 'Bengali': 'bn', 'Bangla': 'bn', 'Bosnian': 'bs', 'Bulgarian': 'bg', 'Catalan': 'ca', 'Cebuano': 'ceb', 'Chinese': 'zh-CN', 'Chinese': 'zh', 'Chinese': 'zh-TW', 'Corsican': 'co', 'Croatian': 'hr', 'Czech': 'cs', 'Danish': 'da', 'Dutch': 'nl', 'English': 'en', 'Esperanto': 'eo', 'Estonian': 'et', 'Finnish': 'fi', 'French': 'fr', 'Frisian': 'fy', 'Galician': 'gl', 'Georgian': 'ka', 'German': 'de', 'Greek': 'el', 'Gujarati': 'gu', 'Haitian Creole': 'ht', 'Hausa': 'ha', 'Hawaiian': 'haw', 'Hebrew': 'he or iw', 'Hindi': 'hi', 'Hmong': 'hmn', 'Hungarian': 'hu', 'Icelandic': 'is', 'Igbo': 'ig', 'Indonesian': 'id', 'Irish': 'ga', 'Italian': 'it', 'Japanese': 'ja', 'Javanese': 'jv', 'Kannada': 'kn', 'Kazakh': 'kk', 'Khmer': 'km', 'Kinyarwanda': 'rw', 'Korean': 'ko', 'Kurdish': 'ku', 'Kyrgyz': 'ky', 'Lao': 'lo', 'Latin': 'la', 'Latvian': 'lv', 'Lithuanian': 'lt', 'Luxembourgish': 'lb', 'Macedonian': 'mk', 'Malagasy': 'mg', 'Malay': 'ms', 'Malayalam': 'ml', 'Maltese': 'mt', 'Maori': 'mi', 'Marathi': 'mr', 'Mongolian': 'mn', 'Myanmar': 'my', 'Nepali': 'ne', 'Norwegian': 'no', 'Nyanja': 'ny', 'Odia': 'or', 'Pashto': 'ps', 'Persian': 'fa', 'Polish': 'pl', 'Portuguese': 'pt', 'Punjabi': 'pa', 'Romanian': 'ro', 'Russian': 'ru', 'Samoan': 'sm', 'Scots Gaelic': 'gd', 'Serbian': 'sr', 'Sesotho': 'st', 'Shona': 'sn', 'Sindhi': 'sd', 'Sinhala': 'si', 'Slovak': 'sk', 'Slovenian': 'sl', 'Somali': 'so', 'Spanish': 'es', 'Sundanese': 'su', 'Swahili': 'sw', 'Swedish': 'sv', 'Tagalog': 'tl', 'Tajik': 'tg', 'Tamil': 'ta', 'Tatar': 'tt', 'Telugu': 'te', 'Thai': 'th', 'Turkish': 'tr', 'Turkmen': 'tk', 'Ukrainian': 'uk', 'Urdu': 'ur', 'Uyghur': 'ug', 'Uzbek': 'uz', 'Vietnamese': 'vi', 'Welsh': 'cy', 'Xhosa': 'xh', 'Yiddish': 'yi', 'Yoruba': 'yo', 'Zulu': 'zu'}

# check language supported or not
    def check_lang(self, lang):
        lang = lang.capitalize()
        if lang in self.supp_langs.keys():
            lang = self.supp_langs[lang]
        elif lang.lower() in self.supp_langs.values():
            lang = lang.lower()
        else:
            return None
        return lang

# translate
    @commands.command(aliases=["translate", "trans"])
    async def ts(self, ctx, lang, *, text = None):
        langs_com = ["langs", "languages", "language", "lang"]
        if lang.lower() not in langs_com and text!=None:
            lang = lang.split("|")
            from_lang = self.check_lang(lang[0].strip()) if lang[0].strip()!='' else 'auto'
            if lang[1].strip() != "":
                to_lang = self.check_lang(lang[1].strip())
                if from_lang != None and to_lang != None:
                    translation = trans.google(text,from_language=from_lang,to_language=to_lang)
                    msg = discord.Embed(title="Translator", color=0xffdf08)
                    msg.add_field(name="Word",value=f"{text.capitalize()}")
                    msg.add_field(name="Translation",value=f"{translation}")
                    await ctx.send(embed=msg)
                else:
                    msg = discord.Embed(title=":warning: Translation Error :warning:", description = "Unsupported language..\nType ```!fibu translate languages``` to see all supported language.", color=0xC70039)
                    await ctx.send(embed=msg)
                    
            else:
                msg = discord.Embed(title=":warning: Translation Error :warning:", description = "Type language correctly.\nDon\'t put space between languages.\nUse `|` to separate from and to languages.\nExample:\n `en|fr`", color=0xC70039)
                await ctx.send(embed=msg)
            
        elif text==None and lang.lower() not in langs_com:
            msg = discord.Embed(title=":warning: Translation Error :warning:", description = "Text is require to translate\nProvide the **text** that you want to translate", color=0xC70039)
            await ctx.send(embed=msg)
        else:
            await ctx.invoke(self.client.get_command("_languages"))
            
# show supported languages
    @commands.command()
    async def _languages(self, ctx):
        all_lang = [[i, j, self.supp_langs[j]] for i, j in enumerate(self.supp_langs, 1)]
        n = 10
        start = 0
        end = n
        the_table = self.make_table(all_lang[start: end])
        
        em_msg = discord.Embed(title = "Supported Languages", description = the_table, color = 0xffdf08, timestamp = time.now()) # the embed message
        em_msg.set_footer(text="Programming Hero")
        em_msg.set_author(name=self.client.user.name,icon_url=self.client.user.avatar_url)
        em_msg.set_footer(text="Programming Hero")
        msg = await ctx.send(embed = em_msg)
        emojis = ["⬅️", "➡️"]
        last_page = False # to control last page emoji reaction
        page = 1
        pages = round(len(self.supp_langs)/n)

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
                reaction, user = await self.client.wait_for("reaction_add", check = lambda re, user: user.id == ctx.author.id and re.message.id == msg.id and re.emoji in emojis, timeout=60)
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                break
            if reaction.emoji == emojis[1]:
                page += 1
                start = end
                end += n
                the_table = self.make_table(all_lang[start: end])
                edit_em_msg = discord.Embed(title = "Supported Languages", description = the_table, color = 0xffdf08, timestamp = time.now())
                edit_em_msg.set_author(name=self.client.user.name,icon_url=self.client.user.avatar_url)
                edit_em_msg.set_footer(text="Programming Hero")
                await msg.edit(embed=edit_em_msg)
                await msg.remove_reaction(reaction, user)
                
            elif reaction.emoji == emojis[0]:
                page -= 1
                end = start
                start -= n
                if page == pages-1:
                    last_page = True
                the_table = self.make_table(all_lang[start: end])
                edit_em_msg = discord.Embed(title = "Supported Languages", description = the_table, color = 0xffdf08, timestamp = time.now())
                edit_em_msg.set_footer(text="Programming Hero")
                edit_em_msg.set_author(name=self.client.user.name,icon_url=self.client.user.avatar_url)

                await msg.edit(embed=edit_em_msg)
                await msg.remove_reaction(reaction, user)
            else:
                pass


    def make_table(self, lang_list):
        
        sl_space = len(str(len(self.supp_langs)))+2
        lang_name_space = max([len(i) for i in self.supp_langs])+2
        iso_space = max([len(i) for i in self.supp_langs.values()])+2 # adding 2 for some space before and after the word

        header = "╔{0:═^{2}}╦{0:═^{3}}╦{0:═^{4}}╗\n\
║{1[0]:^{2}}║{1[1]:^{3}}║{1[2]:^{4}}║\n".format('', ['SL', 'Languages', 'ISO Code'], sl_space, lang_name_space, iso_space)

        main = ""
        for i in lang_list:
           main += "╠{4:═^{1}}╬{4:═^{2}}╬{4:═^{3}}╣\n\
║{0[0]:^{1}}║{0[1]:^{2}}║{0[2]:^{3}}║\n".format(i, sl_space, lang_name_space, iso_space, '')
            
        footer = "╚{0:═^{1}}╩{0:═^{2}}╩{0:═^{3}}╝".format('', sl_space, lang_name_space, iso_space)
        
        table = header + main + footer
        return f"```\n{table}\n```"






def setup(bot):
    bot.add_cog(Translate(bot))