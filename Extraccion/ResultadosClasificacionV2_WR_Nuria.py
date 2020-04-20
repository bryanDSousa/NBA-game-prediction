import numpy as np
import requests as rq
import json
import time
from datetime import datetime
import pandas as pd
from unidecode import unidecode
from urllib.parse import unquote
import os

Clasificacion_Fechas_DF = pd.DataFrame(index=np.arange(0, 400), columns=["Date", "Year", "Season", "Team", "Conf_position",
                                                                         "Win", "Lose", "Percentagewl",
                                                                         "Dif_leader", "Home_win","Home_lose",
                                                                         "Away_win", "Away_lose",
                                                                          "Div_win", "Div_lose",
                                                                         "Cnf_win", "Cnf_lose", 
                                                                         "Icf_win", "Icf_lose"])

k=0
counter = 0
seasons = np.arange(2015,2021,1)
months = ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May" ]
days = np.arange(1,32,1)
for season in seasons:
    for month in months:
        for day in days:
            request = 'https://www.shrpsports.com/nba/stand.php?link=Y&season='+str(season)+\
                       '&divcnf=cnf&month='+month+'&date='+str(day)
            #time.sleep(1)
            counter = counter + 1
            print(counter, "llamadas realizadas de un total de 2800")
            r = rq.get(request)
            i=1
            j=1
            if(r.text.split("<title>")[1].split("had")[0] != "No NBA games " ):
                while i<31:
                    
                    date = r.text.split("after")[1].split("in")[0].strip()
                    date1 = int(date.split(" ")[1])
                    date2 = date.split(" ")[0]
                    date = date2 + " " + str(date1)
                    if(month == "Oct" or month == "Nov" or month == "Dec"):
                        year = season - 1
                    else:
                        year = season
                        
                    team=r.text.split("season="+str(season)+"\">")[i].split("<")[0]

                    win=r.text.split("season="+str(season)+"\">")[i].split("\"> ")[1].split("<")[0].split("-")[0]
                    lose=r.text.split("season="+str(season)+"\">")[i].split("\"> ")[1].split("<")[0].split("-")[1]
                    if(int(win)+int(lose) != 0):
                        percentagewl=int(win)/(int(win)+int(lose))
                    else:
                        percentagewl=0

                    dif=r.text.split("season="+str(season)+"\">")[i].split("\"> ")[3].split("<")[0]
                    if dif[0] == "-":
                        dif=0
                    Home_win=r.text.split("season="+str(season)+"\">")[i].split("\"> ")[4].split("<")[0].split("-")[0]
                    Home_lose=r.text.split("season="+str(season)+"\">")[i].split("\"> ")[4].split("<")[0].split("-")[1]

                    Away_win=r.text.split("season="+str(season)+"\">")[i].split("\"> ")[5].split("<")[0].split("-")[0]
                    Away_lose=r.text.split("season="+str(season)+"\">")[i].split("\"> ")[5].split("<")[0].split("-")[1]


                    Div_win=r.text.split("season="+str(season)+"\">")[i].split("\"> ")[6].split("<")[0].split("-")[0]
                    Div_lose=r.text.split("season="+str(season)+"\">")[i].split("\"> ")[6].split("<")[0].split("-")[1]

                    Cnf_win=r.text.split("season="+str(season)+"\">")[i].split("\"> ")[7].split("<")[0].split("-")[0]
                    Cnf_lose=r.text.split("season="+str(season)+"\">")[i].split("\"> ")[7].split("<")[0].split("-")[1]

                    Icf_win=r.text.split("season="+str(season)+"\">")[i].split("\"> ")[8].split("<")[0].split("-")[0]
                    Icf_lose=r.text.split("season="+str(season)+"\">")[i].split("\"> ")[8].split("<")[0].split("-")[1]

                    #print(j, equipo, win, lose, percentagewl, dif, Home_win, Home_lose, Away_win, Away_lose,
                    #      Div_win, Div_lose, Cnf_win, Cnf_lose, Icf_win, Icf_lose)
                    Clasificacion_Fechas_DF.loc[k]= [date, year, season, team, i, win, lose, percentagewl, 
                                                     dif, Home_win, Home_lose, Away_win, Away_lose,
                                                      Div_win, Div_lose, Cnf_win, Cnf_lose, Icf_win, Icf_lose] 
                    k=k+1
                    if j != 15:
                        j = j + 1
                    else:
                        j = 1
                    if k % 100 == 0:
                        os.system('cls')
                        print(k, "lineas añadidas al DF")
                    i=1+i

