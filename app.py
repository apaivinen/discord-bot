import discord
from discord.ext import commands
import os
from fastapi import FastAPI
import uvicorn

# --- FastAPI web server ---
app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Bot is alive!"}

# --- Discord Bot Setup ---
print(f'Loading bot...')

# Load bot token from environment variables
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Create a bot instance with command prefix '/'
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
bot = commands.Bot(command_prefix="/", intents=intents)

# Event: On bot ready
@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')

# Create a /annabelle group command
@bot.group()
async def annabelle(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.reply("Hi! You can use `/annabelle hello`.")

# Subcommand: /annabelle hello
@annabelle.command()
async def hello(ctx):
    await ctx.reply("Hello! I'm Annabelle. How can I help you today?")

# Run the bot
if __name__ == "__main__":
    # Start the FastAPI web server in a separate thread
    from threading import Thread
    server = Thread(target=lambda: uvicorn.run(app, host="0.0.0.0", port=8000))
    server.start()
    
    # Start the Discord bot
    print("Starting the bot...")
    bot.run(TOKEN)
