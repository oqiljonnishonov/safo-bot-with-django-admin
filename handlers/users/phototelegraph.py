# from aiogram import types
# from loader import dp
# from utils.telegraph import photo_link

# @dp.message_handler(content_types='photo')
# async def handler_photo(message: types.Message):
#     telegram_id = message.chat.id
#     if telegram_id==1731117573:
#         photo=message.photo[-1]
#         link=await photo_link(photo)
#         await message.reply(link)
