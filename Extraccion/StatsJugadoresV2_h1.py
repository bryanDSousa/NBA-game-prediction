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
Stats_DF = pd.DataFrame(index=np.arange(0, 400), columns=[
"Team", 
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
"Tiros de tres anotados",
"Tiros de tres intentados",
"Tiros libres anotados",
"Tiros libres intentados",
"Rebotes ofensivos",
"Rebotes defensivo",
"Rebotes total",
"Asistencias",
"Robos",
"Tapones",
"Perdidas",
"Faltas",
"Puntos",
"MasMenos"])

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
seasons = np.arange(2018,2021,1)
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

                if(mapaEquipos[equipo] in boxcore_url):     
                    Local = True
                else:
                    Local = False
                url_req_boxcore = urlBase + boxcore_url
                r_boxcore = rq.get(url_req_boxcore)
                if(int(puntos) > int(puntos_rival)):         
                    resultado = "W" 
                else:
                    resultado = "L"
                i=1
                
                sep_equipo = "all_box-"+mapaEquipos[equipo]+"-h1-basic"
                  
                maximo_equipo = len(r_boxcore.text.split(sep_equipo)[2].split("Team Totals")[0].split("data-stat=\"player\" csk=\""))
                while i < maximo_equipo:
                    if ("Did Not Play" in r_boxcore.text.split(sep_equipo)[2].split("player\" csk=\"")[i] or
                    "Did Not Dress" in r_boxcore.text.split(sep_equipo)[2].split("player\" csk=\"")[i] or 
                    "Not With Team" in r_boxcore.text.split(sep_equipo)[2].split("player\" csk=\"")[i] or
                    "Player Suspended" in r_boxcore.text.split(sep_equipo)[2].split("player\" csk=\"")[i]):
                        time_transcurrido = time.clock() - tiempo_inicial
                    else:
                        name = r_boxcore.text.split(sep_equipo)[2].split("player\" csk=\"")[i].split("<")[0].split("\"")[0]
                        mp = r_boxcore.text.split(sep_equipo)[2].split("player\" csk=\"")[i].split("mp\" csk=")[1].split(">")[1].split("<")[0]
                        fg = r_boxcore.text.split(sep_equipo)[2].split("player\" csk=\"")[i].split("fg\" >")[1].split("<")[0]
                        fga = r_boxcore.text.split(sep_equipo)[2].split("player\" csk=\"")[i].split("fga\" >")[1].split("<")[0]
                        #fg_pct = "0" + r_boxcore.text.split(sep_equipo)[2].split("player\" csk=\"")[i].split("fg_pct\" >")[1].split("<")[0]
                        fg3 = r_boxcore.text.split(sep_equipo)[2].split("player\" csk=\"")[i].split("fg3\" >")[1].split("<")[0]
                        fg3a = r_boxcore.text.split(sep_equipo)[2].split("player\" csk=\"")[i].split("fg3a\" >")[1].split("<")[0]
                        #fg3_pct = "0" + r_boxcore.text.split(sep_equipo)[2].split("player\" csk=\"")[i].split("fg3_pct\" >")[1].split("<")[0]
                        ft = r_boxcore.text.split(sep_equipo)[2].split("player\" csk=\"")[i].split("ft\" >")[1].split("<")[0]
                        fta = r_boxcore.text.split(sep_equipo)[2].split("player\" csk=\"")[i].split("fta\" >")[1].split("<")[0]
                        #ft_pct = "0" + r_boxcore.text.split(sep_equipo)[2].split("player\" csk=\"")[i].split("ft_pct\" >")[1].split("<")[0]
                        orb = r_boxcore.text.split(sep_equipo)[2].split("player\" csk=\"")[i].split("orb\" >")[1].split("<")[0]
                        drb = r_boxcore.text.split(sep_equipo)[2].split("player\" csk=\"")[i].split("drb\" >")[1].split("<")[0]
                        trn = r_boxcore.text.split(sep_equipo)[2].split("player\" csk=\"")[i].split("trb\" >")[1].split("<")[0]
                        ast = r_boxcore.text.split(sep_equipo)[2].split("player\" csk=\"")[i].split("ast\" >")[1].split("<")[0]
                        stl = r_boxcore.text.split(sep_equipo)[2].split("player\" csk=\"")[i].split("stl\" >")[1].split("<")[0]
                        blk = r_boxcore.text.split(sep_equipo)[2].split("player\" csk=\"")[i].split("blk\" >")[1].split("<")[0]
                        tov = r_boxcore.text.split(sep_equipo)[2].split("player\" csk=\"")[i].split("tov\" >")[1].split("<")[0]
                        pf = r_boxcore.text.split(sep_equipo)[2].split("player\" csk=\"")[i].split("pf\" >")[1].split("<")[0]
                        pts = r_boxcore.text.split(sep_equipo)[2].split("player\" csk=\"")[i].split("pts\" >")[1].split("<")[0]
                        plus_min = r_boxcore.text.split(sep_equipo)[2].split("player\" csk=\"")[i].split("plus_minus\" >")[1].split("<")[0]

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
                                                int(fg),
                                                int(fga),
                                                int(fg3),
                                                int(fg3a),
                                                int(ft),
                                                int(fta),
                                                int(orb),
                                                int(drb),
                                                int(trn),
                                                int(ast),
                                                int(stl),
                                                int(blk),
                                                int(tov),
                                                int(pf,),
                                                int(pts),
                                                plus_min
                             ]
                            
                        #name, equipo, temporada, date, year, opponent, resultado
                    
                    i=i+1

                    
                    k = k + 1
                    if k % 100 == 0:
                        os.system('cls')
                        print(equipo, season)
                        print(k, "lineas añadidas al DF")
                        print(time_transcurrido / 60, "minutos")
                j = j + 1
