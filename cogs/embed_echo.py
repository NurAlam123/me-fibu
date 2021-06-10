import discord
from discord.ext import commands

import re
import os
import json
import asyncio
import typing
from datetime import datetime as time

class EmbedEcho(commands.Cog):
    def __init__(self, client):
        self.bot = client
    
    def build_embed(self, source):
        embed_dict = json.loads(source)
        embed_keys = embed_dict.keys()
        
        error = None
        embed = discord.Embed()
        embed.title = embed_dict.get('title')
        embed.description= embed_dict.get('description')
        if 'color' in embed_keys or 'colour' in embed_keys:
            embed_color = embed_dict.get('color')
            if not embed_color:
                embed_color = embed_dict.get('colour')
            if type(embed_color) == str:
                if embed_color.startswith('#'): # convert color from hex value
                    embed_color = int(f'0x{embed_color.strip("#").strip()}', 16)
                elif embed_color.startswith('rgb'): # convert color from rgb value
                    color = embed_color.strip('rgb').strip().strip('(').strip(')').split(',')
                    color = tuple(map(int, color))
                    color = str(discord.Colour.from_rgb(color[0], color[1], color[2]))
                    embed_color = int(f'0x{color.strip("#").strip()}', 16)
            embed.color = embed_color
        if 'author' in embed_keys:
            author_field = embed_dict.get('author')
            if 'name' in author_field:
                name = author_field.get('name')
            else:
                name = ''
            url = author_field.get('url') if 'url' in author_field else discord.Embed.Empty
            icon_url = author_field.get('icon_url') if 'icon_url' in author_field else discord.Embed.Empty
            
            embed.set_author(name= name, url= url, icon_url= icon_url)
        if 'type' in embed_keys:
            embed_type = embed_dict.get('type')
            embed.type = embed_type
        if 'footer' in embed_keys:
            footer_field = embed_dict.get('footer')
            text = footer_field.get('text') if 'text' in footer_field else discord.Embed.Empty
            icon_url = footer_field.get('icon_url') if 'icon_url' in footer_field else discord.Embed.Empty
       
        if 'thumbnail' in embed_keys:
            thumbnail_url = embed_dict.get('thumbnail')
            #print(thumbnail_url)
            embed.set_thumbnail(url= thumbnail_url)
        if 'image' in embed_keys:
            image_url = embed_dict.get('image')
            embed.set_image(url= image_url)
        if 'fields' in embed_keys:
            fields = embed_dict.get('fields')
            for field in fields:
                if 'name' in field:
                    name = field.get('name')
                if 'value' in field:
                    value = field.get('value')
                if 'inline' in field:
                    inline = field.get('inline')
                else:
                    inline= False
                if 'name' not in field and 'value' not in field:
                    pass
                else:
                    embed.add_field(name= name, value= value, inline= inline)
        if 'url' in embed_keys:
            url = embed_dict.get('url')
            embed.url = url
        
        
        if 'plainText' in embed_keys:
                text = embed_dict.get('plainText')
        elif 'content' in embed_keys:
                text = embed_dict.get('content')
        elif 'message' in embed_keys:
                text = embed_dict.get('message')
        else:
                text = None
        
        return embed, text
    
    
    @commands.command(aliases= ['echoEm'])
    @commands.guild_only()
    @commands.has_permissions(administrator= True, manage_messages= True, manage_guild= True)
    async def echoEmbed(self, ctx, channel: typing.Optional[discord.TextChannel], *, embed_obj= None):
        if not channel:
            channel = ctx.channel
        
        attachments = ctx.message.attachments
        if not embed_obj and attachments:
            for attachment in attachments:
                if attachment.content_type == 'application/json; charset=utf-8' or attachment.content_type == 'text/plain; charset=utf-8':
                    embed_obj = await attachment.read()
                    embed_obj = embed_obj.decode('utf-8')
                    break
        if embed_obj:
            embed_obj = embed_obj.replace("'", '"') # replace single quote (') to double quote (")
            
            if embed_obj.startswith('`') and embed_obj.endswith('`'):
                embed_obj = embed_obj.lstrip('`').rstrip('`')
                if embed_obj.startswith('json\n'):
                    embed_obj = embed_obj.lstrip('json\n')
            if embed_obj.lstrip('{').rstrip('}').strip()=='':
                await ctx.send('You have provided an empty embed object')
            else:
                
                em_msg, text = self.build_embed(embed_obj)
                await ctx.send(content= text, embed= em_msg)
        else:
            await ctx.send('You didn\'t provide any Embed Object or JSON Object to build the embed.\nYou can also write Embed Object or JSON Object in a json or text file and send it to build the embed!!')

    @commands.command('editEm')
    @commands.guild_only()
    @commands.has_permissions(administrator= True, manage_messages= True, manage_guild= True)
    async def editEmbed(self, ctx, message: discord.Message):

        if message.author.id != self.bot.user.id:
            await ctx.send('This is not my message so I can\'t edit it')
        else:
            embeds = message.embeds
            no = 1
            nth = {
                1: 'st',
                2: 'nd',
                3: 'rd'
            }
            cancelled = False
            for embed in embeds:
                try:
                    embed_source = json.dumps(embed.to_dict(), indent= 4)
                    file = False
                    if len(embed_source) >= 1900:
                        with open(f'{ctx.message.id}.json', 'w') as embed_file:
                            embed_file.write(embed_source)
                        embed_file.close()
                        file = True
                    else:
                        file = False
                except Exception as e:
                    print(f'error {e}')
                    break
                else:
                    if file:
                        with open(f'{ctx.message.id}.json', 'r') as file:
                            source_msg = await ctx.send(file= discord.File(file, 'embed.json'))
                        file.close()
                        os.remove(f'{ctx.message.id}.json')
                    else:
                        source_msg = await ctx.send(f'```json\n{embed_source}\n```')
                        
                    if len(embeds) <= 1:
                        msg = '\N{White Small Square}\ufe0f Here is the json object of that embed.\n\N{White Small Square}\ufe0f Just edit it or replace by another embed json object and send it.\n\N{White Small Square}\ufe0f To cancel the process send \'cancle\'!!'
                    else:
                        if no in nth.keys():
                            suffix = nth[no]
                        else:
                            suffix = 'th'
                        msg = f'\N{White Small Square}\ufe0f Here is the json object of {no}{suffix} embed.\nJust copy and edit it or replace by another embed json object and send it.\n\N{White Small Square}\ufe0f Type \'skip\' to skip this embed and go next\n\N{White Small Square}\ufe0f Type \'cancle\' to cancel process!!'
                    await source_msg.reply(msg)
                    while True:
                        replace_msg = await self.bot.wait_for('message', check= lambda msg: msg.author.id==ctx.author.id)
                        attachments = replace_msg.attachments
                        if replace_msg.content.lstrip('{').rstrip('}').strip()=='' and not attachments:
                            await ctx.send('Empty Embed Object...\nFix it and resend again or send \'cancle\' to cancel the process!!')

                        elif replace_msg.content.lower().strip() == 'cancle':
                            await ctx.send('Editing process has been cancelled!!')
                            cancelled = True
                            break
                        elif replace_msg.content.lower().strip() == 'skip':
                            await ctx.send('Skipped!!')
                            break
                        else:
                            if replace_msg.content.startswith('{') and replace_msg.content.endswith('}') or attachments:
                                for attachment in attachments:
                                    if attachment.content_type == 'application/json; charset=utf-8' or attachment.content_type == 'text/plain; charset=utf-8':
                                        embed_obj = await attachment.read()
                                        embed_obj = embed_obj.decode('utf-8')
                                        break
                                    else:
                                        await ctx.send('It\'s not a json or text file!!\nPlease rename it and send again or send \'cancle\' to cancel the process!!')
                                else:
                                    embed_obj = replace_msg.content
                                    
                                    
                                em_msg, text = self.build_embed(embed_obj)
                                    
                                await message.edit(content= text, embed= em_msg)
                                await ctx.send('Embed successfully edited!!')
                                break
                            else:
                                await ctx.send('It\'s not a correct json format!!\nSend correct format again or send \'cancle\' to cancle the process!!')
                        
                    if cancelled:
                        break

    ######## Command Error ########
    @echoEmbed.error
    async def _error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            arg_name = error.param.name
            if arg_name == 'embed_obj':
                await ctx.send(f'Please provide an Embed Object or JSON Object to build the embed!!')
        elif isinstance(error, commands.CommandInvokeError):
            if isinstance(error.__cause__, json.JSONDecodeError):
                await ctx.send('You have provided an invalid Embed Object or JSON Object!!')
            elif isinstance(error.__cause__, discord.HTTPException):
                await ctx.send(f'{error.__cause__.text}')
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send(error)
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
        else:
            await ctx.send(error)
        #raise error
            
            
    @editEmbed.error
    async def _error(self, ctx, error):
        if isinstance(error, commands.MessageNotFound):
            await ctx.send(f'Not found any message that associated with the message id in this server!')
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send(error)
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
        elif isinstance(error, commands.MissingRequiredArgument):
            arg_name = error.param.name
            if arg_name == 'message':
                await ctx.send(f'Please provide a embed message id that I have to edit!!')
        elif isinstance(error, commands.CommandInvokeError):
            if isinstance(error.__cause__, json.JSONDecodeError):
                await ctx.send('You have provided an invalid Embed Object or JSON Object!!')
            elif isinstance(error.__cause__, discord.HTTPException):
                await ctx.send(f'{error.__cause__.text}')
        else:
            await ctx.send(error)
       # raise error
        

def setup(bot):
    bot.add_cog(EmbedEcho(bot))