Clasificacion_Fechas_DF = Clasificacion_Fechas_DF.drop_duplicates(keep='first')


Resultados_DF = pd.DataFrame(index=np.arange(0, 400), columns=["Date", "Year", "Season", "Team", "Opponent", "Local",
                                                               "Points", "Opponent_Points", "Result", "Streak",
                                                              "visitor_fg", "visitor_fga", "visitor_fg_pct", "visitor_fg3",
                                                               "visitor_fg3a", "visitor_fg3_pct", "visitor_ft", "visitor_fta",
                                                               "visitor_ft_pct", "visitor_orb", "visitor_drb", "visitor_trn",
                                                               "visitor_ast", "visitor_stl", "visitor_blk", "visitor_tov", 
                                                               "visitor_pf", "visitor_pts", "visitor_true_shooting_pct", 
                                                               "visitor_effective_fg_pct", "visitor_3pa_rate", "visitor_fta_rate", 
                                                               "visitor_orb_pct", 
                                                               "visitor_drb_pct", "visitor_trb_pct", "visitor_ast_pct",
                                                               "visitor_stl_pct", "visitor_blk_pct", "visitor_tov_pct", 
                                                               "visitor_off_rate", "visitor_def_rate", "local_fg", "local_fga",
                                                               "local_fg_pct", "local_fg3", "local_fg3a", "local_fg3_pct",
                                                               "local_ft", "local_fta", "local_ft_pct", "local_orb", "local_drb", 
                                                               "local_trn", "local_ast", "local_stl", "local_blk", "local_tov",
                                                               "local_pf", "local_pts", "local_true_shooting_pct", "local_effective_fg_pct", "local_3pa_rate", 
                                                               "local_fta_rate", "local_orb_pct", "local_drb_pct", "local_trb_pct", 
                                                               "local_ast_pct", "local_stl_pct", "local_blk_pct", "local_tov_pct",
                                                               "local_off_rate", "local_def_rate", "boxcore_url"])

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
"Philadelphia 76ers" ,
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

i=1

