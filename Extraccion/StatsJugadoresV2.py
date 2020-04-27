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
Stats_DF = pd.DataFrame(index=np.arange(0, 400), columns=["Team", 
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
"Minutes Played",
"Tiros anotados",
"Tiros intentados",
"Porcentaje de tiro",
"Tiros de tres anotados",
"Tiros de tres intentados",
"Porcentaje de tiro de tres",
"Tiros libres anotados",
"Tiros libres intentados",
"Porcentaje de tiro libre",
"Rebotes ofensivos",
"Rebotes defensivo",
"Rebotes total",
"Asistencias",
"Robos",
"Tapones",
"Perdidas",
"Faltas",
"Puntos",
"MasMenos",
"True shooting percentage",
"Effective field goal percentage",
"3Point attempt rate",
"Free throw attempt rate",
"Offensive rebound percentage",
"Defensive rebound percentage",
"Total rebound percentage",
"Assist percentage",
"Steal percentage",
"Block percentage",
"Turnover percentage",
"Offensive rate",
"Defensive rate", 
"Box plus minus", 
"Usage percentage" ])

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
                boxcore_url= r.text.split("Regular Season Table")[1].split("\"box_score_text\" ><a href=\"")[j].split("\">")[0]
                if(mapaEquipos[equipo] in boxcore_url):     #CAMBIA EL CRITERIO PARA LOCAL/VISITANTE
                    Local = True
                else:
                    Local = False
                url_req_boxcore = urlBase + boxcore_url
                r_boxcore = rq.get(url_req_boxcore)
                if(int(puntos) > int(puntos_rival)):         #CAMBIA LA COMPARACION POR BUG
                    resultado = "W" 
                else:
                    resultado = "L"
                i=1
                sep_basic = "all_box-"+mapaEquipos[equipo]+"-game-basic"
                sep_advanced = "all_box-"+mapaEquipos[equipo]+"-game-advanced"
                #print("____________________________")
                maximo = len(r_boxcore.text.split(sep_basic)[2].split("Team Totals")[0].split("data-stat=\"player\" csk=\""))
                while i < maximo:

                    
                    if ("Did Not Play" in r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i] or
                       "Did Not Dress" in r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i] or 
                       "Not With Team" in r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i] or
                       "Player Suspended" in r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i]):
                        time_transcurrido = time.clock() - tiempo_inicial
                    else:
                        name = r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i].split("<")[0].split("\"")[0]
                        mp = r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i].split("mp\" csk=")[1].split(">")[1].split("<")[0]
                        fg = r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i].split("fg\" >")[1].split("<")[0]
                        fga = r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i].split("fga\" >")[1].split("<")[0]
                        fg_pct = "0" + r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i].split("fg_pct\" >")[1].split("<")[0]
                        fg3 = r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i].split("fg3\" >")[1].split("<")[0]
                        fg3a = r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i].split("fg3a\" >")[1].split("<")[0]
                        fg3_pct = "0" + r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i].split("fg3_pct\" >")[1].split("<")[0]
                        ft = r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i].split("ft\" >")[1].split("<")[0]
                        fta = r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i].split("fta\" >")[1].split("<")[0]
                        ft_pct = "0" + r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i].split("ft_pct\" >")[1].split("<")[0]
                        orb = r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i].split("orb\" >")[1].split("<")[0]
                        drb = r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i].split("drb\" >")[1].split("<")[0]
                        trn = r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i].split("trb\" >")[1].split("<")[0]
                        ast = r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i].split("ast\" >")[1].split("<")[0]
                        stl = r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i].split("stl\" >")[1].split("<")[0]
                        blk = r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i].split("blk\" >")[1].split("<")[0]
                        tov = r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i].split("tov\" >")[1].split("<")[0]
                        pf = r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i].split("pf\" >")[1].split("<")[0]
                        pts = r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i].split("pts\" >")[1].split("<")[0]
                        plus_min = r_boxcore.text.split(sep_basic)[2].split("player\" csk=\"")[i].split("plus_minus\" >")[1].split("<")[0]

                        tsp = "0" + r_boxcore.text.split(sep_advanced)[2].split("player\" csk=\"")[i].split("ts_pct\" >")[1].split("<")[0]
                        efgp = "0" + r_boxcore.text.split(sep_advanced)[2].split("player\" csk=\"")[i].split("efg_pct\" >")[1].split("<")[0]
                        f3pa_rate = "0" + r_boxcore.text.split(sep_advanced)[2].split("player\" csk=\"")[i].split("fg3a_per_fga_pct\" >")[1].split("<")[0]
                        fta_rate = "0" + r_boxcore.text.split(sep_advanced)[2].split("player\" csk=\"")[i].split("fta_per_fga_pct\" >")[1].split("<")[0]
                        orb_pct = r_boxcore.text.split(sep_advanced)[2].split("player\" csk=\"")[i].split("orb_pct\" >")[1].split("<")[0]
                        drb_pct = r_boxcore.text.split(sep_advanced)[2].split("player\" csk=\"")[i].split("drb_pct\" >")[1].split("<")[0]
                        trb_pct = r_boxcore.text.split(sep_advanced)[2].split("player\" csk=\"")[i].split("trb_pct\" >")[1].split("<")[0]
                        ast_pct = r_boxcore.text.split(sep_advanced)[2].split("player\" csk=\"")[i].split("ast_pct\" >")[1].split("<")[0]
                        stl_pct = r_boxcore.text.split(sep_advanced)[2].split("player\" csk=\"")[i].split("stl_pct\" >")[1].split("<")[0]
                        blk_pct = r_boxcore.text.split(sep_advanced)[2].split("player\" csk=\"")[i].split("blk_pct\" >")[1].split("<")[0]
                        tov_pct = r_boxcore.text.split(sep_advanced)[2].split("player\" csk=\"")[i].split("tov_pct\" >")[1].split("<")[0]
                        off_rate = r_boxcore.text.split(sep_advanced)[2].split("player\" csk=\"")[i].split("off_rtg\" >")[1].split("<")[0]
                        def_rate = r_boxcore.text.split(sep_advanced)[2].split("player\" csk=\"")[i].split("def_rtg\" >")[1].split("<")[0]
                        bpm = r_boxcore.text.split(sep_advanced)[2].split("player\" csk=\"")[i].split("bpm\" >")[1].split("<")[0]
                        usg_pct = r_boxcore.text.split(sep_advanced)[2].split("player\" csk=\"")[i].split("usg_pct\" >")[1].split("<")[0]
                        #usg_pct
                        Stats_DF.loc[k] = [equipo, 
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
                                                mp,
                                                fg,
                                                fga,
                                                fg_pct,
                                                fg3,
                                                fg3a,
                                                fg3_pct,
                                                ft,
                                                fta,
                                                ft_pct,
                                                orb,
                                                drb,
                                                trn,
                                                ast,
                                                stl,
                                                blk,
                                                tov,
                                                pf,
                                                pts,
                                                plus_min,
                                                tsp,
                                                efgp,
                                                f3pa_rate,
                                                fta_rate,
                                                orb_pct,
                                                drb_pct,
                                                trb_pct,
                                                ast_pct,
                                                stl_pct,
                                                blk_pct,
                                                tov_pct,
                                                off_rate,
                                                def_rate,
                                                 bpm, 
                                                 usg_pct]
                        
                        #name, equipo, temporada, date, year, opponent, resultado
                    
                    i=i+1

                    
                    k = k + 1
                    if k % 100 == 0:
                        os.system('cls')
                        print(equipo, season)
                        print(k, "lineas añadidas al DF")
                        print(time_transcurrido / 60, "minutos")
                j = j + 1
                                                              
directorio = "Jugadores"

try:
    os.stat(directorio)
except:
    os.mkdir(directorio)
    
os.chdir(directorio)

nombre_fichero='Stats_jugadores_'+str(time.strftime("%d_%m_%y"))+'.csv'
Stats_DF.to_csv(nombre_fichero, header=True, index=False)
os.chdir("..")