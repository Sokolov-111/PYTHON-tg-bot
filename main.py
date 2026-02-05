# Lib for using TG bots
import telebot
# Import types for using buttons in bot
from telebot import types
# Create bot and attach a token
bot = telebot.TeleBot('')

@bot.message_handler(commands=['start'])
def start(message):
    markup  = types.InlineKeyboardMarkup(resize_keyboard = True)
    btnLink = types.InlineKeyboardButton(text="Documentation for pytelegrambotapi lib", url="https://pypi.org/project/pyTelegramBotAPI/")
    
    markup.add(btnLink)
    bot.send_message(message.from_user.id, "At this link you can ind telebot lib documentation.🚀", reply_markup = markup)

bot.polling(none_stop = True, interval = 0) 