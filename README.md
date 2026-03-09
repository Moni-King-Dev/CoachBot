# 🤖 CoachBot – Telegram Quiz Bot

CoachBot is a lightweight Telegram bot that delivers **multiple-choice quiz questions**, tracks **user scores**, and maintains a **leaderboard** to encourage learning and competition.

The bot loads quiz questions from a JSON file and allows users to interact through simple Telegram commands.

---

## ✨ Features

* 🧠 **Multiple-Choice Quizzes**
  Loads questions from `questions.json` and presents them interactively.

* 📊 **Score Tracking**
  Tracks user scores across quiz sessions.

* 🏆 **Leaderboard**
  Displays top users based on their quiz performance.

* ⚡ **Simple & Lightweight**
  Easy to deploy and run with minimal configuration.

---

## 🛠 Requirements

* Python **3.9+**
* `python-telegram-bot` (v20+)
* `requests`

Install dependencies:

```bash
pip install python-telegram-bot==21.0.1 requests
```

---

## ⚙️ Configuration

Edit **`bot.py`** and set the following values:

* `BOT_TOKEN` – Your Telegram bot token from BotFather
* `WEBHOOK_URL` – URL where quiz results can be sent (optional)

---

## ▶️ Running the Bot

Start the bot:

```bash
python bot.py
```

Make sure:

* Your **Telegram bot token is valid**
* The bot is started from Telegram

---

## 📱 Available Commands

| Command        | Description                 |
| -------------- | --------------------------- |
| `/start`       | Shows welcome message       |
| `/quiz`        | Starts a quiz session       |
| `/leaderboard` | Displays top users by score |

---

## 📂 Project Files

* `bot.py` – Main Telegram bot logic
* `questions.json` – Quiz questions database

---

## 📜 License

This project is currently unlicensed.
If you plan to reuse or distribute it, consider adding a license such as MIT or Apache 2.0.
