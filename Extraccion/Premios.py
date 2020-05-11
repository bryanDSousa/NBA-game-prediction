import numpy as np
import requests as rq
import json
import time
from datetime import datetime
import pandas as pd
from unidecode import unidecode
from urllib.parse import unquote
import os

years = np.arange(2010,2021,1)

list_awards = ["Most Valuable Player", "Rookie of the Year", "Defensive Player of the Year",
               "Sixth Man of the Year", "Most Improved Player"]

sep_tables = "/table"
sep_player = "csk=\""
sep_first = "votes_first\" >"
sep_points = "points_won\" >"
sep_points_max = "points_max\" >"
sep_share = "award_share\" >"

premiosDF = pd.DataFrame(index=np.arange(0, 400), columns=["nombre", "primero", "puntos", "puntos_maximos",
                                                               "share", "award", "año", "Clave Join"])

k=0
for year in years:
    r = rq.get('https://www.basketball-reference.com/awards/awards_'+str(year)+'.html')
    i=0
    j=1
    while i < len(r.text.split(sep_tables)) -1:
        j=1
        while j < len(r.text.split(sep_tables)[i].split(sep_player)):
            name=r.text.split(sep_tables)[i].split(sep_player)[j].split("\"")[0]
            first=r.text.split(sep_tables)[i].split(sep_player)[j].split(sep_first)[1].split("<")[0]
            pts_Won=r.text.split(sep_tables)[i].split(sep_player)[j].split(sep_points)[1].split("<")[0]
            pts_Max=r.text.split(sep_tables)[i].split(sep_player)[j].split(sep_points_max)[1].split("<")[0]
            share=r.text.split(sep_tables)[i].split(sep_player)[j].split(sep_share)[1].split("<")[0]
            award=list_awards[i]
            clavejoin = name.split(",")[1]+name.split(",")[0]
            clavejoin = clavejoin.replace(" ", "").replace("-", "").replace(".","").\
                                 replace("III", "").replace("II", "").replace("IV","").replace("Jr","").\
                                 replace("Sr","").replace('\'', "")
            clavejoin=unidecode(unquote(clavejoin))
            premiosDF.loc[k]= [name, first, pts_Won, pts_Max, share, award, year, clavejoin]   
            if k % 10 == 0:
                os.system('cls')
                print(k, "lineas añadidas al DF")
            k=k+1
            j=j+1
            
            
        i=i+1

    premiosDF=premiosDF.dropna()


directorio = "Premios_"+str(time.strftime("%d_%m_%y"))

try:
    os.stat(directorio)
except:
    os.mkdir(directorio)
    
os.chdir(directorio)

nombre_fichero='Premios_'+str(time.strftime("%d_%m_%y"))+'.csv'

premiosDF.to_csv(nombre_fichero, header=True, index=False)

os.chdir('..')