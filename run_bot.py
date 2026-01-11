import asyncio
import logging
import os

from dotenv import load_dotenv

from bot.main import main

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        logging.error("TELEGRAM_BOT_TOKEN not found in .env file. Please add it.")
    else:
        try:
            asyncio.run(main(bot_token=bot_token))
        except (KeyboardInterrupt, SystemExit):
            logging.info("Bot stopped")
