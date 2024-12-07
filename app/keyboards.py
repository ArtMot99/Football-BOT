from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Запланировать тренировку"),
        KeyboardButton(text="Начать опрос"),
    ],
    [KeyboardButton(text="Послать QR и посчитать оплату")],
    [KeyboardButton(text="Отменить тренировку")]
])
