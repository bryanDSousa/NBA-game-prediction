import os
import pandas as pd 
import numpy as np
import warnings

warnings.filterwarnings(action='ignore')

path='partidos_V3_22_04_20'
names_list = os.listdir(path)
li = []

for name in names_list:
    df = pd.read_csv(path+"/"+name)
    li.append(df)

Resultados_clasificacion = pd.concat(li, axis=0, ignore_index=True)

lista_columnas = [
 "Date", 
 "Year_x", 
 "Season_x", 
 "local_team", 
 "visitor_team", 
 "Points", 
 "Opponent_Points", 
 "Result", 
 "LOCAL_Racha", 
 "boxcore_url", 
 "LOCAL_Ultimos10Victorias", 
 "LOCAL_Ultimos10VDerrotas", 
 "VISITANTE_Ultimos10Victorias", 
 "VISITANTE_Ultimos10VDerrotas", 
 "VISITANTE_Racha", 
 "local_Conf_position", 
 "local_Win", 
 "local_Lose", 
 "local_Percentagewl", 
 "local_Dif_leader", 
 "local_Home_win", 
 "local_Home_lose", 
 "local_Away_win", 
 "local_Away_lose", 
 "local_Div_win", 
 "local_Div_lose", 
 "local_Cnf_win", 
 "local_Cnf_lose", 
 "local_Icf_win", 
 "local_Icf_lose", 
 "visitor_Conf_position", 
 "visitor_Win", 
 "visitor_Lose", 
 "visitor_Percentagewl", 
 "visitor_Dif_leader", 
 "visitor_Home_win", 
 "visitor_Home_lose", 
 "visitor_Away_win", 
 "visitor_Away_lose", 
 "visitor_Div_win", 
 "visitor_Div_lose", 
 "visitor_Cnf_win", 
 "visitor_Cnf_lose", 
 "visitor_Icf_win", 
 "visitor_Icf_lose"
]



Resultados_clasificacion = Resultados_clasificacion[lista_columnas]
Resultados_clasificacion = Resultados_clasificacion.dropna()
Resultados_clasificacion.rename( columns = {
                                "boxcore_url": "ID Partido",
                                "Year_x": "Year", 
                                "Season_x": "Season"},  
                                inplace = True)        

path = "Stats_jugadores_H1_19_04_20"
names_list = os.listdir(path)
li = []

for name in names_list:
    df = pd.read_csv(path+"/"+name)
    li.append(df)
stats_h1 = pd.concat(li, axis=0, ignore_index=True)

lista_columnas = ["ID Partido", 
 "local_fg", 
 "local_fga", 
 "local_fg3", 
 "local_fg3a", 
 "local_ft", 
 "local_fta", 
 "local_orb", 
 "local_drb", 
 "local_trb", 
 "local_ast", 
 "local_stl", 
 "local_blk", 
 "local_tov", 
 "local_pf", 
 "local_pts", 
 "local_ft_pct", 
 "local_fg_pct", 
 "local_fg3_pct", 
 "visitor_fg", 
 "visitor_fga", 
 "visitor_fg3", 
 "visitor_fg3a", 
 "visitor_ft", 
 "visitor_fta", 
 "visitor_orb", 
 "visitor_drb", 
 "visitor_trb", 
 "visitor_ast", 
 "visitor_stl", 
 "visitor_blk", 
 "visitor_tov", 
 "visitor_pf", 
 "visitor_pts", 
 "visitor_ft_pct", 
 "visitor_fg_pct", 
 "visitor_fg3_pct"
]

stats_h1 = stats_h1[lista_columnas]

Resultados_clasificacion_final = Resultados_clasificacion.merge(stats_h1, on = "ID Partido", how = "left")

# Sueldos:
path = "Sueldos"
name = "sueldos_equipo.csv"
sueldos = pd.read_csv(path + "/" + name)
Resultados_clasificacion_final["clave join local"] = Resultados_clasificacion_final["local_team"] +  Resultados_clasificacion_final["Season"].astype(str) 
Resultados_clasificacion_final["clave join visitante"] = Resultados_clasificacion_final["visitor_team"] +  Resultados_clasificacion_final["Season"].astype(str) 

sueldos["clave join"] = sueldos["Equipo"] + sueldos["Temporada"].astype(str) 
sueldos.rename(columns = {"clave join": "clave join local", 
                        "Sueldo": "Sueldo local"}, inplace = True)        

