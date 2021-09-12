import json
import discord
from discord import File
from tabulate import tabulate
from discord.ext import commands
from easy_pil import Canvas, Editor, Font, Text
from datetime import datetime, timedelta, time


client = commands.Bot(command_prefix="!", intents = discord.Intents.all())
data = "message.json"
warn_data = "warn.json"
voice = {}
class channelid:
    levelchannel = 885735656557527081
    get_tag = 885981121534390302

class roleid:
    admin = 885138315370692638
    mute = 886441347844816966
    Naraka = 885138934219309056
    Lol = 885160394958708778
    CSGO = 886464875965079612
    PUBG = 886464914011615253
    
class emojiid:
    Naraka = "<:Naraka:886450992567181373>"
    Lol = "<:LOL:886451496231772180>"
    CSGO = "<:CSGO:886451495296434206>"
    PUBG = "<:PUBG:886450993053700106>"

async def count(mode,data,member,x=1):
    with open(data, 'r') as file:
                chat_data = json.load(file)
                new_user = str(member.id)
            # Update existing user
    if new_user in chat_data:
        chat_data[new_user] += x
        guild = member.guild
        if mode == "level":
            await checklevel(chat_data,new_user,guild)
        if mode == "warn":
            await checkwarn(chat_data,new_user,guild)
        with open(data, 'w') as update_user_data:
            json.dump(chat_data, update_user_data, indent=4)
    # Add new user
    else:
        chat_data[new_user] = x
        with open(data, 'w') as new_user_data:
            json.dump(chat_data, new_user_data, indent=4)

async def checkwarn(chat_data,new_user,guild):
    channel = guild.get_channel(channelid.levelchannel)
    if chat_data[new_user] == 3:
        member = guild.get_member(int(new_user))
        role = guild.get_role(885731265926541384)
        if role in member.roles:
            return
        else:
            await member.add_roles(role)
        await channel.send("恭喜 "+member.display_name+" 已获得足够活跃度并成为会员！祝你身体健康，保持活跃！")
    if chat_data[new_user] >= 5000:
        member = guild.get_member(int(new_user))
        role = guild.get_role(885731375372705803)
        if role in member.roles:
            return
        else:
            await member.add_roles(role)
        await channel.send("恭喜 "+member.display_name+" 已获得足够活跃度并成为高级会员！祝你身体健康，保持活跃！")

async def checklevel(chat_data,new_user,guild):
    channel = guild.get_channel(channelid.levelchannel)
    if chat_data[new_user] >= 3000 and chat_data[new_user] <= 3000:
        member = guild.get_member(int(new_user))
        role = guild.get_role(885731265926541384)
        if role in member.roles:
            return
        else:
            await member.add_roles(role)
        await channel.send("恭喜 "+member.display_name+" 已获得足够活跃度并成为会员！祝你身体健康，保持活跃！")
    if chat_data[new_user] >= 5000:
        member = guild.get_member(int(new_user))
        role = guild.get_role(885731375372705803)
        if role in member.roles:
            return
        else:
            await member.add_roles(role)
        await channel.send("恭喜 "+member.display_name+" 已获得足够活跃度并成为高级会员！祝你身体健康，保持活跃！")

@client.command()
async def tag(ctx):
    embed1 = discord.Embed(description="请选择你游玩的游戏从而获得对应游戏的身分组（点击下方对应游戏图标）")
    # embed1.add_field(name=" ",value="")
    channel = ctx.guild.get_channel(channelid.get_tag)
    m = await channel.send(embed=embed1)
    await m.add_reaction(emojiid.Naraka)
    await m.add_reaction(emojiid.Lol)
    await m.add_reaction(emojiid.CSGO)
    await m.add_reaction(emojiid.PUBG)

@client.command()
async def warn(ctx,message,reason="未提供"):
    member = message.author
    with open(warn_data, 'r') as file:
        chat_data = json.load(file)
        new_user = str(member.id)

    embed = discord.Embed(
        title="原因："+reason,
        description="违规语句："+message.content + "\n" +"累计警告次数：" + str(chat_data[new_user]),
        colour=discord.Colour.red(),
    )
    embed.set_author(name=member.name+"已被警告",icon_url=member.avatar_url)
    embed.set_footer(text="多次警告可能导致禁言甚至封禁，如果对警告有疑问请联系管理员")
    await count("warn",warn_data,message.author)
    await ctx.reply(embed=embed)
    await message.delete()
    

