import requests
import json
import telebot
from telebot import TeleBot

TOKEN = "5997615388:AAGRBjKJ5URVpXWOL555UBIKFgW4tkqKEKI"

bot: TeleBot = telebot.TeleBot(TOKEN)

Mydict = {
    "/eur": "EUR",
    "/usd": "USD",
    "/rub": "RUB",
}


class ConvertionException(Exception):
    pass


# первые команды
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Валютные операции /conversion'
    bot.reply_to(message, text)


# ЧАСТЬ 1

#  выводим на экран список операций и все актуальные  курсы
@bot.message_handler(commands=['conversion'])
def operations(message: telebot.types.Message):
    text = 'Актуальные курсы:\n  /pln_to_usd \n  /pln_to_rub \n  /pln_to_eur \n  /usd_to_pln \n  /rub_to_pln \n  /eur_to_pln'
    r1 = requests.get(
        'http://api.nbp.pl/api/exchangerates/rates/a/eur/')  # запрос актуального среднего курса евро нац банка Польши
    texts1 = json.loads(r1.content)  # конвертируем в читаемый формат
    Rates1 = texts1.get('rates')  # убираем лишнее
    EUR1 = str(Rates1[0].get('mid'))
    r2 = requests.get(
        'http://api.nbp.pl/api/exchangerates/rates/a/usd/')  # запрос актуального среднего курса доллара нац банка Польши
    texts2 = json.loads(r2.content)  # конвертируем в читаемый формат
    Rates2 = texts2.get('rates')  # убираем лишнее
    USD1 = str(Rates2[0].get('mid'))

    r3 = requests.get(
        'http://api.nbp.pl/api/exchangerates/rates/a/rub/')  # запрос актуального среднего курса рубля нац банка Польши
    texts3 = json.loads(r3.content)  # конвертируем в читаемый формат
    Rates3 = texts3.get('rates')  # убираем лишнее
    RUB1 = str(Rates3[0].get('mid'))  # выводим только курс  в строковом формате иначе будет ошибка
    Mydict = {
        "eur": "",
        "usd": "",
        "rub": "",
    }
    Mydict["eur"] = EUR1
    Mydict["usd"] = USD1
    Mydict["rub"] = RUB1
    for key in Mydict.keys():
        text = '\n'.join((text, key, '->', Mydict[key]))
    bot.reply_to(message, text)


# ЧАСТЬ 2

# а теперь проходим конкретно по конвертациям

# конвертируем злотые в доллары
@bot.message_handler(commands=['pln_to_usd'])
def pln_to_usd(message):
    bot.send_message(message.chat.id, "Введите количесто pln,которые вы хотите конвертировать в usd")

    @bot.message_handler(content_types=['text', ])
    def plnusd(message):
        r = requests.get(
            'http://api.nbp.pl/api/exchangerates/rates/a/usd/')  # запрос актуального среднего курса доллара нац банка Польши
        texts = json.loads(r.content)  # конвертируем в читаемый формат
        Rates = texts.get('rates')  # убираем лишнее
        USD = Rates[0].get('mid')  # наш курс цифрой
        amount = int(message.text)  # конвертируем входящие данные в число
        total = round((amount / USD), 2)  # находим нужное количество
        result = f'{amount} pln это {total} usd'  # выводим результат
        if type(amount) == str:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        bot.send_message(message.chat.id, result)


# конвертируем злотые в рубли
@bot.message_handler(commands=['pln_to_rub'])
def pln_to_rub(message):
    bot.send_message(message.chat.id, "Введите количесто pln,которые вы хотите конвертировать в rub: ")

    @bot.message_handler(content_types=['text', ])
    def plnrub(message):
        r4 = requests.get(
            'http://api.nbp.pl/api/exchangerates/rates/a/rub/')  # запрос актуального среднего курса рубля нац банка Польши
        texts4 = json.loads(r4.content)  # конвертируем в читаемый формат
        Rates4 = texts4.get('rates')  # убираем лишнее
        RUB4 = Rates4[0].get('mid')
        amount4 = int(message.text)
        total4 = round((amount4 / RUB4), 2)
        result4 = f'{amount4} pln это {total4} rub'
        bot.send_message(message.chat.id, result4)


bot.polling(none_stop=True)