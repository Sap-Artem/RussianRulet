import asyncio
import logging
import sys
import random
from os import getenv

from aiogram import F
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardButton
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from aiogram.enums import ParseMode
from aiogram.methods.delete_message import DeleteMessage
from aiogram.methods import DeleteMessage

bot = Bot(token="6702446643:AAFMyBrlTyFZb4GD0ArTCgTQm-aGqNKH77E")
dp = Dispatcher()

bullets = []
play_live = 3
opponent_live = 3
kol = 0
objects = 2
sum = 0
size = 0

class MyCallback(CallbackData, prefix="my"):
    foo: str

def main_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="Начать игру",callback_data=MyCallback(foo="play"))
    return builder.as_markup()

def continuation():
    builder = InlineKeyboardBuilder()
    builder.button(text="Продолжить игру",callback_data=MyCallback(foo="play"))
    return builder.as_markup()

def main_choice():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Взять в руки оружие", callback_data=MyCallback(foo="gun").pack()))
    builder.add(InlineKeyboardButton(text="Использовать предмет", callback_data=MyCallback(foo="use").pack()))
    builder.add(InlineKeyboardButton(text="Вытащить новый предмет", callback_data=MyCallback(foo="give").pack()))
    return builder.adjust(1).as_markup()
def gun_choice():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Выстрелить в оппонента", callback_data=MyCallback(foo="kill").pack()))
    builder.add(InlineKeyboardButton(text="Выстрелить в себя", callback_data=MyCallback(foo="himself").pack()))
    return builder.adjust(1).as_markup()

async def intelect(querty: CallbackQuery):
    global bullets, play_live, opponent_live, kol, objects, sum
    soluthion = 0
    if(len(bullets) == sum):
        soluthion = 1
    elif(sum == 0):
        soluthion = 0
    else:
        soluthion = random.randint(0,1)
    print(soluthion)
    if(soluthion == 0):
        msg = await querty.message.answer(f"Ваш оппонент направляет ружьё на себя")
        await asyncio.sleep(1)
        await msg.delete()
        if(bullets.pop() == 1):
            msg = await querty.message.answer(f"*Ба-бах* Оппонент выстрелили в себя")
            await asyncio.sleep(1)
            await msg.delete()
            opponent_live = opponent_live - 1
            msg = await querty.message.answer(f"Ваше здоровье: " + str(play_live) + "\n" + "Здоровье вашего оппонента: " + str(opponent_live))
            await asyncio.sleep(1)
            await msg.delete()
            print(opponent_live)
            if (opponent_live == 0):
                await querty.message.answer(f"Вы победили!")
            else:
                if (len(bullets) == 0):
                    await fill_bullets(querty)
                await message.answer(f"Ход переходит вам", reply_markup=continuation())
        else:
            msg = await querty.message.answer(f"*Щелчок* Ружьё не выстрелило")
            await asyncio.sleep(1)
            await msg.delete()
            msg = await querty.message.answer(f"Ваше здоровье: " + str(play_live) + "\n" + "Здоровье вашего оппонента: " + str(opponent_live))
            await asyncio.sleep(1)
            await msg.delete()
            print(opponent_live)
            msg = await querty.message.answer(f"Соперник продолжает ход")
            await msg.delete()
            if (len(bullets) == 0):
                await fill_bullets(querty)
            await intelect(querty)
    else:
        msg = await querty.message.answer(f"Ваш оппонент направляет ружьё на вас")
        await asyncio.sleep(1)
        await msg.delete()
        if (bullets.pop() == 1):
            msg = await querty.message.answer(f"*Ба-бах* Оппонент выстрелил в вас")
            await asyncio.sleep(1)
            await msg.delete()
            play_live = play_live - 1
            msg = await querty.message.answer(f"Ваше здоровье: " + str(play_live) + "\n" + "Здоровье вашего оппонента: " + str(opponent_live))
            await asyncio.sleep(1)
            await msg.delete()
            print(play_live)
            if (play_live == 0):
                await querty.message.answer(f"Вы проиграли!")
            else:
                if (len(bullets) == 0):
                    await fill_bullets(querty)
                await querty.message.answer(f"Ход переходит вам", reply_markup=continuation())
        else:
            msg = await querty.message.answer(f"*Щелчок* Ружьё не выстрелило")
            await asyncio.sleep(1)
            await msg.delete()
            msg = await querty.message.answer(f"Ваше здоровье: " + str(play_live) + "\n" + "Здоровье вашего оппонента: " + str(opponent_live))
            await asyncio.sleep(1)
            await msg.delete()
            print(play_live)
            if (len(bullets) == 0):
                await fill_bullets(querty)
            await querty.message.answer(f"Ход переходит вам", reply_markup=continuation())

@dp.message(CommandStart())
async def start_cmd(message:types.Message):
    global bullets, play_live, opponent_live, kol, objects, sum, size
    bullets = []
    play_live = 3
    opponent_live = 3
    kol = 0
    objects = 2
    sum = 0
    size = 0
    await message.answer(f"Осмелишься ли ты сыграть в смертельную рулетку? Садись за стол, и пусть повезёт сильнейшему", reply_markup=main_menu())

