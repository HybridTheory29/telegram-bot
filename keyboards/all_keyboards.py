from botBody import admins
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

def main_kb(user_telegram_id: int):
    kb_list = [
    [KeyboardButton(text='Корзина')],
    [KeyboardButton(text='Главное меню')],
    [KeyboardButton(text='Очистить корзину')]
    ]
    
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text="⚙️ Админ панель")])

    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard

def action_kb():
    
    kb_list = [
    [InlineKeyboardButton(text='Рассчитать стоимость доставки', callback_data='Рассчитать стоимость доставки')],
    [InlineKeyboardButton(text='Информация', callback_data='Информация')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def item_kb():
    
    kb_list = [
    [InlineKeyboardButton(text='Кроссовки👟', callback_data='item_Кроссовки👟'), InlineKeyboardButton(text='Кофты', callback_data='item_Кофты'),],
    [InlineKeyboardButton(text='Футболки👕', callback_data='item_Футболки👕'), InlineKeyboardButton(text='Косметика💅🏻/Аксессуары⌚️', callback_data='item_Косметика💅🏻/Аксессуары⌚️')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard