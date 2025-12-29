<img width="1200" height="630" alt="EPIC_GAME" src="https://github.com/user-attachments/assets/384c8d7f-b312-4f11-8eb1-86671d028bde" />

# Epic Free Games Bot (Telegram)

Epic Free Games Bot is an automated Telegram bot that monitors the Epic Games Store for free game giveaways and sends timely notifications to a configured Telegram chat. This project is designed to ensure that users never miss a free game release by automating the monitoring and notification process.

## Overview

The bot periodically checks the Epic Games Store for currently available free games. When a new free game is detected, it sends a notification message to a Telegram chat with the game name and store link. To avoid repeated alerts, the bot maintains a local record of games that have already been notified.

## Features

The system automatically tracks free games on the Epic Games Store, sends real time Telegram notifications, prevents duplicate messages by storing previously detected games, and supports scheduled automation using GitHub Actions or cron jobs.

## Working Mechanism

The script fetches free game data from the Epic Games Store and compares it against a locally stored list of previously notified games. If a new game is identified, a Telegram message is sent to the configured chat. The game information is then stored locally to ensure the same game is not notified again.

## Technology Stack

The project is developed using Python and integrates with the Telegram Bot API for messaging functionality. HTTP requests are handled using the Requests library. Optional automation is supported through GitHub Actions.

## Project Structure

epic_free_game.py contains the core bot logic  
sent_games.json stores the record of notified games  
requirements.txt lists project dependencies  
README.md provides documentation

## Installation and Setup

Clone the repository using the link below and install the required dependencies using pip.

🔗 https://github.com/sahiljahagirdar/epic-free-games-bot

Ensure Python is installed on the system before running the script.

## Telegram Configuration

Create a Telegram bot using BotFather and obtain the bot token. Retrieve the chat ID where notifications should be sent. Configure the following environment variables before execution.

TELEGRAM_BOT_TOKEN containing the Telegram bot token  
TELEGRAM_CHAT_ID containing the Telegram chat ID  

For automated execution using GitHub Actions, these values should be stored as repository secrets.

## Execution

Run the Python script to start the bot. When a new free game becomes available on the Epic Games Store, a notification will be sent to the configured Telegram chat.

## Example Notification Format

New Free Game on Epic Games  
Game Name  
🔗 https://store.epicgames.com/

## Automation

The bot can be scheduled to run automatically at regular intervals using GitHub Actions or system cron jobs, enabling continuous monitoring without manual intervention.

## Repository

🔗 https://github.com/sahiljahagirdar/epic-free-games-bot

## Author

Sahil Jahagirdar

