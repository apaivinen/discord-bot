import discord
from discord.ext import commands
import os

print(f'Loading bot...')

# Load bot token from environment variables
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Create a bot instance with command prefix '/'
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="/", intents=intents)

# Event: On bot ready
@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')

# Command: /annabelle
@bot.command()
async def annabelle(ctx):
    await ctx.send("Hello! I'm Annabelle. How can I help you today?")

# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN)
