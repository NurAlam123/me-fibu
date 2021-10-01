import discord
from datetime import datetime as time
from discord.ext import commands
import pymongo
import os

class Info(commands.Cog):
    def __init__(self,client):
        self.bot = client
		
#server info
    @commands.command(name = "serverinfo", aliases = ["si"])
    async def serverinfo(self, ctx):
            roles_name = [i.name for i in ctx.guild.roles]
            if roles_name == []:
                roles_name =["No roles!"]
            bots=(ctx.guild.member_count)-len([m for m in ctx.guild.members if not m.bot])
            guild = ctx.guild
            text = len(guild.text_channels)
            voice = len(guild.voice_channels)
            total = text + voice
            owner = self.bot.get_user(ctx.guild.owner_id)
            msg = discord.Embed(title="Information about", color=0xffdf08, timestamp=time.now(),  description=f"```{guild}```")
            msg.set_thumbnail(url=f"{ctx.guild.icon_url}")
            msg.add_field(name="Region",value=f"{guild.region}",inline= False)
            msg.add_field(name="Owner",value=owner,inline= False)
            msg.add_field(name="Members",value=f"{guild.member_count}", inline= False)
            msg.add_field(name="Bots",value=bots, inline= False)
            sep = "\n"
            msg.add_field(name=f"Roles [{len(ctx.guild.roles)}]",value = f"{sep.join(roles_name)}", inline= False)
            msg.add_field(name = "Channels",value = total, inline = False)
            msg.add_field(name = "Text channels",value = text, inline = False)
            msg.add_field(name = "Voice channels",value = voice, inline = False)
            msg.set_author(name = f"{self.bot.user.name}",icon_url=f"{self.bot.user.avatar_url}")
            msg.set_footer(text = f"Programming Hero ")
            await ctx.send(embed = msg)

#our team **need more improvement**
    @commands.command(name = "team")
    async def _team(self, ctx):
        version = self.bot.version
        team = []
        for id in self.bot.TEAM:
            user = await self.bot.fetch_user(id)
            team.append(user)
            
        await ctx.message.add_reaction("⚒️")
        msg = discord.Embed(title="Developer information", description = "Here are my developers:", color = 0xffdf08, timestamp = time.now())
        msg.add_field(name=f"Nur Alam [{team[0]}]",value="Worked on my designing and development.", inline= False)
        msg.add_field(name="Tamim Vaiya [team[1]]",value="Gave suggestions to my developers.", inline= False)
        msg.add_field(name="Rishikesh [team[2]]",value="Worked on my development.", inline= False)
        msg.add_field(name="Soren_Blank [team[3]]",value="Worked on my development.", inline= False)
        msg.set_author(name=f"{self.bot.user.name}",url="https://www.programming-hero.com/",icon_url=f"{self.bot.user.avatar_url}")
        msg.set_footer(text=f"Programming Hero ")
        await ctx.send(embed=msg)
            
            
#fibu info
    @commands.command(name = "botinfo")
    async def _botinfo(self, ctx):
        roles = [i.mention for i in member.roles if i.name!="@everyone"]
        if roles==[]:
            roles =["No roles!"]
        msg = discord.Embed(title="My information",  description="Hey there! I am Fibu. Your friend and a friendly bot. I am from Programming Hero", color=0xffdf08, timestamp=time.now())
        msg.set_thumbnail(url=f"{self.bot.user.avatar_url}")
        msg.add_field(name="Version",value=f"{self.bot.version}", inline= False)
        msg.add_field(name="Prefix",value="```!fibu```", inline= False)
        msg.add_field(name="Released on",value="Jan 1, 2021", inline= False)
        msg.add_field(name="Website",value="[Programming Hero](https://www.programming-hero.com/)", inline= False)
        msg.add_field(name="Application",value="[Android App](https://is.gd/z11RUg)\n[Iphone Version](https://is.gd/eVH92i)", inline= False)
        msg.add_field(name="Social Media",value="[Facebook](https://m.facebook.com/programmingHero/)\n[Instagram](https://is.gd/6m3hgd)\n[Twitter](https://twitter.com/ProgrammingHero?s=09)\n[Youtube](https://is.gd/EulQLJ)\n[Pinterest](https://www.pinterest.com/programminghero1/)", inline= False)
        msg.add_field(name="Team",value="**1. Nur Alam,\n2. Tamim Vaiya,\n3. Rishikesh,\n4. Soren_Blank**\nFor more info type ```!fibu show your team```", inline= False)
        msg.add_field(name=f"Roles [{len(member.roles)-1}]", value=f"{', '.join(roles)}", inline= False)
        msg.set_author(name=f"{self.bot.user.name}",url="https://www.programming-hero.com/",icon_url=f"{self.bot.user.avatar_url}")
        msg.set_footer(text=f"Programming Hero ")
        await ctx.send(embed=msg)


