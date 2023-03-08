from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from datetime import datetime

from loader import db

fan_callback = CallbackData("cours", "item_name")

# 2- usul
# call_fanlar1 = InlineKeyboardMarkup(row_width=1)
# python = InlineKeyboardButton(text='python asoslari', callback_data=fan_callback.new(item_name='python1'))
# call_fanlar1.insert(python)
# django = InlineKeyboardButton(text='Django asoslari', callback_data=fan_callback.new(item_name='django'))
# call_fanlar1.insert(django)
# back = InlineKeyboardButton(text="back", callback_data=fan_callback.new(item_name='back'))
# call_fanlar1.insert(back)
# 1-  usul:
change_language = InlineKeyboardMarkup(row_width=3)
uzbek = InlineKeyboardButton(
    text="O'zbek", callback_data=fan_callback.new(item_name="uzbek")
)
change_language.insert(uzbek)
english = InlineKeyboardButton(
    text="English", callback_data=fan_callback.new(item_name="english")
)
change_language.insert(english)
russian = InlineKeyboardButton(
    text="Russian", callback_data=fan_callback.new(item_name="russian")
)
change_language.insert(russian)


# 2- usul:
# menu=InlineKeyboardMarkup(row_width=1)
# menu.row(InlineKeyboardButton(text='📄 Menu', callback_data='Menu'))

# Menu=InlineKeyboardMarkup(row_width=2)
# menu=InlineKeyboardButton(text='📄 Menu', callback_data=fan_callback.new(item_name='menu'))
# Menu.insert(menu)
# back_change_language=InlineKeyboardButton(text="Change Language", callback_data=fan_callback.new(item_name='back_change_language'))
# change_language.insert(back_change_language)

# menu = InlineKeyboardMarkup() #chiroyli varyant
# menu.row(
#     InlineKeyboardButton(
#         text="📄 Menu",
#         callback_data="Menu"
#     )
# )


menu = InlineKeyboardMarkup(row_width=3)
# menu.row(InlineKeyboardButton(text='📄 Menu', callback_data='Menu'))
menu.row(InlineKeyboardButton(text="O'zbekcha", callback_data="uzMenu"))
menu.row(InlineKeyboardButton(text="English", callback_data="enMenu"))
menu.row(InlineKeyboardButton(text="Russion", callback_data="ruMenu"))
# umumiy :

# Tushuntirish kerak ?-----------------------------------------
# Turli tugmalar uchun CallbackData-obyektlarni yaratish
menu_cd = CallbackData(
    "show_menu",
    "level",
    "category",
    "subcategory",
    "item_id",
    "number",
    "summ",
    "minus",
)
buy_item = CallbackData("show_menu", "level", "count", "item_id")
count_change = CallbackData("show_menu", "level", "product_id", "count", "minus")

# Quyidagi funksiya yordamida menyudagi har bir element uchun calbback data yaratib olinadi
# Agar mahsulot kategoriyasi, ost-kategoriyasi va id raqami berilmagan bo'lsa 0 ga teng bo'ladi
def make_callback_data(
    level, category="0", subcategory="0", item_id="0", number="0", summ="0", minus="0"
):
    return menu_cd.new(
        level=level,
        category=category,
        subcategory=subcategory,
        item_id=item_id,
        number=number,
        summ=summ,
        minus=minus,
    )


# --kategoriya----menudan kegin----menuni bosganda ishga tushadi---1-qadam :------------------------

# Kategoriyalar uchun keyboardyasab olamiz | "0"
async def categories_keyboard():
    print("inline 122")

    # Eng yuqori 0-qavat ekanini ko'rsatamiz
    CURRENT_LEVEL = 0  # "0"

    # Keyboard yaratamiz

    markup = InlineKeyboardMarkup(row_width=2)

    # Bazadagi barcha kategoriyalarni olamiz
    categories = await db.get_categories()
    # Har bir kategoriya uchun quyidagilarni bajaramiz:
    for category in categories:
        # Kategoriyaga tegishli mahsulotlar sonini topamiz
        # number_of_items = await db.count_products(category["category_code"])

        # Tugma matnini yasab olamiz
        button_text = f'{category["category_name"]}'

        # Tugma bosganda qaytuvchi callbackni yasaymiz: Keyingi bosqich +1 va kategoriyalar
        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1, category=category["category_code"]
        )

        # Tugmani keyboardga qo'shamiz
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.row(InlineKeyboardButton(text=f"🛒 Savatni ko'rish", callback_data="savat"))

    # Keyboardni qaytaramiz
    return markup


