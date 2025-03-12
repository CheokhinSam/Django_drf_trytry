from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BotConfigSerializer

    #bot

# myapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BotConfigSerializer

# Discord bot 代碼模板
BOT_CODE_TEMPLATE = """
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
        # 驗證輸入數據
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
            bot_code = BOT_CODE_TEMPLATE.format(prefix=prefix, commands_code=commands_code)

            # 構建響應
            response_data = {
                "bot_code": bot_code,
                "instructions": [
                    "Install discord.py: pip install discord.py",
                    "Create a .env file with: DISCORD_TOKEN=your_token_here",
                    "Update bot.py to use python-dotenv (see example below)",
                    "Save as bot.py and run: python bot.py"
                ],
                "env_example": "Add this to bot.py to use .env:\n"
                              "import os\n"
                              "from dotenv import load_dotenv\n"
                              "load_dotenv()\n"
                              "bot.run(os.getenv('DISCORD_TOKEN'))"
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        # 返回驗證錯誤
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)