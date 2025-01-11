import discord
from discord.ext import commands
import os
from fastapi import FastAPI
import uvicorn
import requests  # Added to handle HTTP requests
import json

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

# --- Event: On bot ready ---
@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')

# --- Event: Respond when the bot is mentioned ---
@bot.event
async def on_message(message):
    # Check if the bot is mentioned and ignore messages from other bots
    if bot.user in message.mentions and not message.author.bot:
        # Remove the bot mention from the message content
        cleaned_message = message.content.replace(f"<@{bot.user.id}>", "").strip()

        # HTTP POST request to the specified endpoint
        url = "https://gamingbuddy-wiki-demo.swedencentral.inference.ml.azure.com/score"
        API_AUTH_TOKEN = os.getenv('API_AUTH_TOKEN')

        if not API_AUTH_TOKEN:
            await message.reply(f"{message.author.mention}, API key is missing.")
            return

        headers = {
            "Authorization": f"Bearer {API_AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {"question": cleaned_message}

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            reply_content = result.get("answer", "I'm not sure how to respond to that.")
        except requests.exceptions.RequestException as e:
            reply_content = f"An error occurred: {str(e)}"

        # Reply with the response from the API
        await message.reply(f"{message.author.mention}, {reply_content}")

    # Process other bot commands
    await bot.process_commands(message)

# --- Group Command: /annabelle ---
@bot.group()
async def annabelle(ctx):
    if ctx.invoked_subcommand is None:
        subcommands = [cmd.name for cmd in annabelle.commands]
        subcommands_list = "\n".join(f"- `/annabelle {cmd}`" for cmd in subcommands)
        await ctx.reply(
            f"Hi! Here are the available `/annabelle` commands:\n{subcommands_list}"
        )

# --- Subcommand: /annabelle hello ---
@annabelle.command()
async def hello(ctx):
    await ctx.reply("Hello! I'm Annabelle. How can I help you today?")

# --- Run the bot ---
if __name__ == "__main__":
    # Start the FastAPI web server in a separate thread
    from threading import Thread
    server = Thread(target=lambda: uvicorn.run(app, host="0.0.0.0", port=8000))
    server.start()

    # Start the Discord bot
    print("Starting the bot...")
    bot.run(TOKEN)