# subkategoriya------------------------------------
# Berilgan kategoriya ostidagi kategoriyalarni qaytaruvchi keyboard | "1"
async def subcategories_keyboard(category):
    print("inline 162")
    CURRENT_LEVEL = 1  # "1"
    markup = InlineKeyboardMarkup(row_width=2)

    # Kategoriya ostidagi kategoriyalarni bazadan olamiz
    subcategories = await db.get_subcategories(category)

    for subcategory in subcategories:
        # Tugma matnini yasaymiz
        button_text = f"{subcategory['subcategory_name']} "

        # Tugma bosganda qaytuvchi callbackni yasaymiz: Keyingi bosqich +1 va kategoriyalar
        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1,
            category=category,
            subcategory=subcategory["subcategory_code"],
        )
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    # Ortga qaytish tugmasini yasaymiz (yuoqri qavatga qaytamiz)
    markup.row(
        InlineKeyboardButton(
            text="⬅️Ortga", callback_data=make_callback_data(level=CURRENT_LEVEL - 1)
        )
    )
    return markup


# ---quy til rulet | subkategoriyadagi mahsulotlar , ghghjg "2"

# Ostkategoriyaga tegishli mahsulotlar uchun keyboard yasaymiz | "2"
async def items_keyboard(category, subcategory):
    print("inline 194")
    CURRENT_LEVEL = 2  # "2"
    markup = InlineKeyboardMarkup(row_width=2)
    # Ost-kategorioyaga tegishli barcha mahsulotlarni olamiz
    items = await db.get_products(category, subcategory)
    for item in items:
        # Tugma matnini yasaymiz
        button_text = f"{item['weight']} - {item['price']}so'm"

        # Tugma bosganda qaytuvchi callbackni yasaymiz: Keyingi bosqich +1 va kategoriyalar
        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1,
            category=category,
            subcategory=subcategory,
            item_id=item["id"],
        )
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    # Ortga qaytish tugmasi
    markup.row(
        InlineKeyboardButton(
            text="⬅️Ortga",
            callback_data=make_callback_data(
                level=CURRENT_LEVEL - 1, category=category
            ),
        )
    )
    return markup


# ----- savatga qo'shish tugmasiga | "3"
def buy_item_data(level, count="0", item_id="0"):
    print("inline 107")
    return buy_item.new(level=level, count=count, item_id=item_id)


#######
# gramlarni bosganda ya'ni kalkulyatorga o'tkazadi va kalkulyator !!! | "3"
def item_keyboard(category, subcategory, item_id, number, summ, minus):
    print("inline 227")
    if int(number) > 0 or int(summ) > 0:
        print("inline 229 if")
        CURRENT_LEVEL = 3
        markup = InlineKeyboardMarkup(row_width=3)
        # description=callback_data.get("description")
        # markup.row(
        #     InlineKeyboardButton(
        #         text=f"sharx: {description}", callback_data="kk_data(item_id=item_id)"
        #     )
        # )

        # markup.row(
        #     InlineKeyboardButton(
        #         text=f"sharx: {description}", callback_data=make_callback_data(
        #             level=CURRENT_LEVEL,
        #             category=category,
        #             subcategory=subcategory,
        #             item_id=item_id,
        #             description=description
        #         )
        #     )
        # )
        r_number = str(int(summ + number))
        markup.row(
            InlineKeyboardButton(
                text=f"Soni: {r_number}", callback_data="kk_data(item_id=item_id)"
            )
        )
        temp = []
        for item in range(1, 10):
            button_text = f"{item} "
            callback_data = make_callback_data(
                level=CURRENT_LEVEL,
                category=category,
                subcategory=subcategory,
                item_id=item_id,
                number=f"{item}",
                summ=f"{r_number}",
            )
            temp.append(
                InlineKeyboardButton(text=button_text, callback_data=callback_data)
            )
            if len(temp) > 2:
                markup.row(*temp)
                temp.clear()

        markup.row(
            InlineKeyboardButton(
                text=f"0",
                callback_data=make_callback_data(
                    level=CURRENT_LEVEL,
                    category=category,
                    subcategory=subcategory,
                    item_id=item_id,
                    number="0",
                    summ=f"{r_number}",
                ),
            ),
            InlineKeyboardButton(
                text=f"◀",
                callback_data=make_callback_data(
                    level=CURRENT_LEVEL + 1,
                    category=category,
                    subcategory=subcategory,
                    item_id=item_id,
                    number=f"",
                    summ=r_number,
                ),
            ),
        )

        markup.row(
            InlineKeyboardButton(
                text=f"➕ Savatga qo'shish",
                callback_data=buy_item_data(level=0, count=r_number, item_id=item_id,),
            ),
            InlineKeyboardButton(text=f"🛒 Savatni ko'rish", callback_data="savat"),
        )
        markup.row(
            InlineKeyboardButton(
                text="⬅️Ortga",
                callback_data=make_callback_data(
                    level=CURRENT_LEVEL - 1,
                    category=category,
                    subcategory=subcategory,
                    item_id=item_id,
                    number=number,
                ),
            )
        )
        return markup
    else:
        print("inline 229 else")

        CURRENT_LEVEL = 3
        # description = db.get_product(description)#####
        markup = InlineKeyboardMarkup(row_width=3)
        ######
        # description=callback_data.get("description")

        # markup.row(
        #     InlineKeyboardButton(
        #         text=f"sharx: {description}", callback_data="kk_data(item_id=item_id)"
        #     )
        # )

        r_number = ""
        markup.row(
            InlineKeyboardButton(
                text=f"Soni: {r_number}", callback_data="kk_data(item_id=" ")"
            )
        )
        temp = []
        for item in range(1, 10):
            button_text = f"{item} "
            callback_data = make_callback_data(
                level=CURRENT_LEVEL,
                category=category,
                subcategory=subcategory,
                item_id=item_id,
                number=f"{item}",
                summ=f"{r_number}",
            )
            temp.append(
                InlineKeyboardButton(text=button_text, callback_data=callback_data)
            )
            if len(temp) > 2:
                markup.row(*temp)
                temp.clear()

        markup.row(
            InlineKeyboardButton(text=f"0", callback_data="kk_data(item_id=" ")")
        )

        markup.row(
            InlineKeyboardButton(text=f"🛒 Savatni ko'rish", callback_data="savat")
        )
        markup.row(
            InlineKeyboardButton(
                text="⬅️Ortga",
                callback_data=make_callback_data(
                    level=CURRENT_LEVEL - 2, category=category, subcategory=subcategory
                ),
            )
        )
        return markup


