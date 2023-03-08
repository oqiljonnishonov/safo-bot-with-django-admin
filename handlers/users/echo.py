from aiogram import types

from loader import dp

from aiogram.types import Message

from handlers.users.inline_menu import list_categories
from keyboards.default.defaultmenubutton import geolakatsya, izoh, tasdiq
from loader import dp
from utils.db_api.db_commands import Database

db = Database()

# Echo bot
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await db.create()
    telegram_id = message.chat.id
    print(telegram_id)
    user_id = await db.get_user_id(telegram_id)
    print(user_id)
    bool = await db.get_user_bool(user_id)
    print(bool)
    if bool:
        text = message.text
        await db.update_user_text(user_id, text)

        telegram_id = message.chat.id
        user_id = await db.get_user_id(telegram_id)
        order = await db.get_user_order(user_id)
        order = await db.get_user_order(user_id)
        msg = "Quyidai mahsulotlar olindi:\n\n"
        user = await db.get_user(telegram_id)
        if user["text"] != None:
            msg += f"{user['text']}\n"
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
            text=msg, chat_id=telegram_id, reply_markup=tasdiq
        )

    else:
        await db.create()
        telegram_id = message.chat.id
        user_id = await db.get_user_id(telegram_id)
        if user_id:
            await list_categories(message)
        else:

            await message.answer(
                """<b>📍Manzilingizni yuboring</b>""",
                parse_mode="HTML",
                reply_markup=geolakatsya,
            )
