import sqlite3
from aiogram import Router, F
from aiogram.types import Message
from keyboards.all_keyboards import main_kb, item_kb
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

start_router = Router()
order_data = {}
yuan_rate = 14

def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

class ClientStatesGroup(StatesGroup):
    item = State() 
    cost = State()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    connection.close()

    await message.answer('Выберите действие в клавиатуре бота.', reply_markup=main_kb(message.from_user.id))

@start_router.message(Command("me"))
async def cmd_me(message: Message):
    user_id = message.from_user.id

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        await message.answer(f"Ваши данные:\n"
                            f"ID: {user['user_id']}\n"
                            f"Username: {user['username']}\n")
    else:
        await message.answer("Вы не найдены в базе данных.")

    conn.close()

@start_router.message(F.text == 'Рассчитать стоимость доставки💰')
async def cmd(message: Message, state: FSMContext):
    await message.answer("Выберите товар:", reply_markup=item_kb(message.from_user.id))
    await state.set_state(ClientStatesGroup.item)
    #user_state[message.from_user.id] = {"step": "awaiting_item"}

@start_router.message(F.text == 'Назад⏪')
async def cmd(message: Message):
    await message.answer('Вы вернулись в главное меню.', reply_markup=main_kb(message.from_user.id))

@start_router.message(F.text == 'Информация❗️')
async def cmd(message: Message):
    await message.answer(f"❗️Бот канала Lotus Logistics❗️\n\n💹Актуальный курс юаня 1¥={yuan_rate}₽💹\n\n👉владелец - @ya_dimass👈")

@start_router.message(F.content_type == "item", StateFilter(ClientStatesGroup.item))
async def choose_item(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['item'] = message.text

    await message.reply('Укажите цену в юанях:')
    await ClientStatesGroup.next()

@start_router.message(StateFilter(ClientStatesGroup.cost))
async def input_cost(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['cost'] = message.text
        print(data)

    await message.reply('Товар добавлен в корзину!')
    await state.finish

"""
@start_router.message()
async def handle_price_input(message: Message):
    user_id = message.from_user.id
    state = user_state.get(user_id)
    item_name = message.text.strip()
    
    if state and state["step"] == "awaiting_item":
        if item_name in ["Кроссовки👟", "Кофты", "Футболки👕", "Косметика💅🏻/Аксессуары⌚️"]:
            user_state[user_id]["item"] = item_name
            user_state[user_id]["step"] = "awaiting_price"
            await message.answer("Введите цену в юанях:")
        return
    
    if state and state["step"] == "awaiting_price":
        try:
            cny_price = float(message.text)
            item_name = user_state[user_id]["item"]

            if item_name == "Кроссовки👟":
                rub_price = cny_price * yuan_rate + 1700
            elif item_name == "Кофты":
                rub_price = cny_price * yuan_rate + 1100
            elif item_name == "Футболки👕":
                rub_price = cny_price * yuan_rate + 850
            elif item_name == "Косметика💅🏻/Аксессуары⌚️":
                rub_price = cny_price * yuan_rate + 700
            
            await edit_cart(state, user_id=message.from_user.id)
            await message.answer(f"Цена для товара '{item_name}' ≈ {rub_price} ₽.\nТовар добавлен в корзину.")

        except ValueError:
            await message.answer("Пожалуйста, введите корректное число.")
        finally:
            user_state.pop(user_id, None)

@start_router.message(Command("cart"))
async def show_cart(message: Message):
    user_id = message.from_user.id

    # Открываем соединение к базе данных
    db_connection = sqlite3.connect("cart.db")
    db_cursor = db_connection.cursor()

    try:
        # Получаем товары пользователя из базы данных
        db_cursor.execute("SELECT item_name, item_price FROM cart WHERE user_id = ?", (user_id,))
        items = db_cursor.fetchall()
    except sqlite3.Error as e:
        await message.answer(f"Ошибка базы данных: {e}")
        return
    finally:
        db_connection.close()  # Закрываем соединение

    if not items:
        await message.answer("Ваша корзина пуста.")
    else:
        total_price = sum(item[1] for item in items)
        cart_details = "\n".join([f"{item[0]}: {item[1]} ₽" for item in items])
        await message.answer(f"Ваша корзина:\n{cart_details}\n\nИтоговая сумма: {total_price} ₽")

@start_router.message(Command("clear"))
async def clear_cart(message: Message):
    user_id = message.from_user.id
    db_cursor.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
    db_connection.commit()
    await message.answer("Ваша корзина очищена.")
"""