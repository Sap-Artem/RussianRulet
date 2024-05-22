import asyncio
import random

from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, FSInputFile

from choice import main_menu, main_choice, gun_choice, object_choice
from gameLogic import intelect, continuation
from fill import fill_bullets
from killTrue import killT
from killFalse import killF

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
damage = 1
opponent_objects = 0
skotch = False
duplet = False

class MyCallback(CallbackData, prefix="my"):
    foo: str

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    global bullets, play_live, opponent_live, kol, kol_objects, sum, size, objects, damage
    bullets = []
    objects = []
    play_live = 5
    opponent_live = 5
    kol = 0
    kol_objects = 0
    sum = 0
    size = 0
    damage = 1
    opponent_objects = 0
    skotch = False
    duplet = False
    photo_input = FSInputFile('./pictures/hello.png', 'rb')
    await bot.send_photo(message.chat.id, photo_input, caption=f"Осмелишься ли ты сыграть в смертельную рулетку? ☠️" + "\n" + "Садись за стол, и пусть повезёт сильнейшему! 💪", reply_markup=main_menu())


@dp.callback_query(MyCallback.filter(F.foo == "play"))
async def my_callback_foo(querty: CallbackQuery):
    try:
        await querty.message.delete()
    except:
        print(querty)
    global sum, size, kol_objects, bullets, play_live, kol, opponent_live, damage, opponent_objects
    print(kol_objects, sum, play_live, opponent_live, kol)
    if len(bullets) == 0:
        bullets, kol_objects, sum, play_live, opponent_live, kol, opponent_objects = await fill_bullets(bot, querty, bullets, kol_objects, sum, play_live, opponent_live, kol, opponent_objects)
    print(*bullets)
    str_object = ""
    if len(objects) == 0:
        str_object = "Отсутствуют"
    else:
        for i in range(0,len(objects)-1):
            str_object = str_object + objects[i] + ", "
        str_object = str_object + objects[len(objects)-1]
        #print(str_object)
    photo_input = FSInputFile('./pictures/main menu.png', 'rb')
    await bot.send_photo(querty.message.chat.id, photo_input, caption=f"Сейчас твой ход! Оцените свои возможности, чтобы придумать эффективную стратегию" + "\n" + "Ваше здоровье: " + str(play_live) + "\n" + "Здоровье противника: " + str(opponent_live) + "\n" + "Ваши предметы: " + str_object + "\n" + "Вы можете вытащить ещё " + str(kol_objects) + " предметов", reply_markup=main_choice(kol, kol_objects))

@dp.callback_query(MyCallback.filter(F.foo == "gun"))
async def my_callback_foo(querty: CallbackQuery):
    await querty.message.delete()
    photo_input = FSInputFile('./pictures/seriousChoice.png', 'rb')
    await bot.send_photo(querty.message.chat.id, photo_input, caption=f"Сделай правильный выбор. В кого будет направлен выстрел?", reply_markup=gun_choice())

@dp.callback_query(MyCallback.filter(F.foo == "give"))
async def my_callback_foo(querty: CallbackQuery):
    await querty.message.delete()
    global objects, kol_objects, kol
    baf = random.randint(0,11)
    #baf = 0
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
        objects.append("просроченное лекарство")
        await querty.message.answer(f"Вы достали просроченное лекарство. У вас есть шанс 50% восстановить 1 HP. В противном случае вы потеряете 2 HP", reply_markup=continuation())
    elif baf == 10:
        objects.append("лезвия")
        await querty.message.answer(f"Вы достали лезвия. У вас есть возможность пожертвовать 1 HP здоровья, чтобы увеличить урон в 3 раза", reply_markup=continuation())
    else:
        objects.append("карточка")
        await querty.message.answer(f"Вы достали магнитную карточку. У вас есть возможность узнать текущее количество заряженных и холостых патронов", reply_markup=continuation())
