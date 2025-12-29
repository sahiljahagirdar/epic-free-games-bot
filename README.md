
<img width="1200" height="630" alt="EPIC_GAME" src="https://github.com/user-attachments/assets/951e907a-839d-4af7-a6cc-79c21f54c28b" />


## 🌟 Overview

Epic Free Games Bot is a Python-based automation tool designed to monitor the Epic Games Store for promotional free game offerings. The application continuously checks for new releases and sends instant notifications through Telegram, ensuring users never miss limited-time free game opportunities. The system implements intelligent duplicate detection to prevent notification spam.

## ✨ Features

- 🔄 **Automated Monitoring** - Periodic checks of the Epic Games Store API for current free game promotions
- 📱 **Real-Time Notifications** - Instant Telegram messages when new free games are detected
- 🚫 **Duplicate Prevention** - Maintains a persistent record of previously notified games to avoid redundant alerts
- ⏰ **Flexible Scheduling** - Supports both GitHub Actions and cron-based automation
- 🪶 **Lightweight Design** - Minimal resource footprint with efficient API usage
- ⚙️ **Easy Configuration** - Simple environment variable-based setup

## 🔧 How It Works

```mermaid
graph LR
    A[Fetch Free Games] --> B{New Game?}
    B -->|Yes| C[Send Telegram Notification]
    B -->|No| D[Skip]
    C --> E[Update sent_games.json]
    E --> F[Wait for Next Check]
    D --> F
```

1. **Data Retrieval** - Fetches current free game listings from the Epic Games Store API
2. **State Comparison** - Compares retrieved data against local notification history stored in `sent_games.json`
3. **Notification Dispatch** - Sends formatted Telegram messages for newly detected free games
4. **State Persistence** - Updates local storage with newly notified games to prevent duplicates

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Language** | Python 3.7+ |
| **HTTP Client** | Requests library |
| **Messaging** | Telegram Bot API |
| **Automation** | GitHub Actions |
| **Storage** | JSON file-based persistence |

## 📦 Installation

### Prerequisites

- Python 3.7 or higher
- Telegram account
- Active internet connection

### Setup Steps

### Setup Steps

**1. Clone the repository:**

```bash
git clone https://github.com/sahiljahagirdar/epic-free-games-bot.git
cd epic-free-games-bot
```

**2. Install required dependencies:**

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### 🤖 Telegram Bot Setup

#### Step 1: Create Your Bot
   - Open Telegram and search for [@BotFather](https://t.me/BotFather)
   - Send `/newbot` command and follow the prompts
   - Save the provided bot token

2. **Obtain Chat ID**:
   - Start a conversation with your bot
   - Send any message to the bot
   - Visit `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Locate the `chat.id` field in the response

### Environment Variables

Configure the following environment variables:

```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
```

For **GitHub Actions** automation, add these as repository secrets:
- Navigate to Settings → Secrets and variables → Actions
- Add `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`

## Usage

### Manual Execution

Run the bot directly from the command line:

```bash
python epic_free_game.py
```

### Sample Notification

When a free game is detected, you'll receive a Telegram message in the following format:

```
🎮 New Free Game on Epic Games Store!

Game Title: [Game Name]
🔗 Claim Now: https://store.epicgames.com/

Don't miss out on this limited-time offer!
```

## Automation

### GitHub Actions

The repository includes a workflow configuration for automated execution:

- Scheduled runs at configurable intervals
- Automatic dependency installation
- Secure credential management via GitHub Secrets

### Cron Jobs

For local or server deployment, configure a cron job:

```bash
# Run every hour
0 * * * * /usr/bin/python3 /path/to/epic-free-games-bot/epic_free_game.py
```

## Project Structure

```
epic-free-games-bot/
├── epic_free_game.py      # Main application logic
├── sent_games.json        # Notification history (auto-generated)
├── requirements.txt       # Python dependencies
├── .github/
│   └── workflows/         # GitHub Actions configurations
├── README.md              # Documentation
└── LICENSE                # License information
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/enhancement`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/enhancement`)
5. Open a Pull Request


## Author

**Sahil Jahagirdar**

- GitHub: [@sahiljahagirdar](https://github.com/sahiljahagirdar)
- Repository: [epic-free-games-bot](https://github.com/sahiljahagirdar/epic-free-games-bot)

---

**Note**: This bot is an independent project and is not affiliated with or endorsed by Epic Games. Please review Epic Games' Terms of Service and ensure compliance when using automated tools to access their services.
