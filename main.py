from aiogram import types, Dispatcher
import requests
from create_bot import dp, bot 
from  aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import weather_token
import datetime


class FSMain (StatesGroup):
    city = State()
    chose = State()

#@dp.message_handler(commands=["start"])
async def start_bot (message :types.Message):
    try:
        await FSMain.city.set()
        await message.answer ("Привет,\nНапиши свой город. ")
    except Exception as ex:
        await message.reply ('Есть проблемы!')
        print (ex)

#@dp.message_handler(state=FSMain.city )
async def chs (message: types.Message, state: FSMContext):
    async with state.proxy() as dta:
        dta['city'] = message.text
    await message.reply('Отлично!')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True )
    markup.add("Погода сейчас","Прогноз")
    await bot.send_message (chat_id=message.chat.id,text='Что показать? ', reply_markup=markup)
    await FSMain.next()


#@dp.message_handler(state= FSMain.chose)
async def script_start (message: types.Message, state: FSMContext):
    async with state.proxy() as dta:
        dta['chose']= message.text
        if message.text == "Погода сейчас":
            try:
                r= requests.get (
                    f'https://api.openweathermap.org/data/2.5/weather?q={dta["city"]}&lang=ru&appid={weather_token}&units=metric'
                )
                data = r.json()

                name  = data['name']
                temperature = data["main"]["temp"]

                min_tempreture = data["main"]['temp_min']
                humidity = data ['main']['humidity']
                pressure = round((data["main"]["pressure"])/1.333)
                wind_sp= data['wind']['speed']
                sunrise= datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
                sunset= datetime.datetime.fromtimestamp(data["sys"]["sunset"])
                desc_weath= data ['weather'][0]['description']


                await message.reply (f"Сейчас: {datetime.datetime.now().strftime('%H:%M')}\n"
                f"Город: {name}\nТемпература: {temperature} C° -- {desc_weath}\nМинимальная температура: {min_tempreture} C°\n"
                f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nСкорость ветра: {wind_sp} м/с\n"
                f"Восход: {sunrise}\nЗакат: {sunset}\n"
                )

            except Exception as ex:
                print (ex)
                await message.reply ("Weather problem")

        elif message.text == "Прогноз":
            try:
                r=requests.get(
                    f'http://api.openweathermap.org/data/2.5/forecast?q={dta["city"]}&lang=ru&cnt=9&appid={weather_token}&units=metric'
                )
                data= r.json()
                data= data["list"]

                for hour in range (9):
                    data_hours= data[hour]
                    time = data_hours["dt_txt"]
                    time= time.split(" ").pop(1)
                    temp= data_hours["main"]["temp"]
                    feels_like = data_hours['main']["feels_like"]
                    desc= data_hours['weather'][0]["description"]
                    wind_s= data_hours["wind"]["speed"]
                    await message.answer (f'-------------------Время: {time} -------------------\n'
                    f'Температура: {temp}C° **{desc}** \nОщущается как: {feels_like} C°\n'
                    f'Ветер: {wind_s} м/с ')

            except Exception as ex: 
                print(ex)
                await message.reply ("Forecast problem")

    await state.finish()




def registr_handlers(dp : Dispatcher):
    dp.register_message_handler(start_bot, commands=['start'])
    dp.register_message_handler(chs, state=FSMain.city)
    dp.register_message_handler(script_start, state=FSMain.chose)
