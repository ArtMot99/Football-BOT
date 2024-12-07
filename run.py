import os
import asyncio
import logging  # Not for production

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from app.handlers import router


async def main():
    load_dotenv()
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)  # Not for production

    asyncio.run(main())
