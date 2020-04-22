import numpy as np
import requests as rq
import json
import time
from datetime import datetime
import pandas as pd
from unidecode import unidecode
from urllib.parse import unquote
import os

SueldosDF = pd.DataFrame(index=np.arange(0, 400), columns=["Nombre", "Equipo", "Sueldo", "Temporada"])

seasons = np.arange(2015,2021,1)
k=0

for season in seasons:
    url = "http://www.espn.com/nba/salaries/_/year/" + str(season)
    req = rq.get(url)

    pag=0

    while pag < 20:
        #sacar datos
        nJugadores = len(req.text.split("player/_/id"))
        i=1
        while i < nJugadores:
            nombre = req.text.split("player/_/id")[i].split(">")[1].split('<')[0]
            equipo = req.text.split('player/_/id')[i].split("</td><td>")[1].split('>')[1].split('<')[0]
            sueldo = req.text.split("player/_/id")[i].split(">$")[1].split('<')[0].replace(',', '')
            if equipo != '':
                SueldosDF.loc[k]= [nombre, equipo, int(sueldo), season]
                #print(nombre, season)
                k=k+1
            else:
                print(nombre, "No pasa", req.url)

            i = i +1 

        if pag==0:
            url_siguiente = "http:" + req.text.split("nofollow\" href=\"")[1].split("\"")[0]
            req = rq.get(url_siguiente)
            pag = pag + 1

        else:
            try:
                url_siguiente = "http:" + req.text.split("nofollow\" href=\"")[2].split("\"")[0]
                req = rq.get(url_siguiente)
                pag = pag + 1
            except:
                print("fin paginacion")
                break
#cambiamos LA Clippers por Los Angeles Clippers para facilitar el join mas adelante
SueldosDF.loc[SueldosDF['Equipo'] == 'LA Clippers', 'Equipo'] = 'Los Angeles Clippers'
SueldosDF_aux = SueldosDF.drop(['Nombre'], axis=1)
sueldos_temporada = SueldosDF_aux.groupby(['Equipo', 'Temporada'], as_index = False ).sum()

directorio = "Sueldos"

try:
    os.stat(directorio)
except:
    os.mkdir(directorio)
    
os.chdir(directorio)

sueldos_temporada.to_csv('sueldos_equipo.csv', header=True, index=False)
SueldosDF.to_csv('sueldos_jugadores.csv', header=True, index=False)

os.chdir("..")


