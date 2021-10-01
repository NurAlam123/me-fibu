import discord
from datetime import datetime as time
from discord.ext import commands
import pymongo
import os
import random

class Info(commands.Cog):
    def __init__(self,client):
        self.bot = client
        self.colors = [0x7700fe, 0x340e72, 0xfdb706]
		
#server info
    @commands.command(name = "serverinfo", aliases = ["si", "guildinfo", "gi"])
    async def serverinfo(self, ctx):
        guild = ctx.guild
        guild_roles = []
        for role in guild.roles:
            role_format = f"{role}"
            guild_roles.append(role_format)
        
        ### Information Variable ###
        guild_roles = "\n".join(f"{i}. {j}" for i, j in enumerate(guild_roles[::-1], 1))
        guild_name = guild.name
        guild_id = guild.id
        guild_owner = guild.owner
        guild_owner_id = guild.owner_id
        guild_region = str(guild.region).capitalize()
        guild_description = guild.description
        guild_icon = str(guild.icon_url)
        guild_created_at = (guild.created_at).strftime("%a, %d-%b-%Y %I:%M %p")
        
        ### Member count ###
        members = guild.member_count
        humans = 0
        online = 0
        offline = 0
        idle = 0
        dnd = 0
        for m in guild.members:
            status = str(m.status)
            if not m.bot:
                humans+=1
            if status == "online":
                online+=1
            elif status == "offline" or status == "invisible":
                offline+=1
            elif status == "idle":
                idle+=1
            elif status == "dnd" or status == "do_not_disturb":
                dnd+=1
        bots = members - humans
        ######
        
        guild_text_channels = len(guild.text_channels)
        guild_voice_channels = len(guild.voice_channels)
        guild_channels = guild_text_channels + guild_voice_channels
        guild_categories = len(guild.categories)
        
        ### Embed Part ###
        info_em = discord.Embed(title= "Server Information", color= random.choice(self.colors))
        info_em.add_field(name= "Name", value= f"{guild_name}", inline= False)
        info_em.add_field(name= "Guild ID", value= f"```\n{guild_id}\n```", inline= False)
        info_em.add_field(name= "Owner", value= f"{guild_owner}", inline= False)
        info_em.add_field(name= "Owner ID", value= f"```\n{guild_owner_id}\n```", inline= False)
        info_em.add_field(name= "Server Created At", value= f"```\n{guild_created_at}\n```")
        info_em.add_field(name= "Region", value= f"{guild_region}", inline= False)
        if guild_description:
            info_em.add_field(name= "Guild Description", value= f"{guild_description}", inline= False)
        info_em.add_field(name= f"Members [{members}]", value= f"```\nHumans: {humans}\nBots: {bots}\n--------------------\nOnline: {online}\nOffline: {offline}\nIdle: {idle}\nDND: {dnd}\n```", inline= False)
        info_em.add_field(name= "Channels and Categories", value= f"```\nCategories: {guild_categories}\n│\n└── Channels: {guild_channels}\n    ├── Text Channels: {guild_text_channels}\n    └── Voice Channels: {guild_voice_channels}\n```", inline= False)
        info_em.add_field(name= "Roles", value= f"```\n{guild_roles}\n```", inline= False)
        
        info_em.set_thumbnail(url= f"{guild_icon}")
        info_em.set_footer(text= f"Requested by {ctx.author} | Programming Hero ")
        await ctx.send(embed= info_em)

#our team **need more improvement**
    @commands.command(name = "team", aliases = ["yourteam"])
    async def _team(self, ctx):
        version = self.bot.version
        team = []
        for id in self.bot.TEAM:
            user = await self.bot.fetch_user(id)
            team.append(user)
            
        await ctx.message.add_reaction("⚒️")
        msg = discord.Embed(title="Developer information", description = "Here are my developers:", color = 0xffdf08, timestamp = time.now())
        msg.add_field(name=f"Nur Alam [`{team[0]}`]",value="Worked on my designing and development.", inline= False)
        msg.add_field(name=f"Tamim Vaiya [`{team[1]}`]",value="Gave suggestions to my developers.", inline= False)
        msg.add_field(name=f"Rishikesh [`{team[2]}`]",value="Worked on my development.", inline= False)
        msg.add_field(name=f"Soren_Blank [`{team[3]}`]",value="Worked on my development.", inline= False)
        msg.add_field(name= f"Shajedul Karim [`{team[4]}`]", value = "Secret supporter behind this secret project!!")
        msg.set_author(name=f"{self.bot.user.name}",url="https://www.programming-hero.com/",icon_url=f"{self.bot.user.avatar_url}")
        msg.set_footer(text=f"Programming Hero ")
        await ctx.send(embed=msg)
            
            