counter=0
k=0
urlBase = "https://www.basketball-reference.com"
for season in seasons:
    for equipo in equiposLista: 
        r = rq.get("https://www.basketball-reference.com/teams/"+mapaEquipos[equipo]+"/"+str(season)+"_games.html")
        counter = counter + 1
        print(counter, "llamadas realizadas de 363")
        if(r.text.split("<title>")[1].split(" (404")[0] != 'Page Not Found'):
            #equipo season
            j=1
            streak1 = 0
            while j<len(r.text.split("Regular Season Table")[1].split("href=\"/boxscores/index.cgi?month=")):
                date = r.text.split("Regular Season Table")[1].split("href=\"/boxscores/index.cgi?month=")[j].split(">")[1].split("<")[0].split(", ")[1].split(",")[0]
                year = r.text.split("Regular Season Table")[1].split("href=\"/boxscores/index.cgi?month=")[j].split(">")[1].split("<")[0].split(", ")[2]
                opponent = r.text.split("Regular Season Table")[1].split("href=\"/boxscores/index.cgi?month=")[j].split(".html\">")[2].split("<")[0]
                puntos = r.text.split("Regular Season Table")[1].split("href=\"/boxscores/index.cgi?month=")[j].split("pts\" >")[1].split("<")[0]
                puntos_rival = r.text.split("Regular Season Table")[1].split("href=\"/boxscores/index.cgi?month=")[j].split("pts\" >")[2].split("<")[0]
                if(int(puntos) > int(puntos_rival)):         #CAMBIA LA COMPARACION POR BUG
                    resultado = "W" 
                else:
                    resultado = "L"
                streak2 = r.text.split("Regular Season Table")[1].split("href=\"/boxscores/index.cgi?month=")[j].split("game_streak\" >")[1].split("<")[0]
                boxcore_url= r.text.split("Regular Season Table")[1].split("\"box_score_text\" ><a href=\"")[j].split("\">")[0]
                url_req_boxcore = urlBase + boxcore_url
                r_boxcore = rq.get(url_req_boxcore)
                if(mapaEquipos[equipo] in boxcore_url):     #CAMBIA EL CRITERIO PARA LOCAL/VISITANTE
                    Local = True
                else:
                    Local = False
                minutos = r_boxcore.text.split("Team Totals")[1].split("mp\" >")[1].split("<")[0]
                if(minutos == "240"):
                    sep1 = 1
                    sep8 = 8
                    sep9 = 9
                    sep16 = 16
                if(minutos == "265"):
                    sep1 = 1
                    sep8 = 9
                    sep9 = 10
                    sep16 = 18
                if(minutos == "290"):
                    sep1 = 1
                    sep8 = 10
                    sep9 = 11
                    sep16 = 20
                if(minutos == "315"):
                    sep1 = 1
                    sep8 = 11
                    sep9 = 12
                    sep16 = 22
                if(minutos == "340"):
                    sep1 = 1
                    sep8 = 12
                    sep9 = 13
                    sep16 = 24  
                #BASIC VISITOR
                visitor_fg = r_boxcore.text.split("Team Totals")[sep1].split("fg\" >")[1].split("<")[0]
                visitor_fga = r_boxcore.text.split("Team Totals")[sep1].split("fga\" >")[1].split("<")[0]
                visitor_fg_pct = "0" + r_boxcore.text.split("Team Totals")[sep1].split("fg_pct\" >")[1].split("<")[0]
                visitor_fg3 = r_boxcore.text.split("Team Totals")[sep1].split("fg3\" >")[1].split("<")[0]
                visitor_fg3a = r_boxcore.text.split("Team Totals")[sep1].split("fg3a\" >")[1].split("<")[0]
                visitor_fg3_pct = "0" + r_boxcore.text.split("Team Totals")[sep1].split("fg3_pct\" >")[1].split("<")[0]
                visitor_ft = r_boxcore.text.split("Team Totals")[sep1].split("ft\" >")[1].split("<")[0]
                visitor_fta = r_boxcore.text.split("Team Totals")[sep1].split("fta\" >")[1].split("<")[0]
                visitor_ft_pct = "0" + r_boxcore.text.split("Team Totals")[sep1].split("ft_pct\" >")[1].split("<")[0]
                visitor_orb = r_boxcore.text.split("Team Totals")[sep1].split("orb\" >")[1].split("<")[0]
                visitor_drb = r_boxcore.text.split("Team Totals")[sep1].split("drb\" >")[1].split("<")[0]
                visitor_trn = r_boxcore.text.split("Team Totals")[sep1].split("trb\" >")[1].split("<")[0]
                visitor_ast = r_boxcore.text.split("Team Totals")[sep1].split("ast\" >")[1].split("<")[0]
                visitor_stl = r_boxcore.text.split("Team Totals")[sep1].split("stl\" >")[1].split("<")[0]
                visitor_blk = r_boxcore.text.split("Team Totals")[sep1].split("blk\" >")[1].split("<")[0]
                visitor_tov = r_boxcore.text.split("Team Totals")[sep1].split("tov\" >")[1].split("<")[0]
                visitor_pf = r_boxcore.text.split("Team Totals")[sep1].split("pf\" >")[1].split("<")[0]
                visitor_pts = r_boxcore.text.split("Team Totals")[sep1].split("pts\" >")[1].split("<")[0]
                #ADVANCED VISITOR
                visitor_tsp = "0" + r_boxcore.text.split("Team Totals")[sep8].split("ts_pct\" >")[1].split("<")[0]
                visitor_efgp = "0" + r_boxcore.text.split("Team Totals")[sep8].split("efg_pct\" >")[1].split("<")[0]
                visitor_3pa_rate = "0" + r_boxcore.text.split("Team Totals")[sep8].split("fg3a_per_fga_pct\" >")[1].split("<")[0]
                visitor_fta_rate = "0" + r_boxcore.text.split("Team Totals")[sep8].split("fta_per_fga_pct\" >")[1].split("<")[0]
                visitor_orb_pct = r_boxcore.text.split("Team Totals")[sep8].split("orb_pct\" >")[1].split("<")[0]
                visitor_drb_pct = r_boxcore.text.split("Team Totals")[sep8].split("drb_pct\" >")[1].split("<")[0]
                visitor_trb_pct = r_boxcore.text.split("Team Totals")[sep8].split("trb_pct\" >")[1].split("<")[0]
                visitor_ast_pct = r_boxcore.text.split("Team Totals")[sep8].split("ast_pct\" >")[1].split("<")[0]
                visitor_stl_pct = r_boxcore.text.split("Team Totals")[sep8].split("stl_pct\" >")[1].split("<")[0]
                visitor_blk_pct = r_boxcore.text.split("Team Totals")[sep8].split("blk_pct\" >")[1].split("<")[0]
                visitor_tov_pct = r_boxcore.text.split("Team Totals")[sep8].split("tov_pct\" >")[1].split("<")[0]
                visitor_off_rate = r_boxcore.text.split("Team Totals")[sep8].split("off_rtg\" >")[1].split("<")[0]
                visitor_def_rate = r_boxcore.text.split("Team Totals")[sep8].split("def_rtg\" >")[1].split("<")[0]
                #BASIC LOCAL
                local_fg = r_boxcore.text.split("Team Totals")[sep9].split("fg\" >")[1].split("<")[0]
                local_fga = r_boxcore.text.split("Team Totals")[sep9].split("fga\" >")[1].split("<")[0]
                local_fg_pct = r_boxcore.text.split("Team Totals")[sep9].split("fg_pct\" >")[1].split("<")[0]
                local_fg3 = r_boxcore.text.split("Team Totals")[sep9].split("fg3\" >")[1].split("<")[0]
                local_fg3a = r_boxcore.text.split("Team Totals")[sep9].split("fg3a\" >")[1].split("<")[0]
                local_fg3_pct = r_boxcore.text.split("Team Totals")[sep9].split("fg3_pct\" >")[1].split("<")[0]
                local_ft = r_boxcore.text.split("Team Totals")[sep9].split("ft\" >")[1].split("<")[0]
                local_fta = r_boxcore.text.split("Team Totals")[sep9].split("fta\" >")[1].split("<")[0]
                local_ft_pct = r_boxcore.text.split("Team Totals")[sep9].split("ft_pct\" >")[1].split("<")[0]
                local_orb = r_boxcore.text.split("Team Totals")[sep9].split("orb\" >")[1].split("<")[0]
                local_drb = r_boxcore.text.split("Team Totals")[sep9].split("drb\" >")[1].split("<")[0]
                local_trn = r_boxcore.text.split("Team Totals")[sep9].split("trb\" >")[1].split("<")[0]
                local_ast = r_boxcore.text.split("Team Totals")[sep9].split("ast\" >")[1].split("<")[0]
                local_stl = r_boxcore.text.split("Team Totals")[sep9].split("stl\" >")[1].split("<")[0]
                local_blk = r_boxcore.text.split("Team Totals")[sep9].split("blk\" >")[1].split("<")[0]
                local_tov = r_boxcore.text.split("Team Totals")[sep9].split("tov\" >")[1].split("<")[0]
                local_pf = r_boxcore.text.split("Team Totals")[sep9].split("pf\" >")[1].split("<")[0]
                local_pts = r_boxcore.text.split("Team Totals")[sep9].split("pts\" >")[1].split("<")[0]
                #ADVANCED LOCAL
                local_tsp = r_boxcore.text.split("Team Totals")[sep16].split("ts_pct\" >")[1].split("<")[0]
                local_efgp = r_boxcore.text.split("Team Totals")[sep16].split("efg_pct\" >")[1].split("<")[0]
                local_3pa_rate = r_boxcore.text.split("Team Totals")[sep16].split("fg3a_per_fga_pct\" >")[1].split("<")[0]
                local_fta_rate = r_boxcore.text.split("Team Totals")[sep16].split("fta_per_fga_pct\" >")[1].split("<")[0]
                local_orb_pct = r_boxcore.text.split("Team Totals")[sep16].split("orb_pct\" >")[1].split("<")[0]
                local_drb_pct = r_boxcore.text.split("Team Totals")[sep16].split("drb_pct\" >")[1].split("<")[0]
                local_trb_pct = r_boxcore.text.split("Team Totals")[sep16].split("trb_pct\" >")[1].split("<")[0]
                local_ast_pct = r_boxcore.text.split("Team Totals")[sep16].split("ast_pct\" >")[1].split("<")[0]
                local_stl_pct = r_boxcore.text.split("Team Totals")[sep16].split("stl_pct\" >")[1].split("<")[0]
                local_blk_pct = r_boxcore.text.split("Team Totals")[sep16].split("blk_pct\" >")[1].split("<")[0]
                local_tov_pct = r_boxcore.text.split("Team Totals")[sep16].split("tov_pct\" >")[1].split("<")[0]
                local_off_rate = r_boxcore.text.split("Team Totals")[sep16].split("off_rtg\" >")[1].split("<")[0]
                local_def_rate = r_boxcore.text.split("Team Totals")[sep16].split("def_rtg\" >")[1].split("<")[0]

                if(streak2[0]=="W"):
                    streak2 = 0 + int(streak2.split(" ")[1])
                else:
                    streak2 = 0 - int(streak2.split(" ")[1])
                j = j + 1
                Resultados_DF.loc[k] = [date, year, season, equipo, opponent, Local, puntos, puntos_rival, resultado, streak1, 
                                        visitor_fg, visitor_fga, visitor_fg_pct, visitor_fg3, visitor_fg3a, visitor_fg3_pct,
                                        visitor_ft, visitor_fta, visitor_ft_pct, visitor_orb, visitor_drb, visitor_trn, 
                                        visitor_ast, visitor_stl, visitor_blk, visitor_tov, visitor_pf, visitor_pts, visitor_tsp, 
                                        visitor_efgp, visitor_3pa_rate, visitor_fta_rate, visitor_orb_pct, visitor_drb_pct, 
                                        visitor_trb_pct, visitor_ast_pct, visitor_stl_pct, visitor_blk_pct, visitor_tov_pct, 
                                        visitor_off_rate, visitor_def_rate, local_fg, local_fga, local_fg_pct, local_fg3, 
                                        local_fg3a, local_fg3_pct, local_ft, local_fta, local_ft_pct, local_orb, local_drb, 
                                        local_trn, local_ast, local_stl, local_blk, local_tov, local_pf, local_pts, local_tsp, 
                                        local_efgp, local_3pa_rate, local_fta_rate, local_orb_pct, local_drb_pct, local_trb_pct, 
                                        local_ast_pct, local_stl_pct, local_blk_pct, local_tov_pct, local_off_rate, local_def_rate,
                                        boxcore_url]
                #print(date, year, season, equipo, opponent, puntos, puntos_rival, resultado, streak1)
                streak1 = streak2
                k = k + 1
                if k % 100 == 0:
                    os.system('cls')
                    print(equipo, season)
                    print(k, "lineas añadidas al DF")
                                                              
            i = i + 1
