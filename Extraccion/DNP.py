import numpy as np
import requests as rq
import json
import time
from datetime import datetime
import pandas as pd
from unidecode import unidecode
from urllib.parse import unquote
import os

#declarar DF
DNP_DF = pd.DataFrame(index=np.arange(0, 400), columns=["Team", 
"Season",
"Date",
"Year",
"ID Partido",
"Local",
"Opponent",
"Team Points",
"Opponent Points",
"Result",
"Name",
"Reason" ])

mapaEquipos = {
"Philadelphia 76ers": 		"PHI",
"Detroit Pistons":			"DET",
"Chicago Bulls":			"CHI",
"Minnesota Timberwolves":	"MIN",
"New York Knicks":			"NYK",
"Denver Nuggets":			"DEN",
"Golden State Warriors":	"GSW",
"Dallas Mavericks":			"DAL",
"New Jersey Nets":			"NJN",
"Charlotte Bobcats":		"CHA",
"Memphis Grizzlies":		"MEM",
"San Antonio Spurs":		"SAS",
"New Orleans Hornets":		"NOH",
"Oklahoma City Thunder":	"OKC",
"Orlando Magic":			"ORL",
"Washington Wizards":		"WAS",
"Cleveland Cavaliers":		"CLE",
"Boston Celtics":			"BOS",
"Portland Trail Blazers":	"POR",
"Los Angeles Lakers":		"LAL",
"Sacramento Kings":			"SAC",
"Indiana Pacers":			"IND",
"Phoenix Suns":				"PHO",
"Utah Jazz":				"UTA",
"Houston Rockets":			"HOU",
"Toronto Raptors":			"TOR",
"Miami Heat":				"MIA",
"Los Angeles Clippers":		"LAC",
"Atlanta Hawks":			"ATL",
"Milwaukee Bucks": 			"MIL",
"Brooklyn Nets":			"BRK",
"New Orleans Pelicans": 	"NOP",
"Charlotte Hornets":		"CHO"
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
counter=0
seasons = np.arange(2016,2021,1)
urlBase = "https://www.basketball-reference.com"
tiempo_inicial = time.clock()
for season in seasons:
    for equipo in equiposLista: 
        r = rq.get("https://www.basketball-reference.com/teams/"+mapaEquipos[equipo]+"/"+str(season)+"_games.html")
        counter = counter + 1
        print(counter, "llamadas realizadas de 363")
        if(r.text.split("<title>")[1].split(" (404")[0] != 'Page Not Found'):
            #equipo season
            j=1
            while j<len(r.text.split("Regular Season Table")[1].split("href=\"/boxscores/index.cgi?month=")):
                date = r.text.split("Regular Season Table")[1].split("href=\"/boxscores/index.cgi?month=")[j].split(">")[1].split("<")[0].split(", ")[1].split(",")[0]
                year = r.text.split("Regular Season Table")[1].split("href=\"/boxscores/index.cgi?month=")[j].split(">")[1].split("<")[0].split(", ")[2]
                opponent = r.text.split("Regular Season Table")[1].split("href=\"/boxscores/index.cgi?month=")[j].split(".html\">")[2].split("<")[0]
                puntos = r.text.split("Regular Season Table")[1].split("href=\"/boxscores/index.cgi?month=")[j].split("pts\" >")[1].split("<")[0]
                puntos_rival = r.text.split("Regular Season Table")[1].split("href=\"/boxscores/index.cgi?month=")[j].split("pts\" >")[2].split("<")[0]
                if(mapaEquipos[equipo] in boxcore_url):     #CAMBIA EL CRITERIO PARA LOCAL/VISITANTE
                    Local = True
                else:
                    Local = False
                boxcore_url= r.text.split("Regular Season Table")[1].split("\"box_score_text\" ><a href=\"")[j].split("\">")[0]
                url_req_boxcore = urlBase + boxcore_url
                r_boxcore = rq.get(url_req_boxcore)
                if(puntos > puntos_rival):
                    resultado = "W" 
                else:
                    resultado = "L"
                i=1
                sep_basic = "all_box-"+mapaEquipos[equipo]+"-game-basic"
                sep_advanced = "all_box-"+mapaEquipos[equipo]+"-game-advanced"
                maximo = len(r_boxcore.text.split(sep_basic)[2].split("Team Totals")[0].split("data-stat=\"player\" csk=\""))
                while i < maximo:
                    if ("Did Not Play" in r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i]):
                        reason = "Did Not Play"
                        name = r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i].split("<")[0].split("\"")[0]
                        DNP_DF.loc[k] = [equipo, 
                                        season,
                                        date,
                                        year,
                                        boxcore_url,
                                        Local,
                                        opponent,
                                        puntos,
                                        puntos_rival,
                                        resultado,
                                        name,
                                        reason]
                        k = k + 1 
                        
                    if ("Did Not Dress" in r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i]):
                        reason = "Did Not Dress"
                        name = r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i].split("<")[0].split("\"")[0]
                        DNP_DF.loc[k] = [equipo, 
                                        season,
                                        date,
                                        year,
                                        boxcore_url,
                                        Local,
                                        opponent,
                                        puntos,
                                        puntos_rival,
                                        resultado,
                                        name,
                                        reason]
                        k = k + 1 

                    if ("Not With Team" in r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i]):
                        reason = "Not With Team"
                        name = r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i].split("<")[0].split("\"")[0]
                        DNP_DF.loc[k] = [equipo, 
                                        season,
                                        date,
                                        year,
                                        boxcore_url,
                                        Local,
                                        opponent,
                                        puntos,
                                        puntos_rival,
                                        resultado,
                                        name,
                                        reason]
                        k = k + 1 
            
                    if ("Player Suspended" in r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i]):
                        reason = "Player Suspended" 
                        name = r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i].split("<")[0].split("\"")[0]
                        DNP_DF.loc[k] = [equipo, 
                                        season,
                                        date,
                                        year,
                                        boxcore_url,
                                        Local,
                                        opponent,
                                        puntos,
                                        puntos_rival,
                                        resultado,
                                        name,
                                        reason]
                        k = k + 1 

                        #name, equipo, temporada, date, year, opponent, resultado
                    
                    i=i+1
                    if k % 100 == 0:
                        os.system('cls')
                        DNP_DF.head(10)
                        time_transcurrido = time.clock() - tiempo_inicial
                        print(equipo, season)
                        print(k, "lineas añadidas al DF")
                        print(time_transcurrido / 60, "minutos")
                j = j + 1
                n_jugadores_inactive = len(r_boxcore.text.split('Inactive')[1].split('referees')[0].split(mapaEquipos[equipo])[1].split('strong')[1].split("html\">"))
                i = 1
                while i < n_jugadores_inactive:
                    reason = "Player Inactive" 
                    name = r_boxcore.text.split('Inactive')[1].split('referees')[0].split(mapaEquipos[equipo])[1].split('strong')[1].split("html\">")[i].split('<')[0]
                    i= i + 1
                    DNP_DF.loc[k] = [equipo, 
                                    season,
                                    date,
                                    year,
                                    boxcore_url,
                                    Local,
                                    opponent,
                                    puntos,
                                    puntos_rival,
                                    resultado,
                                    name,
                                    reason]
                    k = k + 1 
                #r.text.split('Inactive')[1].split('referees')[0].split(mapaEquipos[equipo])[1].split('strong')[1]


directorio = "DNP_"+str(time.strftime("%d_%m_%y"))

try:
    os.stat(directorio)
except:
    os.mkdir(directorio)

os.chdir(directorio)

nombre_fichero='DNP_'+str(time.strftime("%d_%m_%y"))+'.csv'
DNP_DF.to_csv(nombre_fichero, header=True, index=False)
os.chdir("..")