# For use JS syntax
import json
# Lib for using TG bots
import telebot
# Import types for using buttons in bot
from   telebot import types

# --------------------------- #
# Finction for get data from files
def readDataFromFile(key):
    file_name = ""
    if key.strip() == "token":
        file_name = "./data/token.json"
    else:
        file_name = "./data/data.json"

    try:
        with open(file_name, "r", encoding = "utf-8") as file_data:
            data = json.load(file_data)
    except FileExistsError:
        print(f"File error ! File {file_name} does not exist.")
        exit(1)
    
    if data.get(key):
        return data.get(key)
    
    return None

# --------------------------- #
# Create bot and attach a token
bot_token = readDataFromFile("token")
if not bot_token:
    print(f"Token error ! {bot_token} is incorrect.")
    exit(1)

bot = telebot.TeleBot(bot_token)

# --------------------------- #
# Logic at start command
@bot.message_handler(commands=['start'])
def start(message):
    markup        = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btnChooseCity = types.KeyboardButton     (text=readDataFromFile("buttonWeather"))
    
    markup.add(btnChooseCity)
    bot.send_message(message.from_user.id, readDataFromFile("startBotText")             , reply_markup = markup)
    bot.send_message(message.from_user.id, readDataFromFile("buttonWeatherDescription1"), reply_markup = markup)

# --------------------------- #
# Open menu at command
@bot.message_handler(func = lambda f: f.text == readDataFromFile("buttonWeather"))
def weatherMenu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=2)

    button_city1 = types.KeyboardButton(readDataFromFile("button_choose_city1"))
    button_city2 = types.KeyboardButton(readDataFromFile("button_choose_city2"))
    button_other = types.KeyboardButton(readDataFromFile("button_choose_other"))
    button_exit  = types.KeyboardButton(readDataFromFile("button_choose_exit"))

    markup.add(button_city1, button_city2)
    markup.add(button_other, button_exit)

    bot.send_message(message.from_user.id, readDataFromFile("text_choose_city"), reply_markup=markup)

# --------------------------- #
# Show weather in city1 at click button_choose_city1
@bot.message_handler(func = lambda m: m.text in readDataFromFile("button_choose_city1"))
def showAlmatyWeather(message):
    bot.send_message(message.from_user.id, "Погода в Алматы: -1°C")

# --------------------------- #
# Show weather in city2 at click button_choose_city1
@bot.message_handler(func = lambda m: m.text in readDataFromFile("button_choose_city2"))
def showAstanaWeather(message):
    bot.send_message(message.from_user.id, "Погода в Астане: -10°C")

# --------------------------- #
# Can't stop bot work
bot.polling(none_stop = True, interval = 0) 