Resultados_DF = Resultados_DF.dropna()

#REVISAR LOCAL CON NURIA
Resultados_DF_Local = Resultados_DF[Resultados_DF["Local"]]
#Resultados_DF_Local = Resultados_DF

mapaEquipos2 = {
    'Boston Celtics': 'Boston', 
    'Washington Wizards': 'Washington',
    'New Jersey Nets': 'New Jersey',
    'New York Knicks':  'New York',
    'Philadelphia 76ers': 'Philadelphia',  
    'Toronto Raptors': 'Toronto',
    'Chicago Bulls': 'Chicago', 
    'Detroit Pistons': 'Detroit', 
    'Indiana Pacers':  'Indiana',
    'Milwaukee Bucks': 'Milwaukee',
    'Atlanta Hawks': 'Atlanta',
    'Charlotte Bobcats': 'Cha Bobcats',
    'Miami Heat': 'Miami',
    'Orlando Magic': 'Orlando', 
    'Cleveland Cavaliers': 'Cleveland', 
    'Portland Trail Blazers': 'Portland',   
    'Los Angeles Lakers': 'LA Lakers',
    'Denver Nuggets': 'Denver',
    'Minnesota Timberwolves': 'Minnesota',
    'Oklahoma City Thunder': 'Oklahoma City',
    'Utah Jazz': 'Utah',
    'Golden State Warriors': 'Golden State',
    'Phoenix Suns':  'Phoenix',
    'Sacramento Kings': 'Sacramento',
    'Memphis Grizzlies': 'Memphis',
    'New Orleans Hornets':  'NO Hornets',
    'San Antonio Spurs': 'San Antonio',
    'Los Angeles Clippers': 'LA Clippers', 
    'Dallas Mavericks': 'Dallas',
    'Houston Rockets': 'Houston', 
    'Brooklyn Nets': 'Brooklyn',
    'New Orleans Pelicans': 'New Orleans',
    'Charlotte Hornets': 'Charlotte'   
}

