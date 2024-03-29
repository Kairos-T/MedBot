import os
from datetime import datetime
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
import json

# Bot Initialisation


load_dotenv()
token = os.environ.get('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)

# File Initialisation

REMINDER_FILE = 'reminders.json'


def load_reminders():
    if os.path.exists(REMINDER_FILE) and os.path.getsize(REMINDER_FILE) > 0:
        with open(REMINDER_FILE, 'r') as f:
            print("Loading reminders")
            return json.load(f)
    return []


def save_reminders(reminders):
    with open(REMINDER_FILE, 'w') as f:
        json.dump(reminders, f, indent=2)

# Checker


@tasks.loop(seconds=10)
async def check_reminders():
    reminders = load_reminders()
    now = datetime.now()

    reminders_copy = reminders.copy()

    for reminder in reminders_copy:
        reminder_time = datetime.strptime(reminder["time"], "%H:%M")
        if reminder_time <= now:
            channel = bot.get_channel(reminder["channel"])
            if channel:
                await channel.send(f"Reminder for <@{reminder['author']}>: {reminder['reminder']}")
                reminders.remove(reminder)
                save_reminders(reminders)
            else:
                print(f"Channel not found for reminder: {reminder}")


# Events


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    check_reminders.start()

# Commands


@bot.command()
async def add(ctx, time, *, message: str):
    try:
        reminder_time = datetime.strptime(time, "%H:%M").strftime("%H:%M")
    except ValueError:
        await ctx.send("Invalid time format. Please use HH:MM")
        return

    reminders = load_reminders()
    reminders.append({
        "time": reminder_time,
        "reminder": message,
        "channel": ctx.channel.id,
        "author": ctx.author.id
    })
    save_reminders(reminders)

    await ctx.send(f"Reminder added for {reminder_time} - {message}")


bot.run(token)

