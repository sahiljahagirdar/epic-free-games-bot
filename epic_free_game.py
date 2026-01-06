import requests
import json
import os
from datetime import datetime, timezone
from bot_users import get_all_users


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
EPIC_API_URL = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SENT_GAMES_FILE = os.path.join(BASE_DIR, "sent_games.json")
WELCOME_FILE = os.path.join(BASE_DIR, "welcomed_users.json")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


def load_json_set(path):
    if not os.path.exists(path):
        return set()
    with open(path, "r") as f:
        try:
            return set(json.load(f))
        except json.JSONDecodeError:
            return set()

def save_json_set(path, data_set):
    with open(path, "w") as f:
        json.dump(list(data_set), f)


def send_welcome_messages():
    users = get_all_users()
    welcomed_users = load_json_set(WELCOME_FILE)

    for chat_id in users:
        if chat_id not in welcomed_users:
            requests.post(
                TELEGRAM_API_URL,
                data={
                    "chat_id": chat_id,
                    "text": (
                        "🎉 *Yay! You’re subscribed to the Epic Free Games Bot* 🎮\n\n"
                        "You’ll now receive alerts whenever Epic Games releases free games.\n"
                        "Sit back and enjoy free gaming! 🚀"
                    ),
                    "parse_mode": "Markdown"
                },
                timeout=10
            )
            welcomed_users.add(chat_id)

    save_json_set(WELCOME_FILE, welcomed_users)


def load_sent_games():
    return load_json_set(SENT_GAMES_FILE)

def save_sent_games(game_ids):
    save_json_set(SENT_GAMES_FILE, game_ids)

def get_free_games():
    response = requests.get(EPIC_API_URL, timeout=20)
    response.raise_for_status()
    data = response.json()

    games = data["data"]["Catalog"]["searchStore"]["elements"]
    now = datetime.now(timezone.utc)

    free_games = []

    for game in games:
        promotions = game.get("promotions")
        if not promotions:
            continue

        for promo in promotions.get("promotionalOffers", []):
            for offer in promo.get("promotionalOffers", []):
                start = datetime.fromisoformat(offer["startDate"].replace("Z", "+00:00"))
                end = datetime.fromisoformat(offer["endDate"].replace("Z", "+00:00"))

                if start <= now <= end and offer["discountSetting"]["discountPercentage"] == 0:
                    slug = game.get("productSlug") or game.get("urlSlug")
                    if slug:
                        free_games.append({
                            "id": game["id"],
                            "title": game["title"],
                            "slug": slug
                        })

    return free_games

def send_game_alert(message):
    users = get_all_users()

    for chat_id in users:
        requests.post(
            TELEGRAM_API_URL,
            data={
                "chat_id": chat_id,
                "text": message
            },
            timeout=10
        )


if __name__ == "__main__":
    send_welcome_messages()

    sent_games = load_sent_games()
    free_games = get_free_games()

    new_games = [g for g in free_games if g["id"] not in sent_games]

    if not new_games:
        print("No new free games.")
        exit(0)

    message = "🎮 *New Free Games on Epic Games!*\n\n"

    for game in new_games:
        message += f"• {game['title']}\n"
        message += f"https://store.epicgames.com/en-US/p/{game['slug']}\n\n"
        sent_games.add(game["id"])

    send_game_alert(message)
    save_sent_games(sent_games)
