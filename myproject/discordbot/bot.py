# bot.py
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# 加載 .env 文件
load_dotenv()

# 從 .env 中獲取 token
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Bot is ready.')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello, world!')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

bot.run(TOKEN)