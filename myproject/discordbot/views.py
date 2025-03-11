from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BotConfigSerializer

# bot 代碼模板
bot_code_template = """
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='{prefix}', intents=intents)

@bot.event
async def on_ready():
    print('Bot is ready.')

{commands_code}

bot.run('YOUR_TOKEN_HERE')
"""

class GenerateBotView(APIView):
    def post(self, request):
        serializer = BotConfigSerializer(data=request.data)
        if serializer.is_valid():
            prefix = serializer.validated_data['prefix']
            commands = serializer.validated_data['commands']
            # 生成命令代碼
            commands_code = "\n".join([
                f"@bot.command()\nasync def {cmd['name']}(ctx):\n    await ctx.send('''{cmd['response']}''')"
                for cmd in commands
            ])
            # 填充模板
            bot_code = bot_code_template.format(prefix=prefix, commands_code=commands_code)
            # 準備響應數據
            response_data = {
                "bot_code": bot_code,
                "instructions": [
                    "Install discord.py: pip install discord.py",
                    "Get your bot token from https://discord.com/developers/applications",
                    "Replace 'YOUR_TOKEN_HERE' with your token",
                    "Save as bot.py and run: python bot.py"
                ]
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)