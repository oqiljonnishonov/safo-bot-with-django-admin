from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters.builtin import Command


# from utils.db_api.db_commands import Database
from datetime import datetime
from typing import Union

# from aiogram.dispatcher import FSMContext

from loader import dp, db
from keyboards.inline.inlinemenubutton import *

from data.config import SERVER_URL

# @dp.callback_query_handler(fan_callback.filter(item_name='english'))
# async def get_english(call: CallbackQuery):
#     await call.message.answer(text='\tWelcome !\nClick the Menu button below to view the products in our store :', reply_markup=menu)
#     await call.message.delete()

# @dp.callback_query_handler(fan_callback.filter(item_name='menu'))
# async def show_menu(call: CallbackQuery):
#     await call.message.answer(text)


@dp.callback_query_handler(text="uzMenu")
async def show_menu(call: CallbackQuery):
    telegram_id = call.message.chat.id
    user = await db.get_user(telegram_id)

    if not user:
        user_id = call.message.chat.id
        user_name = call.message.chat.full_name

        user_link = call.message.chat.username
        now = datetime.now()
        k1 = False
        await db.add_user(user_name, user_link, user_id, None, None, None, now, k1)

    # Foydalanuvchilarga barcha kategoriyalarni qaytaramiz
    await list_categories(call)


# kategoriya:
# ------------------------------------------------------------


# Kategoriyalarni qaytaruvchi funksiya. Callback query yoki Message qabul qilishi ham mumkin.
# **kwargs yordamida esa boshqa parametrlarni ham qabul qiladi: (category, subcategory, item_id)
# async def list_categories(message: Union[CallbackQuery, Message], **kwargs):
#     print('1')
#     # Keyboardni chaqiramiz

#     markup = await categories_keyboard()

#     # Agar foydalanuvchidan Message kelsa Keyboardni yuboramiz

#     if isinstance(message, Message):

#         # await message.answer("Bo'lim tanlang", reply_markup=markup, )
#         await message.answer.text(text=markup, reply_markup=ReplyKeyboardRemove())
#         print('kat1')

#     # Agar foydalanuvchidan Callback kelsa Callback natbibi o'zgartiramiz
#     elif isinstance(message, CallbackQuery):

#         call = message
#         await call.message.edit_reply_markup(markup)
#         print('kat2')


# kategoriya:
# ------------------------------------------------------------


@dp.callback_query_handler(
    text="buyurtma"
)  # menudan | qo'y go'sht mahsulotlariga "0" | buyurtmani bekor qilish
async def list_categories(message: Union[CallbackQuery, Message], **kwargs):
    print("251-qator")
    # Keyboardni chaqiramiz

    markup = await categories_keyboard()

    # Agar foydalanuvchidan Message kelsa Keyboardni yuboramiz

    if isinstance(message, Message):

        await message.answer(
            "Bo'lim tanlang", reply_markup=markup,
        )

    # Agar foydalanuvchidan Callback kelsa Callback natbibi o'zgartiramiz
    elif isinstance(message, CallbackQuery):

        await message.message.edit_text(text="Bo'lim tanlang", reply_markup=markup)


# ------------------------------------------------------------

# subkategoriya:

# Ost-kategoriyalarni qaytaruvchi funksiya | qo'y go'sht mahsulotlari ichidagi quy rulet... "1":
async def list_subcategories(callback: CallbackQuery, category, **kwargs):
    print("140-qator")
    markup = await subcategories_keyboard(category)

    # Xabar matnini o'zgartiramiz va keyboardni yuboramiz
    await callback.message.edit_reply_markup(markup)


# ---quy til rulet | qo'y go'sht mahsulotlari ichidagi quy til ruletni bosganda uni turlarini ko'rsatadi , ya'ni mahsulotlarni qaytaradi narxi gramini "2" :

