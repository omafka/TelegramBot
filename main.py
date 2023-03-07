import telebot
from telebot import types
from textblob import TextBlob
from settings import API_TOKEN

# создаем экземпляр телеграм бота
bot = telebot.TeleBot(API_TOKEN)


# создаем обработчик команд
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Say hello")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Hello! ", reply_markup=markup)


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message,
                 "You can determine the mood of the message through me. Just send me your message, and I will send it for analysis.")


def polarity_textblob(text):
    x = TextBlob(text).sentiment.polarity
    if x < 0:
        return "Sounds negative."
    elif x == 0:
        return "Sounds neutral."
    else:
        return "Sounds positive."


# создаем обработчик сообщений
@bot.message_handler(func=lambda message: True)
def echo(message):
    if message.text == '👋 Say hello':
        bot.send_message(message.from_user.id, 'What message do you want to check❓')
    else:
        try:
            response = polarity_textblob(message.text)
            bot.reply_to(message, response)
        except:
            bot.reply_to(message, "An error occurred while processing your request.")


# запускаем телеграм бота
bot.polling()