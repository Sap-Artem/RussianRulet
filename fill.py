import asyncio
import random

from aiogram.types import CallbackQuery, FSInputFile


async def fill_bullets(bot, querty: CallbackQuery, bullets1, kol_objects1, sum1, play_live1, opponent_live1, kol1):
    kol_objects1 = kol_objects1 + 2
    size = random.randint(4, 8)
    sum1 = 0
    for i in range(0, size):
        l = random.randint(0, 1)
        bullets1.append(l)
        sum1 = sum1 + l
    if (sum1 == 0) | (sum1 == size):
        k = random.randint(0, size)
        print(k)
        if sum1 == 0:
            bullets1[k] = 1
            sum1 = sum1 + 1
        else:
            bullets1[k] = 0
            sum1 = sum1 - 1
    photo_input = FSInputFile('./pictures/loading.png', 'rb')
    msg = await bot.send_photo(querty.message.chat.id, photo_input, caption=f'В барабан заряжается ' + str(size - sum1) + ' холостых и ' + str(sum1) + ' заряженных патронов')
    await asyncio.sleep(2)
    await msg.delete()
    print(kol_objects1, sum1, play_live1, opponent_live1, kol1)
    return bullets1, kol_objects1, sum1, play_live1, opponent_live1, kol1