from config import weather_token
import requests 
from pprint import pprint 
import datetime 

def get_weather (city, weather_token):

    try:
        r= requests.get (
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&appid={weather_token}&units=metric'
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


        print (f"Сейчас: {datetime.datetime.now().strftime('%H:%M')}\n"
        f"Город: {name}\nТемпература: {temperature} C° -- {desc_weath}\nМинимальная температура: {min_tempreture} C°\n"
        f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nСкорость ветра: {wind_sp} м/с\n"
        f"Восход: {sunrise}\nЗакат: {sunset}\n"
        )

    except Exception as ex:
        print (ex)
        print ('Check your input')


def forecast_weather (city, weather_token):
    try:
        r=requests.get(
            f'http://api.openweathermap.org/data/2.5/forecast?q={city}&lang=ru&cnt=9&appid={weather_token}&units=metric'
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
            print (f'-------------------Время: {time} -------------------\n'
            f'Температура: {temp}C° **{desc}** \nОщущается как: {feels_like} C°\n'
            f'Ветер: {wind_s} м/с ')

    except Exception as ex: 
        print(ex)
        print("Есть проблемы! ")


def main ():
    city = input('Enter your city: ')
    get_weather(city, weather_token)
    chs= input("Показать прогноз?\ny/n\n")
    if chs.strip() == "y":
        forecast_weather(city,weather_token)
    else:
        print("Хорошего дня! ")

main()

