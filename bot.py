import json
import random
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# =============================
# CONFIGURATION
# =============================

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
WEBHOOK_URL = "YOUR_WEBHOOK_URL_HERE"

user_scores = {}

# =============================
# LOAD QUESTIONS
# =============================

def load_questions():
    with open("questions.json", "r", encoding="utf-8") as f:
        return json.load(f)

# =============================
# START COMMAND
# =============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message"""
    message = (
        "👋 Welcome to ICF Quiz Bot!\n\n"
        "📝 Use /quiz to start a quiz.\n"
        "🏆 Use /leaderboard to see top scores."
    )
    await update.message.reply_text(message)

# =============================
# QUIZ COMMAND
# =============================

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the quiz"""
    user_id = update.effective_user.id
    questions = load_questions()
    random.shuffle(questions)

    context.user_data["questions"] = questions[:5]  # pick 5 random questions
    context.user_data["current_question"] = 0
    context.user_data["score"] = 0

    await send_question(update, context)

async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send the current question"""
    current_index = context.user_data["current_question"]
    questions = context.user_data["questions"]

    if current_index >= len(questions):
        await end_quiz(update, context)
        return

    question = questions[current_index]
    options = question["options"]

    keyboard = [[InlineKeyboardButton(opt, callback_data=opt)] for opt in options]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.message.reply_text(question["question"], reply_markup=reply_markup)
    else:
        await update.message.reply_text(question["question"], reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle answer button clicks"""
    query = update.callback_query
    await query.answer()

    selected_option = query.data
    current_index = context.user_data["current_question"]
    questions = context.user_data["questions"]
    correct_answer = questions[current_index]["answer"]

    if selected_option == correct_answer:
        context.user_data["score"] += 1
        await query.edit_message_text(f"✅ Correct!\n\nAnswer: {correct_answer}")
    else:
        await query.edit_message_text(f"❌ Wrong!\n\nCorrect Answer: {correct_answer}")

    context.user_data["current_question"] += 1
    await send_question(update, context)

async def end_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Finish the quiz and send score"""
    user_id = update.effective_user.id
    score = context.user_data["score"]
    total_questions = len(context.user_data["questions"])

    # Store user score
    user_scores[user_id] = user_scores.get(user_id, 0) + score

    result_message = (
        f"🎉 Quiz completed!\n"
        f"You scored {score}/{total_questions} points.\n"
        f"🏆 Your total points: {user_scores[user_id]}"
    )

    # Send results to Webhook.site
    payload = {
        "user_id": user_id,
        "username": update.effective_user.username,
        "score": score,
        "total_score": user_scores[user_id]
    }
    try:
        requests.post(WEBHOOK_URL, json=payload)
    except Exception as e:
        logging.error(f"Failed to send webhook: {e}")

    await update.effective_message.reply_text(result_message)

# =============================
# LEADERBOARD
# =============================

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not user_scores:
        await update.message.reply_text("🏆 No scores yet. Play a quiz with /quiz!")
        return

    sorted_scores = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)
    leaderboard_text = "🏆 *Leaderboard*\n\n"
    for i, (user_id, score) in enumerate(sorted_scores[:10], 1):
        leaderboard_text += f"{i}. User {user_id}: {score} points\n"

    await update.message.reply_text(leaderboard_text, parse_mode="Markdown")

# =============================
# MAIN FUNCTION
# =============================

def main():
    logging.basicConfig(level=logging.INFO)
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(CallbackQueryHandler(button))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
