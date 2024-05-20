from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MyCallback(CallbackData, prefix="my"):
    foo: str

def main_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="Начать игру",callback_data=MyCallback(foo="play"))
    return builder.as_markup()

def main_choice(kol, kol_objects):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Взять в руки оружие", callback_data=MyCallback(foo="gun").pack()))
    print("kol: " + str(kol))
    if kol != 0:
        builder.add(InlineKeyboardButton(text="Использовать предмет", callback_data=MyCallback(foo="use").pack()))
    if kol_objects != 0:
        builder.add(InlineKeyboardButton(text="Вытащить новый предмет", callback_data=MyCallback(foo="give").pack()))
    return builder.adjust(1).as_markup()
def gun_choice():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Выстрелить в оппонента", callback_data=MyCallback(foo="kill").pack()))
    builder.add(InlineKeyboardButton(text="Выстрелить в себя", callback_data=MyCallback(foo="himself").pack()))
    return builder.adjust(1).as_markup()
def object_choice(objects):
    builder = InlineKeyboardBuilder()
    for i in range(len(objects)):
        print(objects[i])
        builder.add(InlineKeyboardButton(text=str(objects[i]), callback_data=MyCallback(foo=objects[i]).pack()))
    builder.add(InlineKeyboardButton(text="Назад", callback_data=MyCallback(foo="play").pack()))
    return builder.adjust(1).as_markup()