async def fill_bullets(querty: CallbackQuery):
    global sum, size
    sum = 0
    size = random.randint(4, 8)
    for i in range(0, size):
        l = random.randint(0, 1)
        bullets.append(l)
        sum = sum + l
    if ((sum == 0) | (sum == size)):
        k = random.randint(0, size)
        if (sum == 0):
            bullets[k] = 1
            sum = sum + 1
        else:
            bullets[k] = 0
            sum = sum - 1
    msg = await querty.message.answer(f'Ваш противник заряжает в барабан ' + str(sum) + ' заряженных и ' + str(size - sum) + ' холостых потронов')
    await asyncio.sleep(2)
    await msg.delete()

@dp.callback_query(MyCallback.filter(F.foo == "play"))
async def my_callback_foo(querty: CallbackQuery, callback_data: MyCallback):
    try:
        await querty.message.delete()
    except:
        print(querty)
    global sum, size
    if (len(bullets) == 0):
        await fill_bullets(querty)
    print(*bullets)
    await querty.message.answer(f"Сейчас твой ход! Оцените свои возможности, чтобы придумать эффективную стратегию" + "\n" + "Ваше здоровье: " + str(play_live) + "\n" + "Здоровье противника: " + str(opponent_live) + "\n" + "Ваши предметы: " + str(kol) + "\n" + "Вы можете вытащить ещё " + str(objects) + " предметов", reply_markup=main_choice())

@dp.callback_query(MyCallback.filter(F.foo == "gun"))
async def my_callback_foo(querty: CallbackQuery, callback_data: MyCallback):
    await querty.message.delete()
    await querty.message.answer(f"Сделай правильный выбор. В кого будет направлен выстрел?", reply_markup=gun_choice())

@dp.callback_query(MyCallback.filter(F.foo == "kill"))
async def my_callback_foo(querty: CallbackQuery, callback_data: MyCallback):
    await querty.message.delete()
    global bullets, play_live, opponent_live, kol, objects
    if (bullets.pop() == 1):
        msg = await querty.message.answer(f"*Ба-бах* Вы успешно выстрелили в оппонента")
        await asyncio.sleep(1)
        await msg.delete()
        opponent_live = opponent_live - 1
        msg = await querty.message.answer(f"Ваше здоровье: " + str(play_live) + "\n" + "Здоровье вашего оппонента: " + str(opponent_live))
        await asyncio.sleep(1)
        await msg.delete()
        if (opponent_live == 0):
            await querty.message.answer(f"Вы победили!")
        else:
            msg = await querty.message.answer(f"Ход переходит противнику")
            await asyncio.sleep(1)
            await msg.delete()
            if (len(bullets) == 0):
                await fill_bullets(querty)
            await intelect(querty)
    else:
        msg = await querty.message.answer(f"*Щелчок* Ружьё не выстрелило")
        await asyncio.sleep(1)
        await msg.delete()
        msg = await querty.message.answer(f"Ваше здоровье: " + str(play_live) + "\n" + "Здоровье вашего оппонента: " + str(opponent_live))
        await asyncio.sleep(1)
        await msg.delete()
        msg = await querty.message.answer(f"Ход переходит противнику")
        await asyncio.sleep(1)
        await msg.delete()
        if (len(bullets) == 0):
            await fill_bullets(querty)
        await intelect(querty)

@dp.callback_query(MyCallback.filter(F.foo == "himself"))
async def my_callback_foo(querty: CallbackQuery, callback_data: MyCallback):
    await querty.message.delete()
    global bullets, play_live, opponent_live, kol, objects
    if (bullets.pop() == 1):
        msg = await querty.message.answer(f"*Ба-бах* Вы выстрелили в себя")
        await asyncio.sleep(1)
        await msg.delete()
        play_live = play_live - 1
        msg = await querty.message.answer(f"Ваше здоровье: " + str(play_live) + "\n" + "Здоровье вашего оппонента: " + str(opponent_live))
        await asyncio.sleep(1)
        await msg.delete()
        if (play_live == 0):
            await querty.message.answer(f"Вы проиграли!")
        else:
            msg = await querty.message.answer(f"Ход переходит противнику")
            await asyncio.sleep(1)
            await msg.delete()
            if (len(bullets) == 0):
                await fill_bullets(querty)
            await intelect(querty)
    else:
        msg = await querty.message.answer(f"*Щелчок* Ружьё не выстрелило")
        await asyncio.sleep(1)
        await msg.delete()
        msg = await querty.message.answer(f"Ваше здоровье: " + str(play_live) + "\n" + "Здоровье вашего оппонента: " + str(opponent_live))
        await asyncio.sleep(1)
        await msg.delete()
        if (len(bullets) == 0):
            await fill_bullets(querty)
        await querty.message.answer(f"Сейчас твой ход! Оцените свои возможности, чтобы придумать эффективную стратегию" + "\n" + "Ваше здоровье: " + str(play_live) + "\n" + "Здоровье противника: " + str(opponent_live) + "\n" + "Ваши предметы: " + str(kol) + "\n" + "Вы можете вытащить ещё " + str(objects) + " предметов", reply_markup=main_choice())

async def main():
    await bot.delete_webhook()
    await dp.start_polling(bot)

asyncio.run(main())