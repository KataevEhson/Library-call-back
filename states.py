from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from service import *
from keybords import *
from aiogram.types import CallbackQuery


router = Router()





class AddBook(StatesGroup):
    get_title = State()
    get_caption = State()
    get_author_id = State()
    get_category_id = State()
    get_pablisher = State()
    
   

class AddCategory(StatesGroup):
    get_title = State()

    

class AddAuthor(StatesGroup):
    get_name = State()
    get_country = State()



class Update_book_class(StatesGroup):
    get_title = State()
    get_caption = State()
    get_pablisher = State()
    get_book_id = State()


class Delete_book(StatesGroup):
    get_book_id = State()



class search_by_category(StatesGroup):
    get_category_id = State()



    
@router.message(F.text == "Добавить книгу")
@router.message(Command("add_book"))
async def add_book_title(message: Message, state: FSMContext):
    if await check_admin(message.from_user.id):
        await message.answer("Введите имя книги:")
        await state.set_state(AddBook.get_title)
    else:
        await message.answer("Только админ может создавать книги!")
        await state.clear()


    
@router.message(AddBook.get_title)
async def add_book_caption(message: Message, state: FSMContext):
    await state.update_data(title = message.text)
    await message.answer("Введите описания книги:")
    await state.set_state(AddBook.get_caption)
    
@router.message(AddBook.get_caption)
async def add_book_author(message: Message, state: FSMContext):
    await state.update_data(caption = message.text)
    buttons = await get_author_button()
    await message.answer("Выберите автора", reply_markup=buttons)
    await state.set_state(AddBook.get_author_id)
    
@router.callback_query(AddBook.get_author_id, F.data.startswith("author_"))
async def add_book_author(callback: CallbackQuery, state: FSMContext):
    author_id = callback.data.split("_")[1]
    await state.update_data(author_id = author_id)
    buttons = await get_category_button()
    await callback.message.answer("Выберите категорию:",reply_markup=buttons)
    await callback.answer("Автор выбран")
    await state.set_state(AddBook.get_category_id)
    
    
@router.callback_query(AddBook.get_category_id, F.data.startswith("category_"))
async def add_book_categroy(callback: CallbackQuery, state: FSMContext):
    category_id = callback.data.split("_")[1]
    await state.update_data(category_id=category_id)
    await callback.answer("Категория выбрана")
    await state.set_state(AddBook.get_pablisher)
    await callback.message.answer("Введите место издания:")
    



@router.message(AddBook.get_pablisher)
async def add_book_categroy(message: Message, state: FSMContext):
    await state.update_data(pablisher = message.text)
    data = await state.get_data()
    status = await create_book_db(data['title'], data['caption'], data['author_id'], data['category_id'], data['pablisher'])
    if status:
        await message.answer("Ваша книга создана")
        
    else:
        await message.answer("Ошибка при создании книги!")
    await state.clear()

        
    

@router.message(F.text == "Добавить категорию")
@router.message(Command("add_category"))
async def add_category(message: Message, state: FSMContext):
    if await check_admin(message.from_user.id):
        await message.answer("Введите имя категории:")
        await state.set_state(AddCategory.get_title)
    else:
        await message.answer("Только админ может создавать книги!")
        await state.clear()











@router.message(AddCategory.get_title)
async def add_category_title(message: Message, state: FSMContext):
    await state.update_data(title = message.text)
    data = await state.get_data()
    status = await create_category_db(data['title'])
    if status:
        await message.answer("Ваша категория создана")
        
    else:
        await message.answer("Ошибка при создании категория!")
    await state.clear()



@router.message(F.text == "Добавить автора")
@router.message(Command("add_author"))
async def add_author(message: Message, state: FSMContext):
    if await check_admin(message.from_user.id):
        await message.answer("Введите имя автора:")
        await state.set_state(AddAuthor.get_name)
    else:
        await message.answer("Только админ может создавать автор!")
        await state.clear()


    
@router.message(AddAuthor.get_name)
async def add_author_name(message: Message, state: FSMContext):
    await state.update_data(full_name = message.text)
    await message.answer("Введите страну автора:")
    await state.set_state(AddAuthor.get_country)



@router.message(AddAuthor.get_country)
async def add_author_country(message: Message, state: FSMContext):
    await state.update_data(country = message.text)
    data = await state.get_data()
    status = await create_author_db(data['full_name'], data['country'])
    if status:
        await message.answer("Ваша автор создана")
    else:
        await message.answer("Ошибка при создании автор!")
    await state.clear()






@router.message(F.text == "Изменить книгу")
@router.message(Command("update_book"))
async def update_id_for_me(message : Message , state : FSMContext):
    await message.answer("Введите ваш title:")
    await state.set_state(Update_book_class.get_title)



@router.message(Update_book_class.get_title)
async def get_title_for_me(message : Message , state : FSMContext):
    await state.update_data(title = message.text)
    await message.answer("Введите ваш caption: ")
    await state.set_state(Update_book_class.get_caption)



@router.message(Update_book_class.get_caption)
async def get_title_for_me(message : Message , state : FSMContext):
    await state.update_data(caption = message.text)
    await message.answer("Введите ваш publisher: ")
    await state.set_state(Update_book_class.get_pablisher)






@router.message(Update_book_class.get_pablisher)
async def get_title_for_me(message : Message , state : FSMContext):
    await state.update_data(publisher = message.text)
    buttons = await get_books_button()
    await message.answer("Выбери книгу: ", reply_markup=buttons)
    await state.set_state(Update_book_class.get_book_id)




@router.callback_query(Update_book_class.get_book_id, F.data.startswith("books_"))
async def get_title_for_me(callback : CallbackQuery , state : FSMContext):
    books_id = int(callback.data.split("_")[1])
    await state.update_data(book_id = books_id)
    data = await state.get_data()
    await update_book(data['title'], data['caption'], data['publisher'], data['book_id'])
    await callback.answer("книга выбрана!!!")
    await state.clear()
   
   













@router.message(F.text == "Удалить книгу")
@router.message(Command("delete_book"))
async def update_id_for_(message : Message , state : FSMContext):
    buttons = await get_books_button()
    await message.answer("Выберите книгу которую хотите удалитъ: ", reply_markup=buttons)
    await state.set_state(Delete_book.get_book_id)






@router.callback_query(Delete_book.get_book_id, F.data.startswith("books_"))
async def get_title_for_me(callback : CallbackQuery , state : FSMContext):
    books_id = int(callback.data.split("_")[1])
    await state.update_data(book_id = books_id)
    data = await state.get_data()
    await delete_boooooooook(data['book_id'])
    await callback.answer("книга выбрана!!!")
    await state.clear()
   
   


@router.message(F.text == "Поиск по категории")
@router.message(Command("search_by_category"))
async def add_book_author(message: Message, state: FSMContext):
    buttons = await get_category_button()
    await message.answer("Выберите категорию:",reply_markup=buttons)
    await state.set_state(search_by_category.get_category_id)
    
    


@router.callback_query(search_by_category.get_category_id, F.data.startswith("category_"))
async def add_book_categroy(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.split("_")[1])
    await state.update_data(category_id=category_id)
    data = await state.get_data()
    a1 =await search_by_category_id(data["category_id"])
    result = ""
    for i in a1:
        result+= f"""
    Id: {i['books_id']}  
    Имя: {i['title']}  
    Описания: {i['caption']}
    Издательство: {i['publisher']}
"""
    await callback.message.answer(result)
    await state.clear()

    