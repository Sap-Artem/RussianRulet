import asyncio
import random

from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from fill import fill_bullets
from randomObjects import random_objects, hill_objects, damage_objects, look_objects, negative_objects, one_objects


async def opponent_solution(querty, bullets, opponent_objects, opponent_live, opponent_damage, play_live, sum, solution_lite, finish):
    if (len(bullets) == sum) | (solution_lite == 1):
        solution = 1
        damage_lite = -1
        for i in range(0, len(opponent_objects)):
            opponent_objects, opponent_live, opponent_damage, i, damage_lite = await damage_objects(querty, opponent_objects, i, opponent_live, opponent_damage, damage_lite)
            if damage_lite != -1:
                break
    elif (sum == 0) | (solution_lite == 0):
        solution_lite = -1
        for i in range(0, len(opponent_objects)):
            bullets, opponent_objects, i, solution_lite = await negative_objects(querty, bullets, opponent_objects, i, solution_lite)
            if solution_lite != -1:
                break
        if solution_lite == 1:
            return await opponent_solution(querty, bullets, opponent_objects, opponent_live, opponent_damage, play_live, sum, solution_lite, finish)
        if solution_lite == 0:
            return 0, bullets, opponent_objects, opponent_live, opponent_damage, play_live, sum, finish
        solution = 0
    else:
        if (sum == 1) & (len(bullets) == 2):
            print("1+1")
            for i in range(0, len(opponent_objects)):
                bullets, opponent_objects, play_live, i, finish = await one_objects(querty, bullets, opponent_objects, play_live, i)
                if finish == 1:
                    return 1, bullets, opponent_objects, opponent_live, opponent_damage, play_live, sum, finish
        print("что?")
        for i in range(0, len(opponent_objects)):
            bullets, opponent_objects, i, solution_lite = await look_objects(querty, bullets, opponent_objects, i, solution_lite)
            print("opponent_damage = " + str(opponent_damage))
            if solution_lite != -1:
                break
        if solution_lite == 1:
            return await opponent_solution(querty, bullets, opponent_objects, opponent_live, opponent_damage, play_live, sum, solution_lite, finish)
        if solution_lite == 0:
            return await opponent_solution(querty, bullets, opponent_objects, opponent_live, opponent_damage, play_live, sum, solution_lite, finish)
        pre_solution = random.randint(0, len(bullets) - 1)
        if pre_solution < sum:
            solution = 1
        else:
            solution = 0
    return solution, bullets, opponent_objects, opponent_live, opponent_damage, play_live, sum, finish