# ===============Delete====================  kalkulyator | "4"
def delete_keyboard(category, subcategory, item_id, number, summ, minus):
    print("inline 356")
    if int(summ) != 0:
        print("inline 358 if")
        CURRENT_LEVEL = 4
        r_number = str(int(int(summ) / 10))
        markup = InlineKeyboardMarkup(row_width=3)
        markup.row(
            InlineKeyboardButton(
                text=f"Soni: {r_number}", callback_data="buy_item.new(item_id=item_id)"
            )
        )
        temp = []
        for item in range(1, 10):
            button_text = f"{item} "
            callback_data = make_callback_data(
                level=CURRENT_LEVEL - 1,
                category=category,
                subcategory=subcategory,
                item_id=item_id,
                number=f"{item}",
                summ=f"{r_number}",
            )
            temp.append(
                InlineKeyboardButton(text=button_text, callback_data=callback_data)
            )
            if len(temp) > 2:
                markup.row(*temp)
                temp.clear()

        markup.row(
            InlineKeyboardButton(
                text=f"0",
                callback_data=make_callback_data(
                    level=CURRENT_LEVEL - 1,
                    category=category,
                    subcategory=subcategory,
                    item_id=item_id,
                    number=str(0),
                    summ=f"{r_number}",
                ),
            ),
            InlineKeyboardButton(
                text=f"◀",
                callback_data=make_callback_data(
                    level=CURRENT_LEVEL,
                    category=category,
                    subcategory=subcategory,
                    item_id=item_id,
                    number=f"",
                    summ=f"{r_number}",
                ),
            ),
        )
        # )

        markup.row(
            InlineKeyboardButton(
                text=f"➕ Savatga qo'shish",
                callback_data=buy_item_data(level=0, count=r_number, item_id=item_id,),
            ),
            InlineKeyboardButton(text=f"🛒 Savatni ko'rish", callback_data="savat"),
        )

        markup.row(
            InlineKeyboardButton(
                text="⬅️Ortga",
                callback_data=make_callback_data(
                    level=minus,
                    category=category,
                    subcategory=subcategory,
                    item_id=item_id,
                ),
            )
        )
        return markup
    else:
        print("inline 434 else")
        CURRENT_LEVEL = 3
        markup = InlineKeyboardMarkup(row_width=3)
        r_number = ""
        markup.row(
            InlineKeyboardButton(
                text=f"Soni: {r_number}", callback_data="buy_item.new(item_id=item_id)"
            )
        )
        temp = []
        for item in range(1, 10):
            button_text = f"{item} "
            callback_data = make_callback_data(
                level=CURRENT_LEVEL,
                category=category,
                subcategory=subcategory,
                item_id=item_id,
                number=f"{item}",
                summ=f"{r_number}",
            )
            temp.append(
                InlineKeyboardButton(text=button_text, callback_data=callback_data)
            )
            if len(temp) > 2:
                markup.row(*temp)
                temp.clear()

        markup.row(
            InlineKeyboardButton(
                text=f"0", callback_data="buy_item.new(item_id=item_id)"
            )
        )
        markup.row(
            InlineKeyboardButton(
                text=f"🛒 Savatni ko'rish", callback_data="buy_item.new(item_id=item_id)"
            )
        )
        markup.row(
            InlineKeyboardButton(
                text="⬅️Ortga",
                callback_data=make_callback_data(
                    level=CURRENT_LEVEL - 2, category=category, subcategory=subcategory
                ),
            )
        )
        return markup


