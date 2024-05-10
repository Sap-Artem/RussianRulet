import asyncio
import random

from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery

from choice import main_menu, main_choice, gun_choice
from gameLogic import intelect, continuation
from fill import fill_bullets

bot = Bot(token="6702446643:AAFMyBrlTyFZb4GD0ArTCgTQm-aGqNKH77E")
dp = Dispatcher()

bullets = []
objects = []
play_live = 5
opponent_live = 5
kol = 0
kol_objects = 0
sum = 0
size = 0

class MyCallback(CallbackData, prefix="my"):
    foo: str

@dp.message(CommandStart())
async def start_cmd(message:types.Message):
    global bullets, play_live, opponent_live, kol, kol_objects, sum, size, objects
    bullets = []
    objects = []
    play_live = 5
    opponent_live = 5
    kol = 0
    kol_objects = 0
    sum = 0
    size = 0
    await message.answer(f"Осмелишься ли ты сыграть в смертельную рулетку? Садись за стол, и пусть повезёт сильнейшему", reply_markup=main_menu())

@dp.callback_query(MyCallback.filter(F.foo == "play"))
async def my_callback_foo(querty: CallbackQuery):
    try:
        await querty.message.delete()
    except:
        print(querty)
    global sum, size, kol_objects, bullets, play_live, kol, opponent_live
    print(kol_objects, sum, play_live, opponent_live, kol)
    if len(bullets) == 0:
        bullets, kol_objects, sum, play_live, opponent_live, kol = await fill_bullets(querty, bullets, kol_objects, sum, play_live, opponent_live, kol)
    print(*bullets)
    str_object = ""
    if len(objects) == 0:
        str_object = "Отсутствуют"
    else:
        for i in range(0,len(objects)-1):
            str_object = str_object + objects[i] + ", "
        str_object = str_object + objects[len(objects)-1]
        #print(str_object)
    await querty.message.answer(f"Сейчас твой ход! Оцените свои возможности, чтобы придумать эффективную стратегию" + "\n" + "Ваше здоровье: " + str(play_live) + "\n" + "Здоровье противника: " + str(opponent_live) + "\n" + "Ваши предметы: " + str_object + "\n" + "Вы можете вытащить ещё " + str(kol_objects) + " предметов", reply_markup=main_choice(kol, kol_objects))

@dp.callback_query(MyCallback.filter(F.foo == "gun"))
async def my_callback_foo(querty: CallbackQuery):
    await querty.message.delete()
    await querty.message.answer(f"Сделай правильный выбор. В кого будет направлен выстрел?", reply_markup=gun_choice())

@dp.callback_query(MyCallback.filter(F.foo == "give"))
async def my_callback_foo(querty: CallbackQuery):
    await querty.message.delete()
    global objects, kol_objects, kol
    baf = random.randint(0,10)
    kol_objects = kol_objects - 1
    kol = kol + 1
    if baf == 0:
        objects.append("бинт")
        await querty.message.answer(f"Вы достали бинт. У вас есть возможность востановить здоровье на 1 HP", reply_markup=continuation())
    elif baf == 1:
        objects.append("аптечка")
        await querty.message.answer(f"Вы достали аптечку. У вас есть возможность востановить здоровье на 2 HP", reply_markup=continuation())
    elif baf == 2:
        objects.append("обрез")
        await querty.message.answer(f"Вы достали обрез. У вас есть возможность увеличить урон от выстрела в 2 раза", reply_markup=continuation())
    elif baf == 3:
        objects.append("клещи")
        await querty.message.answer(f"Вы достали клещи. У вас есть возможность вытащить следующую пулю из карабина", reply_markup=continuation())
    elif baf == 4:
        objects.append("лупа")
        await querty.message.answer(f"Вы достали лупу. У вас есть возможность подглядеть тип следующего патрона", reply_markup=continuation())
    elif baf == 5:
        objects.append("скотч")
        await querty.message.answer(f"Вы достали скотч. У вас есть возможность связать оппоненту руки и походить дважды", reply_markup=continuation())
    elif baf == 6:
        objects.append("дуплет")
        await querty.message.answer(f"Вы достали дуплет. У вас есть возможность выстрелить двумя пулями одновременно", reply_markup=continuation())
    elif baf == 7:
        objects.append("пулеворот")
        await querty.message.answer(f"Вы достали пулеворот. У вас есть возможность поменять тип следующей пули на противоположный", reply_markup=continuation())
    elif baf == 8:
        objects.append("шаверма")
        await querty.message.answer(f"Вы достали шаверму. Свежая шаверма востановит 2 HP, просроченная уменьшит здоровье на 1 HP. Вероятность, что шаверма просроченная 50%", reply_markup=continuation())
    elif baf == 9:
        objects.append("лезвия")
        await querty.message.answer(f"Вы достали лезвия. У вас есть возможность пожертвовать 1 HP здоровья, чтобы увеличить урон в 3 раза", reply_markup=continuation())
    else:
        objects.append("карточка")
        await querty.message.answer(f"Вы достали магнитную карточку. У вас есть возможность узнать текущее количество заряженных и холостых патронов", reply_markup=continuation())

