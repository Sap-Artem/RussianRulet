import asyncio

from aiogram.types import CallbackQuery, FSInputFile

from choice import main_choice
from fill import fill_bullets
from gameLogic import intelect


async def killT(bot, querty: CallbackQuery, bullets, kol_objects, sum, play_live, opponent_live, kol, damage, skotch, objects, kol_opponent_objects, opponent_objects):
    photo_input = FSInputFile('./pictures/shot.png', 'rb')
    msg = await bot.send_photo(querty.message.chat.id, photo_input, caption=f"*Ба-бах* Вы выстрелили в оппонента")
    await asyncio.sleep(2)
    await msg.delete()
    #print("?damage=" + str(damage))
    opponent_live = opponent_live - damage
    damage = 1
    sum = sum - 1
    msg = await querty.message.answer(f"Ваше здоровье: " + str(play_live) + "\n" + "Здоровье вашего оппонента: " + str(opponent_live))
    await asyncio.sleep(1)
    await msg.delete()
    print(skotch)
    if opponent_live <= 0:
        photo_input = FSInputFile('./pictures/lucky.png', 'rb')
        await bot.send_photo(querty.message.chat.id, photo_input, caption=f"Вы победили!")
        return bullets, kol_objects, sum, play_live, opponent_live, kol, damage, skotch, objects, kol_opponent_objects, opponent_objects
    else:
        if not skotch:
            msg = await querty.message.answer(f"Ход переходит противнику")
            await asyncio.sleep(1)
            await msg.delete()
            if len(bullets) == 0:
                bullets, kol_objects, sum, play_live, opponent_live, kol, kol_opponent_objects = await fill_bullets(bot, querty, bullets, kol_objects, sum,play_live, opponent_live, kol, kol_opponent_objects)
            bullets, kol_objects, sum, play_live, opponent_live, kol, damage, kol_opponent_objects, opponent_objects = await intelect(bot, querty, bullets, play_live, opponent_live, kol, kol_objects, sum, damage, kol_opponent_objects, opponent_objects)
            return bullets, kol_objects, sum, play_live, opponent_live, kol, damage, skotch, objects, kol_opponent_objects, opponent_objects
        else:
            skotch = False
            print("T-> " + str(skotch))
            if len(bullets) == 0:
                bullets, kol_objects, sum, play_live, opponent_live, kol, kol_opponent_objects = await fill_bullets(bot, querty, bullets, kol_objects, sum,play_live, opponent_live, kol, kol_opponent_objects)
            str_object = ""
            if len(objects) == 0:
                str_object = "Отсутствуют"
            else:
                for i in range(0, len(objects) - 1):
                    str_object = str_object + objects[i] + ", "
                str_object = str_object + objects[len(objects) - 1]
            photo_main = FSInputFile('./pictures/main menu.png', 'rb')
            await bot.send_photo(querty.message.chat.id, photo_main, caption=f"Сейчас твой ход! Оцените свои возможности, чтобы придумать эффективную стратегию" + "\n" + "Ваше здоровье: " + str(play_live) + "\n" + "Здоровье противника: " + str(opponent_live) + "\n" + "Ваши предметы: " + str_object + "\n" + "Вы можете вытащить ещё " + str(kol_objects) + " предметов", reply_markup=main_choice(kol, kol_objects))
            return bullets, kol_objects, sum, play_live, opponent_live, kol, damage, skotch, objects, kol_opponent_objects, opponent_objects
