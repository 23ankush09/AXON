import os
import discord
from discord.ext import commands
import openai
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
openai.api_key = os.getenv('OPENAI_API_KEY')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} is online!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore own messages

    # Check if bot is mentioned (tagged)
    if bot.user.mentioned_in(message):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Or gpt-4 if available
                messages=[{"role": "user", "content": message.content.replace(f'<@{bot.user.id}>', '').strip()}]
            )
            await message.channel.send(response.choices[0].message.content)
        except Exception as e:
            await message.channel.send("Sorry, I had an issue responding.")

    await bot.process_commands(message)

bot.run(TOKEN)
