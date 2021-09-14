import json
import discord
from discord import File
from tabulate import tabulate
from discord.ext import commands
from easy_pil import Canvas, Editor, Font
from datetime import datetime, timedelta
import asyncio
# from discord_slash import SlashCommand, SlashContext


client = commands.Bot(command_prefix="!F", intents = discord.Intents.all())
data = "message.json"
warn_data = "warn.json"
grole_data = "grole.json"
rrole_data = "rrole.json"
voice = {}
admin = 885138315370692638
class channelid:
    levelchannel = 653862558045831169
    get_tag = 886948326442950746
    admin_channel = 883851550768893952

@client.event
async def on_ready():
    for guild in client.guilds:
        for role in guild.roles:
            if role.name == "频道管理员":
                global admin
                admin = role.id

async def count(data,member,x=1):
    with open(data, 'r') as file:
                chat_data = json.load(file)
                new_user = str(member.id)
            # Update existing user
    if new_user in chat_data:
        chat_data[new_user] += x
        with open(data, 'w') as update_user_data:
            json.dump(chat_data, update_user_data, indent=4)
    # Add new user
    else:
        chat_data[new_user] = x
        with open(data, 'w') as new_user_data:
            json.dump(chat_data, new_user_data, indent=4)

async def checkwarn(chat_data,new_user,guild):
    return
#     channel = guild.get_channel(channelid.admin_channel)
#     member = await guild.fetch_member(new_user)
#     if chat_data[new_user] == 3:
#         await tempmute(channel,member,7,"d",reason = "已被警告三次")
#     if chat_data[new_user] == 5:
#         await member.ban(reason="已被警告五次")
#         chat_data[new_user] = 0
#         with open(data, 'w') as new_user_data:
#             json.dump(chat_data, new_user_data, indent=4)


async def checklevel(chat_data,new_user,guild):
    channel = guild.get_channel(channelid.levelchannel)
    if chat_data[new_user] >= 3000 and chat_data[new_user] <= 3005:
        member = guild.get_member(int(new_user))
        role = guild.get_role(885731265926541384)
        if role in member.roles:
            return
        else:
            await member.add_roles(role)
        await channel.send("恭喜 "+member.display_name+" 已获得足够活跃度并成为会员！祝你身体健康，保持活跃！")
#     if chat_data[new_user] >= 5000:
#         member = guild.get_member(int(new_user))
#         role = guild.get_role(885731375372705803)
#         if role in member.roles:
#             return
#         else:
#             await member.add_roles(role)
#         await channel.send("恭喜 "+member.display_name+" 已获得足够活跃度并成为高级会员！祝你身体健康，保持活跃！")

@client.command()
async def tag(ctx):
    channel = ctx.guild.get_channel(channelid.get_tag)
    game = discord.Embed(description="请选择你游玩的游戏从而获得对应游戏的身分组（点击下方对应游戏图标）")
    game.set_footer(text="若没有你目前游玩游戏的图标请与管理员联系")
    global game_m
    game_m = await channel.send(embed=game)
    with open(grole_data, 'r') as gfile:
        game_data = json.load(gfile)
    for emoji in game_data:
        await game_m.add_reaction(emoji)

    region = discord.Embed(description="请选择你目前所在的地区从而获得对应的身分组（点击下方对应旗帜图标）")
    region.set_footer(text="若没有你目前所在地区的旗帜请与管理员联系")
    global region_m
    region_m = await channel.send(embed=region)
    with open(rrole_data, 'r') as rfile:
        region_data = json.load(rfile)
    for emoji in region_data:
        await region_m.add_reaction(emoji)

@client.command()
async def addgametag(ctx,tagid,emoji):
    with open(grole_data, 'r') as gfile:
        game_data = json.load(gfile)
        if str(emoji) in game_data:
            return
        else:
            game_data[str(emoji)] = int(tagid)
            with open(grole_data, 'w') as new_data:
                json.dump(game_data, new_data, indent=4)
            await game_m.add_reaction(emoji)
            await ctx.send("新游戏tag已成功加入列表")
            

@client.command()
async def addregiontag(ctx,tagid,emoji):
    with open(rrole_data, 'r') as rfile:
        region_data = json.load(rfile)
        if str(emoji) in region_data:
            return
        else:
            region_data[str(emoji)] = int(tagid)
            with open(rrole_data, 'w') as new_data:
                json.dump(region_data, new_data, indent=4)
            await region_m.add_reaction(emoji)
            await ctx.send("新国家tag已成功加入列表")

