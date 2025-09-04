import discord
from discord.ext import commands
from discord import app_commands

bot = commands.Bot(command_prefix = ")", intents=discord.Intents.all())

class ResponseButtons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="test",style=discord.ButtonStyle.blurple)
    async def optionA(self, interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.send_message("omg it worked", ephemeral=True)


@bot.tree.command(name="sat", description="sat")
async def sat(interaction: discord.Interaction, value: int):
    await interaction.response.send_message("hello!", ephemeral=True)

@bot.command()
async def testbuttons(ctx):
    await ctx.send("hello", view = ResponseButtons())

@bot.event
async def on_ready():
    print("bot online!!!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except:
        print("ha didn't work lmaooooo")

tokenFile = open("token.env", "r")
token = tokenFile.read()
tokenFile.close()
bot.run(token)