import telebot
import yfinance as yf
from telebot import types

bot = telebot.TeleBot('put here your API key')


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Hi, <b>{message.from_user.first_name} <u>{message.from_user.last_name}</u></b>'
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(commands=['help'])
def help_(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
    btn1 = types.KeyboardButton('Price FB')
    btn2 = types.KeyboardButton('Price MSFT')
    btn3 = types.KeyboardButton('Price TSLA')
    btn4 = types.KeyboardButton('Price AAPL')
    btn5 = types.KeyboardButton('Price AMZN')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id, 'Choose a company.', reply_markup=markup)


def stock_request(message):
    request = message.text.split()
    if len(request) < 2 or request[0].lower() not in "price":
        return False
    else:
        return True


@bot.message_handler(func=stock_request)
def send_price(message):
    request = message.text.split()[1]
    data = yf.download(tickers=request, period='5m', interval='1m')
    if data.size > 0:
        data = data.reset_index()
        data["format_date"] = data['Datetime'].dt.strftime('%m/%d %I:%M %p')
        data.set_index('format_date', inplace=True)
        print(data.to_string())
        bot.send_message(message.chat.id, data['Close'].to_string(header=False))
    else:
        bot.send_message(message.chat.id, "No data!?")


bot.polling(none_stop=True)
