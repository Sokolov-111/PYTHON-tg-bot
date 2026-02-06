# For use JS syntax
import json
# Lib for using TG bots
import telebot
# Import types for using buttons in bot
from   telebot import types
# Import lib for web scraping
import requests

# --------------------------- #
# Function for get data from files
def readDataFromFile(key):
    file_name = ""
    if key.strip() in ["token", "weather_api"]:
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
# Function to get weather
def get_weather(city="Almaty"):
    # API key (can get in weatherapi.com)
    API_KEY = readDataFromFile("weather_api")

    if not API_KEY:
        return "❌ API key not found. Please add weather_api to token.json"
    
    # URL for request
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": API_KEY,
        "q": city,
        "lang": "en"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data     = response.json()
        
        if "error" in data:
            error_msg = data.get("message", "Unknown error")
            return f"❌ Error: {error_msg}"
        
        # Get data
        temp        = data["current"]["temp_c"]
        feels_like  = data["current"]["feelslike_c"]
        humidity    = data["current"]["humidity"]
        wind_speed  = data["current"]["wind_kph"] / 3.6 
        description = data["current"]["condition"]["text"]
        
        # Create answer
        weather_info = (
            f"🌤  Weather in {data['location']['name']}:\n"
            f"🌡  Temperature: {temp}°C\n"
            f"🤖 Feel as: {feels_like}°C\n"
            f"💧  Damp: {humidity}%\n"
            f"💨 Wind: {wind_speed:.1f} м/с\n"
            f"📝 {description}"
        )
        
        return weather_info
        
    except Exception as e:
        return f"❌ Get weather error: {str(e)}"

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
    weather = get_weather("Almaty")
    bot.send_message(message.from_user.id, weather)

# --------------------------- #
# Show weather in city2 at click button_choose_city1
@bot.message_handler(func = lambda m: m.text in readDataFromFile("button_choose_city2"))
def showAstanaWeather(message):
    weather = get_weather("Astana")
    bot.send_message(message.from_user.id, weather)

# --------------------------- #
# Can't stop bot work
bot.polling(none_stop = True, interval = 0) 