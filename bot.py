import os
import discord
from discord.ext import commands
from discord.ext.commands import Context
from cogs import tag, main
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
# from discord_slash import SlashCommand, SlashContext

cogs = [tag,main]
client = commands.Bot(command_prefix="!", intents = discord.Intents.all())
# for cog in cogs:
#     cog.setup(client)

@client.command()
async def reload(ctx: Context, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send("Reloaded Cog")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[0:-3]}')

client.run("ODg2NjE4MTY2Nzk1NTk5OTEy.YT4Ngw.iWxWLLtwN3vcO2jgCuQnRJYW8Rw")
