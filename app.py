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

        # List available commands
        available_commands = """
        **Available Commands:**
        - `/annabelle hello` — Say hello to Annabelle
        """

        # Reply with a response including the cleaned message
        response = f"Hello {message.author.mention}! You mentioned me with:\n> {cleaned_message}\n\n{available_commands}"
        await message.reply(response)

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
