import discord
from discord.ext import commands
from discord import app_commands

client = commands.Bot(command_prefix = ")", intents=discord.Intents.all())

@client.event
async def on_ready():
    print("bot online!!!")
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} commands")
    except:
        print("ha didn't work lmaooooo")

client.run(discordAPIkey)