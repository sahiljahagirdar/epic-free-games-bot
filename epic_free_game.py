import requests
import json
import os
from datetime import datetime, timezone
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


URL = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"


DATA_FILE = "sent_games.json"


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
                start = datetime.fromisoformat(
                    offer["startDate"].replace("Z", "+00:00")
                )
                end = datetime.fromisoformat(
                    offer["endDate"].replace("Z", "+00:00")
                )

                # Offer must be active right now
                if not (start <= now <= end):
                    continue

                # Must be 100% free
                if offer["discountSetting"]["discountPercentage"] != 0:
                    continue

                slug = game.get("productSlug") or game.get("urlSlug")
                if not slug:
                    continue

                free_games.append({
                    "id": game["id"],
                    "title": game["title"],
                    "slug": slug
                })

    return free_games


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()


if __name__ == "__main__":
    sent_games = load_sent_games()
    free_games = get_free_games()

    # Detect new free games only
    new_games = [g for g in free_games if g["id"] not in sent_games]

    if not new_games:
        print("No new free games.")
    else:
        message = "🎮 New Free Games on Epic Games!\n\n"

        for game in new_games:
            link = f"https://store.epicgames.com/en-US/p/{game['slug']}"
            message += f"• {game['title']}\n"
            message += f"👉 {link}\n\n"
            sent_games.add(game["id"])

        
        print(message)
        send_telegram_message(message)

        
        save_sent_games(sent_games)
