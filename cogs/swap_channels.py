import discord
import os
import pymongo
from discord.ext import commands
from discord.ext.commands import has_permissions


class SwapCommands(commands.Cog):
    def __init__(self, client):
        self.bot = client
    
    # add swap channels

    @commands.command()
    @has_permissions(administrator= True, manage_guild= True)
    async def swap(self, ctx, from_channel: discord.TextChannel= None, to_channel= None):
        channel_ok = False
        if not from_channel or not to_channel:
            channel_ok = False
            await ctx.send("Provide channel correctly!!")
        elif from_channel:
            pass
        
        if channel_ok:
            con_fibu = pymongo.MongoClient(os.getenv("DB"))
            db = con_fibu["fibu"] #database
            tb = db["swap_channels"] #table
            get_guild = tb.find_one({"guild_id": ctx.guild.id})
            if get_guild:
                new_value = {"swap_channels": {"from_channel": from_channel.id, "to_channel": to_channel.id}}
                tb.update_one({"guild_id": ctx.guild.id},{"$set": new_value})
                await ctx.message.add_reaction("✅")
            else:
                def message_check(message):
                    return message.author.id == ctx.author.id
                msg = await ctx.send('Should I DM user that his/her message swapped?\nSend Yes/No or True/False by replying this message.')
                
                
                id = 1
                if not msg_format:
                    msg_format = 'Username: {user.name}\nUserID: {user.id}\nMessage:\n{message}'
                value = {
                    'guild_id': ctx.guild.id,
                    'from_channel': {from_channel.id: id},
                    'to_channel': {id: to_channel.id},
                    'dm': dm,
                }
                from_channel_dict = {from_channel: id}
                to_channel_dict = {id: to_channel}
                if dm:
                    is_dm = {id: True}
                    if dm_msg:
                        dm_msg_dict = {id: f'{dm_msg}'}
                    else:
                        dm_msg_dict = {id: None}
                else:
                    is_dm = {id: False}
                value = {"guild_id": ctx.guild.id, "from_channel": from_channel.id, "to_channel": to_channel.id}
                tb.insert_one(value)
                await ctx.message.add_reaction("✅")

# remove swap channels
    @commands.command()
    @has_permissions(administrator= True, manage_guild= True)
    async def removeSwap(self, ctx):
        con_fibu = pymongo.MongoClient(os.getenv("DB"))
        db = con_fibu["fibu"] #database
        tb = db["guild_data"] #table
        #guild = tb.find_one({"guild_id":ctx.guild.id})
        new_value = {"swap_channels": {"from_channel": None, "to_channel": None}}
        tb.update_one({"guild_id": ctx.guild.id},{"$set": new_value})
        await ctx.message.add_reaction("✅")

######### permission Handling #########
    @swap.error
    async def _error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
        if isinstance(error, commands.ChannelNotFound):
            await ctx.send(f"**From channel** is out of guild!\nPlease provide a channel that exists in this guild to swap messages from that channel.")
               
                    
                            
    @removeSwap.error
    async def _error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have permissions to do that!")
            
def setup(bot):
    bot.add_cog(SwapCommands(bot))