# savatga qo'shish , kalkulyatordagi |


async def insert_buy(count, item_id, telegram_id):
    print("inline 483")
    telegram_id = int(telegram_id)
    user_id = await db.get_user_id(telegram_id)
    now = datetime.now()
    count1 = int(count)
    product_id = int(item_id)
    order = await db.get_user_order_id(user_id, product_id)
    markup = InlineKeyboardMarkup(row_width=2)
    if count1 != 0 and order == None:
        print("inline 494 if")
        k1 = False
        await db.add_order(count1, now, product_id, user_id, k1)
        # Eng yuqori 0-qavat ekanini ko'rsatamiz
        CURRENT_LEVEL = 0
        # Bazadagi barcha kategoriyalarni olamiz
        categories = await db.get_categories()
        # Har bir kategoriya uchun quyidagilarni bajaramiz:
        for category in categories:
            # Tugma matnini yasab olamiz
            button_text = f'{category["category_name"]}'
            # Tugma bosganda qaytuvchi callbackni yasaymiz: Keyingi bosqich +1 va kategoriyalar
            callback_data = make_callback_data(
                level=CURRENT_LEVEL + 1, category=category["category_code"]
            )
            # Tugmani keyboardga qo'shamiz
            markup.insert(
                InlineKeyboardButton(text=button_text, callback_data=callback_data)
            )
        markup.row(
            InlineKeyboardButton(text=f"🛒 Savatni ko'rish", callback_data="savat")
        )
    elif order["id"]:
        print("inline 519 else")
        order = await db.get_user_order_id(user_id, product_id)
        order_id = order["id"]
        count = int(order["count"]) + int(count)
        await db.update_order_count(order_id, count)
        CURRENT_LEVEL = 0
        # Bazadagi barcha kategoriyalarni olamiz
        categories = await db.get_categories()
        # Har bir kategoriya uchun quyidagilarni bajaramiz:
        for category in categories:
            # Kategoriyaga tegishli mahsulotlar sonini topamiz
            # number_of_items = await db.count_products(category["category_code"])

            # Tugma matnini yasab olamiz
            button_text = f'{category["category_name"]}'

            # Tugma bosganda qaytuvchi callbackni yasaymiz: Keyingi bosqich +1 va kategoriyalar
            callback_data = make_callback_data(
                level=CURRENT_LEVEL + 1, category=category["category_code"]
            )

            # Tugmani keyboardga qo'shamiz
            markup.insert(
                InlineKeyboardButton(text=button_text, callback_data=callback_data)
            )
        markup.row(
            InlineKeyboardButton(text=f"🛒 Savatni ko'rish", callback_data="savat")
        )
    return markup


# --savat | savatni ko'rish | + , - ,  ko'paytirib , kamaytirish


def count_change_data(level, product_id="0", minus="0", count="0"):
    print("inline 114")
    return count_change.new(
        level=level, product_id=product_id, count=count, minus=minus
    )


# savat | + , - ,  ko'paytirib , kamaytirish
async def get_orders(user_id):
    print("inline 549")
    markup = InlineKeyboardMarkup(row_width=3)
    order = await db.get_user_order(user_id)
    if order:
        print("inline 557 if")
        for i in order:
            produc_name = await db.get_product_subcategory(i["product_id"])
            markup.row(
                InlineKeyboardButton(
                    text="-",
                    callback_data=count_change_data(
                        level=0, product_id=i["id"], count=i["count"]
                    ),
                ),
                InlineKeyboardButton(
                    text=f"{produc_name['subcategory_name']}", callback_data="name"
                ),
                InlineKeyboardButton(
                    text="+",
                    callback_data=count_change_data(
                        level=1, product_id=i["id"], count=i["count"],
                    ),
                ),
            )
        markup.row(
            InlineKeyboardButton(
                text="🧾 Buyurtmani tasdiqlash", callback_data=f"ordertype",
            )
        )
        markup.row(
            InlineKeyboardButton(text="Yana buyurtma berish", callback_data=f"buyurtma")
        )
    else:
        print("inline 598 else")
        pass
    return markup
