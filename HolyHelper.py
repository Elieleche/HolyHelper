import discord
from discord.ext import tasks, commands
import random
import json
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)


def load_verses(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        verses = json.load(f)
    return verses

verses = load_verses('versets.json')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    daily_verse.start()
    await bot.tree.sync()
    print("Slash commands synchronized.")

@tasks.loop(hours=24)
async def daily_verse():
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                role = discord.utils.get(channel.guild.roles, name="Chrétien")
                verse = random.choice(verses)
                await channel.send(f"{role.mention} Voici le verset du jour : {verse}")
                break

@bot.tree.command(name="verset", description="Affiche un verset biblique au hasard")
async def verset(interaction: discord.Interaction):
    verse = random.choice(verses)
    book_and_verse = verse.split(" - ")[0]
    verse_text = verse.split(" - ")[1]
    embed = discord.Embed(title=book_and_verse, description=verse_text, color=0x00ff00)
    embed.set_footer(text="Envoyé par HolyHelper")
    await interaction.response.send_message(embed=embed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    response = None

    if "le seigneur soit avec vous" in message.content.lower():
        response = f"{message.author.mention} Et avec votre esprit"
    elif "au nom du père , du fils , et du saint esprit" in message.content.lower():
        response = f"{message.author.mention} Amen !"
    elif "je crois en dieu" in message.content.lower():
        response = f"{message.author.mention} Je crois en Dieu, le Père tout-puissant, créateur du ciel et de la terre ; et en Jésus-Christ, son Fils unique, notre Seigneur, qui a été conçu du Saint-Esprit, est né de la Vierge Marie, a souffert sous Ponce Pilate, a été crucifié, est mort et a été enseveli, est descendu aux enfers, le troisième jour est ressuscité des morts, est monté aux cieux, est assis à la droite de Dieu le Père tout-puissant, d’où il viendra juger les vivants et les morts. Je crois en l’Esprit-Saint, à la sainte Eglise catholique, à la communion des saints, à la rémission des péchés, à la résurrection de la chair, à la vie éternelle. Amen."

    if response:
        await message.channel.send(response)
        
    await bot.process_commands(message)

quiz_questions = [
    {
        "question": "Quel est le jour où les chrétiens doivent se consacrer à Dieu ?",
        "choices": ["Le samedi", "Le vendredi", "Le dimanche"],
        "answer": "Le dimanche"
    },
    {
        "question": "Chez les chrétiens, Dieu existe en ?",
        "choices": ["Une personne", "Trois personnes", "Sept personnes"],
        "answer": "Trois personnes"
    },
    {
        "question": "Quel est le nom originel de Dieu, chez les chrétiens ?",
        "choices": ["Jehovah", "Yahve", "Allah"],
        "answer": "Yahve"
    },
    {
        "question": "Sur quelle croyance essentielle repose la foi chrétienne ?",
        "choices": ["La résurrection", "La transfiguration", "La communion"],
        "answer": "La résurrection"
    },
    {
        "question": "Le pape est le premier des évêques. Mais de quelle ville est-il l'évêque ?",
        "choices": ["De Jérusalem", "Du Vatican", "De Rome"],
        "answer": "De Rome"
    },
    {
        "question": "Qui participent à son 'élection' ?",
        "choices": ["Les évêques", "Les évêques et les cardinaux", "Les cardinaux"],
        "answer": "Les cardinaux"
    },
    {
        "question": "Quel territoire administre un évêque ?",
        "choices": ["Une province", "Un diocèse", "Une paroisse"],
        "answer": "Un diocèse"
    },
    {
        "question": "Quel est le moment le plus important de la messe chez les chrétiens ?",
        "choices": ["L'Eucharistie", "La 2e lecture (de l'Evangile)", "La bénédiction"],
        "answer": "L'Eucharistie"
    },
    {
        "question": "Quelle est la branche religieuse originelle dans le christianisme ?",
        "choices": ["L'orthodoxie", "Le catholicisme", "Le protestantisme"],
        "answer": "Le catholicisme"
    },
    {
        "question": "Quel fut l'évènement qui consacra la scission entre les chrétiens d'Occident et d'Orient ?",
        "choices": ["Le schisme", "Les thèses de Luther", "Le concile de Nicée"],
        "answer": "Le schisme"
    },
    {
        "question": "L'évangile est un livre qui raconte la vie publique du Christ et son message. Quatre évangiles ont été reconnus et intégrés dans la Bible tandis que d'autres ne le sont pas car ils sont ?",
        "choices": ["Millénaristes", "Apocryphes", "Eschatologiques"],
        "answer": "Apocryphes"
    },
    {
        "question": "Qui n'a pas écrit un évangile reconnu et officiel ?",
        "choices": ["Pierre", "Marc", "Luc"],
        "answer": "Pierre"
    },
    {
        "question": "Quelle est la partie de la Bible exclusivement chrétienne ?",
        "choices": ["Le Pentateuque", "Les Evangiles", "Le Nouveau Testament"],
        "answer": "Le Nouveau Testament"
    },
    {
        "question": "Qui aurait écrit l'Apocalypse, le dernier livre de la Bible ?",
        "choices": ["Paul", "Jean", "Thomas"],
        "answer": "Jean"
    },
    {
        "question": "Quel homme a évangélisé sans relâche le bassin Méditerranéen au Ier siècle de notre ère ?",
        "choices": ["Jacques", "Paul", "Pierre"],
        "answer": "Paul"
    },
    {
        "question": "Quelle est la fête la plus importante chez les chrétiens ?",
        "choices": ["La Toussaint", "Pâques", "Noël"],
        "answer": "Pâques"
    },
    {
        "question": "La prière la plus importante (donnée par le Christ lui-même) ?",
        "choices": ["Notre Père", "Je crois en Dieu (le Credo)", "Je vous salue Marie"],
        "answer": "Notre Père"
    },
    {
        "question": "Lorsqu'un homme (ou femme) parvient à la sainteté, il (elle) a bénéficié d'une ?",
        "choices": ["Canonisation", "Béatification", "Sanctification"],
        "answer": "Canonisation"
    },
    {
        "question": "Quel est le seul péché qui n'est pas pardonné par Dieu ?",
        "choices": ["Le meurtre", "Le blasphème", "L'athéisme"],
        "answer": "Le blasphème"
    },
    {
        "question": "Quel est le village français où la Sainte Vierge n'est pas apparue ?",
        "choices": ["Ars", "Pontmain", "Lourdes"],
        "answer": "Ars"
    }
]

user_scores = {}

@bot.tree.command(name="quiz", description="Commence un quiz chrétien")
async def quiz(interaction: discord.Interaction):
    question_data = random.choice(quiz_questions)
    question = question_data["question"]
    choices = question_data["choices"]
    correct_answer = question_data["answer"]

    buttons = [discord.ui.Button(label=choice, custom_id=choice) for choice in choices]

    view = discord.ui.View()

    for button in buttons:
        view.add_item(button)

    async def button_callback(interaction: discord.Interaction):
        selected_answer = interaction.data["custom_id"]
        user_id = interaction.user.id

        if selected_answer == correct_answer:
            if user_id in user_scores:
                user_scores[user_id] += 1
            else:
                user_scores[user_id] = 1
            await interaction.response.send_message("Bonne réponse ! +1 point", ephemeral=True)
        else:
            await interaction.response.send_message(f"Mauvaise réponse. La bonne réponse était: {correct_answer}", ephemeral=True)

        for item in view.children:
            item.disabled = True

        await interaction.message.edit(view=view)

    for button in buttons:
        button.callback = button_callback

    await interaction.response.send_message(question, view=view)

@bot.tree.command(name="score", description="Affiche ton score")
async def score(interaction: discord.Interaction):
    user_id = interaction.user.id
    score = user_scores.get(user_id, 0)
    await interaction.response.send_message(f"Votre score est: {score} point(s).")


bot.run(TOKEN)
