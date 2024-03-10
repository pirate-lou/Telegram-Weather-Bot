import telebot
import requests

bot = telebot.TeleBot('6430800201:AAE03JWskdUiWo5cqSiBiNfssP5Lsrljqlc')
start_txt = 'Привет! Это бот прогноза погоды.\n\nОтправь мне название города.'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, start_txt, parse_mode='Markdown')

@bot.message_handler(content_types=['text'])
def weather(message):
    city = message.text
    url = ('https://api.openweathermap.org/data/2.5/weather?q='+city+
           '&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347')
    weather_data = requests.get(url).json()
    print(weather_data)

    temperature = weather_data['main']['temp']
    temperature_feels = weather_data['main']['feels_like']
    wind = weather_data['wind']['speed']
    pressure = round(weather_data['main']['pressure'])
    humidity = weather_data['main']['humidity']
    # gust = weather_data['wind']['gust']

    code_to_smile = {
            "Clear": "Ясно \U00002600",
            "Clouds": "Облачно \U00002601",
            "Rain": "Дождь \U00002614",
            "Drizzle": "Дождь \U00002614",
            "Thunderstorm": "Гроза \U000026A1",
            "Snow": "Снег \U0001F328",
            "Mist": "Туман \U0001F32B"
            }
    weather_description = weather_data["weather"][0]["main"]
    if weather_description in code_to_smile:
        wd = code_to_smile[weather_description]
    else:
        wd = "Я не могу определить какая погода за окном, поднимись и сам посмотри"

    city = 'Погода в городе: ' + city
    temperature = 'Температура: ' + str(temperature) + '°C' + ' - ' + wd + '\nОщущается как: ' + str(temperature_feels) + '°C'
    wind = 'Ветер: ' + str(wind) + ' м/с' 
    # gust = 'Порывы ветра: ' + str(gust) +  ' м/с' 
    humidity = 'Влажность: ' + str(humidity) + '%'
    pressure = 'Давление: ' + str(pressure) + ' мм.рт.ст.'

    bot.send_message(message.chat.id, 
                    city + '\n' + temperature + '\n' + humidity +
                    '\n'+ wind + '\n' + pressure)

bot.polling(none_stop = True, interval  = 0)