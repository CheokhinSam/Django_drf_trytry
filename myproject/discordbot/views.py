from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BotConfigSerializer

#bot


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
    

#llm

import os
from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings, AzureOpenAI

load_dotenv()

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_BASE = os.getenv("AZURE_OPENAI_ENDPOINT")
EMBEDDING_DEPLOYMENT = os.getenv("EMBEDDING_DEPLOYMENT")
LLM_DEPLOYMENT = os.getenv("LLM_DEPLOYMENT")

from rest_framework.decorators import api_view
from rest_framework.response import Response
from langchain_openai import AzureChatOpenAI

@api_view(['POST'])
def llm_api(request):
    question = request.data.get('question')
    if not question:
        return Response({"error": "Question is required"}, status=400)
    
    llm = AzureChatOpenAI(
        azure_deployment=LLM_DEPLOYMENT,
        api_key=AZURE_OPENAI_API_KEY,
        azure_endpoint=AZURE_OPENAI_API_BASE,
        api_version="2023-05-15"
    )
    
    system_message = "You are a helpful assistant."
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": question}
    ]
    
    try:
        response = llm(messages)
        return Response({"response": response.content})
    except Exception as e:
        return Response({"error": str(e)}, status=500)