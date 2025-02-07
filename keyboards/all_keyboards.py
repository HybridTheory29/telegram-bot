from botBody import admins
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def main_kb(user_telegram_id: int):
    kb_list = [
    [KeyboardButton(text='Рассчитать стоимость доставки💰')],
    [KeyboardButton(text='Информация❗️')]
    ]
    
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text="⚙️ Админ панель")])

    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
    return keyboard

def item_kb(user_telegram_id: int):
    kb_list = [
    [KeyboardButton(text='Кроссовки👟'), KeyboardButton(text='Кофты'),],
    [KeyboardButton(text='Футболки👕'), KeyboardButton(text='Косметика💅🏻/Аксессуары⌚️')],
    [KeyboardButton(text='Назад⏪')]
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
    return keyboard