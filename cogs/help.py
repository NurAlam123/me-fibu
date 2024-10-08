import discord
from datetime import datetime as time
from discord.ext import commands

# ========== commands =============


def com_help(client, ctx):
    msg = discord.Embed(title='Help on commands',
                        color=0xffdf08, timestamp=time.now())
    msg.add_field(name='```!fibu math <equation>```',
                  value='Get the result of your math equation. i.e: **!fibu math 2+2**', inline=False)
    msg.add_field(name='```!fibu quote```',
                  value="Get a random quote from WikiQuote", inline=False)
    #msg.add_field(name="```!fibu echo [channel] <message>```",value="To echo a message by Fibu.\n[channel] is optional but (message) is required", inline = False)
    msg.add_field(name='```!fibu yt video <video title>```',
                  value='To search a youtube video', inline=False)
    msg.add_field(name='```!fibu yt channel <channel name>```',
                  value='To search a youtube channel', inline=False)
    msg.add_field(name="```!fibu how <search_word>```",
                  value="Get information from WikiHow", inline=False)
    msg.add_field(name="```!fibu randomHow```",
                  value="Get a random WikiHow content.", inline=False)
    msg.add_field(name='```!fibu covid <country_name>```',
                  value='Get statistics of coronavirus of specific country', inline=False)
    msg.add_field(name="```!fibu joke```",
                  value="To get a random joke", inline=False)
    msg.add_field(name='```!fibu wiki <search word>```',
                  value='Search any details on wikipedia', inline=False)
    msg.add_field(name='```!fibu translate <from_language>|<to_language> <text>```',
                  value="Translate your text to another language. Example:\n **!fibu translate en|fr Hello**", inline=False)
    msg.add_field(name="```!fibu google <query>```",
                  value="Search something on Google.", inline=False)
    msg.set_author(name=f'{client.user.name}',
                   icon_url=f'{client.user.avatar_url}')
    msg.set_footer(text='Fibu | Programming Hero ')
    return ctx.send(embed=msg)

# ============= info ===============


def info_help(client, ctx):
    msg = discord.Embed(title='Help on information commands',
                        color=0xffdf08, timestamp=time.now())
    msg.add_field(name='```!fibu serverinfo```',
                  value='Get information about the server', inline=False)
    msg.add_field(name='```!fibu count members```',
                  value='Get the number of members in the server', inline=False)
    msg.add_field(name='```!fibu team```',
                  value='Get the information about my team', inline=False)
    msg.add_field(name='```!fibu yourinfo```',
                  value='Get information about me', inline=False)
    msg.add_field(name='```!fibu avatar [member]```',
                  value='To get or see avatar of your or mentioned user', inline=False)
    msg.add_field(name='```!fibu userinfo```',
                  value='Get information you or a mentioned user', inline=False)
    msg.set_footer(text='Fibu | Programming Hero ')
    msg.set_author(name=f'{client.user.name}',
                   icon_url=f'{client.user.avatar_url}')
    return ctx.send(embed=msg)

# ========= others ==============


def others_help(client, ctx):
    msg = discord.Embed(title='Help on other commands',
                        color=0xffdf08, timestamp=time.now())
    msg.add_field(name='```!fibu hello```',
                  value='Greet you in server', inline=False)
    msg.add_field(name='```!fibu dm```',
                  value='Greet you in DM.', inline=False)
    msg.add_field(name='```!fibu ok```',
                  value='If you want to say ok to me.', inline=False)
    msg.add_field(name='```!fibu thank you```',
                  value='If you want to thanked me.', inline=False)
    msg.set_footer(text='Fibu | Programming Hero ')
    msg.set_author(name=f'{client.user.name}',
                   icon_url=f'{client.user.avatar_url}')
    return ctx.send(embed=msg)

# =========== qna ===============


def qna_help(client, ctx):
    msg = discord.Embed(title='Help on qna commands',
                        color=0xffdf08, timestamp=time.now())
    msg.add_field(name='``` !fibu ans your_question```',
                  value='Get the answer of your question', inline=False)
    msg.set_author(name=f'{client.user.name}',
                   icon_url=f'{client.user.avatar_url}')
    msg.set_footer(text='Programming Hero ')
    return ctx.send(embed=msg)

# ==============================


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
    # help

    @commands.group(case_insensitive=True)
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.message.add_reaction('✅')
            help_msg = discord.Embed(
                title='Help on all features', description='My prefix is ```\n!fibu ```', color=0xffdf08, timestamp=time.now())
            help_msg.add_field(name="All Commands",
                               value='```!fibu help commands```', inline=False)
            # help_msg.add_field(name='QNA',
            #		value='```
            #!fibu help qna```')
            help_msg.add_field(
                name='Info', value='```!fibu help info```', inline=False)
            help_msg.add_field(
                name='Others', value='```!fibu help others```', inline=False)
            help_msg.set_author(
                name=f'{self.client.user.name}', icon_url=f'{self.client.user.avatar_url}')
            help_msg.set_footer(text='Programming Hero ')
            await ctx.send(embed=help_msg)

# commands_help
    @help.command()
    async def commands(self, ctx):
        await ctx.message.add_reaction("✅")
        await com_help(self.client, ctx)

# qna_help
    @help.command()
    async def qna(self, ctx):
        await ctx.message.add_reaction('✅')
        await qna_help(self.client, ctx)

# info_help
    @help.command()
    async def info(self, ctx):
        await ctx.message.add_reaction('✅')
        await info_help(self.client, ctx)

# others_help
    @help.command()
    async def others(self, ctx):
        await ctx.message.add_reaction('✅')
        await others_help(self.client, ctx)


def setup(bot):
    bot.add_cog(Help(bot))
