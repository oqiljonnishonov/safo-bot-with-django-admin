from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from handlers.users.inline_menu import list_categories
from utils.db_api.db_commands import Database

from loader import dp, db

from data.config import ADMINS
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from keyboards.default.defaultmenubutton import *

# buyurtmani tasdiqlash | savatdagi :
@dp.callback_query_handler(text="ordertype")
async def Menu(callback: CallbackQuery):
    print("22-qator")
    user_id = callback.message.chat.id
    # await db.delete_user(user_id)
    await callback.message.delete()
    # await callback.message.answer("📍Manzilingizni yuboring", reply_markup=geolakatsya)
    await callback.message.answer(
        """<b>Maxsulotni olish usulini tanlang va manzilingizni yuboring 📍 </b>""",
        parse_mode="HTML",
        reply_markup=geolakatsya,
    )


# yetkazib berish | location: -------------
@dp.message_handler(content_types=["location"])
async def location(message: Message):
    print("34-qator")
    user_id = message.chat.id
    user_name = message.from_user.full_name
    user_link = message.from_user.username
    lat = message.location.latitude
    long = message.location.longitude
    id = await db.get_user_id(user_id)

    lat = str(lat)
    long = str(long)
    await db.update_user1(id, lat, long)

    await message.answer(
        """<b>📍Manzilni to'g'ri yubordingizmi?</b>""",
        parse_mode="HTML",
        reply_markup=knopka,
    )


@dp.message_handler(text="⬅️Ortga")
async def Ortga1(message: Message):
    print("94-qator")
    await message.answer(
        """<b>📍Manzilingizni yuboring</b>""",
        parse_mode="HTML",
        reply_markup=geolakatsya,
    )


# -------------------

# tasdiqlash | buyurtmani -----------
@dp.message_handler(text="✅Xa")
async def Xa(message: Message):
    print("52-qator")
    await message.answer(
        """<b>👇Telefon nomeringizni yuboring</b>""",
        parse_mode="HTML",
        reply_markup=kontakt,
    )


@dp.message_handler(text="❌Yo'q")
async def Yoq(message: Message):
    print("58-qator")
    await message.answer(
        """<b>Manzilingizni boshidan yuboring</b>""",
        parse_mode="HTML",
        reply_markup=geolakatsya,
    )


# ----------------------------

# contact | nomer yuborish
@dp.message_handler(content_types=["contact"])
async def contact(message: Message, state: FSMContext):
    print("64-qator")
    db = Database()
    await db.create()
    telefon_raqam = str(message.contact["phone_number"])
    telegram_id = message.chat.id
    user_id = await db.get_user_id(telegram_id)
    await db.update_user2(user_id, telefon_raqam)
    telegram_id = message.chat.id
    user_id = await db.get_user_id(telegram_id)
    bool = True
    await db.update_user_bool(user_id, bool)
    await message.answer(
        """<b>Olingan maxsulotlarga izoh qoldiring</b>""",
        parse_mode="HTML",
        reply_markup=izoh,
    )


@dp.message_handler(text="Izoh")
async def izohlar(message: Message):
    print("423-qator")
    telegram_id = message.chat.id
    user_id = await db.get_user_id(telegram_id)
    bool = True
    await db.update_user_bool(user_id, bool)
    await message.answer(
        """<b>Olingan maxsulotlarga izoh qoldiring</b>""",
        parse_mode="HTML",
        reply_markup=izoh,
    )


# buyurtmani tekshirish:
@dp.message_handler(text="Buyurtmani tekshirish")
async def tekshirish(message: Message):
    print("270-qator")
    telegram_id = message.chat.id
    user_id = await db.get_user_id(telegram_id)
    order = await db.get_user_order(user_id)
    order = await db.get_user_order(user_id)
    msg = "Quyidai mahsulotlar olindi:\n\n"
    user = await db.get_user(telegram_id)
    if user["text"] != None:
        print("278-qator if")
        msg += f"{user['text']}\n"
    count = 1
    count = 1
    price = 0
    price1 = 0
    for i in order:
        produc = await db.get_product_subcategory(i["product_id"])
        price = (i["count"]) * (produc["price"])
        msg += (
            f"{count}. {i['count']} ta -  {produc['subcategory_name']} - {price} so'm\n"
        )
        count = count + 1
        price1 += price
    msg += f"Umumiy: {price1} so'm "
    await message.bot.send_message(text=msg, chat_id=telegram_id, reply_markup=tasdiq)


# buyurtmani tasdiqlash:
@dp.message_handler(text="Buyurtmani tasdiqlash")
async def to_admin(message: Message):
    print("297-qator")
    telegram_id = message.chat.id
    user_id = await db.get_user_id(telegram_id)
    order = await db.get_user_order(user_id)

    order = await db.get_user_order(user_id)
    if order:
        msg = "Quyidai mahsulotlar olindi:\n\n"
        user = await db.get_user(telegram_id)

        msg += f" Xaridorning ma'lumotlari\n\n"
        msg += f"{1}.id - {user['telegram_id']}   \n"
        msg += f"{2}.Ism - {user['full_name']}   \n"
        msg += f"{3}.Link - {user['username']}   \n"
        msg += f"{4}.Tel: +{user['phone_number']}   \n\n\n"

        if user["text"] != None:
            msg += f"Xarid uchun izoh \n\n"
            msg += f"{user['text']}\n\n"
        msg += f" Xarid qilingan mahsulotlar  \n\n"
        count = 1
        count = 1
        price = 0
        price1 = 0
        for i in order:
            produc = await db.get_product_subcategory(i["product_id"])
            price = (i["count"]) * (produc["price"])
            msg += f"{count}. {i['count']} ta -  {produc['subcategory_name']} - {price} so'm\n"
            count = count + 1
            price1 += price
        msg += f"Umumiy: {price1} so'm "

        await message.bot.send_message(
            text="Xaridingiz uchun rahmat! Sizning ma'lumotlaringiz tasdiqlandi",
            chat_id=telegram_id,
            reply_markup=ReplyKeyboardRemove(),
        )
        user = await db.get_user(telegram_id)
        text = None
        await db.update_user_text(user_id, text)
        await db.update_user_location(user_id, text, text)
        for i in ADMINS:
            await message.bot.send_message(text=msg, chat_id=i)
            if user["latitude"]:
                await message.bot.send_location(
                    chat_id=i,
                    latitude=user["latitude"],
                    longitude=user["longitude"],
                    reply_to_message_id=user["phone_number"],
                )
        await db.delete_order(user_id)
        bool = False
        await db.update_user_bool(user_id, bool)


# buyurtmani bekor qilish:
@dp.message_handler(text="Buyurtmani bekor qilish")
async def bekorqilish(call: Message):
    print("201-qator")
    telegram_id = call.chat.id
    user_id = await db.get_user_id(telegram_id)
    order = await db.get_user_order1(user_id)
    text = None
    await db.update_user_text(user_id, text)
    await db.update_user_location(user_id, text, text)

    for i in order:
        await db.delete_order1(i["id"])
    await call.answer(
        "Buyurtma bekor qilindi", reply_markup=ReplyKeyboardRemove(),
    )
    await list_categories(call)
