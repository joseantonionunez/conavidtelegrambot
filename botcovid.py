import sys
import telepot 
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import numpy as np
from numpy  import array
import json
import requests
import urllib.request
import time


##Transforms the data from CSSEGISandData/COVID-19 into a json file.
##Fuente: https://github.com/pomber/covid19
##Using info published by https://systems.jhu.edu/research/public-health/ncov/

url = 'https://pomber.github.io/covid19/timeseries.json'
req = urllib.request.Request(url)
r = urllib.request.urlopen(req).read()
cont = json.loads(r.decode('utf-8'))

## Token
T = sys.argv[1]  # get token from command-line
def handle(msg):
    content_type, chat_type, chat_id=telepot.glance(msg)
    print(content_type,chat_type, chat_id)

    if content_type=='text':
        texto = msg['text']
        paises = ['Spain','Chile','Italy','Germany','Portugal','United Kingdom','France', 'China', 'Argentina']
        if texto in paises:
            lista=[]
            for item in cont[texto]:
                lista.append(item['confirmed'])
            a = np.array(lista)
            var = int(a[len(a)-2]*100/(a[len(a)-8]))-100
            calculo = str(a[len(a)-1]) + ' total de casos confirmados \nCon una variación de ' + str(var) + '% respecto a la semana pasada: (' + str(a[len(a)-8]) + ').\nCasos últimos 7 días anteriores:\n'
            for i in range(2,9):
                calculo += str(a[len(a)-i]) + ', '
            calculo += '\nÙltima actualización: ' + str(item['date']) + '.'
            bot.sendMessage(chat_id, 'Ultima cifra de contagiados para ' + texto +':\n' + calculo)
        elif texto == "Sobre los datos":
            bot.sendMessage(chat_id, 'Los datos han sido extraidos desde ' + url + '.\nPara más información, visita https://github.com/pomber/covid19')
        elif texto == "Sobre mi":
            bot.sendMessage(chat_id, 'Si deseas contactarme, escribeme a @lyseon.\nPuedes descargar el código fuente desde https://github.com/joseantonionunez/conavidtelegrambot.git')
        else:
            calculo = "Hola, " + str(msg['chat']['first_name']) + ', Selecciona el país que deseas saber las últimas cifras del coronavirus'
            bot.sendMessage(chat_id, calculo,
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=[
                                    [KeyboardButton(text="China"), KeyboardButton(text="Spain"), KeyboardButton(text="Italy")]
                                    ,[KeyboardButton(text="United Kingdom"), KeyboardButton(text="Germany"), KeyboardButton(text="Portugal")]
                                    ,[KeyboardButton(text="France"), KeyboardButton(text="Chile"), KeyboardButton(text="Argentina")]
                                    ,[KeyboardButton(text="Sobre los datos"), KeyboardButton(text="Sobre mi")]
                                ]
                            ))
            

   

bot=telepot.Bot(T)
MessageLoop(bot,handle).run_as_thread()
print('escuchando...')

while 1:
    time.sleep(10)

