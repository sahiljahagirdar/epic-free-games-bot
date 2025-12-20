import requests
import json
import os
from datetime import datetime, timezone

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

                if not (start <= now <= end):
                    continue

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


if __name__ == "__main__":
    sent_games = load_sent_games()
    free_games = get_free_games()

    new_games = [g for g in free_games if g["id"] not in sent_games]

    if not new_games:
        print("No new free games.")
    else:
        print("🎮 NEW Free Games on Epic Games:\n")
        for game in new_games:
            link = f"https://store.epicgames.com/en-US/p/{game['slug']}"
            print(f"• {game['title']}")
            print(f"  Claim: {link}\n")
            sent_games.add(game["id"])

        save_sent_games(sent_games)
