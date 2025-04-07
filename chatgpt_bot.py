import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

BOT_TOKEN = "7789834661:AAHNc2RRSv4iwlUp9el6XDTGM52cEi9HuF4"
OPENROUTER_API_KEY = "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"

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# GPT response function
def get_gpt_response(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://t.me/YOUR_BOT_USERNAME",  # optional
        "X-Title": "TelegramBot"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        content = response.json()['choices'][0]['message']['content']
        return content + " 🤖"
    else:
        return f"❌ Error: {response.status_code}"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! 🤖 I'm your GPT bot. Just send me a message.")

# Handle messages
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    await update.message.chat.send_action(action="typing")
    response = get_gpt_response(msg)
    await update.message.reply_text(response)

# Main runner
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    print("🤖 Bot is running 24/7 (on server)...")
    app.run_polling()

if __name__ == "__main__":
    main()