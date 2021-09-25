import discord
from discord.ext import commands
import json
from tabulate import tabulate
from easy_pil import Canvas, Editor, Font
from datetime import datetime, timedelta
import asyncio
from discord import File

grole_data = "grole.json"
rrole_data = "rrole.json"
data = "message.json"
warn_data = "warn.json"
admin = 471396850625151075
admin_channel = 883851550768893952
tag_channel = 886948326442950746
level_channel = 886948052026400820

def setup(client):
    client.add_cog(main(client))

class main(commands.Cog):
    def __init__(self,client):
        self.client = client

    async def count(self,data,member,x=1):
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

    async def checkwarn(self,chat_data,new_user,guild):
        channel = guild.get_channel(admin_channel)
        member = await guild.fetch_member(new_user)
        if chat_data[new_user] == 3:
            await self.tempmute(channel,member,7,"d",reason = "已被警告三次")
        if chat_data[new_user] == 5:
            await member.ban(reason="已被警告五次")
            chat_data[new_user] = 0
            with open(data, 'w') as new_user_data:
                json.dump(chat_data, new_user_data, indent=4)


    async def checklevel(chat_data,new_user,guild):
        channel = guild.get_channel(level_channel)
        if chat_data[new_user] >= 3000:
            member = guild.get_member(int(new_user))
            role = guild.get_role(888032719144120381)
            if role in member.roles:
                return
            else:
                await member.add_roles(role)
            await channel.send("恭喜 "+member.display_name+" 已获得足够活跃度并成为会员！祝你身体健康，保持活跃！")

    @commands.command()
    async def F(self,ctx,*,text):
        if(ctx.author.voice):
            channel = ctx.author.voice.channel
            name = channel.name
            Invite = await channel.create_invite()
            embed = discord.Embed()
            link = "["+name+"]("+str(Invite)+")"
            embed.description = text+"\n"+link
            await ctx.send(embed=embed)
        else:
            await ctx.send("请加入语音频道后再使用该指令")

    @commands.command()
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

    @commands.Cog.listener()
    async def on_reaction_add(self,reaction,user):
        guild = user.guild
        if reaction.message.channel.id == 886948853578878997:
            if guild.get_role(298168855706992650) not in user.roles :
                await reaction.remove(user)
        if reaction.message.channel.id == 886948912005517352:
            if guild.get_role(189833260157763593) not in user.roles :
                await reaction.remove(user)
        if user.bot:
            return
        if reaction.emoji == ('🙅‍♂️'):
            if guild.get_role(admin) in user.roles:
                await self.warn(reaction.message,reaction.message,"不合规语句")
            return
        emoji = str(reaction.emoji)
        with open(grole_data, 'r') as file:
                    chat_data = json.load(file)
        if emoji in chat_data:
            await user.add_roles(guild.get_role(chat_data[emoji]))
        with open(rrole_data, 'r') as rfile:
                    region_data = json.load(rfile)
        if emoji in region_data:
            await user.add_roles(guild.get_role(region_data[emoji]))

    async def warn(self,ctx,message,reason="未提供"):
        print("1")
        member = message.author
        await self.count(warn_data,message.author)
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
        await ctx.reply(embed=embed)
        await message.delete()
        await self.checkwarn(chat_data,new_user,message.guild)

    # @commands.command()
    # async def rank(ctx):
    #     with open(data, 'r') as file:
    #         chat_data = json.load(file)
    #         user = str(ctx.author.id)
    #     progress = chat_data[user]
    #     if progress >= 3000:
    #         goal = 5000
    #     else:
    #         goal = 3000

    #     percent = (progress/goal)*100
    #     if percent > 100:
    #         percent = 100

    #     await ctx.author.avatar_url.save("avt.png")
    #     background = Editor(Canvas((934, 282), "#23272a"))
    #     profile = Editor("avt.png").resize((190, 190)).circle_image()
    #     poppins = Font().poppins(size=30)

    #     background.rectangle((20, 20), 894, 242, "#2a2e35")
    #     background.paste(profile, (50, 50))
    #     background.ellipse((42, 42), width=206, height=206, outline="#43b581", stroke_width=10)
    #     background.rectangle((260, 180), width=630, height=40, fill="#484b4e", radius=20)
    #     background.bar(
    #         (260, 180),
    #         max_width=630,
    #         height=40,
    #         percentage=percent,
    #         fill="#00fa81",
    #         radius=20,
    #     )
    #     background.text((270, 120), ctx.author.name, font=poppins, color="#00fa81")
    #     background.text(
    #         (870, 125),
    #         f"{progress} / {goal}",
    #         font=poppins,
    #         color="#00fa81",
    #         align="right",
    #     )
    #     file = File(fp=background.image_bytes, filename="card.png")
    #     await ctx.send(file=file)

    # @client.event
    # async def on_message(message):
    #     if not message.author.bot:
    #         if not message.content.startswith('!'):
    #             await count(data,message.author,1)
    #             with open(data, 'r') as file:
    #                 chat_data = json.load(file)
    #                 new_user = str(message.author.id)
    #             await checklevel(chat_data,new_user,message.channel.guild)
    #     await client.process_commands(message)

    # @client.event
    # async def on_voice_state_update(member,before,after):
    #     if before.channel == None and after.channel != None:
    #         voice[member.id] = datetime.now()
    #     if before.channel != None and after.channel == None:
    #         dt = datetime.now() - voice[member.id]
    #         x = int(dt/timedelta(second = 1))*6
    #         await count(data,member,x)
