import sys
import os
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
from datetime import datetime
import matplotlib.pyplot as plt


##Transforms the data from CSSEGISandData/COVID-19 into a json file.
##Fuente: https://github.com/pomber/covid19
##Using info published by https://systems.jhu.edu/research/public-health/ncov/


#### programando usando json nativo de python
url = 'https://pomber.github.io/covid19/timeseries.json'
req = urllib.request.Request(url)
r = urllib.request.urlopen(req).read()
cont = json.loads(r.decode('utf-8'))

#### programando sobre json usando pandas
import pandas as pd
df= pd.read_json (url, orient='records')
paises2=[]
for col in df.columns: 
    paises2.append(col)


## Token
T = sys.argv[1]  # get token from command-line
def handle(msg):
    content_type, chat_type, chat_id=telepot.glance(msg)
    logtxt= str(msg['chat']['first_name']) + ";" + str(msg['text'])+";"+str(datetime.now())
    print(logtxt)
    # Append-adds at last 
    file1 = open("C:/JAN/telegram/logtxt.txt","a")#append mode 
    file1.write(logtxt+"\n") 
    file1.close()     
    if content_type=='text':
        texto = msg['text']
        if texto in paises2:
            lista=[]
            c=[]
            d=[]
            r=[]
            dt=[]
            diac=[]
            diar=[]
            diad=[]
            for item in cont[texto]:
                lista.append(item['confirmed'])
                c.append(item['confirmed'])
                d.append(item['deaths'])
                r.append(item['recovered'])
                dt.append(item['date'])
            a = np.array(lista)
            c15 = c[len(dt)-15:len(dt)-1]
            r15 = r[len(dt)-15:len(dt)-1]
            d15 = d[len(dt)-15:len(dt)-1]

            ayerc = c[len(dt)-16:len(dt)-2]
            ayerr = r[len(dt)-16:len(dt)-2]
            ayerd = d[len(dt)-16:len(dt)-2]
            
            diac= list( map(lambda x,y : x-y, c15,ayerc) )
            diar= list( map(lambda x,y : x-y, r15,ayerr) )
            diad= list( map(lambda x,y : x-y, d15,ayerd) )

            var = int(a[len(a)-2]*100/(a[len(a)-8]+1))-100
            calculo = str(a[len(a)-1]) + ' total de casos confirmados \nCon una variación de ' + str(var) + '% respecto a la semana pasada: (' + str(a[len(a)-8]) + ').\nCasos últimos 7 días anteriores:\n'
            for i in range(2,9):
                calculo += str(a[len(a)-i]) + ', '
            calculo += '\nÙltima actualización: ' + str(item['date']) + '.'
            bot.sendMessage(chat_id, 'Ultima cifra de contagiados para ' + texto +':\n' + calculo)

            # multiple line plot
            plt.clf()
            fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(8, 3))
            axes[0].plot( range(1,len(dt)+1), c, marker='.', markerfacecolor='black', markersize=6, color='skyblue', linewidth=4)
            axes[0].plot( range(1,len(dt)+1), d, marker='.', markerfacecolor='black', markersize=6, color='red', linewidth=4)
            axes[0].plot( range(1,len(dt)+1), r, marker='.', markerfacecolor='black', markersize=6, color='green', linewidth=4)
#            axes[0].xticks(dt, dt, rotation='vertical')
            axes[0].legend(["contagiados","fallecidos","recuperados"])
            axes[0].set_title(texto)

            axes[1].set_title("Ult 15 días")
            axes[1].plot(range(1,15), c[len(dt)-15:len(dt)-1], marker='.', markerfacecolor='black', markersize=6, color='skyblue', linewidth=4)
            axes[1].plot(range(1,15), d[len(dt)-15:len(dt)-1], marker='.', markerfacecolor='black', markersize=6, color='red', linewidth=4)
            axes[1].plot(range(1,15), r[len(dt)-15:len(dt)-1], marker='.', markerfacecolor='black', markersize=6, color='green', linewidth=4)
#            axes[1].xticks(dt[len(dt)-15:len(dt)-1], dt[len(dt)-15:len(dt)-1], rotation='vertical')

            axes[2].set_title("Diario")
            axes[2].plot(range(1,15), diac, marker='.', markerfacecolor='black', markersize=6, color='skyblue', linewidth=4)
            axes[2].plot(range(1,15), diad, marker='.', markerfacecolor='black', markersize=6, color='red', linewidth=4)
            axes[2].plot(range(1,15), diar, marker='.', markerfacecolor='black', markersize=6, color='green', linewidth=4)
            axes[2].xlabel= "(" + str(item['date'])+" ) generado por covid19joseupcbot"
#            axes[1].xticks(dt[len(dt)-15:len(dt)-1], dt[len(dt)-15:len(dt)-1], rotation='vertical')
            fig.tight_layout()
            img_url = "C:/JAN/telegram/photos/" + str(chat_id) + ".png"
            print(img_url)
            plt.savefig(img_url)
            bot.sendPhoto(chat_id,open(img_url, 'rb'))
            os.remove(img_url)

        elif texto == "Sobre los datos":
            bot.sendMessage(chat_id, 'Los datos han sido extraidos desde ' + url + '.\nPara más información, visita https://github.com/pomber/covid19')
        elif texto == "Sobre mi":
            bot.sendMessage(chat_id, 'Si deseas contactarme, escribeme a @lyseon.\nPuedes descargar el código fuente desde https://github.com/joseantonionunez/conavidtelegrambot.git')
        elif texto[0] == "?":
            start_letter = texto[1].upper()
            with_letter = [x for x in paises2 if x.startswith(start_letter)] 
            keyboard=[] 
            for i in range(len(with_letter)):
                keyboard.append(with_letter[5*i:5*i+5])
            keyboard.append(["Otros paises", "/start"])

            bot.sendMessage(chat_id, start_letter,
                reply_markup=ReplyKeyboardMarkup(
                keyboard=keyboard ))
            
        elif texto == "Otros paises":
            keyboard = []
            row1 = ["?A","?B","?C","?D","?E","?F"]
            keyboard.append(row1)
            row2 = ["?G","?H","?I","?J","?K","?L"]
            keyboard.append(row2)
            row3 = ["?M","?N","?O","?P","?Q","?R"]
            keyboard.append(row3)
            row4 = ["?S","?T","?U","?V","?W","?X"]
            keyboard.append(row4)
            row5 = ["?Y","?Z","/start"]
            keyboard.append(row5)
            bot.sendMessage(chat_id, "Presiona en la letra deseada del país a consultar: ",
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=keyboard ))
        else:
            calculo = "Hola, " + str(msg['chat']['first_name']) + ', Selecciona el país que deseas saber las últimas cifras del coronavirus'
            bot.sendMessage(chat_id, calculo,
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=[
                                    [KeyboardButton(text="China"), KeyboardButton(text="Spain"), KeyboardButton(text="Italy")]
                                    ,[KeyboardButton(text="United Kingdom"), KeyboardButton(text="Germany"), KeyboardButton(text="Portugal")]
                                    ,[KeyboardButton(text="France"), KeyboardButton(text="Chile"), KeyboardButton(text="Argentina")]
                                    ,[KeyboardButton(text="Sobre los datos"), KeyboardButton(text="Sobre mi"), KeyboardButton(text="Otros paises")]
                                ]
                            ))


bot=telepot.Bot(T)
MessageLoop(bot,handle).run_as_thread()
print('escuchando...')

while 1:
    time.sleep(10)