i=0
df_row = pd.DataFrame(index=np.arange(0, 400), columns=Resultados_DF_Local.columns)
while i < len(Resultados_DF_Local):
    row = Resultados_DF_Local.iloc[i] 
    date = row['Date']
    year = row['Year']
    team = row['Team']
    opponent = row['Opponent']
    row_com_team = Clasificacion_Fechas_DF[ (Clasificacion_Fechas_DF['Team'] == mapaEquipos2[team]) & 
                                 (Clasificacion_Fechas_DF['Year'] == int(year)) &     
                                 (Clasificacion_Fechas_DF['Date'] == date)]
    row_com_opp =  Clasificacion_Fechas_DF[(Clasificacion_Fechas_DF['Team'] == mapaEquipos2[opponent]) & 
                                 (Clasificacion_Fechas_DF['Year'] == int(year)) &    
                                 (Clasificacion_Fechas_DF['Date'] == date)]
    df_row.loc[0]=row
    df_row= df_row.dropna()

    row_com_team.rename(columns={'Conf_position': 'local_Conf_position', 'Win': 'local_Win', 'Lose': 'local_Lose',
   'Percentagewl': 'local_Percentagewl', 'Dif_leader': 'local_Dif_leader', 'Home_win': 'local_Home_win', 'Home_lose': 'local_Home_lose', 
    'Away_win': 'local_Away_win', 'Away_lose': 'local_Away_lose', 'Div_win': 'local_Div_win', 'Div_lose': 'local_Div_lose',
    'Cnf_win': 'local_Cnf_win', 'Cnf_lose': 'local_Cnf_lose', 'Icf_win': 'local_Icf_win',
   'Icf_lose': 'local_Icf_lose'}, inplace=True) #LOCAL
    row_com_opp.rename(columns={'Conf_position': 'visitor_Conf_position', 'Win': 'visitor_Win', 'Lose': 'visitor_Lose',
   'Percentagewl': 'visitor_Percentagewl', 'Dif_leader': 'visitor_Dif_leader', 'Home_win': 'visitor_Home_win', 'Home_lose': 'visitor_Home_lose', 
    'Away_win': 'visitor_Away_win', 'Away_lose': 'visitor_Away_lose', 'Div_win': 'visitor_Div_win', 'Div_lose': 'visitor_Div_lose',
    'Cnf_win': 'visitor_Cnf_win', 'Cnf_lose': 'visitor_Cnf_lose', 'Icf_win': 'visitor_Icf_win',
   'Icf_lose': 'visitor_Icf_lose'}, inplace=True)  #VISITANTE



    df_aux = df_row.merge(row_com_team, on='Date', how='left').merge(row_com_opp, on='Date', how='left')
    if(i == 0):
        df_final = df_aux
    df_final = df_final.append(df_aux)
    if i % 10 == 0:
        os.system('cls')
    print(i, "lineas añadidas. Total:", len(Resultados_DF_Local), 100*i/len(Resultados_DF_Local), "%")
    i=i+1

df_final = df_final.drop(['Team', 'Team_y'], axis=1)
df_final.rename(columns={'Team_x': 'local_team', 'Opponent': 'visitor_team'}, inplace = True)

directorio = "partidos_Nuria"

try:
    os.stat(directorio)
except:
    os.mkdir(directorio)
    
os.chdir(directorio)

nombre_fichero='partidos_Nuria_'+str(time.strftime("%d_%m_%y"))+'.csv'
df_final.to_csv(nombre_fichero, header=True, index=False)
os.chdir("..")