#user info
    @commands.command(name = "userinfo", aliases = ["ui"])
    async def info(self,ctx,member: discord.Member):
        if member.id == self.bot.user.id:
            await ctx.invoke(self.bot.get_command("botinfo"))
        else:
            roles = [i.mention for i in member.roles if i.name!="@everyone"]
            if roles==[]:
                roles =["No roles!"]
            msg = discord.Embed(title="User information", description=f"{member.mention}",color=0xffdf08,timestamp=time.now())
            msg.add_field(name="Name",value=f"{member.name}", inline= False)
            msg.set_thumbnail(url=member.avatar_url)
            msg.add_field(name="Created at",value=f"{(member.created_at).strftime('%a, %d-%b-%Y %I:%M %p')}", inline= False)
            msg.add_field(name="Joined at",value=f"{(member.joined_at).strftime('%a, %d-%b-%Y %I:%M %p')}", inline= False)
            msg.add_field(name=f"Roles [{len(member.roles)-1}]",value=f"{', '.join(roles)}", inline= False)
            
            con_fibu = pymongo.MongoClient(os.getenv("DB"))
            db = con_fibu["fibu"]
            tb = db["all_about_challenge"]
            find_user = tb.find_one({"user_id": member.id, "guild_id": ctx.guild.id})
            if find_user is not None:
                output = f"Level: {find_user['level']}\nXP: {find_user['xp']}/{find_user['need_xp']}"
                msg.add_field(name="Challenge Profile", value=output, inline=False)
                challenges_name = find_user["challenges"]
                if challenges_name == []:
                    pass
                else:
                    all_challenges = ""
                    for no, challenge_name in enumerate(challenges_name, 1):
                        all_challenges += f"{no}. {challenge_name}\n"
                    msg.add_field(name="Solved Challenges", value = f"```\n{all_challenges}\n```", inline=False)	
            
            else:
                pass
            msg.set_author(name=f"{self.bot.user.name}",url="https://www.programming-hero.com/",icon_url=f"{self.bot.user.avatar_url}")
            msg.set_footer(text="Programming Hero ")
            await ctx.send(embed=msg)

#avatar
    @commands.command(name = "avatar", aliases=["av"])
    async def _av(self,ctx, member: discord.Member):
        avatar = discord.Embed(title="Avatar", color=0xffdf08, timestamp=time.now())
        avatar.set_author(name=f"{self.bot.user.name}", icon_url=self.bot.user.avatar_url)
        avatar.set_footer(text="Programming Hero ")
        avatar.set_image(url = member.avatar_url)
        await ctx.send(embed=avatar)

#member count
    @commands.command()
    async def count(self, ctx, arg = None):
        if arg == None:
            pass
        elif arg.lower()=="members":
            bots=(ctx.guild.member_count)-len([m for m in ctx.guild.members if not m.bot])
            msg=discord.Embed(title="Members", color=0xffdf08, timestamp=time.now())
            msg.add_field(name="Server Name",value=f"{ctx.guild.name}", inline= False)
            msg.add_field(name="Members",value=f"{ctx.guild.member_count}", inline= False)
            msg.add_field(name="Humans",value=f"{(ctx.guild.member_count)-bots}", inline= False)
            msg.add_field(name="Bots",value=f"{bots}", inline= False)
            msg.set_author(name=f"{self.bot.user.name}",icon_url=f"{self.bot.user.avatar_url}")
            msg.set_footer(text=f"Programming Hero ")
            await ctx.send(embed=msg)
            

def setup(bot):
    bot.add_cog(Info(bot))