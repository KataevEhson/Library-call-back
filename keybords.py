from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from service import *




users_key = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Покозать книги"),KeyboardButton(text="Поиск по категории")],
        [KeyboardButton(text="Поиск по автору"), KeyboardButton(text="Помощь")]
    ],
    resize_keyboard=True
)




admin_key = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить книгу"), KeyboardButton(text="Изменить книгу")],
        [KeyboardButton(text="Удалить книгу"), KeyboardButton(text="Покозать книги")],
        [KeyboardButton(text="Добавить категорию"), KeyboardButton(text="Добавить автора")],
        [KeyboardButton(text="Поиск по категории"), KeyboardButton(text="Поиск по автору")],
        [KeyboardButton(text="Помощь")]   
    ],
    resize_keyboard=True
)





async def get_author_button():
    data = await get_author()
    keyboards = []
    for author in data:
        keyboards.append([InlineKeyboardButton(text=f"{author['full_name']}", callback_data=f"author_{author['autor_id']}")])
    keybor = InlineKeyboardMarkup(inline_keyboard=keyboards)
    return keybor








async def get_category_button():
    data = await get_category()
    keyboards = []
    for i in data:
        keyboards.append([InlineKeyboardButton(text=f"{i['category']}", callback_data=f"category_{i['category_id']}")])
    keybor = InlineKeyboardMarkup(inline_keyboard=keyboards)
    return keybor




# get_books_for_button_callback




async def get_books_button():
    data = await get_books_for_button_callback()
    keyboards = []
    for i in data:
        keyboards.append([InlineKeyboardButton(text=f"{i['title']}", callback_data=f"books_{i['books_id']}")])
    keybor = InlineKeyboardMarkup(inline_keyboard=keyboards)
    return keybor

