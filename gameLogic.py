import asyncio
import random

from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from fill import fill_bullets

async def intelect(bot, querty: CallbackQuery, bullets, play_live, opponent_live, kol, kol_objects, sum, damage, opponent_objects):
    print("итнелект |")
    print(sum, len(bullets))
    if len(bullets) == sum:
        solution = 1
    elif sum == 0:
        solution = 0
    else:
        pre_solution = random.randint(0, len(bullets)-1)
        if pre_solution < sum:
            solution = 1
        else:
            solution = 0
    if solution == 0:
        msg = await querty.message.answer(f"Ваш оппонент направляет ружьё на себя")
        await asyncio.sleep(1)
        await msg.delete()
        if bullets.pop() == 1:
            photo_input = FSInputFile('./pictures/shot.png', 'rb')
            msg = await bot.send_photo(querty.message.chat.id, photo_input, caption=f"*Ба-бах* Оппонент выстрелил в себя")
            await asyncio.sleep(2)
            await msg.delete()
            opponent_live = opponent_live - 1
            sum = sum - 1
            msg = await querty.message.answer(f"Ваше здоровье: " + str(play_live) + "\n" + "Здоровье вашего оппонента: " + str(opponent_live))
            await asyncio.sleep(1)
            await msg.delete()
            if opponent_live <= 0:
                photo_input = FSInputFile('./pictures/lucky.png', 'rb')
                await bot.send_photo(querty.message.chat.id, photo_input, caption=f"Вы победили!")
                return bullets, kol_objects, sum, play_live, opponent_live, kol, damage, opponent_objects
            else:
                if len(bullets) == 0:
                    bullets, kol_objects, sum, play_live, opponent_live, kol, opponent_objects = await fill_bullets(bot, querty, bullets, kol_objects, sum, play_live, opponent_live, kol, opponent_objects)
                photo_input = FSInputFile('./pictures/continue.png', 'rb')
                await bot.send_photo(querty.message.chat.id, photo_input, caption=f"Ход переходит вам", reply_markup=continuation())
                return bullets, kol_objects, sum, play_live, opponent_live, kol, damage, opponent_objects
        else:
            photo_input = FSInputFile('./pictures/miss.png', 'rb')
            msg = await bot.send_photo(querty.message.chat.id, photo_input, caption=f"*Щелчок* Ружьё не выстрелило")
            await asyncio.sleep(2)
            await msg.delete()
            msg = await querty.message.answer(f"Ваше здоровье: " + str(play_live) + "\n" + "Здоровье вашего оппонента: " + str(opponent_live))
            await asyncio.sleep(1)
            await msg.delete()
            msg = await querty.message.answer(f"Соперник продолжает ход")
            await asyncio.sleep(1)
            await msg.delete()
            if len(bullets) == 0:
                bullets, kol_objects, sum, play_live, opponent_live, kol, opponent_objects = await fill_bullets(bot, querty, bullets, kol_objects, sum, play_live, opponent_live, kol, opponent_objects)
            bullets, kol_objects, sum, play_live, opponent_live, kol, damage, opponent_objects = await intelect(bot, querty, bullets, play_live, opponent_live, kol, kol_objects, sum, damage, opponent_objects)
            return bullets, kol_objects, sum, play_live, opponent_live, kol, damage, opponent_objects
    else:
        msg = await querty.message.answer(f"Ваш оппонент направляет ружьё на вас")
        await asyncio.sleep(1)
        await msg.delete()
        if bullets.pop() == 1:
            photo_input = FSInputFile('./pictures/shot.png', 'rb')
            msg = await bot.send_photo(querty.message.chat.id, photo_input,caption=f"*Ба-бах* Оппонент выстрелил в вас")
            await asyncio.sleep(2)
            await msg.delete()
            play_live = play_live - 1
            sum = sum - 1
            msg = await querty.message.answer(f"Ваше здоровье: " + str(play_live) + "\n" + "Здоровье вашего оппонента: " + str(opponent_live))
            await asyncio.sleep(1)
            await msg.delete()
            print(play_live)
            if play_live <= 0:
                photo_input = FSInputFile('./pictures/lose.png', 'rb')
                await bot.send_photo(querty.message.chat.id, photo_input, caption=f"Вы проиграли!")
                return bullets, kol_objects, sum, play_live, opponent_live, kol, damage, opponent_objects
            else:
                if len(bullets) == 0:
                    bullets, kol_objects, sum, play_live, opponent_live, kol, opponent_objects = await fill_bullets(bot, querty, bullets, kol_objects, sum, play_live, opponent_live, kol, opponent_objects)
                photo_input = FSInputFile('./pictures/continue.png', 'rb')
                await bot.send_photo(querty.message.chat.id, photo_input, caption=f"Ход переходит вам", reply_markup=continuation())
                return bullets, kol_objects, sum, play_live, opponent_live, kol, damage, opponent_objects
        else:
            photo_input = FSInputFile('./pictures/miss.png', 'rb')
            msg = await bot.send_photo(querty.message.chat.id, photo_input, caption=f"*Щелчок* Ружьё не выстрелило")
            await asyncio.sleep(2)
            await msg.delete()
            msg = await querty.message.answer(f"Ваше здоровье: " + str(play_live) + "\n" + "Здоровье вашего оппонента: " + str(opponent_live))
            await asyncio.sleep(1)
            await msg.delete()
            print(play_live)
            if len(bullets) == 0:
                bullets, kol_objects, sum, play_live, opponent_live, kol, opponent_objects = await fill_bullets(bot, querty, bullets, kol_objects, sum, play_live, opponent_live, kol, opponent_objects)
            photo_input = FSInputFile('./pictures/continue.png', 'rb')
            await bot.send_photo(querty.message.chat.id, photo_input, caption=f"Ход переходит вам", reply_markup=continuation())
            return bullets, kol_objects, sum, play_live, opponent_live, kol, damage, opponent_objects

def continuation():
    builder = InlineKeyboardBuilder()
    builder.button(text="Продолжить игру", callback_data=MyCallback(foo="play"))
    return builder.as_markup()

class MyCallback(CallbackData, prefix="my"):
    foo: str