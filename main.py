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

@bot.message_handler(commands=['start'])
def start(message):
    markup  = types.InlineKeyboardMarkup(resize_keyboard = True)
    btnLink = types.InlineKeyboardButton(text="Documentation for pytelegrambotapi lib", url="https://pypi.org/project/pyTelegramBotAPI/")
    
    markup.add(btnLink)
    bot.send_message(message.from_user.id, "At this link you can ind telebot lib documentation.🚀", reply_markup = markup)

# --------------------------- #
# Can't stop bot work
bot.polling(none_stop = True, interval = 0) 