import discord
from discord.ext import commands
import json

def setup(client):
    client.add_cog(tag(client))

tag_channel = 885981121534390302
grole_data = "grole.json"
rrole_data = "rrole.json"

class tag(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.command()
    async def tag(self,ctx):
        for channel in ctx.guild.channels:
            if channel.name == "📬领取𝖳𝖠𝖦🎫":
                tag_channel = channel.id
        
        channel = ctx.guild.get_channel(tag_channel)
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

    @commands.command()
    async def addtag(self,ctx,mode,name,emoji):
        if mode == "game":
            data = grole_data
            m = game_m
        elif mode == "region":
            data = rrole_data
            m = region_m
        with open(data, 'r') as file:
            tag_data = json.load(file)
            if str(emoji) in tag_data:
                tag_data[str(emoji)] = int(role.id)
                return
            else:
                for role in ctx.guild.roles:
                    if role.name == name:
                        tag_data[str(emoji)] = int(role.id)
                        with open(rrole_data, 'w') as new_data:
                            json.dump(tag_data, new_data, indent=4)
                        await m.add_reaction(emoji)
                        await ctx.send("新tag已成功加入列表")

    @commands.Cog.listener()
    async def on_reaction_remove(self,reaction,user):
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


