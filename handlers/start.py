import sqlite3
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.all_keyboards import main_kb, item_kb, action_kb
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
    waiting_item = State() 
    waiting_price = State()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Выберите действие в клавиатуре бота.', reply_markup=main_kb(message.from_user.id))

@start_router.message(F.text == 'Назад⏪')
async def cmd(message: Message):
    await message.answer('Вы вернулись в главное меню.', reply_markup=main_kb(message.from_user.id))

@start_router.message(F.text == 'Информация❗️')
async def cmd(message: Message):
    await message.answer(f"❗️Бот канала Lotus Logistics❗️\n\n💹Актуальный курс юаня 1¥={yuan_rate}₽💹\n\n👉владелец - @ya_dimass👈")

@start_router.message(F.text == 'Рассчитать стоимость доставки💰')
async def cmd(message: Message, state: FSMContext):
    await message.answer("Выберите товар:", reply_markup=item_kb(message.from_user.id)) 
    await state.set_state(ClientStatesGroup.waiting_item)

@start_router.callback_query(lambda c: c.data.startswith("item_"))
async def process_product_selection(callback: CallbackQuery, state: FSMContext):
    item = callback.data.split("_")[1]

    await state.update_data(item=item)
    await callback.message.answer(f"Вы выбрали товар: {item}. Теперь введите его цену в юанях:")
    await state.set_state(ClientStatesGroup.waiting_price)
    await callback.answer()

'''
@start_router.message(ClientStatesGroup.waiting_item)
async def choose_item(message: Message, state: FSMContext):
    item = message.text
    await state.update_data(item=item)

    await message.reply('Укажите цену товара в юанях:')
    await state.set_state(ClientStatesGroup.waiting_price)
'''

@start_router.message(ClientStatesGroup.waiting_price)
async def get_item_price(message: Message, state: FSMContext):
    try:
        price = float(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите корректную цену (число).")
        return
    
    data = await state.get_data()
    item = data.get("item")

    if item == "Кроссовки👟":
        cost_in_rub = price * yuan_rate + 1700
    elif item == "Кофты":
        cost_in_rub = price * yuan_rate + 1100
    elif item == "Футболки👕":
        cost_in_rub = price * yuan_rate + 850
    elif item == "Косметика💅🏻/Аксессуары⌚️":
        cost_in_rub = price * yuan_rate + 700

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('INSERT INTO products (item, price) VALUES (?, ?)', (item, price))
    item_id = cursor.lastrowid
    connection.commit()

    user_id = message.from_user.id
    cursor.execute('INSERT INTO cart (user_id, item_id) VALUES (?, ?)', (user_id, item_id))
    connection.commit()

    connection.close()

    await message.answer(f"Товар '{item}' добавлен в корзину.\n"
                         f"Цена: {price} юаней (~{cost_in_rub:.2f} рублей).")

    await state.clear()

@start_router.message(Command('cart'))
async def cmd_cart(message: Message):
    user_id = message.from_user.id

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('''
    SELECT products.item, products.price
    FROM cart
    JOIN products ON cart.item_id = products.id
    WHERE cart.user_id = ?
    ''', (user_id,))
    items = cursor.fetchall()

    if items:
        response = "Ваша корзина:\n"
        total_cost = 0
        for item in items:
            cost_in_rub = item['price'] * yuan_rate
            response += f"- {item['item']}: {item['price']} юаней (~{cost_in_rub:.2f} рублей)\n"
            total_cost += item['price']
        response += f"Общая стоимость: {total_cost} юаней (~{total_cost * yuan_rate:.2f} рублей)."
    else:
        response = "Ваша корзина пуста."

    await message.answer(response)
    connection.close()