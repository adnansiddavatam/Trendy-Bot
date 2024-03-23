from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Emojis
SUCCESS_EMOJI = "✅"
ERROR_EMOJI = "❌"
SEARCH_EMOJI = "🔍"

def google_search(query):
    api_key = "3506cca21164d40ab27ae2918eebc4dce2ad27eb0d98b7a7f90ca3d3665df1d1"  # Replace with your actual SerpApi key
    url = f"https://serpapi.com/search.json?engine=google&q={query}&api_key={api_key}"

    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get('organic_results', [])

        search_results = ""
        for i, result in enumerate(results[:5], start=1):
            title = result['title']
            link = result['link']
            search_results += f"{i}. {title}\n   {link}\n"

        return search_results
    else:
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Hi! Please use /search <query> {SEARCH_EMOJI} to search Google.')

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if not args:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Please provide a search query.')
        return
    query = ' '.join(args)
    logger.info(f"Searching Google for: {query}")
    search_results = google_search(query)
    if search_results:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=search_results)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{ERROR_EMOJI} Error searching Google. Please try again later.")

def main() -> None:
    application = Application.builder().token("6818899701:AAFQWTesKlamnHSezxCHfxj2sbIramIqkMM").build()  # Replace with your Telegram bot token

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search))

    logger.info("Bot started successfully.")
    application.run_polling()

if __name__ == '__main__':
    main()