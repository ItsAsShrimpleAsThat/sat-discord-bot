import discord
from discord.ext import commands
from discord import app_commands
import getsat
import json

# discord stuff
bot = commands.Bot(command_prefix = ")", intents=discord.Intents.all())

saveFile = open("save.sat", "r")
# save = json.load(saveFile)
saveFile.close()

# sat settings
domains = getsat.getDomains(True, True, True, True, False, False, False, False)
question = getsat.getRandomQuestion(domains)

class MCQButtons(discord.ui.View):
    def __init__(self, *, ansOptions, ansCorrect, rationale:str):
        self.ansOptions = ansOptions
        self.ansCorrect = ansCorrect
        self.rationale = rationale
        self.usersThatAnswered = set()
        super().__init__(timeout=None)

        for option in ansOptions:
            button = discord.ui.Button(label=option, style=discord.ButtonStyle.primary, custom_id=option)
            print(ansCorrect)

            button.callback = self.callback(option)
            self.add_item(button)

    def callback(self, option):
        async def callback(interaction:discord.Interaction):
            if(interaction.user.id in self.usersThatAnswered):
                await interaction.response.send_message("You've already answered this question!", ephemeral=True)
                return
            
            self.usersThatAnswered.add(interaction.user.id)
            if(option in self.ansCorrect):
                await interaction.response.send_message("# Correct!\n" + self.rationale, ephemeral=True)
            else:
                await interaction.response.send_message("# Incorrect!\n" + self.rationale, ephemeral=True)
            
        return callback
    
    

    




@bot.tree.command(name="sat", description="sat")
async def sat(interaction: discord.Interaction):
    global question
    print(question.id)
    message = "# SAT Question of the Day!\n"
    message += "Difficulty: " + question.difficulty.toString() + "\n"
    message += "Domain: " + question.domain + "\n\n"

    message += question.stimulus + "\n"
    message += question.stem + "\n"
    message += "\n"
    for k, v in question.ansOptions.items():
        message += k + ") " + v + "\n"

    files = []
    for img in question.images:
        files.append(discord.File(img, "sat.png"))

    await interaction.response.send_message(message, view=MCQButtons(ansOptions=question.ansOptions, ansCorrect=question.ansCorrect, rationale=question.rationale),files=files)
    
    question = getsat.getRandomQuestion(domains)


@bot.tree.command(name="blockquote", description="sat")
async def blockquote(interaction: discord.Interaction):
    blockquotequestion = getsat.getQuestionByID("ba974387")
    message = "# SAT Question of the Day!\n"
    message += "Difficulty: " + blockquotequestion.difficulty.toString() + "\n"
    message += "Domain: " + blockquotequestion.domain + "\n\n"

    message += blockquotequestion.stimulus + "\n"
    message += blockquotequestion.stem + "\n"
    message += "\n"
    for k, v in blockquotequestion.ansOptions.items():
        message += k + ") " + v + "\n"

    files = []
    for img in blockquotequestion.images:
        files.append(discord.File(img, "sat.png"))

    await interaction.response.send_message(message, view=MCQButtons(ansOptions=blockquotequestion.ansOptions, ansCorrect=blockquotequestion.ansCorrect, rationale=blockquotequestion.rationale),files=files)

#     await interaction.response.send_message()




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