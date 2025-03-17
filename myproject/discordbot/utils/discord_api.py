import requests
from nacl.signing import VerifyKey
import logging
from dotenv import load_dotenv
import os

# 加載 .env 文件
load_dotenv()

# 配置日誌
logging.basicConfig(level=logging.INFO)

def verify_key(raw_body: bytes, signature: str, timestamp: str, client_public_key: str):
    """驗證 Discord Webhook 請求的簽名"""
    if not all([raw_body, signature, timestamp, client_public_key]):
        logging.error("Missing required parameters for signature verification")
        return False
    message = f'{timestamp}{raw_body.decode("utf-8")}'.encode()
    try:
        vk = VerifyKey(bytes.fromhex(client_public_key))
        vk.verify(message, bytes.fromhex(signature))
        return True
    except Exception as ex:
        logging.error(f"Signature verification failed: {ex}")
        return False

def create_app_command(app_id, sk):
    """創建 Discord 應用命令"""
    url = f"https://discord.com/api/v10/applications/{app_id}/commands"
    json = {
        "name": "qpygpt",
        "type": 1,
        "description": "Chat with AI",
        "options": [
            {"name": "query", "description": "query text", "type": 3, "required": True}
        ]
    }
    headers = {"Authorization": f"Bot {os.getenv('DISCORD_BOT_TOKEN', sk)}"}
    try:
        res = requests.post(url, headers=headers, json=json)
        res.raise_for_status()
        return res.text
    except requests.RequestException as ex:
        logging.error(f"Failed to create command: {ex}")
        return str(ex)

def edit_origin_interaction_message(app_id, interaction_token, content):
    """編輯 Discord Webhook 的原始消息"""
    url = f"https://discord.com/api/v10/webhooks/{app_id}/{interaction_token}/messages/@original"
    json = {"content": content}
    headers = {"Authorization": f"Bot {os.getenv('DISCORD_BOT_TOKEN')}"}
    try:
        res = requests.patch(url, json=json, headers=headers)
        res.raise_for_status()
        return res.text
    except requests.RequestException as ex:
        logging.error(f"Failed to edit message: {ex}")
        return str(ex)