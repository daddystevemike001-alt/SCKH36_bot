import os
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Read the Bot Token from Railway's environment variables
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Triggered when a user sends /start."""
    welcome_text = (
        "👋 **Welcome to the Character & Word Counter Bot!**\n\n"
        "Send me any text, and I will instantly analyze it for you and check "
        "how it fits into common social media limits!"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def analyze_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Triggered whenever a user sends text to the bot."""
    text = update.message.text
    
    # Core calculations
    char_count_with_spaces = len(text)
    char_count_no_spaces = len(text.replace(" ", "").replace("\n", "").replace("\r", ""))
    word_count = len(text.split()) if text.strip() else 0
    
    # Basic sentence splitter (counts ending periods, exclamation marks, and question marks)
    sentences = len(re.split(r'[.!?]+', text)) - 1
    sentences = max(1, sentences) if word_count > 0 else 0
    
    # Paragraphs (separated by double newlines)
    paragraphs = len([p for p in text.split('\n\n') if p.strip()]) if text.strip() else 0

    # Format the platform limits comparison
    def get_status_icon(count, limit):
        return "✅ Fit" if count <= limit else "❌ Over limit"

    # Compile a beautiful report
    report = (
        f"📊 **Your Text Analysis:**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📝 **Words:** {word_count}\n"
        f"🔤 **Characters (with spaces):** {char_count_with_spaces}\n"
        f"🔤 **Characters (no spaces):** {char_count_no_spaces}\n"
        f"💬 **Sentences:** {sentences}\n"
        f"📂 **Paragraphs:** {paragraphs}\n\n"
        f"📱 **Social Media Limits:**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"• **SMS (160 Chars):** {get_status_icon(char_count_with_spaces, 160)} ({char_count_with_spaces}/160)\n"
        f"• **X / Twitter (280 Chars):** {get_status_icon(char_count_with_spaces, 280)} ({char_count_with_spaces}/280)\n"
        f"• **Meta Description (160 Chars):** {get_status_icon(char_count_with_spaces, 160)} ({char_count_with_spaces}/160)\n"
        f"• **Instagram Caption (2,200 Chars):** {get_status_icon(char_count_with_spaces, 2200)} ({char_count_with_spaces}/2200)\n"
    )

    await update.message.reply_text(report, parse_mode="Markdown")

if __name__ == "__main__":
    if not BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set.")
        exit(1)

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register the command and message handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analyze_text))

    print("Bot is starting up... Polling for messages.")
    # drop_pending_updates prevents processing old messages on reboot
    app.run_polling(drop_pending_updates=True)
