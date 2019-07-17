import telebot
import time
import requests

bot_token = 'your_bot_token'

bot = telebot.TeleBot(token = bot_token)

def find_at(msg):
    for text in msg:
        if '@' in text:
            return text

def vin_check(msg):
    response = requests.get("https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/{}?format=json".format(msg),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    json = response.json()
    json = json['Results']
    final = json[0]
    final_string = 'VIN number: ' + msg + ',\nMake: ' + final["Make"] + ',\nModel: ' + final["Model"] + ',\nModelYear: ' + final["ModelYear"] + ',\nPlantCountry: ' + final["PlantCountry"]
    return(final_string)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Welcome!')

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, 'To use this bot, send it a username')

@bot.message_handler(func=lambda msg: msg.text is not None and '@' in msg.text)
def at_answer(message):
    texts = message.text.split()
    at_text = find_at(texts)
    cleared_text = at_text[1:]
    bot.reply_to(message, vin_check(cleared_text))

while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)