Stats_DF = Stats_DF.dropna()

#local_df
Local = Stats_DF[Stats_DF["Local"] == True]
Local = Local.drop(['Name', 'Local', 'Opponent', 'Team Points', 'Opponent Points', 'Minutes Played', 'MasMenos'], axis=1)
Local = Local.groupby(
             ['ID Partido', 'Date', 'Year', 'Season', 'Team', 'Result'], as_index = False
                     ).sum()
#calculo de Porcentaje
Local["Porcentaje de tiro libre"] = 100 * Local['Tiros libres anotados'] / Local['Tiros libres intentados']
Local["Porcentaje de tiro"] = 100 * Local['Tiros anotados'] / Local['Tiros intentados']
Local["Porcentaje de tiro de tres"] = 100 * Local['Tiros de tres anotados'] / Local['Tiros de tres intentados']

#rename
#ID Partido, clave del join
#Date,Year,Season tal cual
Local.rename(columns={
    'Team': 'local_team',
    'Tiros anotados': 'local_fga', 
    'Tiros intentados': 'local_fga', 
    'Tiros de tres anotados': 'local_fg3',
    'Tiros de tres intentados': 'local_fg3a',
    'Tiros libres anotados': 'local_ft',
    'Tiros libres intentados': 'local_fta',
    'Rebotes ofensivos': 'local_orb',
    'Rebotes defensivo': 'local_drb',
    'Rebotes total': 'local_trb',
    'Asistencias': 'local_ast',
    'Robos': 'local_stl',
    'Tapones': 'local_blk',
    'Perdidas': 'local_tov',
    'Faltas': 'local_pf',
    'Puntos': 'local_pts',
    'Porcentaje de tiro libre': 'local_ft_pct', 
    'Porcentaje de tiro': 'local_fg_pct',
    'Porcentaje de tiro de tres': 'local_fg3_pct'
    }, inplace = True)

#visitante_DF 
Visitante = Stats_DF[Stats_DF["Local"] == False]
Visitante = Visitante.drop(['Name', 'Local', 'Result', 'Opponent', 'Team Points', 'Opponent Points', 'Minutes Played', 'MasMenos', 'Result','Date', 'Year', 'Season'], axis=1)
Visitante = Visitante.groupby(
             ['ID Partido', 'Team'], as_index = False
                     ).sum()
#calculo de Porcentaje
Visitante["Porcentaje de tiro libre"] = 100 * Visitante['Tiros libres anotados'] / Visitante['Tiros libres intentados']
Visitante["Porcentaje de tiro"] = 100 *  Visitante['Tiros anotados'] / Visitante['Tiros intentados']
Visitante["Porcentaje de tiro de tres"] = 100 *  Visitante['Tiros de tres anotados'] / Visitante['Tiros de tres intentados']
#rename 
#ID Partido,
#Team, visitor_team
#Tiros anotados,Tiros intentados,Tiros de tres anotados,Tiros de tres intentados,Tiros libres anotados,Tiros libres intentados,Rebotes ofensivos,Rebotes defensivo,Rebotes total,Asistencias,Robos,Tapones,Perdidas,Faltas,Puntos
Visitante.rename(columns={
    'Team': 'visitor_team',
    'Tiros anotados': 'visitor_fga', 
    'Tiros intentados': 'visitor_fga', 
    'Tiros de tres anotados': 'visitor_fg3',
    'Tiros de tres intentados': 'visitor_fg3a',
    'Tiros libres anotados': 'visitor_ft',
    'Tiros libres intentados': 'visitor_fta',
    'Rebotes ofensivos': 'visitor_orb',
    'Rebotes defensivo': 'visitor_drb',
    'Rebotes total': 'visitor_trb',
    'Asistencias': 'visitor_ast',
    'Robos': 'visitor_stl',
    'Tapones': 'visitor_blk',
    'Perdidas': 'visitor_tov',
    'Faltas': 'visitor_pf',
    'Puntos': 'visitor_pts',
    'Porcentaje de tiro libre': 'visitor_ft_pct', 
    'Porcentaje de tiro': 'visitor_fg_pct',
    'Porcentaje de tiro de tres': 'visitor_fg3_pct'
    }, inplace = True)            

Stats_h1 = Local.merge(Visitante, on='ID Partido', how='left')

directorio = "Stats_jugadores_H1_"+str(time.strftime("%d_%m_%y"))

try:
    os.stat(directorio)
except:
    os.mkdir(directorio)
    
os.chdir(directorio)

#nombre_fichero='Stats_jugadores_'+str(time.strftime("%d_%m_%y"))+'.csv'
Stats_h1.to_csv('stats_h1.csv', header=True, index=False)

os.chdir("..")