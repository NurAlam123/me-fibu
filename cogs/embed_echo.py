import discord
from discord.ext import commands

import re
import json
import asyncio

class EmbedEcho(commands.Cog):
    def __init__(self, client):
        self.bot = client
    
    @commands.command(aliases= ['echoEm'])
    async def echoEmbed(self, ctx, channel: discord.Textchannel= None, *, embed_obj):
        if not channel:
            channel = ctx.channel
        if embed_obj.startswith('`') and embed_obj.endswith('`'):
            embed_obj = embed_obj.lstrip('`').rstrip('`')
            if embed_obj.startswith('json\n'):
                embed_obj = embed_obj.lstrip('json\n')
        try:
            embed_obj = json.loads(embed_obj)
        except json.JSONDecodeError:
            await ctx.send('Invalid Embed Object!!')
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
            await ctx.send(content= text, embed= em_msg)
    
    
    @commands.command()
    async def editEmbed(self, ctx, channel: discord.TextChannel, message_id: int):
        pass



def setup(bot):
    bot.add_cog(EmbedEcho(bot))