from asyncio import sleep
from aiogram import F, Router
from aiogram.types import Message, PollAnswer
from aiogram.filters import CommandStart
from aiogram.enums import ChatAction

import app.keyboards as kb

router = Router()
votes = set()  # Set с проголосовавшими за вариант 0 в опросе

# ID группы, куда отправляется опрос
GROUP_CHAT_ID = -1002283871042


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        text="Выберете пункт меню",
        reply_markup=kb.main
    )


@router.message(F.text == "Начать опрос")
async def send_poll(message: Message):
    question = "Идешь на тренировку?"
    options = ["Да", "Не знаю", "Нет"]
    is_anonymous = False

    # Отправляем опрос в группу
    poll_message = await message.bot.send_poll(
        chat_id=GROUP_CHAT_ID,
        question=question,
        options=options,
        is_anonymous=is_anonymous
    )

    poll_id = poll_message.poll.id
    await message.bot.send_message(
        chat_id=message.chat.id,
        text=f"Опрос отправлен. Его ID {poll_id}"
    )


@router.poll_answer()
async def handle_poll_answer(poll_answer: PollAnswer):
    username = poll_answer.user.username
    options_ids = poll_answer.option_ids  # Выбранные варианты ответа

    if 0 in options_ids:
        votes.add(username)
    else:
        votes.discard(username)

    print(votes)


@router.message()
async def echo(message: Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING
    )
    await sleep(1)
    await message.answer(text="Я не знаю эту команду 🤷🏻‍♂️")