@dp.callback_query(MyCallback.filter(F.foo == "use"))
async def my_callback_foo(querty: CallbackQuery):
    await querty.message.delete()
    global bullets, play_live, opponent_live, kol, kol_objects, sum
    await querty.message.answer(f"Выберите один из предметов:",reply_markup=object_choice())

@dp.callback_query(MyCallback.filter(F.foo == "kill"))
async def my_callback_foo(querty: CallbackQuery):
    await querty.message.delete()
    global bullets, play_live, opponent_live, kol, kol_objects, sum
    if bullets.pop() == 1:
        msg = await querty.message.answer(f"*Ба-бах* Вы успешно выстрелили в оппонента")
        await asyncio.sleep(1)
        await msg.delete()
        opponent_live = opponent_live - 1
        sum = sum - 1
        msg = await querty.message.answer(f"Ваше здоровье: " + str(play_live) + "\n" + "Здоровье вашего оппонента: " + str(opponent_live))
        await asyncio.sleep(1)
        await msg.delete()
        if opponent_live == 0:
            await querty.message.answer(f"Вы победили!")
        else:
            msg = await querty.message.answer(f"Ход переходит противнику")
            await asyncio.sleep(1)
            await msg.delete()
            if len(bullets) == 0:
                bullets, kol_objects, sum, play_live, opponent_live, kol = await fill_bullets(querty, bullets, kol_objects, sum, play_live, opponent_live, kol)
            bullets, kol_objects, sum, play_live, opponent_live, kol = await intelect(querty, bullets, play_live, opponent_live, kol, kol_objects, sum)
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
        if len(bullets) == 0:
            bullets, kol_objects, sum, play_live, opponent_live, kol = await fill_bullets(querty, bullets, kol_objects, sum, play_live, opponent_live, kol)
        bullets, kol_objects, sum, play_live, opponent_live, kol = await intelect(querty, bullets, play_live, opponent_live, kol, kol_objects, sum)

@dp.callback_query(MyCallback.filter(F.foo == "himself"))
async def my_callback_foo(querty: CallbackQuery):
    await querty.message.delete()
    global bullets, play_live, opponent_live, kol, kol_objects, sum
    if bullets.pop() == 1:
        msg = await querty.message.answer(f"*Ба-бах* Вы выстрелили в себя")
        await asyncio.sleep(1)
        await msg.delete()
        play_live = play_live - 1
        sum = sum - 1
        msg = await querty.message.answer(f"Ваше здоровье: " + str(play_live) + "\n" + "Здоровье вашего оппонента: " + str(opponent_live))
        await asyncio.sleep(1)
        await msg.delete()
        if play_live == 0:
            await querty.message.answer(f"Вы проиграли!")
        else:
            msg = await querty.message.answer(f"Ход переходит противнику")
            await asyncio.sleep(1)
            await msg.delete()
            if (len(bullets) == 0):
                bullets, kol_objects, sum, play_live, opponent_live, kol = await fill_bullets(querty, bullets, kol_objects, sum, play_live, opponent_live, kol)
            bullets, kol_objects, sum, play_live, opponent_live, kol = await intelect(querty, bullets, play_live, opponent_live, kol, kol_objects, sum)
    else:
        msg = await querty.message.answer(f"*Щелчок* Ружьё не выстрелило")
        await asyncio.sleep(1)
        await msg.delete()
        msg = await querty.message.answer(f"Ваше здоровье: " + str(play_live) + "\n" + "Здоровье вашего оппонента: " + str(opponent_live))
        await asyncio.sleep(1)
        await msg.delete()
        if len(bullets) == 0:
            bullets, kol_objects, sum, play_live, opponent_live, kol = await fill_bullets(querty, bullets, kol_objects, sum, play_live, opponent_live, kol)
        print(*bullets)
        print(*objects)
        str_object = ""
        if len(objects) == 0:
            str_object = "Отсутствуют"
        else:
            for i in range(0, len(objects) - 1):
                str_object = str_object + objects[i] + ", "
            str_object = str_object + objects[len(objects) - 1]
            print(str_object)
        await querty.message.answer(f"Сейчас твой ход! Оцените свои возможности, чтобы придумать эффективную стратегию" + "\n" + "Ваше здоровье: " + str(play_live) + "\n" + "Здоровье противника: " + str(opponent_live) + "\n" + "Ваши предметы: " + str_object + "\n" + "Вы можете вытащить ещё " + str(kol_objects) + " предметов", reply_markup=main_choice(kol, kol_objects))

async def main():
    await bot.delete_webhook()
    await dp.start_polling(bot)

asyncio.run(main())