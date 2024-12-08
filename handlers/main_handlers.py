from aiogram import F, Router
from aiogram.types import Message, PollAnswer, ReplyKeyboardRemove
from aiogram.filters import CommandStart

import keyboards.main_keyboard as kb
from messages.date_time_messages import message_for_group_about_training, input_training_time
from messages.participant_messages import caption_of_pay_photo
from states.main_states import WAITING_FOR_DATE, WAITING_FOR_PARTICIPANTS, user_state, WAITING_FOR_TIME
from constants.main_constants import GROUP_CHAT_ID, TOTAL_AMOUNT, VOTES
from validators.validators import ValidationError, validate_participants, validate_time_range, validate_date

router = Router()


@router.message(F.text == "Начать опрос")
async def send_poll(message: Message):
    question = "Идешь на тренировку?"
    options = ["Да ✅", "Не знаю 🤷🏻", "Нет ❌"]
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
        text=f"Опрос отправлен. Его ID {poll_id}",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(F.text == "Послать QR и посчитать оплату")
async def ask_for_participants(message: Message):
    user_state[message.from_user.id] = {"state": WAITING_FOR_PARTICIPANTS}
    await message.answer(
        "Введите количество участников тренировки",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(F.text == "Запланировать тренировку")
async def ask_for_date(message: Message):
    user_state[message.from_user.id] = {"state": WAITING_FOR_DATE}
    await message.answer(
        "Введите дату следующей тренировки в формате ДД.ММ.ГГГГ",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        text="Выберете пункт меню",
        reply_markup=kb.main
    )


@router.poll_answer()
async def handle_poll_answer(poll_answer: PollAnswer):
    username = poll_answer.user.username
    options_ids = poll_answer.option_ids

    if 0 in options_ids:
        VOTES.add(username)
    else:
        VOTES.discard(username)

    print(VOTES)


@router.message(F.text)
async def handle_input(message: Message):
    user_id = message.from_user.id
    current_state = user_state.get(user_id, {})

    if current_state.get("state") == WAITING_FOR_DATE:
        try:
            date = validate_date(message.text)
            user_state[user_id] = {"state": WAITING_FOR_TIME, "date": date}

            await message.answer(input_training_time)
        except ValidationError as e:
            await message.answer(str(e))

    elif current_state.get("state") == WAITING_FOR_TIME:
        try:
            time_input = message.text
            start_time, end_time = validate_time_range(time_input)
            date_obj = current_state.get("date")

            if not date_obj:
                raise ValidationError("Дата тренировки не найдена.")

            group_message = message_for_group_about_training.format(
                date=date_obj.strftime('%d.%m.%Y'),
                start_time=start_time.strftime('%H:%M'),
                end_time=end_time.strftime('%H:%M')
            )

            await message.bot.send_message(chat_id=GROUP_CHAT_ID, text=group_message)
            await message.answer("Сообщение отправлено в группу!")
            user_state.pop(user_id, None)
        except ValidationError as e:
            await message.answer(str(e))

    elif current_state.get("state") == WAITING_FOR_PARTICIPANTS:
        try:
            participants = validate_participants(message.text)
            amount_per_person = TOTAL_AMOUNT / participants

            await message.bot.send_photo(
                chat_id=GROUP_CHAT_ID,
                photo="https://dhiway.com/wp-content/uploads/2021/09/Artboard-2-1.png",
                caption=caption_of_pay_photo.format(amount_per_person=round(amount_per_person))
            )

            await message.answer("Сообщение с QR-кодом и суммой отправлено в группу!")
            user_state.pop(user_id, None)
        except ValidationError as e:
            await message.answer(str(e))
