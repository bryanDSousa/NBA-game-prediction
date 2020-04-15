import numpy as np
import requests as rq
import json
import time
from datetime import datetime
import pandas as pd
from unidecode import unidecode
from urllib.parse import unquote
import os

Distancias_DF = pd.DataFrame(index=np.arange(0, 400), columns=["Equipo A", "Equipo B", "Distancia"])

mapaEquiposCiudades = {
    "Philadelphia 76ers": 		"philadelphia",
    "Detroit Pistons":			"detroit",
    "Chicago Bulls":			"chicago",
    "Minnesota Timberwolves":	"mineapolis",
    "New York Knicks":			"nueva-york",
    "Denver Nuggets":			"denver",
    "Golden State Warriors":	"oakland",
    "Dallas Mavericks":			"dallas",
    "New Jersey Nets":			"brooklyn",
    "Charlotte Bobcats":		"charlotte",
    "Memphis Grizzlies":		"new-south-memphis",
    "San Antonio Spurs":		"san-antonio",
    "New Orleans Hornets":		"nueva-orleans",
    "Oklahoma City Thunder":	"oklahoma-city",
    "Orlando Magic":			"orlando",
    "Washington Wizards":		"washington",
    "Cleveland Cavaliers":		"cleveland",
    "Boston Celtics":			"boston",
    "Portland Trail Blazers":	"portland",
    "Los Angeles Lakers":		"los-angeles",
    "Sacramento Kings":			"sacramento",
    "Indiana Pacers":			"indianapolis",
    "Phoenix Suns":				"phoenix",
    "Utah Jazz":				"salt-lake-city",
    "Houston Rockets":			"houston",
    "Toronto Raptors":			"toronto",
    "Miami Heat":				"miami",
    "Los Angeles Clippers":		"los-angeles",
    "Atlanta Hawks":			"atlanta",
    "Milwaukee Bucks": 			"milwaukee",
    "Brooklyn Nets":			"brooklyn",
    "New Orleans Pelicans": 	"nueva-orleans",
    "Charlotte Hornets":		"charlotte"
}
equiposLista = [
"Philadelphia 76ers", 
"Detroit Pistons",
"Chicago Bulls",
"Minnesota Timberwolves",
"New York Knicks",
"Denver Nuggets",
"Golden State Warriors",
"Dallas Mavericks",
"New Jersey Nets",
"Charlotte Bobcats",
"Memphis Grizzlies",
"San Antonio Spurs",
"New Orleans Hornets",
"Oklahoma City Thunder",
"Orlando Magic",
"Washington Wizards",
"Cleveland Cavaliers",
"Boston Celtics",
"Portland Trail Blazers",
"Los Angeles Lakers",
"Sacramento Kings",	
"Indiana Pacers",
"Phoenix Suns",	
"Utah Jazz",
"Houston Rockets",
"Toronto Raptors",
"Miami Heat",
"Los Angeles Clippers",
"Atlanta Hawks",
"Milwaukee Bucks", 
"Brooklyn Nets",
"New Orleans Pelicans", 
"Charlotte Hornets"
]
k=0
url_base = "https://www.geodatos.net/distancias/"
for equipo in equiposLista:
    for equipo2 in equiposLista:
        if(mapaEquiposCiudades[equipo] != mapaEquiposCiudades[equipo2]):
            url = url_base + "de-"+ mapaEquiposCiudades[equipo] +"-a-" + mapaEquiposCiudades[equipo2]
            r = rq.get(url)
            distancia = r.text.split("style=\"font-size:1em;\"><b>")[1].split("k")[0].strip().replace(",", "")
            Distancias_DF.loc[k]=[equipo, equipo2, distancia]
            k=k+1
            if k % 100 == 0:
                os.system('cls')
                print(k, "lineas añadidas al DF")

directorio = "distancias"
try:
    os.stat(directorio)
except:
    os.mkdir(directorio)

os.chdir(directorio)
nombre_fichero='distancias.csv'
Distancias_DF.to_csv(nombre_fichero, header=True, index=False)