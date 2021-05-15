from discord.ext import commands
from discord import utils
import discord
import re


### only server animated emojis
class emoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def _message(self, message):
        if message.author.bot:
            return
        if ":" in message.content:

            emotes = re.findall(r":\w+:", message.content)
            user_message = message.content
            
            em = False
            for emote in emotes:
                emoji = utils.get(self.bot.emojis, name= emote.strip(":"))
                if emoji:
                    if emoji.animated:
                        server_emoji = f"<a:{emoji.name}:{emoji.id}>"
                        user_message = user_message.replace(emote, server_emoji)
                        em = True
            if em:
                webhooks = await message.channel.webhooks()
                webhook = utils.get(webhooks, name = "Server Emoji")
                if webhook is None:
                    webhook = await message.channel.create_webhook(name = "Server Emoji")
                await webhook.send(user_message, username = message.author.name, avatar_url = message.author.avatar_url)
                await message.delete()

def setup(bot):
	bot.add_cog(emoji(bot))