from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Link to the football hall.
google_map_url = "https://maps.app.goo.gl/QtAWzxVxDhs6JZsF6?g_st=com.google.maps.preview.copy"

inline_keyboard_with_map = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Как добраться", url=google_map_url)]
    ]
)