@dp.callback_query(MyCallback.filter(F.foo == "use"))
async def my_callback_foo(querty: CallbackQuery):
    await querty.message.delete()
    global bullets, play_live, opponent_live, kol, kol_objects, sum, damage, objects
    photo_input = FSInputFile('./pictures/objects.png', 'rb')
    await bot.send_photo(querty.message.chat.id, photo_input, caption=f"Выберите один из предметов:", reply_markup=object_choice(objects))
@dp.callback_query(MyCallback.filter(F.foo == "бинт"))
async def my_callback_foo(querty: CallbackQuery):
    await querty.message.delete()
    global bullets, play_live, opponent_live, kol, kol_objects, sum, damage, objects
    play_live = play_live + 1
    kol = kol - 1
    objects.remove("бинт")
    await querty.message.answer(f"Вы использовали бинт. Ваше здоровье восстановлено на 1 HP:", reply_markup=continuation())
@dp.callback_query(MyCallback.filter(F.foo == "аптечка"))
async def my_callback_foo(querty: CallbackQuery):
    await querty.message.delete()
    global bullets, play_live, opponent_live, kol, kol_objects, sum, damage, objects
    play_live = play_live + 2
    kol = kol - 1
    objects.remove("аптечка")
    await querty.message.answer(f"Вы использовали аптечку. Ваше здоровье восстановлено на 2 HP:", reply_markup=continuation())
@dp.callback_query(MyCallback.filter(F.foo == "обрез"))
async def my_callback_foo(querty: CallbackQuery):
    await querty.message.delete()
    global bullets, play_live, opponent_live, kol, kol_objects, sum, damage, objects
    damage = damage + 1
    kol = kol - 1
    print("!damage=" + str(damage))
    objects.remove("обрез")
    await querty.message.answer(f"Вы использовали обрез. Урон следующего выстрела увеличен на единицу:", reply_markup=continuation())
@dp.callback_query(MyCallback.filter(F.foo == "клещи"))
async def my_callback_foo(querty: CallbackQuery):
    await querty.message.delete()
    global bullets, play_live, opponent_live, kol, kol_objects, sum, damage, objects
    if bullets[len(bullets)-1] == 0:
        await querty.message.answer(f"Вы использовали клещи. Вы вытащили следующий патрон из ружья. Его гильза оказалась пустой", reply_markup=continuation())
    else:
        await querty.message.answer(f"Вы использовали клещи. Вы вытащили следующий патрон из ружья. Его гильза оказалась заряженной",reply_markup=continuation())
    bullets.pop()
    kol = kol - 1
    objects.remove("клещи")
@dp.callback_query(MyCallback.filter(F.foo == "лупа"))
async def my_callback_foo(querty: CallbackQuery):
    await querty.message.delete()
    global bullets, play_live, opponent_live, kol, kol_objects, sum, damage, objects
    if bullets[len(bullets)-1] == 0:
        await querty.message.answer(f"Вы использовали лупу. Следующий патрон в ружье - холостой", reply_markup=continuation())
    else:
        await querty.message.answer(f"Вы использовали лупу. Следующий патрон в ружье - заряженный",reply_markup=continuation())
    kol = kol - 1
    objects.remove("лупа")
@dp.callback_query(MyCallback.filter(F.foo == "скотч"))
async def my_callback_foo(querty: CallbackQuery):
    await querty.message.delete()
    global bullets, play_live, opponent_live, kol, kol_objects, sum, damage, skotch, duplet, objects
    skotch = True
    await querty.message.answer(f"Руки вашего соперника связаны скотчем. Вы сможете выстрелить два раза подряд", reply_markup=continuation())
    kol = kol - 1
    objects.remove("скотч")
@dp.callback_query(MyCallback.filter(F.foo == "дуплет"))
async def my_callback_foo(querty: CallbackQuery):
    await querty.message.delete()
    global bullets, play_live, opponent_live, kol, kol_objects, sum, damage, skotch, duplet, objects
    duplet = True
    kol = kol - 1
    objects.remove("дуплет")
    await querty.message.answer(f"Вы использовали дуплет. В следующий раз ружьё выстрелит двумя пулями одновременно", reply_markup=continuation())

