import discord
from discord.ext import commands

import re
import json
import asyncio
import typing

class EmbedEcho(commands.Cog):
    def __init__(self, client):
        self.bot = client
    
    @commands.command(aliases= ['echoEm'])
    @commands.guild_only()
    @commands.has_permissions(administrator= True, manage_messages= True, manage_guild= True)
    async def echoEmbed(self, ctx, channel: typing.Optional[discord.TextChannel], *, embed_obj):
        if not channel:
            channel = ctx.channel
        
        if embed_obj.startswith('`') and embed_obj.endswith('`'):
            embed_obj = embed_obj.lstrip('`').rstrip('`')
            if embed_obj.startswith('json\n'):
                embed_obj = embed_obj.lstrip('json\n')
        if embed_obj.lstrip('{').rstrip('}').strip()=='':
            await ctx.send('You have provided an empty embed object')
        else:
            embed_obj = json.loads(embed_obj)
            em_msg = discord.Embed.from_dict(embed_obj)
            if 'plainText' in embed_obj.keys():
                text = embed_obj.get('plainText')
            elif 'content' in embed_obj.keys():
                text = embed_obj.get('content')
            elif 'message' in embed_obj.keys():
                text = embed_obj.get('message')
            else:
                text = None
            await ctx.send(content= text, embed= em_msg)

    @commands.command()
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
                except Exception as e:
                    print(f'error {e}')
                    break
                else:
                    source_msg = await ctx.send(f'```json\n{embed_source}\n```')
                        
                    if len(embeds) <= 1:
                        msg = '\N{White Small Square}\ufe0f Here is the json object of that embed.\n\N{White Small Square}\ufe0f Just copy and edit it or replace by another embed json object and send it.\n\N{White Small Square}\ufe0f To cancel the process send \'cancle\'!!'
                    else:
                        if no in nth.keys():
                            suffix = nth[no]
                        else:
                            suffix = 'th'
                        msg = f'\N{White Small Square}\ufe0f Here is the json object of {no}{suffix} embed.\nJust copy and edit it or replace by another embed json object and send it.\n\N{White Small Square}\ufe0f Type \'skip\' to skip this embed and go next\n\N{White Small Square}\ufe0f Type \'cancle\' to cancel process!!'
                    await source_msg.reply(msg)
                    while True:
                        replace_msg = await self.bot.wait_for('message', check= lambda msg: msg.author.id==ctx.author.id)
                        if replace_msg.content.lstrip('{').rstrip('}').strip()=='':
                            await ctx.send('Empty Embed Object...\nFix it and resend again or send \'cancle\' to cancel the process!!')

                        elif replace_msg.content.lower().strip() == 'cancle':
                            await ctx.send('Editing process has been cancelled!!')
                            cancelled = True
                            break
                        elif replace_msg.content.lower().strip() == 'skip':
                            await ctx.send('Skipped!!')
                            break
                        else:
                            if replace_msg.content.startswith('{') and replace_msg.content.startswith('{'):
                                try:
                                    embed_obj = json.loads(replace_msg.content)
                                except json.JSONDecodeError:
                                    await ctx.send('Invalid Embed Object...\nFix it and resend again or send \'cancle\' to cancel the process!!')
                                else:
                                    em_msg = discord.Embed.from_dict(embed_obj)
                                    if 'plainText' in embed_obj.keys():
                                        text = embed_obj.get('plainText')
                                    elif 'content' in embed_obj.keys():
                                        text = embed_obj.get('content')
                                    elif 'message' in embed_obj.keys():
                                        text = embed_obj.get('message')
                                    else:
                                        text = None
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
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send(error)
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
    
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
        else:
            await ctx.send(error)
        

def setup(bot):
    bot.add_cog(EmbedEcho(bot))