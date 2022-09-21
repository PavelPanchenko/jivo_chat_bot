import json
import logging

import requests

from src.settings.config import SEND_URL


def is_online():
    return requests.get(f"{SEND_URL}/status").json()


async def send_to_jivo_chat_message(message, text):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15",
        "Accept": "*/*",
        "Content-Type": "application/json"
    }
    payload = {
        "sender": {
            "id": str(message.chat.id),
            "name": message.chat.full_name,
            "photo": "https://cdn.icon-icons.com/icons2/2506/PNG/512/user_icon_150670.png",
            "phone": str(message.chat.id)
        },
        "message": {
            "type": "text",
            "id": "Новое сообщение",
            "text": text
        }
    }
    try:
        response = requests.post(SEND_URL, data=json.dumps(payload), headers=headers).status_code
        return response
    except Exception as ex:
        logging.warning(ex)
