from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text="Привет!")


@router.message()
async def echo(message: Message):
    await message.answer(text="Я не знаю эту команду 🤷🏻‍♂️")