@client.command()
async def warn(ctx,message,reason="未提供"):
    return
#     member = message.author
#     await count(warn_data,message.author)
#     with open(warn_data, 'r') as file:
#         chat_data = json.load(file)
#         new_user = str(member.id)

#     embed = discord.Embed(
#         title="原因："+reason,
#         description="违规语句："+message.content + "\n" +"累计警告次数：" + str(chat_data[new_user]),
#         colour=discord.Colour.red(),
#     )
#     embed.set_author(name=member.name+"已被警告",icon_url=member.avatar_url)
#     embed.set_footer(text="多次警告可能导致禁言甚至封禁，如果对警告有疑问请联系管理员")
#     await ctx.reply(embed=embed)
#     await message.delete()
#     await checkwarn(chat_data,new_user,message.guild)
    

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
        return
#         await warn(ctx,ctx.message,"不规范使用指令")

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
            await count(data,message.author,1)
            with open(data, 'r') as file:
                chat_data = json.load(file)
                new_user = str(message.author.id)
            await checklevel(chat_data,new_user,message.channel.guild)
    await client.process_commands(message)

@client.event
async def on_voice_state_update(member,before,after):
    if before.channel == None and after.channel != None:
        voice[member.id] = datetime.now()
    if before.channel != None and after.channel == None:
        dt = datetime.now() - voice[member.id]
        x = int(dt/timedelta(minutes = 1))*6
        await count(data,member,x)

@client.event
async def on_reaction_add(reaction,user):
    if user.bot:
        return
    if reaction.emoji == ('🙅‍♂️'):
        if user.guild.get_role(admin) in user.roles:
            await warn(reaction.message,reaction.message,"不合规语句")
    
    emoji = str(reaction.emoji)
    with open(grole_data, 'r') as file:
                chat_data = json.load(file)
    if emoji in chat_data:
        await user.add_roles(user.guild.get_role(chat_data[emoji]))

    with open(rrole_data, 'r') as rfile:
                region_data = json.load(rfile)
    if emoji in region_data:
        await user.add_roles(user.guild.get_role(region_data[emoji]))

@client.event
async def on_reaction_remove(reaction,user):
    if user.bot:
        return
    emoji = str(reaction.emoji)
    with open(grole_data, 'r') as gfile:
                game_data = json.load(gfile)
    if emoji in game_data:
        await user.remove_roles(user.guild.get_role(game_data[emoji]))
    
    with open(rrole_data, 'r') as rfile:
                region_data = json.load(rfile)
    if emoji in region_data:
        await user.remove_roles(user.guild.get_role(region_data[emoji]))

@client.command()
async def tempmute(ctx, member: discord.Member, time: int, d, *, reason=None):
    guild = ctx.guild

    for role in guild.roles:
        if role.name == "禁言":
            await member.add_roles(role)

            embed = discord.Embed(title="muted!", description=f"{member.mention} has been tempmuted ", colour=discord.Colour.light_gray())
            embed.add_field(name="reason:", value=reason, inline=False)
            embed.add_field(name="time left for the mute:", value=f"{time}{d}", inline=False)
            await ctx.send(embed=embed)

            if d == "s":
                await asyncio.sleep(time)

            if d == "m":
                await asyncio.sleep(time*60)

            if d == "h":
                await asyncio.sleep(time*60*60)

            if d == "d":
                await asyncio.sleep(time*60*60*24)

            await member.remove_roles(role)

            embed = discord.Embed(title="unmute (temp) ", description=f"unmuted -{member.mention} ", colour=discord.Colour.light_gray())
            await ctx.send(embed=embed)

            return

# @client.event
# async def on_message_delete(message):
#     guild = message.guild
#     async for log in message.guild.audit_logs(action=discord.AuditLogAction.message_delete, limit=1):
#         delete_by = "{0.user.id}".format(log)
#     member = guild.get_member(int(delete_by))
#     if member != message.author:
#         await warn(message,message,"不合规语句")

client.run("ODg2NjE4MTY2Nzk1NTk5OTEy.YT4Ngw.iWxWLLtwN3vcO2jgCuQnRJYW8Rw")
