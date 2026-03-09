## CoachBot

CoachBot is a simple Telegram quiz bot that asks multiple-choice questions and keeps track of user scores with a leaderboard.

### Features

- Multiple-choice quiz questions loaded from `questions.json`
- Score tracking across quiz sessions
- Simple leaderboard that shows top users by score

### Requirements

- Python 3.9+
- `python-telegram-bot` (v20+)
- `requests`

Install dependencies:

```bash
pip install python-telegram-bot==21.0.1 requests
```

### Configuration

In `bot.py`, set:

- `BOT_TOKEN` to your Telegram bot token
- `WEBHOOK_URL` to the URL where you want quiz results to be sent (or leave as a dummy value if you do not need webhooks)

### Running the bot

Run the bot with:

```bash
python bot.py
```

Make sure your bot is started in Telegram and that the token is valid. Then you can use:

- `/start` to see the welcome message
- `/quiz` to start a quiz
- `/leaderboard` to see top scores

