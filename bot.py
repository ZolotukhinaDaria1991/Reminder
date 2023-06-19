import logging
from datetime import datetime, timedelta
import asyncio

from aiogram import Bot, Dispatcher, executor, types

TOKEN = '6089939502:AAF_27tBrrD3dyfN-xeeTWt3FHhnyL_Vxs0'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    # получаем ID чата
    chat_id = message.chat.id
    await message.answer(
        f'''
        Привет!
        Твой chat_id: {chat_id},
        Я запустил напоминалку.
        Теперь каждый день примерно в это время ты узнаешь:
        Какой спринт и сколько до его окончания.
        Если хочешь узнать статус спринта, пиши
        команду "/check" в любое время дня и ночи.
        пиши команду "/show_all" если хочешь
        вывести все расписание. ''')
    await check_schedule(chat_id)


@dp.message_handler(commands=['check'])
async def process_check_command(message: types.Message):
    # получаем ID чата
    chat_id = message.chat.id
    await check_date_time_sprint(chat_id)


@dp.message_handler(commands=['show_all'])
async def process_show_all_command(message: types.Message):
    chat_id = message.chat.id
    await show_all_date_sprint(chat_id)

# Даты начала спринтов и каникул
schedule = [
    {"number": 1, "start": "16/05/2023", "end": "28/05/2023"},
    {"number": 2, "start": "29/05/2023", "end": "04/06/2023"},
    {"number": 3, "start": "05/06/2023", "end": "18/06/2023"},
    {"number": 4, "start": "19/06/2023", "end": "02/07/2023"},
    {"number": 5, "start": "03/07/2023", "end": "09/07/2023"},
    {"number": 6, "start": "10/07/2023", "end": "23/07/2023"},
    {"number": 7, "start": "24/07/2023", "end": "13/08/2023"},
    {"number": 8, "start": "14/08/2023", "end": "27/08/2023"},
    {"number": None, "start": "28/08/2023", "end": "03/09/2023"},
    {"number": 9, "start": "04/09/2023", "end": "17/09/2023"},
    {"number": 10, "start": "18/09/2023", "end": "01/10/2023"},
    {"number": 11, "start": "02/10/2023", "end": "15/10/2023"},
    {"number": None, "start": "16/10/2023", "end": "22/10/2023"},
    {"number": 12, "start": "23/10/2023", "end": "12/11/2023"},
    {"number": 13, "start": "13/11/2023", "end": "26/11/2023"},
    {"number": 14, "start": "27/11/2023", "end": "10/12/2023"},
    {"number": 15, "start": "11/12/2023", "end": "14/01/2024"},
    {"number": None, "start": "15/01/2024", "end": "21/01/2024"},
    {"number": 16, "start": "22/01/2024", "end": "04/02/2024"},
    {"number": 17, "start": "05/02/2024", "end": "18/02/2024"},
    {"number": 18, "start": "19/02/2024", "end": "03/03/2024"},
    {"number": 19, "start": "04/03/2024", "end": "17/03/2024"},
    {"number": 20, "start": "18/03/2024", "end": "31/03/2024"},
    {"number": None, "start": "01/04/2024", "end": "07/04/2024"},
    {"number": 21, "start": "08/04/2024", "end": "21/04/2024"},
    {"number": 22, "start": "22/04/2024", "end": "19/05/2024"},
    {"number": 23, "start": "20/05/2024", "end": "02/06/2024"},
    {"number": None, "start": "03/06/2024", "end": "09/06/2024"},
    {"number": 24, "start": "10/06/2024", "end": "14/07/2024"},
    {"number": 25, "start": "15/07/2024", "end": "28/07/2024"}
]


def plural_days(n_days):
    days = ['день', 'дня', 'дней']
    if n_days % 10 == 1 and n_days % 100 != 11:
        index = 0
    elif 2 <= n_days % 10 <= 4 and (n_days % 100 < 10 or n_days % 100 >= 20):
        index = 1
    else:
        index = 2
    return f'{n_days} {days[index]}'