@dp.callback_query(MyCallback.filter(F.foo == "пулеворот"))
async def my_callback_foo(querty: CallbackQuery):
    await querty.message.delete()
    global bullets, play_live, opponent_live, kol, kol_objects, sum, damage, skotch, duplet, objects
    g = bullets.pop()
    if g == 0:
        bullets.append(1)
    else:
        bullets.append(0)
    objects.remove("пулеворот")
    kol = kol - 1
    await querty.message.answer(f"Вы использовали пулеворот. Тип следующей пули заменён на противоположный", reply_markup=continuation())

@dp.callback_query(MyCallback.filter(F.foo == "шаверма"))
async def my_callback_foo(querty: CallbackQuery):
    await querty.message.delete()
    global bullets, play_live, opponent_live, kol, kol_objects, sum, damage, skotch, duplet, objects
    r = random.randint(0, 1)
    if r == 1:
        play_live = play_live + 2
        await querty.message.answer(f"Вы использовали шаверму. Вам повезло: вы восстановили 2 единицы здоровья",reply_markup=continuation())
    else:
        play_live = play_live - 1
        await querty.message.answer(f"Вы использовали шаверму. Вам неповезло: вы потеряли 1 единицу здоровья", reply_markup=continuation())
    objects.remove("шаверма")
    kol = kol - 1
@dp.callback_query(MyCallback.filter(F.foo == "просроченное лекарство"))
async def my_callback_foo(querty: CallbackQuery):
    await querty.message.delete()
    global bullets, play_live, opponent_live, kol, kol_objects, sum, damage, skotch, duplet, objects
    r = random.randint(0, 1)
    if r == 1:
        play_live = play_live + 1
        await querty.message.answer(f"Вы использовали просроченное лекарство. Вам повезло: вы восстановили 1 единицы здоровья",reply_markup=continuation())
    else:
        play_live = play_live - 2
        await querty.message.answer(f"Вы использовали просроченное лекарство. Вам неповезло: вы потеряли 2 единицу здоровья", reply_markup=continuation())
    objects.remove("просроченное лекарство")
@dp.callback_query(MyCallback.filter(F.foo == "лезвия"))
async def my_callback_foo(querty: CallbackQuery):
    await querty.message.delete()
    global bullets, play_live, opponent_live, kol, kol_objects, sum, damage, objects
    damage = damage + 3
    play_live = play_live - 1
    print("!damage=" + str(damage))
    objects.remove("лезвия")
    await querty.message.answer(f"Вы использовали лезвие. Вы потеряли 1 HP, урон следующего выстрела увеличен на 2:", reply_markup=continuation())

@dp.callback_query(MyCallback.filter(F.foo == "карточка"))
async def my_callback_foo(querty: CallbackQuery):
    await querty.message.delete()
    global bullets, play_live, opponent_live, kol, kol_objects, sum, damage, objects
    objects.remove("карточка")
    await querty.message.answer(f"Вы использовали карточку. Вы узнали, что в ружье находится " + str(sum) + " заряженных патронов и " + str(len(bullets)-sum) + " холостых", reply_markup=continuation())