#fibu info
    @commands.command(name = "botinfo", aliases= ["yourinfo"])
    async def _botinfo(self, ctx):
        msg = discord.Embed(title="My information",  description="Hey there! I am Fibu. Your friend and a friendly bot. I am from Programming Hero", color=0xffdf08, timestamp=time.now())
        msg.set_thumbnail(url=f"{self.bot.user.avatar_url}")
        msg.add_field(name="Version",value=f"{self.bot.version}", inline= False)
        msg.add_field(name="Prefix",value="```!fibu```", inline= False)
        msg.add_field(name="Released on",value="Jan 1, 2021", inline= False)
        msg.add_field(name="Website",value="[Programming Hero](https://www.programming-hero.com/)", inline= False)
        msg.add_field(name="Application",value="[Android App](https://is.gd/z11RUg)\n[Iphone Version](https://is.gd/eVH92i)", inline= False)
        msg.add_field(name="Social Media",value="[Facebook](https://m.facebook.com/programmingHero/)\n[Instagram](https://is.gd/6m3hgd)\n[Twitter](https://twitter.com/ProgrammingHero?s=09)\n[Youtube](https://is.gd/EulQLJ)\n[Pinterest](https://www.pinterest.com/programminghero1/)", inline= False)
        msg.add_field(name="Team",value="**1. Nur Alam,\n2. Tamim Vaiya,\n3. Rishikesh,\n4. Soren_Blank\n5. Shajedul Karim**\nFor more info type ```!fibu show your team```", inline= False)
        #msg.add_field(name=f"Roles [{len(member.roles)-1}]", value=f"{", ".join(roles)}", inline= False)
        msg.set_author(name=f"{self.bot.user.name}",url="https://www.programming-hero.com/",icon_url=f"{self.bot.user.avatar_url}")
        msg.set_footer(text=f"Programming Hero ")
        await ctx.send(embed=msg)


