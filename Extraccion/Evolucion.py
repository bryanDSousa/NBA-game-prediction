import numpy as np
import requests as rq
import json
import time
from datetime import datetime
import pandas as pd
from unidecode import unidecode
from urllib.parse import unquote
import os

EvolucionDF = pd.DataFrame(index=np.arange(0, 400), columns=["nombre",
                                                           "tirosTotalesAnotados",
                                                           "tirosTotalesIntentados",
                                                          "tirosTotalesPorcentaje",
                                                          "tiros3Anotados",
                                                          "tiros3Intentados",
                                                          "tiros3Porcentaje",
                                                           "tiros2Anotados",
                                                          "tiros2Intentados",
                                                          "tiros2Porcentaje",
                                                          "tirosLibresAnotados",
                                                          "tirosLibresIntentados",
                                                          "tirosLibresPorcentaje",
                                                          "rebotesOfensivos",
                                                          "rebotesDefensivos",
                                                          "rebotesTotales",
                                                          "asistencias",
                                                          "robos",
                                                          "perdidas",
                                                          "tapones",
                                                          "faltas", 
                                                          "puntos",
                                                          "temporada"])
year_list = np.arange(1990,2020,1)
sep_player = "csk=\""

k=0
j=0
for year in year_list:
    r = rq.get("https://www.basketball-reference.com/leagues/NBA_"+str(year)+"_totals.html")
    i=2
    print(j, "temporadas obtenidas de un total de", len(year_list))
    print((100*j)/len(year_list), "%")
    j=j+1
    if r.ok != True:
        print("error")
    while i < len(2*r.text.split("player\" csk=\"")):
        
        name= r.text.split(sep_player)[i].split("\"")[0]
        tirosAnotados=r.text.split(sep_player)[i].split("fg\" >")[1].split("<")[0]
        tirosIntentados=r.text.split(sep_player)[i].split("fga\" >")[1].split("<")[0]
        tirosPorcentaje=r.text.split(sep_player)[i].split("fg_pct\" >")[1].split("<")[0]
        tiros3Anotados=r.text.split(sep_player)[i].split("fg3\" >")[1].split("<")[0]
        tiros3Intentados=r.text.split(sep_player)[i].split("fg3a\" >")[1].split("<")[0]
        tiros3Porcentaje=r.text.split(sep_player)[i].split("fg3_pct\" >")[1].split("<")[0]
        tiros2Anotados=r.text.split(sep_player)[i].split("fg2\" >")[1].split("<")[0]
        tiros2Intentados=r.text.split(sep_player)[i].split("fg2a\" >")[1].split("<")[0]
        tiros2Porcentaje=r.text.split(sep_player)[i].split("fg2_pct\" >")[1].split("<")[0]
        tirosLibresAnotados=r.text.split(sep_player)[i].split("ft\" >")[1].split("<")[0]
        tirosLibresIntentados=r.text.split(sep_player)[i].split("fta\" >")[1].split("<")[0]
        tirosLibresPorcentaje=r.text.split(sep_player)[i].split("ft_pct\" >")[1].split("<")[0]
        rebotesOfensivos=r.text.split(sep_player)[i].split("orb\" >")[1].split("<")[0]
        rebotesDefensivos=r.text.split(sep_player)[i].split("drb\" >")[1].split("<")[0]
        rebotesTotal=r.text.split(sep_player)[i].split("trb\" >")[1].split("<")[0]
        asistencias=r.text.split(sep_player)[i].split("ast\" >")[1].split("<")[0]
        robos=r.text.split(sep_player)[i].split("stl\" >")[1].split("<")[0]
        perdidas=r.text.split(sep_player)[i].split("tov\" >")[1].split("<")[0]
        tapones=r.text.split(sep_player)[i].split("blk\" >")[1].split("<")[0]
        faltas=r.text.split(sep_player)[i].split("pf\" >")[1].split("<")[0]
        puntos=r.text.split(sep_player)[i].split("pts\" >")[1].split("<")[0]
        i=i+2
        
        temporada=str(year-1)+"/"+str(year)
        #print(name, temporada)
        EvolucionDF.loc[k]= [name, tirosAnotados, tirosIntentados, tirosPorcentaje, tiros3Anotados, tiros3Intentados,
                            tiros3Porcentaje, tiros2Anotados, tiros2Intentados, tiros2Porcentaje, tirosLibresAnotados,
                            tirosLibresIntentados, tirosLibresPorcentaje, rebotesOfensivos, rebotesDefensivos, 
                            rebotesTotal, asistencias, robos, perdidas, tapones, faltas, puntos, temporada]   
        k=k+1
    os.system('cls')

        
EvolucionDF = EvolucionDF.dropna()

directorio = "evolucion"+str(time.strftime("%d_%m_%y"))

try:
    os.stat(directorio)
except:
    os.mkdir(directorio)
    
os.chdir(directorio)

nombre_fichero='evolucion'+str(time.strftime("%d_%m_%y"))+'.csv'

EvolucionDF.to_csv(nombre_fichero, header=True, index=False)

os.chdir('..')