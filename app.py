import discord
from discord.ext import commands
import os
from fastapi import FastAPI
import uvicorn
import aiohttp

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

# Function to split text into chunks of 2000 characters or less
def split_message(content, max_length=2000):
    return [content[i:i + max_length] for i in range(0, len(content), max_length)]

# --- Event: Respond when the bot is mentioned ---
@bot.event
async def on_message(message):
    # Check if the bot is mentioned and ignore messages from other bots
    if bot.user in message.mentions and not message.author.bot:
        # Remove the bot mention from the message content
        cleaned_message = message.content.replace(f"<@{bot.user.id}>", "").strip()

        # URL to query
        url = "https://chatgpt.com/g/g-678275c1d07481918d518ffe6a87b791-phasmophobia-guide"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        # Retrieve and decode the content
                        page_content = await response.text()

                        # Split the content into chunks of 2000 characters
                        chunks = split_message(page_content)

                        # Send each chunk as a separate message
                        for chunk in chunks:
                            await message.reply(chunk)
                    else:
                        # Handle non-200 status codes
                        await message.reply(f"Sorry {message.author.mention}, I couldn't retrieve the page. Status code: {response.status}")
            except Exception as e:
                # Handle request errors
                await message.reply(f"An error occurred: {str(e)}")

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
