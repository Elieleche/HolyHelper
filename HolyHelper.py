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

bot.run(TOKEN)
