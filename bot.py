import os
import json
import discord
from discord.ext import commands
from discord.ext.commands import Context
from cogs import main
from dotenv import load_dotenv, find_dotenv
# from discord_slash import SlashCommand, SlashContext

load_dotenv(find_dotenv())
cogs = [main]
client = commands.Bot(command_prefix="!", intents = discord.Intents.all())
tag_channel = 886948326442950746
grole_data = "grole.json"
rrole_data = "rrole.json"

@client.event
async def on_ready():
    for x in client.guilds:
        if x.name == "游戏社区":
            guild = x
    channel = guild.get_channel(tag_channel)
    with open(grole_data, 'r') as gfile:
        data = json.load(gfile)
    text = "请选择你游玩的游戏从而获得对应游戏的身分组（点击下方对应游戏图标）\n\n"
    text += tags(guild,data)
    game = discord.Embed(description=text)
    game.set_footer(text="若没有你目前游玩游戏的图标请与管理员联系")
    global game_m
    game_m = await channel.send(embed=game)
    for emoji in data:
        await game_m.add_reaction(emoji)

    with open(rrole_data, 'r') as gfile:
        data = json.load(gfile)
    text = "请选择你目前所在的地区从而获得对应的身分组（点击下方对应旗帜图标）\n\n"
    text += tags(guild,data)
    region = discord.Embed(description=text)
    region.set_footer(text="若没有你目前所在地区的旗帜请与管理员联系")
    global region_m
    region_m = await channel.send(embed=region)
    for emoji in data:
        await region_m.add_reaction(emoji)

def tags(guild,data):
    a = ""
    for tag in data:
        role = guild.get_role(data[tag])
        a += tag + ":   " + role.name + "\n\n"
    return a 

@client.command()
async def addtag(ctx,mode,name,emoji):
    if mode == "game":
        data = grole_data
        m = game_m
        text = "请选择你游玩的游戏从而获得对应游戏的身分组（点击下方对应游戏图标）\n\n"
        footer = "若没有你目前游玩游戏的图标请与管理员联系"
    elif mode == "region":
        data = rrole_data
        m = region_m
        text = "请选择你目前所在的地区从而获得对应的身分组（点击下方对应旗帜图标）\n\n"
        footer = "若没有你目前所在地区的旗帜请与管理员联系"
    
    with open(data, 'r') as file:
        tag_data = json.load(file)
        if str(emoji) in tag_data:
            ctx.send("该tag已在库中")
            return
        else:
            for role in ctx.guild.roles:
                if role.name == name:
                    tag_data[str(emoji)] = int(role.id)
                    with open(rrole_data, 'w') as new_data:
                        json.dump(tag_data, new_data, indent=4)
                    with open(data, 'r') as file:
                        new_data = json.load(file)
                    text += tags(ctx.guild,new_data)
                    embed = discord.Embed(description=text)
                    embed.set_footer(text=footer)
                    await m.edit(embed=embed)
                    await m.add_reaction(emoji)
                    await ctx.send("新tag已成功加入列表")

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
async def reload(ctx: Context, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send("Reloaded Cog")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[0:-3]}')

client.run("ODg2NjE4MTY2Nzk1NTk5OTEy.YT4Ngw.iWxWLLtwN3vcO2jgCuQnRJYW8Rw")
