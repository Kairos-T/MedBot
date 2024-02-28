import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

token = os.environ.get('DISCORD_TOKEN')
print(token)

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

    bot.load_extension('cogs.reminders')

bot.run(token)
