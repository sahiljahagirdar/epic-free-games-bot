import requests
import json
import os
from datetime import datetime, timezone
from bot_users import get_all_users

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
URL = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "sent_games.json")

def load_sent_games():
    if not os.path.exists(DATA_FILE):
        return set()
    with open(DATA_FILE, "r") as f:
        return set(json.load(f))

def save_sent_games(game_ids):
    with open(DATA_FILE, "w") as f:
        json.dump(list(game_ids), f)

def get_free_games():
    response = requests.get(URL)
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

def send_telegram_message(message):
    users = get_all_users()
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    for chat_id in users:
        requests.post(url, data={
            "chat_id": chat_id,
            "text": message
        })

if __name__ == "__main__":
    sent_games = load_sent_games()
    free_games = get_free_games()

    new_games = [g for g in free_games if g["id"] not in sent_games]

    if not new_games:
        print("No new free games.")
        exit()

    message = "🎮 New Free Games on Epic Games!\n\n"
    for game in new_games:
        message += f"• {game['title']}\n"
        message += f"https://store.epicgames.com/en-US/p/{game['slug']}\n\n"
        sent_games.add(game["id"])

    send_telegram_message(message)
    save_sent_games(sent_games)
