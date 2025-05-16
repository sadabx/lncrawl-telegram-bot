import os
import subprocess
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Set your bot token here
BOT_TOKEN = '7781934391:AAF-GSp5sXPXdLVLdgb5G31qNrx8pdTn_gs'

DOWNLOAD_DIR = 'Lightnovels'

# Ensure the download directory exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a novel URL or name to download!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    if query.startswith("http"):
        cmd = [
            "lncrawl",
            "-s", query,
            "--format", "epub",
            "--output", DOWNLOAD_DIR,
            "--single",
            "--suppress"
        ]
    else:
        cmd = [
            "lncrawl",
            "-q", query,
            "--format", "epub",
            "--output", DOWNLOAD_DIR,
            "--single",
            "--suppress"
        ]

    await update.message.reply_text("Downloading, please wait...")

    try:
        subprocess.run(cmd, check=True)
        files = os.listdir(DOWNLOAD_DIR)
        epub_files = [f for f in files if f.endswith('.epub')]

        if not epub_files:
            await update.message.reply_text("❌ Download failed or no EPUB found.")
            return

        file_path = os.path.join(DOWNLOAD_DIR, epub_files[-1])
        await update.message.reply_document(document=open(file_path, 'rb'))
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
