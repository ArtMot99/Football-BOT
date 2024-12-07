import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart

load_dotenv()

bot = Bot(
    token=os.getenv("TOKEN")
)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text="Привет!")


@dp.message()
async def echo(message: Message):
    await message.answer(text="Я не знаю эту команду 🤷🏻‍♂️")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
