from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp

from keyboards.inline.inlinemenubutton import change_language, menu


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(
        f"Assalamu Aleykum , {message.from_user.full_name} !\nClick the Menu button below to view the products in our store :",
        reply_markup=menu,
    )
