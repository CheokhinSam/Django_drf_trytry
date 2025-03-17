from langchain_ollama import OllamaLLM
import logging
from dotenv import load_dotenv
import os

# 加載 .env 文件
load_dotenv()

logging.basicConfig(level=logging.INFO)
llm = OllamaLLM(model="deepseek-r1:1.5b", base_url="http://localhost:11434")

def generate_ai_response(message):
    try:
        response_msg = llm.invoke(message)
    except Exception as e:
        logging.error(f"LLM invocation failed: {e}")
        response_msg = f"Error: {str(e) if str(e) else 'Error with local model'}"
    return response_msg