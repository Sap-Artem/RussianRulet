import asyncio
import random

def random_objects(objects):
    baf = random.randint(0, 11)
    if baf == 0:
        objects.append("бинт")
    elif baf == 1:
        objects.append("аптечка")
    elif baf == 2:
        objects.append("обрез")
    elif baf == 3:
        objects.append("клещи")
    elif baf == 4:
        objects.append("лупа")
    elif baf == 5:
        objects.append("скотч")
    elif baf == 6:
        objects.append("дуплет")
    elif baf == 7:
        objects.append("пулеворот")
    elif baf == 8:
        objects.append("шаверма")
    elif baf == 9:
        objects.append("просроченное лекарство")
    elif baf == 10:
        objects.append("лезвия")
    else:
        objects.append("карточка")
    return baf, objects

async def hill_objects(querty, opponent_objects, i, opponent_live):
    if opponent_objects[i] == "бинт":
        opponent_objects.pop(i)
        opponent_live = opponent_live + 1
        msg = await querty.message.answer(f"Ваш оппонент использовал бинт. Его здоровье восстановлено на 1 HP")
        await asyncio.sleep(2)
        await msg.delete()
        i = i - 1
    elif opponent_objects[i] == "аптечка":
        opponent_objects.pop(i)
        opponent_live = opponent_live + 2
        msg = await querty.message.answer(f"Ваш оппонент использовал аптечку. Его здоровье восстановлено на 2 HP")
        await asyncio.sleep(2)
        await msg.delete()
        i = i - 1
    elif opponent_objects[i] == "шаверма":
        opponent_objects.pop(i)
        r = random.randint(0, 1)
        if r == 1:
            opponent_live = opponent_live + 2
            msg = await querty.message.answer(f"Ваш оппонент съел шаверму. К счастью для него, шаверма оказалась вкусной и сытной. Его здоровье восстановлено на 2 HP")
            await asyncio.sleep(2)
            await msg.delete()
        else:
            opponent_live = opponent_live - 1
            msg = await querty.message.answer(f"Ваш оппонент съел шаверму. К сожалению для него, шаверма оказалась протухшей. Его здоровье уменьено на 1 HP")
            await asyncio.sleep(2)
            await msg.delete()
        i = i - 1
    elif opponent_objects[i] == "просроченное лекарство":
        opponent_objects.pop(i)
        r = random.randint(0, 1)
        if r == 1:
            opponent_live = opponent_live + 1
            msg = await querty.message.answer(f"Ваш оппонент съел просроченное лекарство. К счастью для него, лекарство не смогло ему навредить. Его здоровье восстановлено на 1 HP")
            await asyncio.sleep(2)
            await msg.delete()
        else:
            opponent_live = opponent_live - 2
            msg = await querty.message.answer(f"Ваш оппонент съел просроченное лекарство. К сожалению для него, лекарство дало негативный побочный эффект. Его здоровье уменьшено на 2 HP")
            await asyncio.sleep(2)
            await msg.delete()
        i = i - 1
    return opponent_objects, opponent_live, i

async def damage_objects(querty, opponent_objects, i, opponent_live, opponent_damage, damage_lite):
    if opponent_objects[i] == "обрез":
        opponent_objects.pop(i)
        opponent_damage = opponent_damage + 1
        msg = await querty.message.answer(f"Ваш оппонент использовал обрез. Урон его следующего выстрела увеличен на 1 единицу")
        await asyncio.sleep(2)
        await msg.delete()
    elif (opponent_objects[i] == "лезвия") & (opponent_live > 1):
        opponent_objects.pop(i)
        opponent_damage = opponent_damage + 2
        opponent_live = opponent_live - 1
        msg = await querty.message.answer(f"Ваш оппонент использовал лезвия. Он потерял 1 HP, но урон его следующего выстрела увеличен на 2 единицы")
        await asyncio.sleep(2)
        await msg.delete()
    i = i - 1
    damage_lite = 1
    return opponent_objects, opponent_live, opponent_damage, i, damage_lite

async def look_objects(querty, bullets, opponent_objects, i, solution_lite):
    if opponent_objects[i] == "лупа":
        opponent_objects.pop(i)
        msg = await querty.message.answer(f"Ваш оппонент использовал лупу. Он ехидно улыбается)")
        await asyncio.sleep(2)
        await msg.delete()
        if bullets[len(bullets) - 1] == 0:
            solution_lite = 0
        else:
            solution_lite = 1
    i = i - 1
    return bullets, opponent_objects, i, solution_lite

async def negative_objects(querty, bullets, opponent_objects, i, solution_lite):
    if opponent_objects[i] == "пулеворот":
        opponent_objects.pop(i)
        msg = await querty.message.answer(f"Ваш оппонент использовал пулеворот. Он изменил полярность следующей пули")
        await asyncio.sleep(2)
        await msg.delete()
        if bullets[len(bullets) - 1] == 0:
            bullets[len(bullets) - 1] = 1
            solution_lite = 1
        else:
            bullets[len(bullets) - 1] = 0
            solution_lite = 0
    i = i - 1
    return bullets, opponent_objects, i, solution_lite
async def one_objects(querty, bullets, opponent_objects, play_live, i):
    if opponent_objects[i] == "скотч":
        opponent_objects.pop(i)
        msg = await querty.message.answer(f"Ваш оппонент использовал скотч. Теперь он может сделать 2 выстрела подряд")
        await asyncio.sleep(2)
        await msg.delete()
        msg = await querty.message.answer(f"Ваш оппонент направляет ружьё на вас")
        await asyncio.sleep(2)
        await msg.delete()
        msg = await querty.message.answer(f"*Щелчок* Ружьё не выстрелило")
        await asyncio.sleep(2)
        await msg.delete()
        msg = await querty.message.answer(f"Ваш оппонент направляет ружьё на вас")
        await asyncio.sleep(2)
        await msg.delete()
        msg = await querty.message.answer(f"*Ба-бах* Оппонент выстрелил в вас")
        await asyncio.sleep(2)
        await msg.delete()
        msg = await querty.message.answer(f"Вы потеряли 1 HP")
        await asyncio.sleep(1)
        await msg.delete()
        play_live = play_live - 1
        bullets = []
        i = i - 1
    elif opponent_objects[i] == "дуплет":
        opponent_objects.pop(i)
        msg = await querty.message.answer(f"Ваш оппонент использовал дуплет. Теперь он может выстрелить двумя пулями одновременно")
        await asyncio.sleep(2)
        await msg.delete()
        msg = await querty.message.answer(f"Ваш оппонент направляет ружьё на вас")
        await asyncio.sleep(2)
        await msg.delete()
        msg = await querty.message.answer(f"*Ба-бах* Оппонент выстрелил в вас")
        await asyncio.sleep(2)
        await msg.delete()
        msg = await querty.message.answer(f"Вы потеряли 1 HP")
        await asyncio.sleep(1)
        await msg.delete()
        play_live = play_live - 1
        bullets = []
        i = i - 1
    return bullets, opponent_objects, play_live, i, 1