# Ost-kategoriyaga tegishli mahsulotlar ro'yxatini yuboruvchi funksiya
async def list_items(callback: CallbackQuery, category, subcategory, **kwargs):
    print("149-qator")
    markup = await items_keyboard(category, subcategory)

    await callback.message.edit_text(text="Mahsulot tanlang", reply_markup=markup)


# Biror mahsulot uchun Xarid qilish tugmasini yuboruvchi funksiya , kalkulyatorga o'tkazadi va kalkulyator !!! | "3"
async def show_item(
    callback: CallbackQuery, category, subcategory, item_id, number, summ, minus
):
    print("157-qator")
    markup = item_keyboard(category, subcategory, item_id, number, summ, minus)

    # murkup.row(InlineKeyboardButton(text=item['description']))
    # Mahsulot haqida ma'lumotni bazadan olamiz

    # item = await db.get_product(item_id)
    # if item["photo"]:
    #     # text = f'<a href="{SERVER_URL}/media/{item["photo"]}"> </a>\n\n'
    #     text = f"<a href='https://telegra.ph/file/bffd751d16edcc64a1aa1.jpg'></a>"

    # else:
    #     text = f"<a href='https://www.planetware.com/wpimages/2020/02/france-in-pictures-beautiful-places-to-photograph-eiffel-tower.jpg'> </a>"
    # text += f"Narxi: {item['price']}so'm\n{item['description']}"

    # await callback.message.edit_text(text=text, reply_markup=markup)

    item = await db.get_product(item_id)
    if item["photo"]:
        print("rams if 1")
        # text = f'<a href="{SERVER_URL}/media/{item["photo"]}"> </a>\n\n'
        # text += f"<a href='https://telegra.ph/file/bffd751d16edcc64a1aa1.jpg'></a>"
        text = f'<a href="{SERVER_URL}/media/blog_images/{item["photo"]}"> </a>'

    else:
        print("rasm else")
        text = f"<a href='https://telegra.ph/file/bffd751d16edcc64a1aa1.jpg'> </a>"
    text += f"Narxi: {item['price']}so'm\n{item['description']}"

    await callback.message.edit_text(text=text, reply_markup=markup)


# -------------------------------------------------------------

#  uchirish uchun kalkulyator delete | "4"
async def delete_str(
    callback: CallbackQuery, category, subcategory, item_id, number, summ, minus
):
    print("176-qator")
    markup = delete_keyboard(category, subcategory, item_id, number, summ, minus)
    # item = await db.get_product(item_id)
    # if item["photo"]:
    #     # text = f'<a href="{SERVER_URL}/media/{item["photo"]}"> </a>\n\n'
    #     text = f"<a href='https://telegra.ph/file/bffd751d16edcc64a1aa1.jpg'></a>"

    # else:
    #     text = f"https://telegra.ph/file/bffd751d16edcc64a1aa1.jpg'></a>"
    # text += f"Narxi: {item['price']}so'm\n{item['description']}"
    item = await db.get_product(item_id)
    if item["photo"]:
        print("rams if")
        # text = f'<a href="{SERVER_URL}/media/{item["photo"]}"> </a>\n\n'
        # text += f"<a href='https://telegra.ph/file/bffd751d16edcc64a1aa1.jpg'> </a>"
        text = f'<a href="{SERVER_URL}/media/blog_images/{item["photo"]}"> </a>'
        # text = f'<link rel="" href="photos/{item["photo"]}">\n\n'

    else:
        print("rasm else")
        text = f"<a href='https://telegra.ph/file/bffd751d16edcc64a1aa1.jpg'> </a>"
    text += f"Narxi: {item['price']}so'm\n{item['description']}"

    # await callback.message.edit_text(text=text, reply_markup=markup)

    await callback.message.edit_text(text=text, parse_mode="HTML", reply_markup=markup)


# -------------------------
# savatga qo'shish | kalkulyatorda |