async def send_notification(text: str, chat_id: int):
    # Отправляем уведомление в чат
    await bot.send_message(chat_id, text)
    await asyncio.sleep(3)


async def check_schedule(chat_id):
    # Проверяем расписание каждый день
    while True:
        await check_date_time_sprint(chat_id)
        await asyncio.sleep(60*60*24)  # Ждем 1 день


async def check_date_time_sprint(chat_id):
    current_now = datetime.now().date()

    # Ищем спринт, который начинается или заканчивается в текущее время
    for sprint in schedule:
        start_date = datetime.strptime(sprint['start'], '%d/%m/%Y').date()
        end_date = datetime.strptime(sprint['end'], '%d/%m/%Y').date()

        if (sprint["number"] is None and current_now == end_date):
            await send_notification(
                '''Каникулы начинаются!!!
                Или жёсткий дедлайн смотря как
                ты ухаживал за своим Питоном!
                Если не укратил своего Питона до сих пор,
                то оформляем перевод =(
                Если все в порядке, то
                выпусти погулять своего Питона сегодня.
                P.S. Питон будет жить!!!''', chat_id)
        elif (sprint["number"] is None and
              current_now >= start_date and current_now <= end_date):
            await send_notification(
                f'''Сейчас каникулы! Но не отчаивайся
                Осталось {plural_days((end_date - current_now).days)}.
                И снова возьмешься за своего Питона. ''', chat_id)

        elif current_now == start_date:
            await send_notification(
                f'''Начался {sprint["number"]}-й спринт!
                Осталось {plural_days((end_date - current_now).days)}
                до его окончания!
                Так что не натягивай сильно долго своего Питона,
                начинай завязывать его уже сейчас! ''', chat_id)

        elif current_now == end_date:
            await send_notification(
                (f'''Спринт {sprint["number"]}
                 закончится уже сегодня!!!
                 Завязывай хвосты питонам, если еще не успел! '''), chat_id)

        elif (current_now >= start_date and current_now <= end_date):
            await send_notification(
                (f'''Сейчас идет {sprint["number"]}-й спринт!
                 Следующий начнется через
                 {plural_days((end_date - current_now).days)}
                 Уже совсем скоро!
                 Начинай завязывать его хвосты уже сегодня! '''), chat_id)


async def show_all_date_sprint(chat_id):
    current_now = datetime.now().date()

    # Ищем спринт, который начинается или заканчивается в текущее время
    for sprint in schedule:
        start_date = datetime.strptime(sprint['start'], '%d/%m/%Y').date()
        end_date = datetime.strptime(sprint['end'], '%d/%m/%Y').date()
        start_str = ''

        duration = (start_date - current_now).days
        duration_str = ''
        if duration < 0:
            duration_str = 'Уже прошел! Ура!'
        elif duration == 0:
            duration_str = (
                'Идет сейчас!')
        else:
            duration_str = (
                'С сегодняшнего дня до него осталось: '
                f'{plural_days(duration)}')

        if sprint['number'] is None:
            start_str = 'Жесткий дедлайн '
            {(start_date + timedelta(days=-1)).strftime('%d.%m.%Y')}
            ' или каникулы. '
            'Смотря кто-как гладил своего Питона по выходным! '
        else:
            start_str = f'Спринт № {sprint["number"]}. '
        await send_notification(
            (f'''{start_str}
             Дата начала {start_date.strftime('%d.%m.%Y')}
             Дата окончания {end_date.strftime('%d.%m.%Y')}
             Продлится {plural_days((end_date - start_date).days)}
            {duration_str}'''), chat_id)

if __name__ == '__main__':
    # Запускаем проверку расписания и бота в отдельных потоках
    logging.info("Starting polling...")
    executor.start_polling(dp, skip_updates=True)
