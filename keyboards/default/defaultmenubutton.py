from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# buyurtmani tasdiqlash :
geolakatsya = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🚕Yetkazib berish ", request_location=True),
            KeyboardButton(text="🏃Olib ketish", request_contact=True),
        ],
    ],
    resize_keyboard=True,
)

# yetkazib berish | tasdiqlash:
knopka = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅Xa"), KeyboardButton(text="❌Yo'q")],
        [KeyboardButton(text="⬅ Orqaga"),],
    ],
    resize_keyboard=True,
)
# contact button
kontakt = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Mening raqamim", request_contact=True),],
        [KeyboardButton(text="⬅️Ortga"),],
    ],
    resize_keyboard=True,
)


izoh = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Buyurtmani tekshirish"),],], resize_keyboard=True
)


tasdiq = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Buyurtmani tasdiqlash"),
            KeyboardButton(text="Buyurtmani bekor qilish"),
        ],
        [KeyboardButton(text="📍 Manzilni o'zgartirish", request_location=True),],
    ],
    resize_keyboard=True,
)