#user info
    @commands.command(name = "userinfo", aliases = ["ui"])
    async def userinfo(self, ctx, member: discord.Member= None):
        if not member:
            member = ctx.author
        if member.id == self.bot.user.id:
            await ctx.invoke(self.bot.get_command("botinfo"))
        else:
            ## Connect with database ##
            con_fibu = pymongo.MongoClient(os.getenv("DB"))
            db = con_fibu["fibu"]
            #tb = db["challenge_data"]
            tb = db["all_about_challenge"]
            
            find_user = tb.find_one({"user_id": member.id, "guild_id": member.guild.id})
            roles = []
            for role in member.roles:
                if role.name != "@everyone":
                    role_format = f"{role}"
                    roles.append(role_format)
                    
            #### Information Variables ####
            roles_format = "\n".join(f"{i}. {j}" for i, j in enumerate(roles, 1)) if len(roles) != 0 else "No Roles"
            guild = member.guild
            user_id = member.id
            user_name = member.name
            user_tag = member.discriminator
            user_nickname = member.nick
            user_status = str(member.status)
            bot_user = member.bot
            user_avatar = str(member.avatar_url)
            status_emoji = {
                "online": "<:online:848818909292658729>", 
                "offline": "<:offline:848818930830016533>", 
                "invisible": "<:offline:848818930830016533>",
                "idle": "<:idle:848818891446681620>",
                "dnd": "<:dnd:848819104446283806>", 
                "do_not_disturb": "<:dnd:848819104446283806>",
            }
            badges_value = {
                0: None,
                1 << 0: "Discord Employee",
                1 << 1: "Partnered Server Owner",
                1 << 2: "HypeSquad Events",
                1 << 3: "Bug Hunter Level 1",
                1 << 6: "House Bravery",
                1 << 7: "House Brilliance",
                1 << 8: "House Balance",
                1 << 9: "Early Supporter",
                1 << 10: "Team User",
                1 << 14: "Bug Hunter Level 2",
                1 << 16: "Verified Bot",
                1 << 17: "Early Verified Bot Developer",
                1 << 18: "Discord Certified Moderator"
            }
            
            user_activities = member.activities
            status = user_status.capitalize() if user_status != "dnd" else user_status.upper()
            
            user_badges = ""
            user_all_badges = member.public_flags.all()
            for no, badge in enumerate(user_all_badges, 1):
                value = badge.value
                user_badges+= f"{no}. {badges_value[value]}\n"
            joined_guild = (member.joined_at).strftime("%a, %d-%b-%Y %I:%M %p")
            created_acc = (member.created_at).strftime("%a, %d-%b-%Y %I:%M %p")
            
            suf = "Bot " if bot_user else ""
            
            #### Embed Part ####
            info_em = discord.Embed(title= f"{suf}User Information", color= random.choice(self.colors))
            info_em.add_field(name= "Name", value= f"```\n{user_name}\n```", inline= True)
            info_em.add_field(name= "Tag", value= f"```\n#{user_tag}\n```", inline= True)
            info_em.add_field(name= "ID", value= f"```\n{user_id}\n```", inline= False)
            if user_nickname:
                info_em.add_field(name= "Nickname", value= f"```\n{user_nickname}\n```", inline= False)
            info_em.add_field(name= "Status", value= f"{status_emoji[user_status]} ─ **{status}**", inline= False)
            info_em.add_field(name= f"Joined {guild.name} at", value= f"```\n{joined_guild}\n```", inline= False)
            info_em.add_field(name= "Account Created at", value= f"```\n{created_acc}\n```", inline= False)
            info_em.add_field(name= "Badges", value= user_badges, inline= False) if not user_badges else None
           #### challenge"s information ####
            if find_user:
                output = f"Level: {find_user['level']}\nXP: {find_user['xp']}/{find_user['need_xp']}"
                info_em.add_field(name= "Challenge Profile", value= output, inline= False)
                challenges_name = find_user["challenges"]
                if challenges_name:
                    all_challenges = ""
                    for no, challenge_name in enumerate(challenges_name, 1):
                        all_challenges += f"{no}. {challenge_name}\n"
                    info_em.add_field(name= "Solved Challenges", value= f"```\n{all_challenges}\n```", inline= False)
            ########
            info_em.add_field(name= f"Roles [{len(roles)}]", value= f"```\n{roles_format}\n```", inline= False)
            info_em.set_thumbnail(url= f"{user_avatar}")
            #info_em.set_author(name= f"{self.bot.user.name}", icon_url= f"{self.bot.user.avatar_url}")
            info_em.set_footer(text= f"Requested by {ctx.author}\nFibu | Programming Hero ")
            
            await ctx.send(embed= info_em)

#avatar
    @commands.command(name = "avatar", aliases=["av"])
    async def _av(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        avatar = discord.Embed(title="Avatar", color=0xffdf08, timestamp=time.now())
        avatar.set_author(name=f"{self.bot.user.name}", icon_url=self.bot.user.avatar_url)
        avatar.set_footer(text="Programming Hero ")
        avatar.set_image(url = member.avatar_url)
        await ctx.send(embed=avatar)

#member count
    @commands.command()
    async def count(self, ctx, arg = None):
        guild = ctx.guild
        members = guild.member_count
        humans = 0
        bots = 0
        online = 0
        offline = 0
        idle = 0
        dnd = 0
        for m in guild.members:
            if not m.bot:
                humans+=1
            else:
                bots += 1
            
            status = str(m.status)
            if status == "online":
                online+=1
            elif status == "offline" or status == "invisible":
                offline+=1
            elif status == "idle":
                idle+=1
            elif status == "dnd" or status == "do_not_disturb":
                dnd+=1
 
        if arg == None:
            pass
        elif arg.lower()=="members":
            msg = discord.Embed(title="Members", color=0xffdf08, timestamp=time.now())
            msg.add_field(name="Server Name",value=f"{guild.name}", inline= False)
            msg.add_field(name="Members",value=f"{members}", inline= False)
            msg.add_field(name="Humans",value=f"{humans}", inline= False)
            msg.add_field(name="Bots",value=f"{bots}", inline= False)
            msg.add_field(name = "Online", value = f"{online}", inline = False)
            msg.add_field(name = "Offline", value = f"{offline}", inline = False)
            msg.add_field(name = "Idle", value = f"{idle}", inline = False)
            msg.add_field(name = "DND", value = f"{dnd}", inline = False)
            
            msg.set_author(name=f"{self.bot.user.name}",icon_url=f"{self.bot.user.avatar_url}")
            msg.set_footer(text=f"Requested by {ctx.author}\nFibu | Programming Hero ")
            await ctx.send(embed=msg)

def setup(bot):
    bot.add_cog(Info(bot))