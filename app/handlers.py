from asyncio import sleep

from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums import ChatAction

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING
    )
    await sleep(1)
    await message.answer(text="Привет!")


@router.message()
async def echo(message: Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING
    )
    await sleep(1)
    await message.answer(text="Я не знаю эту команду 🤷🏻‍♂️")
