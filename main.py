
import requests
import json
import telebot
from telebot import types
from translate import Translator
from telebot import types


russian_flag = "🇷🇺"
british_flag = "🇬🇧"
key = ""
base_url = "http://api.openweathermap.org/data/2.5/weather?"
token = ""
bot = telebot.TeleBot(token)
aboba = []


@bot.message_handler(commands=['start'])
def start(message):
    mess = f"Выбери язык/Choose language"
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton(russian_flag)
    item2=types.KeyboardButton(british_flag)
    markup.add(item1)
    markup.add(item2)
    bot.send_message(message.chat.id, mess, parse_mode="html", reply_markup=markup)



@bot.message_handler(content_types=['text'])
def main(message):
    if message.text == russian_flag:
        aboba.clear()
        a = telebot.types.ReplyKeyboardRemove()
        mess = f"Привет <b>{message.from_user.first_name}</b> , напиши свой город!"
        aboba.append("ru")
        bot.send_message(message.chat.id, mess, parse_mode="html",reply_markup=a)
    elif message.text == british_flag:
        aboba.clear()
        a = telebot.types.ReplyKeyboardRemove()
        mess = f"Hello <b>{message.from_user.first_name}</b> , write your city!"
        aboba.append("en")
        bot.send_message(message.chat.id, mess, parse_mode="html",reply_markup=a)
    elif aboba[0] == "ru":
        complete_url = base_url + "appid=" + key + "&q=" + message.text
        translator = Translator(from_lang="en",to_lang="ru")
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            z = x["weather"]
            temp = int(y["temp"])
            main = z[0]["description"]
            final_temp = str(temp - 273) + " C"
            end_text = translator.translate(main)
            bot.send_message(message.chat.id, final_temp)
            bot.send_message(message.chat.id, end_text)
        else:
            error = "Город не найден!"
            bot.send_message(message.chat.id, error)
    elif aboba[0] == "en":
        complete_url = base_url + "appid=" + key + "&q=" + message.text
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            z = x["weather"]
            temp = int(y["temp"])
            main = z[0]["description"]
            final_temp = str(temp - 273) + " C"
            bot.send_message(message.chat.id, final_temp)
            bot.send_message(message.chat.id, main)
        else:
            error = "City not found!"
            bot.send_message(message.chat.id, error)


bot.polling(none_stop=True)