@dp.callback_query_handler(buy_item.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    print("434-qator")
    current_level = callback_data.get("level")
    count = callback_data.get("count")

    item_id = callback_data.get("item_id")

    levels = {
        "0": but_item,  #
        # "1": list_subcategories,  # Ost-kategoriyalarni qaytaramiz
    }
    current_level_function = levels[current_level]
    await current_level_function(call, count=count, item_id=item_id)


async def but_item(call: CallbackQuery, count, item_id, **kwargs):
    print("191-qator")
    telegram_id = call.message.chat.id

    markup = await insert_buy(count, item_id, telegram_id)
    await call.answer("Savatga qo'shildi", show_alert=True)
    await call.message.edit_text(text="Bo'lim tanlang ", reply_markup=markup)


# -----

# savat-------|


@dp.callback_query_handler(text="savat")
async def savat(call: CallbackQuery):
    print("217-qator")
    telegram_id = call.message.chat.id
    user_id = await db.get_user_id(telegram_id)
    order = await db.get_user_order1(user_id)
    if not order:
        print("222-qator if")
        await list_categories(CallbackQuery)
        await call.answer("Savat bo'sh!", show_alert=True)

    else:
        print("227-qator else")
        markup = await get_orders(user_id)
        order = await db.get_user_order(user_id)
        msg = "Quyidagi mahsulotlar olindi:\n"
        count = 1
        price = 0
        price1 = 0
        for i in order:
            if i["count"] == 0:
                null_id = i["id"]
                await db.delete_order1(null_id)
        for i in order:
            produc = await db.get_product_subcategory(i["product_id"])
            kk = produc["subcategory_name"]
            price = (i["count"]) * (produc["price"])
            msg += f"{count}. {i['count']} ta -  {kk} - {price} so'm\n"
            count = count + 1
            price1 += price
        msg += f"Umumiy: {price1} so'm "
        await call.message.edit_text(text=msg, reply_markup=markup)


# -------------
# + , - | savatdagi :


@dp.callback_query_handler(count_change.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    print("498-qator")
    """
    :param call: Handlerga kelgan Callback query
    :param callback_data: Tugma bosilganda kelgan ma'lumotlar
    """

    # Foydalanuvchi so'ragan Level (qavat)
    current_level = callback_data.get("level")

    # Foydalanuvchi so'ragan Kategoriya
    product_id = callback_data.get("product_id")

    # Ost-kategoriya (har doim ham bo'lavermaydi)
    count = callback_data.get("count")

    # Mahsulot ID raqami (har doim ham bo'lavermaydi)
    minus = int(callback_data.get("minus"))

    # Har bir Level (qavatga) mos funksiyalarni yozib chiqamiz
    levels = {
        "0": count_minus,  # Kategoriyalarni qaytaramiz
        "1": count_plus,  # Ost-kategoriyalarni qaytaramiz
        # "2": list_items,  # Mahsulotlarni qaytaramiz
        # "3": show_item,  # Mahsulotni ko'rsatamiz
        # "4": delete_str,  # Elementni uchirish
        # "5": change_number,  # Mahsulotni ko'rsatamiz
    }

    # Foydalanuvchidan kelgan Level qiymatiga mos funksiyani chaqiramiz
    current_level_function = levels[current_level]

    # Tanlangan funksiyani chaqiramiz va kerakli parametrlarni uzatamiz
    await current_level_function(call, product_id=product_id, count=count, minus=minus)


# savat (-):
async def count_minus(call: CallbackQuery, product_id, count, minus):
    print("369-qator")
    plus = int(count)
    product_id = int(product_id)
    telegram_id = call.message.chat.id
    user_id = await db.get_user_id(telegram_id)
    user_order = await db.get_user_order(user_id)

    count_order = 0
    for i in user_order:
        count_order += 1

    if count_order > 1 or plus > 1:
        print("381-qator if")
        kk = int(plus) - 1

        await db.count_update(product_id, kk)
        telegram_id = call.message.chat.id
        user_id = await db.get_user_id(telegram_id)
        markup = await get_orders(user_id)
        order = await db.get_user_order(user_id)
        msg = "Quyidai mahsulotlar olindi:\n"
        count = 1
        price = 0
        price1 = 0
        for i in order:
            if i["count"] == 0:
                null_id = i["id"]
                await db.delete_order1(null_id)
        order1 = await db.get_user_order(user_id)
        for i in order1:
            produc = await db.get_product_subcategory(i["product_id"])
            price = (i["count"]) * (produc["price"])

            msg += f"{count}. {i['count']} ta -  {produc['subcategory_name']} - {price} so'm\n"
            count = count + 1
            price1 += price
        msg += f"Umumiy: {price1} so'm "
        await call.message.edit_text(text=msg, reply_markup=markup)
    elif count_order == 1 and plus == 1:
        print("408-qator elif")
        await db.delete_order1(product_id)
        markup = await categories_keyboard()
        await call.answer("Savat bo'shatildi! ", show_alert=True)
        await call.message.edit_text(text="Bo'lim tanlang", reply_markup=markup)
    else:
        print("414-qator else")
        await db.delete_order1(product_id)
        # await call.message.answer("Savat bush!", )
        markup = await categories_keyboard()
        await call.message.edit_text(text="Bo'lim tanlang", reply_markup=markup)

# savat(+):
async def count_plus(call: CallbackQuery, product_id, count, minus):
    print("346-qator")
    plus = int(count) + 1
    await db.count_update(product_id, plus)

    telegram_id = call.message.chat.id
    user_id = await db.get_user_id(telegram_id)
    markup = await get_orders(user_id)
    order = await db.get_user_order(user_id)
    msg = "Quyidai mahsulotlar olindi:\n"
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
    await call.message.edit_text(text=msg, reply_markup=markup)


# ---------------------------------

# -------------------------------------------------------------------------
# Yuqoridagi barcha funksiyalar uchun yagona handler ---------------------
@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    print("454-qator")
    """
    :param call: Handlerga kelgan Callback query
    :param callback_data: Tugma bosilganda kelgan ma'lumotlar
    """

    # Foydalanuvchi so'ragan Level (qavat)
    current_level = callback_data.get("level")
    #####
    # description = callback_data.get("description")
    #####
    # Foydalanuvchi so'ragan Kategoriya
    category = callback_data.get("category")

    # Ost-kategoriya (har doim ham bo'lavermaydi)
    subcategory = callback_data.get("subcategory")

    # Mahsulot ID raqami (har doim ham bo'lavermaydi)
    item_id = int(callback_data.get("item_id"))

    number = callback_data.get("number")
    summ = callback_data.get("summ")
    minus = callback_data.get("minus")
    photo = callback_data.get("photos")

    # Har bir Level (qavatga) mos funksiyalarni yozib chiqamiz
    levels = {
        "0": list_categories,  # Kategoriyalarni qaytaramiz | qo'y go'sht mahsulotlariga kirganda va qaytganda
        "1": list_subcategories,  # Ost-kategoriyalarni qaytaramiz | qo'y go'sht mahsulotlariga kirganda va qaytganda
        "2": list_items,  # Mahsulotlarni qaytaramiz | gram va narxlarda
        "3": show_item,  # Mahsulotni ko'rsatamiz |  gram va narxlarni bosganda kalkulyatorga o'tishda va kalkulyator !!!
        "4": delete_str,  # Elementni uchirish | kalkulyatorda
        # "5": change_number,  # Mahsulotni ko'rsatamiz
    }

    # Foydalanuvchidan kelgan Level qiymatiga mos funksiyani chaqiramiz
    current_level_function = levels[current_level]

    # Tanlangan funksiyani chaqiramiz va kerakli parametrlarni uzatamiz
    await current_level_function(
        call,
        category=category,
        subcategory=subcategory,
        item_id=item_id,
        number=number,
        summ=summ,
        minus=minus,
    )
    #######
