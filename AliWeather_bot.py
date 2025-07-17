import telebot
import requests
import os
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')


# Создаем экземпляр бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Функция для получения данных о погоде
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        city_name = data['name']
        temp = data['main']['temp']
        weather_description = data['weather'][0]['description']
        return f"Погода в {city_name}:\nТемпература: {temp}°C\nОписание: {weather_description}"
    else:
        return "Город не найден."

# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне название города, и я скажу тебе погоду.")

# Обработка сообщений с названием города
@bot.message_handler(func=lambda message: True)
def send_weather(message):
    city = message.text
    weather_info = get_weather(city)
    bot.reply_to(message, weather_info)

# Запуск бота
bot.polling()