@client.command()
async def zd(ctx,*,text):
    if(ctx.author.voice):
        channel = ctx.author.voice.channel
        name = channel.name
        Invite = await channel.create_invite()
        embed = discord.Embed()
        link = "["+name+"]("+str(Invite)+")"
        embed.description = text+"\n"+link
        await ctx.send(embed=embed)
    else:
        await warn(ctx,ctx.message,"不规范使用指令")

@client.command()
async def rank(ctx):
    with open(data, 'r') as file:
        chat_data = json.load(file)
        user = str(ctx.author.id)
    progress = chat_data[user]
    if progress >= 3000:
        goal = 5000
    else:
        goal = 3000
    
    percent = (progress/goal)*100
    if percent > 100:
        percent = 100
    
    await ctx.author.avatar_url.save("avt.png")
    background = Editor(Canvas((934, 282), "#23272a"))
    profile = Editor("avt.png").resize((190, 190)).circle_image()
    poppins = Font().poppins(size=30)

    background.rectangle((20, 20), 894, 242, "#2a2e35")
    background.paste(profile, (50, 50))
    background.ellipse((42, 42), width=206, height=206, outline="#43b581", stroke_width=10)
    background.rectangle((260, 180), width=630, height=40, fill="#484b4e", radius=20)
    background.bar(
        (260, 180),
        max_width=630,
        height=40,
        percentage=percent,
        fill="#00fa81",
        radius=20,
    )
    background.text((270, 120), ctx.author.name, font=poppins, color="#00fa81")
    background.text(
        (870, 125),
        f"{progress} / {goal}",
        font=poppins,
        color="#00fa81",
        align="right",
    )
    file = File(fp=background.image_bytes, filename="card.png")
    await ctx.send(file=file)

@client.event
async def on_message(message):
    if not message.author.bot:
        if not message.content.startswith('!'):
            await count("level",data,message.author,1000)
    await client.process_commands(message)

@client.event
async def on_voice_state_update(member,before,after):
    if before.channel == None and after.channel != None:
        voice[member.id] = datetime.now()
    if before.channel != None and after.channel == None:
        dt = datetime.now() - voice[member.id]
        x = int(dt/timedelta(seconds = 1))*600
        await count(data,member,x)

@client.event
async def on_reaction_add(reaction,user):
    if user.bot:
        return
    if reaction.emoji == ('🙅‍♂️'):
        if user.guild.get_role(roleid.admin) in user.roles:
            await warn(reaction.message,reaction.message,"不合规语句")
    if str(reaction.emoji) == (emojiid.Naraka):
        await user.add_roles(user.guild.get_role(roleid.Naraka))
    if str(reaction.emoji) == (emojiid.Lol):
        await user.add_roles(user.guild.get_role(roleid.Lol))
    if str(reaction.emoji) == (emojiid.CSGO):
        await user.add_roles(user.guild.get_role(roleid.CSGO))
    if str(reaction.emoji) == (emojiid.PUBG):
        await user.add_roles(user.guild.get_role(roleid.PUBG))

@client.event
async def on_reaction_remove(reaction,user):
    if user.bot:
        return
    if str(reaction.emoji) == (emojiid.Naraka):
        await user.remove_roles(user.guild.get_role(roleid.Naraka))
    if str(reaction.emoji) == (emojiid.Lol):
        await user.remove_roless(user.guild.get_role(roleid.Lol))
    if str(reaction.emoji) == (emojiid.CSGO):
        await user.remove_roles(user.guild.get_role(roleid.CSGO))
    if str(reaction.emoji) == (emojiid.PUBG):
        await user.remove_roles(user.guild.get_role(roleid.PUBG))

# @client.event
# async def on_message_delete(message):
#     guild = message.guild
#     async for log in message.guild.audit_logs(action=discord.AuditLogAction.message_delete, limit=1):
#         delete_by = "{0.user.id}".format(log)
#     member = guild.get_member(int(delete_by))
#     if member != message.author:
#         await warn(message,message,"不合规语句")

client.run("ODUxOTk3OTk2MzA3OTcyMTI3.YMAa9w.g5r-LxxZnBPh75tpRopmhuXYnho")