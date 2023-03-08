# from email import message
# import imp
# from aiogram import Bot, types
# # from data.config import BOT_TOKEN
# from loader import dp , bot
# from aiogram.types import InputFile , CallbackQuery

# @dp.message_handler(text='rasm')
# async def sent_photo(message: types.Message):
#     telegram_id = message.chat.id
#     if telegram_id==1731117573:

#         # photo_link='https://telegra.ph/file/74d9cf1a50c09cd2bbecf.jpg'
#         # photo_id='AgACAgIAAxkBAAMaYynt9J8r7f_yosdgl9SjHpXpC4QAAri9MRv-KFBJR4PSrn3q93EBAAMCAAN5AAMpBA'
#         photo_file=InputFile(path_or_bytesio='photos/sendphoto.jpg')#3-usul
#         # await message.reply_photo(photo_link,caption='bu link_rasm')
#         await message.reply_photo(photo_file,caption='')#3-usul
#         # await Bot.send_photo(chat_id=message.from_user.id, photo=photo_file,caption='jhgfds')#yuborishni boshqa usuli , bu lichkaga yozish , aynan bitta user ga

# # @dp.callback_query_handler(text='Menu')
# # async def send_photo(call: CallbackQuery):
# #     telegram_id= call.message.chat.id
# #     photo_file=InputFile(path_or_bytesio='photos/sendphoto.jpg')
# #     await Bot.send_photo(chat_id=message.from_user.id, photo=photo_file,caption='')