@dp.callback_query(MyCallback.filter(F.foo == "kill"))
async def my_callback_foo(querty: CallbackQuery):
    await querty.message.delete()
    global bullets, play_live, opponent_live, kol, kol_objects, sum, damage, duplet, skotch, objects, opponent_objects
    if (duplet) & (len(bullets) > 1):
        g1 = bullets.pop()
        g2 = bullets.pop()
        print("gg что?" + str(g1) + " " + str(g2))
        damage = g1 + g2
        if damage > 0:
            bullets, kol_objects, sum, play_live, opponent_live, kol, damage, skotch, objects, opponent_objects = await killT(bot, querty, bullets, kol_objects, sum, play_live, opponent_live, kol, damage, skotch, objects, opponent_objects)
        else:
            bullets, kol_objects, sum, play_live, opponent_live, kol, damage, skotch, objects, opponent_objects = await killF(bot, querty, bullets, kol_objects, sum, play_live, opponent_live, kol, damage, skotch, objects, opponent_objects)
    else:
        if bullets.pop() == 1:
            bullets, kol_objects, sum, play_live, opponent_live, kol, damage, skotch, objects, opponent_objects = await killT(bot, querty, bullets, kol_objects, sum, play_live, opponent_live, kol, damage, skotch, objects, opponent_objects)
        else:
            bullets, kol_objects, sum, play_live, opponent_live, kol, damage, skotch, objects, opponent_objects = await killF(bot, querty, bullets, kol_objects, sum, play_live, opponent_live, kol, damage, skotch, objects, opponent_objects)
@dp.callback_query(MyCallback.filter(F.foo == "himself"))
async def my_callback_foo(querty: CallbackQuery):
    await querty.message.delete()
    global bullets, play_live, opponent_live, kol, kol_objects, sum, damage, opponent_objects
    if bullets.pop() == 1:
        photo_input = FSInputFile('./pictures/shot.png', 'rb')
        msg = await bot.send_photo(querty.message.chat.id, photo_input, caption=f"*Ба-бах* Вы выстрелили в себя")
        await asyncio.sleep(2)
        await msg.delete()
        play_live = play_live - 1
        sum = sum - 1
        msg = await querty.message.answer(f"Ваше здоровье: " + str(play_live) + "\n" + "Здоровье вашего оппонента: " + str(opponent_live))
        await asyncio.sleep(1)
        await msg.delete()
        if play_live <= 0:
            photo_input = FSInputFile('./pictures/lose.png', 'rb')
            await bot.send_photo(querty.message.chat.id, photo_input, caption=f"Вы проиграли!")
        else:
            msg = await querty.message.answer(f"Ход переходит противнику")
            await asyncio.sleep(1)
            await msg.delete()
            if (len(bullets) == 0):
                bullets, kol_objects, sum, play_live, opponent_live, kol, opponent_objects = await fill_bullets(bot, querty, bullets, kol_objects, sum, play_live, opponent_live, kol, opponent_objects)
            bullets, kol_objects, sum, play_live, opponent_live, kol, damage, opponent_objects = await intelect(bot, querty, bullets, play_live, opponent_live, kol, kol_objects, sum, damage, opponent_objects)
    else:
        photo_input = FSInputFile('./pictures/miss.png', 'rb')
        msg = await bot.send_photo(querty.message.chat.id, photo_input, caption=f"*Щелчок* Ружьё не выстрелило")
        await asyncio.sleep(2)
        await msg.delete()
        msg = await querty.message.answer(f"Ваше здоровье: " + str(play_live) + "\n" + "Здоровье вашего оппонента: " + str(opponent_live))
        await asyncio.sleep(1)
        await msg.delete()
        if len(bullets) == 0:
            bullets, kol_objects, sum, play_live, opponent_live, kol, opponent_objects = await fill_bullets(bot, querty, bullets, kol_objects, sum, play_live, opponent_live, kol, opponent_objects)
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
        photo_input = FSInputFile('./pictures/main menu.png', 'rb')
        await bot.send_photo(querty.message.chat.id, photo_input, caption=f"Сейчас твой ход! Оцените свои возможности, чтобы придумать эффективную стратегию" + "\n" + "Ваше здоровье: " + str(play_live) + "\n" + "Здоровье противника: " + str(opponent_live) + "\n" + "Ваши предметы: " + str_object + "\n" + "Вы можете вытащить ещё " + str(kol_objects) + " предметов", reply_markup=main_choice(kol, kol_objects))
async def main():
    await bot.delete_webhook()
    await dp.start_polling(bot)
asyncio.run(main())