sueldos = sueldos[["clave join local", "Sueldo local"]]

Resultados_clasificacion_final = Resultados_clasificacion_final.merge(sueldos, on ="clave join local", how ="left")

sueldos.rename(columns = {"clave join local": "clave join visitante", 
                        "Sueldo local": "Sueldo visitante"}, inplace = True)        

Resultados_clasificacion_final = Resultados_clasificacion_final.merge(sueldos, on ="clave join visitante", how ="left")

Resultados_clasificacion_final = Resultados_clasificacion_final.drop(['clave join visitante', 'clave join local'], axis=1)

# Conferencias y divisiones
divisiones = pd.DataFrame(index=np.arange(1, 31), columns=["Equipo", "Division", "Conferencia"])

divisiones.loc[1] = ["Toronto Raptors", "Atlantic Division", "Este"]
divisiones.loc[2] = ["Boston Celtics", "Atlantic Division", "Este"]
divisiones.loc[3] = ["Philadelphia 76ers", "Atlantic Division", "Este"]
divisiones.loc[4] = ["Brooklyn Nets", "Atlantic Division", "Este"]
divisiones.loc[5] = ["New York Knicks", "Atlantic Division", "Este"]
divisiones.loc[6] = ["Milwaukee Bucks", "Central Division", "Este"]
divisiones.loc[7] = ["Indiana Pacers", "Central Division", "Este"]
divisiones.loc[8] = ["Chicago Bulls", "Central Division", "Este"]
divisiones.loc[9] = ["Detroit Pistons", "Central Division", "Este"]
divisiones.loc[10] = ["Cleveland Cavaliers", "Central Division", "Este"]
divisiones.loc[11] = ["Miami Heat", "Southeast Division", "Este"]
divisiones.loc[12] = ["Orlando Magic", "Southeast Division", "Este"]
divisiones.loc[13] = ["Washington Wizards", "Southeast Division", "Este"]
divisiones.loc[14] = ["Charlotte Hornets", "Southeast Division", "Este"]
divisiones.loc[15] = ["Atlanta Hawks", "Southeast Division", "Este"]
divisiones.loc[16] = ["Denver Nuggets", "Northwest Division", "Oeste"]
divisiones.loc[17] = ["Utah Jazz", "Northwest Division", "Oeste"]
divisiones.loc[18] = ["Oklahoma City Thunder", "Northwest Division", "Oeste"]
divisiones.loc[19] = ["Portland Trail Blazers", "Northwest Division", "Oeste"]
divisiones.loc[20] = ["Minnesota Timberwolves", "Northwest Division", "Oeste"]
divisiones.loc[21] = ["Los Angeles Lakers", "Pacific Division", "Oeste"]
divisiones.loc[22] = ["Los Angeles Clippers", "Pacific Division", "Oeste"]
divisiones.loc[23] = ["Sacramento Kings", "Pacific Division", "Oeste"]
divisiones.loc[24] = ["Phoenix Suns", "Pacific Division", "Oeste"]
divisiones.loc[25] = ["Golden State Warriors", "Pacific Division", "Oeste"]
divisiones.loc[26] = ["Houston Rockets", "Southwest Division", "Oeste"]
divisiones.loc[27] = ["Dallas Mavericks", "Southwest Division", "Oeste"]
divisiones.loc[28] = ["Memphis Grizzlies", "Southwest Division", "Oeste"]
divisiones.loc[29] = ["New Orleans Pelicans", "Southwest Division", "Oeste"]
divisiones.loc[30] = ["San Antonio Spurs", "Southwest Division", "Oeste"]

divisiones.rename(columns={"Conferencia": "Local_Conferencia", 
                            "Division": "Local_Division",
                            "Equipo": "local_team"},
                            inplace=True)

Resultados_clasificacion_final = Resultados_clasificacion_final.merge(divisiones, on = "local_team", how = "left" )

divisiones.rename(columns={"Local_Conferencia": "Visitor_Conferencia", 
                            "Local_Division": "Visitor_Division", 
                            "local_team": "visitor_team"},
                            inplace=True)

Resultados_clasificacion_final = Resultados_clasificacion_final.merge(divisiones, on = "visitor_team", how = "left" )


# AWS. BUG NULLS EN VISITOR AWS 

