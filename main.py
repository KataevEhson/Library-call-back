from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
from states import router as state_router
from conection import *
from service import *
import os
import asyncio
from keybords import *

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


bot = Bot(token=BOT_TOKEN)


dp = Dispatcher()



@dp.message(Command("start"))
async def start_bot(message: Message):
    if await  get_user_by_id(message.from_user.id):
        status = await check_admin(message.from_user.id)
        if status:
            await message.answer(f"Привет администратор @{message.from_user.username}", reply_markup=admin_key)
        else:
            await message.answer(f"С возвращением! @{message.from_user.username}", reply_markup=users_key)
    else:
        user = message.from_user
        await create_user(user.username, user.full_name, user.id)
        await message.answer(f"Привет @{message.from_user.username}", reply_markup=users_key)


@dp.message(F.text == "Покозать книги")
@dp.message(Command("get_books"))
async def get_books_bot(message: Message):
    books = await get_book()
    if books:
        text = ""
        for book in books:
            text+= f"""
    Id: {book['books_id']}  
    Имя: {book['title']}  
    Описания: {book['caption']}
    Издательство: {book['publisher']}
    Автор: {book['full_name']}
    Категория: {book['category']}
                """
        await message.answer(text)
    else:
        await message.answer("Нету книг")




@dp.message(Command("help"))
async def help_message(message : Message):
    await message.answer("""
Привет бро етот бот про библиотку ЧТО УМЕЕТ БОТ???

Если вы admin вы можете добавит изменит удалит книги

Если вы user то вы можете прочитат по категории или по автору книги
""")














async def main():
    await create_table()
    print("Bot started")
    dp.include_router(state_router)
    await dp.start_polling(bot)
    
    
    
if __name__ == "__main__":
    asyncio.run(main())