import discord
from discord.ext import commands
from discord import app_commands
import getsat

# discord stuff
bot = commands.Bot(command_prefix = ")", intents=discord.Intents.all())


# sat settings
domains = getsat.getDomains(True, True, True, True, False, False, False, False)
question = getsat.getRandomQuestion(domains)

class MCQButtons(discord.ui.View):
    def __init__(self, *, ansOptions, ansCorrect, rationale:str):
        self.ansOptions = ansOptions
        self.ansCorrect = ansCorrect
        self.rationale = rationale
        super().__init__(timeout=None)

        for option in ansOptions:
            button = discord.ui.Button(label=option, style=discord.ButtonStyle.primary, custom_id=option)
            print(ansCorrect)

            button.callback = self.callback(option)
            self.add_item(button)

    def callback(self, option):
        async def callback(interaction:discord.Interaction):
            if(option in self.ansCorrect):
                await interaction.response.send_message("# Correct!\n" + self.rationale, ephemeral=True)
            else:
                await interaction.response.send_message("# Incorrect!\n" + self.rationale, ephemeral=True)
            
            self.stop()
        return callback
    
    

    




@bot.tree.command(name="sat", description="sat")
async def sat(interaction: discord.Interaction):
    message = "# SAT Question of the Day!\n"

    message += question.stimulus + "\n"
    message += question.stem + "\n"
    message += "\n"
    for k, v in question.ansOptions.items():
        message += k + ") " + v + "\n"

    await interaction.response.send_message(message, view=MCQButtons(ansOptions=question.ansOptions, ansCorrect=question.ansCorrect, rationale=question.rationale))





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