import os
import json
from datetime import datetime, timedelta
import discord
from discord.ext import commands, tasks


REMINDER_FILE = 'reminders.json'


def load_reminders():
    if os.path.exists(REMINDER_FILE):
        with open(REMINDER_FILE, 'r') as f:
            return json.load(f)
    return []


def save_reminders(reminders):
    with open(REMINDER_FILE, 'w') as f:
        json.dump(reminders, f)


class Reminder(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.reminders = load_reminders()
        self.remind.start()
        print(f"cog loaded: {self.qualified_name}")

    def cog_unload(self):
        self.remind.cancel()
        print(f"cog unloaded: {self.qualified_name}")

    @tasks.loop(seconds=10)
    async def remind(self):
        now = datetime.now()

        for reminder in self.reminders:
            next_time = datetime.fromisoformat(reminder['next_time'])
            if not reminder['done'] and reminder['next_time'] <= now:
                channel = self.bot.get_channel(reminder['channel_id'])
                await channel.send(f"Reminder: {reminder['message']}")
                reminder['done'] = True
                reminder['next_time'] = (next_time + timedelta(seconds=reminder['interval'])).isoformat()





