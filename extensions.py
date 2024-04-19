import json
import requests
import telebot

bot = telebot.TeleBot("7030598940:AAEB8o_kW_MXcsSbu7juWvNvDX-H205V-gU")
class APIException(Exception):
    def __init__(self, text):
        self.text = text

class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        url = f'https://api.exchangerate-api.com/v4/latest/{base}'
        response = requests.get(url)
        data = json.loads(response.text)
        
        if quote not in data['rates']:
            raise APIException(f'Ошибочка: {quote}')
        
        if not amount.isdigit():
            raise APIException('Небольшая ошибка. Пожалуйста вводите числа.')
        
        exchange_rate = data['rates'][quote]
        converted_amount = float(amount) * exchange_rate
        return converted_amount


@bot.message_handler(commands=['start', 'help'])
def send_instructions(message):
    instructions = "Добро пожаловать в CurrencyConverterBot, бот способен конвертировать USD, RUB, EUR! Пожалуйста, введите валюту которою вы хотите конвертировать ,потом валюту в которую будем конвертировать, и наконец сумму для конвертации. Ввод должен происходить в следующем формате: <валюта, из которой мы переводим> <валюта, в котороу мы переводим> <сумма>. Пример: RUB USD 1000"
    bot.reply_to(message, instructions)

@bot.message_handler(commands=['values'])
def send_values(message):
    values = "Доступные валюты: USD, EUR, RUB"
    bot.reply_to(message, values)

@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    try:
        text = message.text.split()
        if len(text) != 3:
            raise APIException('Вы ошиблись, попробуйте снова.')
        
        base = text[0].upper()
        quote = text[1].upper()
        amount = text[2]
        
        converted_amount = CurrencyConverter.get_price(base, quote, amount)
        response = f'{amount} {base} is equal to {converted_amount} {quote}'
        bot.reply_to(message, response)
    
    except APIException as e:
        bot.reply_to(message, f'Error: {e.text}')
    except Exception as e:
        bot.reply_to(message, f'An error occurred: {str(e)}')

bot.polling(non_stop = True)