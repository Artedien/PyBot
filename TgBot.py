from datetime import datetime
from operator import truediv
from urllib import request
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings
import datetime
import ephem

logging.basicConfig(filename='bot.log',level=logging.INFO)
datetime.datetime.now()
PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {'username': settings.USERNAME, 'password': settings.PASSWORD}}

def greet_user(update, context):
    print('Вызван /start')
    print(update)
    update.message.reply_text('Hello')

def talk_to_me(update,context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)

def find_planet (planet_name):
    print('Запрос на позицию планеты')
    try:
         planet_name = planet_name.split(' ')
         return planet_name[1]
    except IndexError:
         return planet_name[0]

def planet_position(update, contex):  
    planet = find_planet(update.message.text) 
    planet_info = getattr(ephem, planet)()
    planet_info.compute(datetime.datetime.now())
    planet_place = ephem.constellation(planet_info)   
    update.message.reply_text(f'{planet} position - {planet_place}')
    return(planet_place)

def text_counter(update, context):
    text = update.message.text.split()
    print(text)
    print(len(text))
    if len(text) == 1:
        update.message.reply_text(f'Пустая строка')  
    else:
        update.message.reply_text(f'Длина строки: {len(text)-1}')  
def main():
    mybot = Updater(settings.API_KEY,use_context = True, request_kwargs=PROXY)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('wordcount',text_counter ))
    dp.add_handler(CommandHandler('planet', planet_position))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))


    logging.info('бот стартовал')
    mybot.start_polling()
    mybot.idle()

if __name__== '__main__':
    main()