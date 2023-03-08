# from io import BytesIO
# from os import link #kiritish chiqarish
# from aiogram import types
# import data
# from loader import bot
# import aiohttp

# async def photo_link(photo: types.photo_size.PhotoSize):
#     with await photo.download(BytesIO()) as file:
#         form = aiohttp.FormData() #forma yasash
#         form.add_field(
#             name='file',
#             value=file
#         )
#         async with await bot.session.post('https://telegra.ph/upload',data=form) as response:
#             img_src=await response.json()
#     link ='https://telegra.ph' + img_src[0]['src']
#     return link
#     # bot.get_session