async def intelect(bot, querty: CallbackQuery, bullets, play_live, opponent_live, kol, kol_objects, sum, damage, kol_opponent_objects, opponent_objects):
    print("интеллект |")
    print(sum, len(bullets))
    opponent_damage = 1
    finish = 0
    if kol_opponent_objects > 0:
        msg = await querty.message.answer(f"Ваш оппонент вытащил из мешка два загадочных предмета")
        await asyncio.sleep(2)
        await msg.delete()
        baf1, opponent_objects = random_objects(opponent_objects)
        baf2, opponent_objects = random_objects(opponent_objects)
        #opponent_objects.append("скотч")
        print(*opponent_objects)
        if opponent_live < 4:
            j = 0
            while j < len(opponent_objects):
                print("i= " + str(j))
                opponent_objects, opponent_live, j = await hill_objects(querty, opponent_objects, j, opponent_live)
                j = j + 1
                print("!i= " + str(j))
        kol_opponent_objects -= 2
    solution, bullets, opponent_objects, opponent_live, opponent_damage, play_live, sum, finish = await opponent_solution(querty, bullets, opponent_objects, opponent_live, opponent_damage, play_live, sum, -1, 0)
    if finish == 1:
        bullets, kol_objects, sum, play_live, opponent_live, kol, kol_opponent_objects = await fill_bullets(bot, querty, bullets, kol_objects, sum, play_live, opponent_live, kol, kol_opponent_objects)
        photo_input = FSInputFile('./pictures/continue.png', 'rb')
        await bot.send_photo(querty.message.chat.id, photo_input, caption=f"Ход переходит вам", reply_markup=continuation())
        return bullets, kol_objects, sum, play_live, opponent_live, kol, damage, kol_opponent_objects, opponent_objects
    if solution == 0:
        msg = await querty.message.answer(f"Ваш оппонент направляет ружьё на себя")
        await asyncio.sleep(2)
        await msg.delete()
        if bullets.pop() == 1:
            photo_input = FSInputFile('./pictures/shot.png', 'rb')
            msg = await bot.send_photo(querty.message.chat.id, photo_input, caption=f"*Ба-бах* Оппонент выстрелил в себя")
            await asyncio.sleep(2)
            await msg.delete()
            opponent_live -= 1
            sum -= 1
            msg = await querty.message.answer(f"Ваше здоровье: {play_live}\nЗдоровье вашего оппонента: {opponent_live}")
            await asyncio.sleep(1)
            await msg.delete()
            if opponent_live <= 0:
                photo_input = FSInputFile('./pictures/lucky.png', 'rb')
                await bot.send_photo(querty.message.chat.id, photo_input, caption=f"Вы победили!")
                return bullets, kol_objects, sum, play_live, opponent_live, kol, damage, kol_opponent_objects, opponent_objects
            else:
                if len(bullets) == 0:
                    bullets, kol_objects, sum, play_live, opponent_live, kol, kol_opponent_objects = await fill_bullets(bot, querty, bullets, kol_objects, sum, play_live, opponent_live, kol, kol_opponent_objects)
                photo_input = FSInputFile('./pictures/continue.png', 'rb')
                await bot.send_photo(querty.message.chat.id, photo_input, caption=f"Ход переходит вам", reply_markup=continuation())
                return bullets, kol_objects, sum, play_live, opponent_live, kol, damage, kol_opponent_objects, opponent_objects
        else:
            photo_input = FSInputFile('./pictures/miss.png', 'rb')
            msg = await bot.send_photo(querty.message.chat.id, photo_input, caption=f"*Щелчок* Ружьё не выстрелило")
            await asyncio.sleep(2)
            await msg.delete()
            msg = await querty.message.answer(f"Ваше здоровье: {play_live}\nЗдоровье вашего оппонента: {opponent_live}")
            await asyncio.sleep(1)
            await msg.delete()
            msg = await querty.message.answer(f"Соперник продолжает ход")
            await asyncio.sleep(1)
            await msg.delete()
            print("bullets: = " + str(bullets))
            if len(bullets) == 0:
                bullets, kol_objects, sum, play_live, opponent_live, kol, kol_opponent_objects = await fill_bullets(bot, querty, bullets, kol_objects, sum, play_live, opponent_live, kol, kol_opponent_objects)
            return await intelect(bot, querty, bullets, play_live, opponent_live, kol, kol_objects, sum, damage, kol_opponent_objects, opponent_objects)
    else:
        print("opponent_damage: " + str(opponent_damage))
        msg = await querty.message.answer(f"Ваш оппонент направляет ружьё на вас")
        await asyncio.sleep(2)
        await msg.delete()
        if bullets.pop() == 1:
            photo_input = FSInputFile('./pictures/shot.png', 'rb')
            msg = await bot.send_photo(querty.message.chat.id, photo_input, caption=f"*Ба-бах* Оппонент выстрелил в вас")
            await asyncio.sleep(2)
            await msg.delete()
            play_live -= opponent_damage
            sum -= 1
            msg = await querty.message.answer(f"Ваше здоровье: {play_live}\nЗдоровье вашего оппонента: {opponent_live}")
            await asyncio.sleep(1)
            await msg.delete()
            if play_live <= 0:
                photo_input = FSInputFile('./pictures/lose.png', 'rb')
                await bot.send_photo(querty.message.chat.id, photo_input, caption=f"Вы проиграли!")
                return bullets, kol_objects, sum, play_live, opponent_live, kol, damage, kol_opponent_objects, opponent_objects
            else:
                if len(bullets) == 0:
                    bullets, kol_objects, sum, play_live, opponent_live, kol, kol_opponent_objects = await fill_bullets(bot, querty, bullets, kol_objects, sum, play_live, opponent_live, kol, kol_opponent_objects)
                photo_input = FSInputFile('./pictures/continue.png', 'rb')
                await bot.send_photo(querty.message.chat.id, photo_input, caption=f"Ход переходит вам", reply_markup=continuation())
                return bullets, kol_objects, sum, play_live, opponent_live, kol, damage, kol_opponent_objects, opponent_objects
        else:
            photo_input = FSInputFile('./pictures/miss.png', 'rb')
            msg = await bot.send_photo(querty.message.chat.id, photo_input, caption=f"*Щелчок* Ружьё не выстрелило")
            await asyncio.sleep(2)
            await msg.delete()
            msg = await querty.message.answer(f"Ваше здоровье: {play_live}\nЗдоровье вашего оппонента: {opponent_live}")
            await asyncio.sleep(1)
            await msg.delete()
            if len(bullets) == 0:
                bullets, kol_objects, sum, play_live, opponent_live, kol, kol_opponent_objects = await fill_bullets(bot, querty, bullets, kol_objects, sum, play_live, opponent_live, kol, kol_opponent_objects)
            photo_input = FSInputFile('./pictures/continue.png', 'rb')
            await bot.send_photo(querty.message.chat.id, photo_input, caption=f"Ход переходит вам", reply_markup=continuation())
            return bullets, kol_objects, sum, play_live, opponent_live, kol, damage, kol_opponent_objects, opponent_objects


def continuation():
    builder = InlineKeyboardBuilder()
    builder.button(text="Продолжить игру", callback_data=MyCallback(foo="play"))
    return builder.as_markup()


class MyCallback(CallbackData, prefix="my"):
    foo: str
