#!/usr/bin/env python

###########################################################

from telegram import Update, ParseMode

from telegram.ext import (
    Updater, 
    CallbackContext, 
    CommandHandler, 
    MessageHandler, 
    Filters, 
    Defaults
)

import pytz

import logging

import wikipedia

import json 
import requests

###########################################################

TELEGRAM_TOKEN = "xxxxx"

WEATHER_TOKEN = "xxxxx"
 
IMAGE_URL = "http://openweathermap.org/img/wn/"
IMAGE_POSTFIX = "@2x.png"

###########################################################

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)  # DEBUG, INFO

logger = logging.getLogger(__name__)

defaults = Defaults(parse_mode=ParseMode.HTML, tzinfo=pytz.timezone('America/Bogota'))

###########################################################

updater = Updater(token=TELEGRAM_TOKEN)
dispatcher = updater.dispatcher

###########################################################

def doStart(update: Update, context: CallbackContext):
    update.message.reply_text(text=f"Hola soy tu amigo el bot.")

def doCaps(update: Update, context: CallbackContext):
    text = ' '.join(context.args).upper()
    update.message.reply_text(text)

def fallback(update: Update, context: CallbackContext):
    update.message.reply_text(text=f"Lo siento, no entiendo lo que me dices.")

def doAdd(update: Update, context: CallbackContext):
    # print (context.match.groups())
    
    a,b = context.match.group(1, 2)
    # r = a+b
    r = float(a) + float (b)

    update.message.reply_text(text=f"El resultado es {r}")

def doWhatIs(update: Update, context: CallbackContext):
    query = context.match.group(1)

    try:
        result = wikipedia.summary(query)
    except Exception as err:
        update.message.reply_text(text=f"{err}")

    update.message.reply_text(text=result)

def doTemp(update: Update, context: CallbackContext):
    city = context.match.group(1)

    url = f"https://api.openweathermap.org/data/2.5/weather?appid={WEATHER_TOKEN}&units=metric&lang=es&q={city}"

    response = requests.get(url)
    
    # update.message.reply_text(text=response.content.decode("utf8"))

    weather = json.loads(response.content.decode("utf8"))

    data = {
        "temp":        weather["main"]["temp"],
        "feelsLike":   weather["main"]["feels_like"],
        "tempMin":     weather["main"]["temp_min"],
        "tempMax":     weather["main"]["temp_max"],
        "pressure":    weather["main"]["pressure"],
        "humidity":    weather["main"]["humidity"],
        "visibility":  weather["visibility"],
        "weather":     weather["weather"][0]["main"],
        "description": weather["weather"][0]["description"],
        "icon":        weather["weather"][0]["icon"],
    }

    result = ( f"The temperature in {city} is {data['temp']} C.\n"
               f"Feels like {data['feelsLike']} C.\n"
               f"Humidity {data['humidity']}% / visibility {float(data['visibility'])/1000} km." )

    update.message.reply_text(text=result)

def doWeather(update: Update, context: CallbackContext):
    print (context.match.groups())

    city = context.match.group(1)

    url = f"https://api.openweathermap.org/data/2.5/weather?appid={WEATHER_TOKEN}&units=metric&lang=es&q={city}"

    response = requests.get(url)
    
    weather = json.loads(response.content.decode("utf8"))

    data = {
        "temp":        weather["main"]["temp"],
        "feelsLike":   weather["main"]["feels_like"],
        "tempMin":     weather["main"]["temp_min"],
        "tempMax":     weather["main"]["temp_max"],
        "pressure":    weather["main"]["pressure"],
        "humidity":    weather["main"]["humidity"],
        "visibility":  weather["visibility"],
        "weather":     weather["weather"][0]["main"],
        "description": weather["weather"][0]["description"],
        "icon":        weather["weather"][0]["icon"],
    }

    imageUrl = IMAGE_URL + data['icon'] + IMAGE_POSTFIX

    context.bot.send_photo(chat_id=update.effective_chat.id, photo=imageUrl)
    update.message.reply_text(text=f"El clima en {city.upper()} es {data['description'].upper()}.") 

###########################################################

dispatcher.add_handler(CommandHandler('start', doStart))

dispatcher.add_handler(CommandHandler('caps', doCaps))

# fallback

# sumador
dispatcher.add_handler(MessageHandler(Filters.regex(r'^add ([-+]?\d*\.\d+|\d+) and ([-+]?\d*\.\d+|\d+)$'), doAdd))

# wikipedia
dispatcher.add_handler(MessageHandler(Filters.regex(r'^whatis (.*)$'), doWhatIs))

# openweathermap
dispatcher.add_handler(MessageHandler(Filters.regex(r'^temp (.*)$'), doTemp))

dispatcher.add_handler(MessageHandler(Filters.regex(r'^(?:weather|w) (.*)$'), doWeather))

dispatcher.add_handler(MessageHandler(Filters.all, fallback))

###########################################################

updater.start_polling()
updater.idle()

###########################################################

# $ npm install -global nodemon
# $ nodemon --exec python3 hello.py 
# $ nodemon bot.py

# if __name__ == '__main__':
#     main()
