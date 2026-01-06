# telegram_listener.py
import requests
import os
from bot_users import save_user,user_exists

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def get_updates(offset=None):
    params = {"timeout": 100}
    if offset:
        params["offset"] = offset
    return requests.get(f"{URL}/getUpdates", params=params).json()

def send_message(chat_id, text):
    requests.post(f"{URL}/sendMessage", data={
        "chat_id": chat_id,
        "text": text
    })

def listen():
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates.get("result", []):
            offset = update["update_id"] + 1

            if "message" not in update:
                continue

            message = update["message"]
            chat_id = message["chat"]["id"]
            text = message.get("text", "")

            if text == "/start":
                if user_exists(chat_id):
                    send_message(
                        chat_id,
                        "✅ Already subscribed, you will receive the updates 😄"
                    )
                else:
                    save_user(chat_id)
                    send_message(
                        chat_id,
                        "🎮 You’re subscribed to Epic Free Games alerts!"
                    )


if __name__ == "__main__":
    listen()
