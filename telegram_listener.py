import requests
from bot_users import save_user

BOT_TOKEN = "YOUR_BOT_TOKEN"
URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def get_updates(offset=None):
    params = {"timeout": 100}
    if offset:
        params["offset"] = offset
    return requests.get(f"{URL}/getUpdates", params=params).json()

def handle_updates():
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates["result"]:
            offset = update["update_id"] + 1

            if "message" in update:
                message = update["message"]
                chat_id = message["chat"]["id"]
                text = message.get("text", "")

                if text == "/start":
                    save_user(chat_id)
                    send_message(chat_id, "🎮 You’ll now receive Epic Free Games alerts!")

def send_message(chat_id, text):
    requests.post(f"{URL}/sendMessage", data={
        "chat_id": chat_id,
        "text": text
    })

if __name__ == "__main__":
    handle_updates()
