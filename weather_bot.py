import requests
import datetime
from API_config import tg_token, ow_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

# importing tokens from API_config.py
bot = Bot(token=tg_token)
dispatcher = Dispatcher(bot)


# making bot searchable in TG
@dispatcher.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Доброго дня! Для того, щоб дізнатися погоду, напишіть назву міста:")


@dispatcher.message_handler()
async def get_weather(message: types.Message):
    # weather conditions with emojis
    weather_conditions = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Хмари \U00002601",
        "Rain": "Дощ \U00002614",
        "Drizzle": "Легкий дощ \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Сніг \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    # using "requests" to import data from Open Weather
    try:
        ow_response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={ow_token}&units=metric"
        )
        data = ow_response.json()

        # weather description
        weather_data = data["weather"][0]["main"]
        if weather_data in weather_conditions:
            weather_data_ans = weather_conditions[weather_data]

        # weather data from OW
        city = data["name"]
        weather_now = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind_speed = data["wind"]["speed"]
        sunrise_time = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_time = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        # Output response to the user through bot
        await message.reply(f"""
        На вулиці {datetime.datetime.now().strftime("%d-%m-%Y")}
        Погода у місті {city}:
        Температура: {weather_now} C°, {weather_data_ans}
        Вологість повітря: {humidity} %
        Атм.тиск: {pressure} мм рт. ст.
        Швидкість вітру: {wind_speed} м/с
        Схід сонця: {sunrise_time}
        Захід сонця: {sunset_time}
        Бажаю приємного дня! \U0001f609
            """)
    # if typo in the name of the city, throw error
    except:
        await message.reply("Перевірте правильність написання назви міста \U0001f622")


if __name__ == '__main__':
    executor.start_polling(dispatcher)