jugadores = pd.read_csv('Jugadores/Stats_jugadores_27_04_20.csv')
jugadores = jugadores.dropna()

# Modificamos el formato de algunas variables

jugadores['Year'] = jugadores['Year'].astype(int)
jugadores['Season'] = jugadores['Season'].astype(int)

jugadores['Team Points'] = jugadores['Team Points'].astype(int)
jugadores['Opponent Points'] = jugadores['Opponent Points'].astype(int)
jugadores['Result'] = np.where(jugadores['Team Points'] > jugadores['Opponent Points'], 'W', 'L')

jugadores = jugadores.drop(columns=['Date'])
jugadores['Date']=jugadores['ID Partido'].str.extract(pat='(2\w{7})')


# Dividimos el DF a nivel de temporada para obtener el mejor jugador por equipo en cada una de ellas

jugadoresAWS = jugadores.loc[jugadores['Season'] >= 2016]

jugadoresAWS.rename(columns={'Tiros anotados': 'CCC', 'Tiros intentados': 'CCI', 'Tiros libres anotados': 'C1C',
                                  'Tiros libres intentados': 'C1I', 'Rebotes ofensivos': 'RO', 'Rebotes defensivo': 'RD',
                                  'Asistencias': 'As', 'Robos': 'BR', 'Tapones': 'TF', 'Perdidas': 'BP', 'Faltas': 'FPC', 
                                  'Puntos': 'Pts'}, inplace=True)

jugadoresAWS = jugadoresAWS.loc[:, ['Team', 'Season', 'Date', 'ID Partido', 'Local', 'Opponent', 'Result', 'Name', 
                               'Minutes Played', 'CCC', 'CCI', 'C1C', 'C1I', 'RO', 'RD', 'As', 'BR', 'TF', 'BP', 'FPC', 'Pts']]


# Calculamos el AWS
jugadoresAWS['AWS'] = jugadoresAWS['Pts'] + jugadoresAWS['BR'] + jugadoresAWS['BP'] + \
                           + 0.5 * (jugadoresAWS['As'] + jugadoresAWS['TF'] - jugadoresAWS['FPC']) + \
                           + 0.7 * (jugadoresAWS['RO'] - jugadoresAWS['CCI']) + \
                           + 0.3 * (jugadoresAWS['RD'] - jugadoresAWS['CCC']) - 0.35 * jugadoresAWS['C1I'] - \
                           + 0.15 * jugadoresAWS['C1C']

li = []
seasons = np.arange(2016,2021,1)
namelist = jugadoresAWS['Name'].unique()
for name in namelist:
    for season in seasons:
        df = jugadoresAWS[(jugadoresAWS['Name'] == name) & (jugadoresAWS['Season'] == season)]
        df['AWS_MEDIO'] = df['AWS'].rolling(100, min_periods = 1).mean()
        df = df[["ID Partido", "Local", "AWS_MEDIO"]]
        df['AWS_MEDIO'] = df['AWS_MEDIO'].shift(periods=1, fill_value=0)
        li.append(df)
    
df_1 = pd.concat(li, axis=0, ignore_index=True)
df_1 = df_1.groupby(['ID Partido', 'Local'], as_index = False).agg({"AWS_MEDIO": "mean"})

df_1.rename(columns = {"AWS_MEDIO": "AWS_MEDIO_AGRUPADO"}, inplace = True)

df_1_local = df_1[df_1["Local"] == True]
df_1_local.rename(columns = {"AWS_MEDIO_AGRUPADO": "LOCAL_AWS_MEDIO_AGRUPADO"}, inplace = True)
df_1_local = df_1_local.drop(columns=['Local'])

df_1_visitante = df_1[df_1["Local"] == False]
df_1_visitante.rename(columns = {"AWS_MEDIO_AGRUPADO": "VISITOR_AWS_MEDIO_AGRUPADO"}, inplace = True)
df_1_visitante = df_1_visitante.drop(columns=['Local'])

df_joined = df_1_local.merge(df_1_visitante, on = "ID Partido", how = "left")

Resultados_clasificacion_final = Resultados_clasificacion_final.merge(df_joined, on = "ID Partido", how = "left" )

Resultados_clasificacion_final["local_ft_pct"].fillna(0, inplace=True)
Resultados_clasificacion_final["visitor_ft_pct"].fillna(0, inplace=True)

Resultados_clasificacion_final.to_csv("input.csv", header=True, index=False)
