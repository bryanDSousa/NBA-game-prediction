import os
import pandas as pd 
import numpy as np
import warnings

warnings.filterwarnings(action='ignore')

path='partidos_V3_30_04_20'
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
 "LOCAL_Ultimos10Derrotas", 
 "VISITANTE_Ultimos10Victorias", 
 "VISITANTE_Ultimos10Derrotas", 
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
#Resultados_clasificacion = Resultados_clasificacion.dropna()
Resultados_clasificacion.rename( columns = {
                                "boxcore_url": "ID Partido",
                                "Year_x": "Year", 
                                "Season_x": "Season"},  
                                inplace = True)  

#Resultados_clasificacion.to_csv("1.csv", header=True, index=False)
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

#Resultados_clasificacion_final.to_csv("2.csv", header=True, index=False)

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
#Resultados_clasificacion_final.to_csv("partidos_prueba.csv", header=True, index=False)


# AWS.  

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
#sacar campo fecha y ordenar
jugadoresAWS["FechaOrd"] = jugadoresAWS["ID Partido"].str.slice(11, 19)
for season in seasons:
    for name in namelist:
        df = jugadoresAWS[(jugadoresAWS['Name'] == name) & (jugadoresAWS['Season'] == season)]
        df = df.sort_values(by=['FechaOrd'])
        df['AWS_MEDIO'] = df['AWS'].rolling(100, min_periods = 1).mean()
        df = df[["Name", "ID Partido", "Local", "AWS_MEDIO"]]
        df['AWS_MEDIO'] = df['AWS_MEDIO'].shift(periods=1, fill_value=0)
        li.append(df)
    
df_1 = pd.concat(li, axis=0, ignore_index=True)
df_1 = df_1.groupby(['ID Partido', 'Local'], as_index = False).mean()

df_1.rename(columns = {"AWS_MEDIO": "AWS_MEDIO_AGRUPADO"}, inplace = True)

df_1_local = df_1[df_1["Local"] == True]
df_1_local.rename(columns = {"AWS_MEDIO_AGRUPADO": "LOCAL_AWS_MEDIO_AGRUPADO"}, inplace = True)
df_1_local = df_1_local.drop(columns=['Local'])

df_1_visitante = df_1[df_1["Local"] == False]
df_1_visitante.rename(columns = {"AWS_MEDIO_AGRUPADO": "VISITOR_AWS_MEDIO_AGRUPADO"}, inplace = True)
df_1_visitante = df_1_visitante.drop(columns=['Local'])

df_joined = df_1_local.merge(df_1_visitante, on = "ID Partido", how = "left")

#df_joined.to_csv("agrupado_unido.csv", header=True, index=False)

Resultados_clasificacion_final = Resultados_clasificacion_final.merge(df_joined, on = "ID Partido", how = "left" )

#Corrige bug: 
Resultados_clasificacion_final["local_ft_pct"].fillna(0, inplace=True)
Resultados_clasificacion_final["visitor_ft_pct"].fillna(0, inplace=True)

Resultados_clasificacion_final.loc[Resultados_clasificacion_final['Result'] == 0, 'Result'] = "W"
Resultados_clasificacion_final.loc[Resultados_clasificacion_final['Result'] == 1, 'Result'] = "L"
Resultados_clasificacion_final.loc[Resultados_clasificacion_final['Result'] == "W", 'Result'] = 1
Resultados_clasificacion_final.loc[Resultados_clasificacion_final['Result'] == "L", 'Result'] = 0

############### WP 
#TODO REVISAR
partidos = Resultados_clasificacion_final.drop_duplicates()
partidos = partidos.dropna()
# Modificamos el formato de algunas variables 

partidos = partidos.drop(columns=['Date'])
partidos['Date']=partidos['ID Partido'].str.extract(pat='(2\w{7})')

partidos['Year'] = partidos['Year'].astype(int)
partidos['Season'] = partidos['Season'].astype(int)
partidos['Points'] = partidos['Points'].astype(int)
partidos['Opponent_Points'] = partidos['Opponent_Points'].astype(int)
partidos['Result_local'] = np.where(partidos['Points'] > partidos['Opponent_Points'], 'W', 'L')
partidos['Result_visitor'] = np.where(partidos['Points'] < partidos['Opponent_Points'], 'W', 'L')


# Seleccionamos las temporadas a incluir en nuestro modelo

temporada = 2016

partidos = partidos.loc[partidos['Season'] >= temporada]


#### Creamos el DF para la regresión a nivel de equipo ####

# Dividimos el DF en dos para tenerlo a nivel de equipo, es decir, una fila con el dato del local y otra con el visitante

partidos_visitor = partidos.loc[:, ['Date', 'Year', 'Season', 'ID Partido', 'local_team', 'visitor_team', 'Opponent_Points', 
           'Result_visitor', 'visitor_fg', 'visitor_fga', 'visitor_fg_pct', 'visitor_fg3', 'visitor_fg3a','visitor_fg3_pct',
           'visitor_ft', 'visitor_fta', 'visitor_ft_pct', 'visitor_orb', 'visitor_drb', 'visitor_ast', 'visitor_stl', 
           'visitor_blk', 'visitor_tov', 'visitor_pf', 'visitor_pts', 'visitor_Conf_position', 'visitor_Win', 'visitor_Lose', 
           'visitor_Percentagewl', 'visitor_Dif_leader', 'visitor_Home_win', 'visitor_Home_lose', 'visitor_Away_win', 
           'visitor_Away_lose', 'visitor_Div_win', 'visitor_Div_lose', 'visitor_Cnf_win', 'visitor_Cnf_lose', 'visitor_Icf_win',
           'visitor_Icf_lose', 'local_ft', 'local_fg3', 'local_fg', 'local_tov', 'Sueldo visitante', 'Visitor_Division', 
           'Visitor_Conferencia', 'visitor_trb', 'VISITANTE_Ultimos10Victorias', 'VISITANTE_Ultimos10Derrotas', 
           'VISITANTE_Racha', 'VISITOR_AWS_MEDIO_AGRUPADO']]


# Eliminamos los datos del visitante para el DF del local

partidos = partidos.drop(columns=['Opponent_Points', 'Result_visitor', 'Result', 'visitor_fga', 'visitor_fg_pct',
           'visitor_fg3a','visitor_fg3_pct', 'visitor_fta', 'visitor_ft_pct', 'visitor_orb', 'visitor_drb', 
           'visitor_ast', 'visitor_stl', 'visitor_blk', 'visitor_pf', 'visitor_pts', 'visitor_Conf_position',
           'visitor_Win', 'visitor_Lose', 'visitor_trb', 'visitor_Percentagewl', 'visitor_Dif_leader', 'visitor_Home_win',
           'visitor_Home_lose', 'visitor_Away_win','visitor_Away_lose', 'visitor_Div_win', 'visitor_Div_lose','visitor_Cnf_win',
           'visitor_Cnf_lose', 'visitor_Icf_win', 'visitor_Icf_lose', 'Sueldo visitante', 'Visitor_Division',
           'Visitor_Conferencia', 'VISITANTE_Ultimos10Victorias', 'VISITANTE_Ultimos10Derrotas', 'VISITANTE_Racha',
            'VISITOR_AWS_MEDIO_AGRUPADO'])


# Unificamos los nombres de las variables en ambos DF

partidos = partidos.rename(columns=lambda x: x.replace('local_', ''))
partidos = partidos.rename(columns=lambda x: x.replace('LOCAL_', ''))
partidos = partidos.rename(columns=lambda x: x.replace('Local_', ''))

partidos.rename(columns={'Result_local': 'Result', 'team': 'team_PoV', 'visitor_team': 'Opponent_team', 
                         'visitor_ft': 'FTM_opp', 'visitor_fg': 'FG_opp', 'visitor_fg3': '3FGM_opp', 'visitor_tov': 'TO_opp',
                         'Sueldo local': 'Sueldo'}, inplace=True)


partidos_visitor = partidos_visitor.rename(columns=lambda x: x.replace('visitor_', ''))
partidos_visitor = partidos_visitor.rename(columns=lambda x: x.replace('VISITANTE_', ''))
partidos_visitor = partidos_visitor.rename(columns=lambda x: x.replace('Visitor_', ''))
partidos_visitor = partidos_visitor.rename(columns=lambda x: x.replace('VISITOR_', ''))

partidos_visitor.rename(columns={'Result_visitor': 'Result', 'team': 'team_PoV', 'local_team': 'Opponent_team', 
                                 'Opponent_Points': 'Points', 'local_ft': 'FTM_opp', 'local_fg': 'FG_opp', 
                                 'local_fg3': '3FGM_opp', 'local_tov': 'TO_opp', 'Sueldo visitante':'Sueldo'}, inplace=True)


# Unimos ambos DF verticamente 

partidos_union = pd.concat([partidos, partidos_visitor])


# Creamos las variables necesarias para el cálculo

partidos_union['2FGM'] = partidos_union['fg'] - partidos_union['fg3']
partidos_union['FGMS'] = partidos_union['fga'] - partidos_union['fg']
partidos_union['FTMS'] = partidos_union['fta'] - partidos_union['ft']
partidos_union['2FGM_opp'] = partidos_union['FG_opp'] - partidos_union['3FGM_opp']

partidos_union.rename(columns={'fg3': '3FGM', 'ft': 'FTM', 'orb': 'REBO', 'drb': 'REBD', 'tov': 'TO', 'stl': 'STL', 
                                 'blk': 'BLK'}, inplace=True)


# Generamos la variable dummy Win que tomará valor 1 si el equipo ganó el encuentro

partidos_union['Win'] = np.where(partidos_union['Result'] == 'W', 1, 0)


# Creamos un DF con las variables del modelo

partidos_union_reg = partidos_union.loc[:, ['3FGM', '2FGM', 'FTM', 'FGMS', 'FTMS', 'REBO', 'REBD', 'TO', 'STL', 
                                            'FTM_opp', 'BLK', '3FGM_opp', '2FGM_opp', 'TO_opp', 'Win', 'Percentagewl']]

print(partidos_union_reg.head(5))


#### Generamos el modelo de regresión ####

# Creamos las variables X e Y del modelo

x = partidos_union_reg.loc[:, ['3FGM', '2FGM', 'FTM', 'FGMS', 'FTMS', 'REBO', 'REBD', 'TO', 'STL', 
                                            'FTM_opp', 'BLK',  '3FGM_opp', '2FGM_opp', 'TO_opp']]

y = partidos_union_reg.loc[:, ['Percentagewl']]


from statsmodels.api import OLS

model = OLS(y,x).fit()

print('\n',model.summary())

var = pd.DataFrame(dict(zip(x.columns,model.params)),index=[0]).T

jugadores = pd.read_csv('Jugadores/Stats_jugadores_27_04_20.csv')
jugadores = jugadores.dropna()

# Modificamos el formato de algunas variables

# Modificamos el formato de algunas variables

jugadores['Year'] = jugadores['Year'].astype(int)
jugadores['Season'] = jugadores['Season'].astype(int)

jugadores['Team Points'] = jugadores['Team Points'].astype(int)
jugadores['Opponent Points'] = jugadores['Opponent Points'].astype(int)
jugadores['Result'] = np.where(jugadores['Team Points'] > jugadores['Opponent Points'], 'W', 'L')

jugadores = jugadores.drop(columns=['Date'])
jugadores['Date']=jugadores['ID Partido'].str.extract(pat='(2\w{7})')


# Seleccionamos las temporadas a incluir en nuestro modelo

jugadores_WP = jugadores.loc[jugadores['Season'] >= temporada]


# Creamos las variables necesarias para el cálculo

jugadores_WP['2FGM'] = jugadores_WP['Tiros anotados'] - jugadores_WP['Tiros de tres anotados']
jugadores_WP['FGMS'] = jugadores_WP['Tiros intentados'] - jugadores_WP['Tiros anotados']
jugadores_WP['FTMS'] = jugadores_WP['Tiros libres intentados'] - jugadores_WP['Tiros libres anotados']


# Renombramos las variables que vamos a usar para nuestro calculo del AWS

jugadores_WP.rename(columns={'Tiros de tres anotados': '3FGM', 'Tiros libres anotados': 'FTM', 'Rebotes ofensivos': 'REBO',
                                 'Rebotes defensivo': 'REBD', 'Robos': 'STL', 'Tapones': 'BLK', 'Perdidas': 'TO'}, inplace=True)


# Generamos la variable de faltas del total del equipo para obtener el porcentaje de faltas de cada jugador sobre ese total

jugadores_WP_Faltas = jugadores_WP.groupby(['ID Partido', 'Team'], as_index=False).agg({'Faltas':'sum',
                                                                                        'TO':'sum',
                                                                                        'REBD':'sum',
                                                                                        'REBO':'sum',
                                                                                        'BLK':'sum'})
                                                                                       

jugadores_WP_df_jugador = pd.merge(jugadores_WP, jugadores_WP_Faltas, how='left', on=['ID Partido', 'Team'])

jugadores_WP_df_jugador.rename(columns={'Faltas_x': 'Faltas jugador', 'Faltas_y': 'Faltas equipo', 'TO_x': 'TO', 'TO_y': 'TOTM',
                                        'REBD_x': 'REBD', 'REBD_y': 'REBDTM', 'REBO_x': 'REBO', 'REBO_y': 'REBOTM',
                                        'BLK_x': 'BLK', 'BLK_y': 'BLKTM'}, inplace=True)

jugadores_WP_df_jugador['Pct faltas jugador'] = jugadores_WP_df_jugador['Faltas jugador'] / jugadores_WP_df_jugador['Faltas equipo']


# Generamos las variables *_opp con los datos realizados del total del equipo oponente

jugadores_WP_df_opp = jugadores_WP_df_jugador.groupby(['ID Partido', 'Local'], as_index=False).agg({'FTM':'sum',
                                                                                                    '3FGM':'sum',
                                                                                                    '2FGM':'sum',
                                                                                                    'TO':'sum'})

jugadores_WP_df_opp['Local'] = np.where(jugadores_WP_df_opp['Local'] == True, 'False', 'True')

jugadores_WP_df_opp.rename(columns={'FTM': 'FTM_opp_team', '3FGM': '3FGM_opp', '2FGM': '2FGM_opp', 'TO':'TO_opp'}, inplace=True)

jugadores_WP_df_jugador['Local'] = jugadores_WP_df_jugador['Local'].astype(str)

jugadores_WP_df_jugador = pd.merge(jugadores_WP_df_jugador, jugadores_WP_df_opp, how='left', on=['ID Partido', 'Local'])


# Obtenemos el DF final para el cálculo del WP

jugadores_WP_df_jugador['FTM_opp'] = jugadores_WP_df_jugador['Pct faltas jugador'] * jugadores_WP_df_jugador['FTM_opp_team']

jugadores_WP_df_jugador['WP'] = var[0]['3FGM'] * jugadores_WP_df_jugador['3FGM'] + var[0]['2FGM'] * jugadores_WP_df_jugador['2FGM'] + \
                + var[0]['FTM'] * jugadores_WP_df_jugador['FTM'] + var[0]['FGMS'] * jugadores_WP_df_jugador['FGMS'] + \
                + var[0]['FTMS'] * jugadores_WP_df_jugador['FTMS'] + var[0]['REBO'] * jugadores_WP_df_jugador['REBO'] + \
                + var[0]['REBD'] * jugadores_WP_df_jugador['REBD'] + var[0]['TO'] * jugadores_WP_df_jugador['TO'] + \
                + var[0]['STL'] * jugadores_WP_df_jugador['STL'] + var[0]['FTM_opp'] * jugadores_WP_df_jugador['FTM_opp'] + \
                + var[0]['BLK'] * jugadores_WP_df_jugador['BLK']

jugadores_WP_df_jugador['WP_team'] = var[0]['3FGM_opp'] * jugadores_WP_df_jugador['3FGM_opp'] + \
            + var[0]['2FGM_opp'] * jugadores_WP_df_jugador['2FGM_opp'] + var[0]['TO_opp'] * jugadores_WP_df_jugador['TO_opp'] + \
            + var[0]['TO'] * jugadores_WP_df_jugador['TOTM'] + var[0]['REBO'] * jugadores_WP_df_jugador['REBOTM'] + \
            + var[0]['REBD'] * jugadores_WP_df_jugador['REBDTM'] + var[0]['BLK'] * jugadores_WP_df_jugador['BLKTM']

jugadores_WP_df_jugador['WP_adj'] = jugadores_WP_df_jugador['WP'] + jugadores_WP_df_jugador['WP_team']


############### WP MEDIO AGRUPADO 
li = []
seasons = np.arange(2016,2021,1)
namelist = jugadores_WP_df_jugador['Name'].unique()
#sacar campo fecha y ordenar
jugadores_WP_df_jugador["FechaOrd"] = jugadores_WP_df_jugador["ID Partido"].str.slice(11, 19)
#jugadores_WP_df_jugador.to_csv("pruebas.csv", header=True, index=False)

for season in seasons:
    for name in namelist:
        df = jugadores_WP_df_jugador[(jugadores_WP_df_jugador['Name'] == name) & (jugadores_WP_df_jugador['Season'] == int(season))]
        df = df.sort_values(by=['FechaOrd'])
        df['WP_MEDIO'] = df['WP'].rolling(100, min_periods = 1).mean()
        df = df[["Name", "ID Partido", "Local", "WP_MEDIO"]]
        df['WP_MEDIO'] = df['WP_MEDIO'].shift(periods=1, fill_value=0)
        li.append(df)
    
df_1 = pd.concat(li, axis=0, ignore_index=True)
df_1 = df_1.groupby(['ID Partido', 'Local'], as_index = False).mean()

df_1.rename(columns = {"WP_MEDIO": "WP_MEDIO_AGRUPADO"}, inplace = True)

df_1_local = df_1[df_1["Local"] == "True"]
df_1_local.rename(columns = {"WP_MEDIO_AGRUPADO": "LOCAL_WP_MEDIO_AGRUPADO"}, inplace = True)
df_1_local = df_1_local.drop(columns=['Local'])

df_1_visitante = df_1[df_1["Local"] == "False"]
df_1_visitante.rename(columns = {"WP_MEDIO_AGRUPADO": "VISITOR_WP_MEDIO_AGRUPADO"}, inplace = True)
df_1_visitante = df_1_visitante.drop(columns=['Local'])

df_joined = df_1_local.merge(df_1_visitante, on = "ID Partido", how = "left")
#################

Resultados_clasificacion_final = Resultados_clasificacion_final.merge(df_joined, on = "ID Partido", how = "left" )

#Resultados_clasificacion LEER DE NUEVO
path='partidos_V3_30_04_20'
names_list = os.listdir(path)
li = []

for name in names_list:
    df = pd.read_csv(path+"/"+name)
    li.append(df)

Resultados_clasificacion = pd.concat(li, axis=0, ignore_index=True)
Resultados_clasificacion = Resultados_clasificacion.drop(['Season'], axis=1)
Resultados_clasificacion.rename( columns = {
                                "boxcore_url": "ID Partido",
                                "Year_x": "Year", 
                                "Season_x": "Season"},  
                                inplace = True)  
                                
li = []
seasons = np.arange(2016,2021,1)
teamList = Resultados_clasificacion['local_team'].unique()
#sacar campo fecha y ordenar
Resultados_clasificacion["FechaOrd"] = Resultados_clasificacion["ID Partido"].str.slice(11, 19)

variables_local = [
"ID Partido",
"FechaOrd",
"local_team",
"local_fg", 
"local_fga", 
"local_fg_pct", 
"local_fg3", 
"local_fg3a", 
"local_fg3_pct", 
"local_ft", 
"local_fta", 
"local_ft_pct", 
"local_orb", 
"local_drb", 
"local_trn", 
"local_ast", 
"local_stl", 
"local_blk", 
"local_tov", 
"local_pf", 
"local_pts", 
"local_true_shooting_pct", 
"local_effective_fg_pct", 
"local_3pa_rate", 
"local_fta_rate", 
"local_orb_pct", 
"local_drb_pct", 
"local_trb_pct", 
"local_ast_pct", 
"local_stl_pct", 
"local_blk_pct", 
"local_tov_pct", 
"local_off_rate", 
"local_def_rate"]

variables_visitante = [
"ID Partido",
"FechaOrd",
"visitor_team",    
"visitor_fg", 
"visitor_fga", 
"visitor_fg_pct", 
"visitor_fg3", 
"visitor_fg3a", 
"visitor_fg3_pct", 
"visitor_ft", 
"visitor_fta", 
"visitor_ft_pct", 
"visitor_orb", 
"visitor_drb", 
"visitor_trn", 
"visitor_ast", 
"visitor_stl", 
"visitor_blk", 
"visitor_tov", 
"visitor_pf", 
"visitor_pts", 
"visitor_true_shooting_pct", 
"visitor_effective_fg_pct", 
"visitor_3pa_rate", 
"visitor_fta_rate", 
"visitor_orb_pct", 
"visitor_drb_pct", 
"visitor_trb_pct", 
"visitor_ast_pct", 
"visitor_stl_pct", 
"visitor_blk_pct", 
"visitor_tov_pct", 
"visitor_off_rate", 
"visitor_def_rate"]

variables = [
"fg", 
"fga", 
"fg_pct", 
"fg3", 
"fg3a", 
"fg3_pct", 
"ft", 
"fta", 
"ft_pct", 
"orb", 
"drb", 
"trn", 
"ast", 
"stl", 
"blk", 
"tov", 
"pf", 
"pts", 
"true_shooting_pct", 
"effective_fg_pct", 
"3pa_rate", 
"fta_rate", 
"orb_pct", 
"drb_pct", 
"trb_pct", 
"ast_pct", 
"stl_pct", 
"blk_pct", 
"tov_pct", 
"off_rate", 
"def_rate"]

for season in seasons:
    for team in teamList:
        df_local = Resultados_clasificacion[(Resultados_clasificacion['local_team'] == team) & (Resultados_clasificacion['Season'] == int(season))]
        df_local = df_local[variables_local]
        df_local = df_local.rename(columns=lambda x: x.replace('local_', ''))

        #tranformar las variables. 1º quitar las visitor y 2º renombrar sin prefijo local
        df_visitor = Resultados_clasificacion[(Resultados_clasificacion['visitor_team'] == team) & (Resultados_clasificacion['Season'] == int(season))]
        df_visitor = df_visitor[variables_visitante]
        df_visitor = df_visitor.rename(columns=lambda x: x.replace('visitor_', ''))

        #tranformar las variables. 1º quitar las local y 2º renombrar sin prefijo visitor

        df = df_local.append(df_visitor)
        df = df.sort_values(by=['FechaOrd'])
        df = df.drop_duplicates(subset = "ID Partido")
        for variable in variables:
            df[variable+"_MEDIO"] = df[variable].rolling(100, min_periods = 1).mean()
            df[variable+"_MEDIO"] = df[variable].shift(periods=1, fill_value=0)

        li.append(df)
    
df_1 = pd.concat(li, axis=0, ignore_index=True)

#rename con el diccionario de codigo-equipo si codigo en ID partido rename a LOCAL, si no, rename a visitante 
#df['color'] = np.where(df['Set']=='Z', 'green', 'red')
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

df_1['team'] = df_1['team'].map(mapaEquipos)
df_1['Local'] = np.where(df_1['ID Partido'].str.slice(20, 23) == df_1['team'], True, False)

df_1_local = df_1[df_1['Local'] == True]
df_1_local = df_1_local.drop_duplicates()

df_1_visitante = df_1[df_1['Local'] == True]
df_1_visitante = df_1_visitante.drop_duplicates()

columnas = ["ID Partido", 
"fg_MEDIO", 
"fga_MEDIO", 
"fg_pct_MEDIO", 
"fg3_MEDIO", 
"fg3a_MEDIO", 
"fg3_pct_MEDIO", 
"ft_MEDIO", 
"fta_MEDIO", 
"ft_pct_MEDIO", 
"orb_MEDIO", 
"drb_MEDIO", 
"trn_MEDIO", 
"ast_MEDIO", 
"stl_MEDIO", 
"blk_MEDIO", 
"tov_MEDIO", 
"pf_MEDIO", 
"pts_MEDIO", 
"true_shooting_pct_MEDIO", 
"effective_fg_pct_MEDIO", 
"3pa_rate_MEDIO", 
"fta_rate_MEDIO", 
"orb_pct_MEDIO", 
"drb_pct_MEDIO", 
"trb_pct_MEDIO", 
"ast_pct_MEDIO", 
"stl_pct_MEDIO", 
"blk_pct_MEDIO", 
"tov_pct_MEDIO", 
"off_rate_MEDIO", 
"def_rate_MEDIO"
]

df_1_local = df_1_local[columnas]
df_1_visitante = df_1_visitante[columnas]

#RENAME
df_1_local.rename( columns = {"fg_MEDIO": "local_fg_MEDIO",
                            "fga_MEDIO": "local_fga_MEDIO",
                            "fg_pct_MEDIO": "local_fg_pct_MEDIO",
                            "fg3_MEDIO": "local_fg3_MEDIO",
                            "fg3a_MEDIO": "local_fg3a_MEDIO",
                            "fg3_pct_MEDIO": "local_fg3_pct_MEDIO",
                            "ft_MEDIO": "local_ft_MEDIO",
                            "fta_MEDIO": "local_fta_MEDIO",
                            "ft_pct_MEDIO": "local_ft_pct_MEDIO",
                            "orb_MEDIO": "local_orb_MEDIO",
                            "drb_MEDIO": "local_drb_MEDIO",
                            "trn_MEDIO": "local_trn_MEDIO",
                            "ast_MEDIO": "local_ast_MEDIO",
                            "stl_MEDIO": "local_stl_MEDIO",
                            "blk_MEDIO": "local_blk_MEDIO",
                            "tov_MEDIO": "local_tov_MEDIO",
                            "pf_MEDIO": "local_pf_MEDIO",
                            "pts_MEDIO": "local_pts_MEDIO",
                            "true_shooting_pct_MEDIO": "local_true_shooting_pct_MEDIO",
                            "effective_fg_pct_MEDIO": "local_effective_fg_pct_MEDIO",
                            "3pa_rate_MEDIO": "local_3pa_rate_MEDIO",
                            "fta_rate_MEDIO": "local_fta_rate_MEDIO",
                            "orb_pct_MEDIO": "local_orb_pct_MEDIO",
                            "drb_pct_MEDIO": "local_drb_pct_MEDIO",
                            "trb_pct_MEDIO": "local_trb_pct_MEDIO",
                            "ast_pct_MEDIO": "local_ast_pct_MEDIO",
                            "stl_pct_MEDIO": "local_stl_pct_MEDIO",
                            "blk_pct_MEDIO": "local_blk_pct_MEDIO",
                            "tov_pct_MEDIO": "local_tov_pct_MEDIO",
                            "off_rate_MEDIO": "local_off_rate_MEDIO",
                            "def_rate_MEDIO": "local_def_rate_MEDIO"
                            },  
                            inplace = True) 
df_1_visitante.rename( columns = {"fg_MEDIO": "visitor_fg_MEDIO",
                            "fga_MEDIO": "visitor_fga_MEDIO",
                            "fg_pct_MEDIO": "visitor_fg_pct_MEDIO",
                            "fg3_MEDIO": "visitor_fg3_MEDIO",
                            "fg3a_MEDIO": "visitor_fg3a_MEDIO",
                            "fg3_pct_MEDIO": "visitor_fg3_pct_MEDIO",
                            "ft_MEDIO": "visitor_ft_MEDIO",
                            "fta_MEDIO": "visitor_fta_MEDIO",
                            "ft_pct_MEDIO": "visitor_ft_pct_MEDIO",
                            "orb_MEDIO": "visitor_orb_MEDIO",
                            "drb_MEDIO": "visitor_drb_MEDIO",
                            "trn_MEDIO": "visitor_trn_MEDIO",
                            "ast_MEDIO": "visitor_ast_MEDIO",
                            "stl_MEDIO": "visitor_stl_MEDIO",
                            "blk_MEDIO": "visitor_blk_MEDIO",
                            "tov_MEDIO": "visitor_tov_MEDIO",
                            "pf_MEDIO": "visitor_pf_MEDIO",
                            "pts_MEDIO": "visitor_pts_MEDIO",
                            "true_shooting_pct_MEDIO": "visitor_true_shooting_pct_MEDIO",
                            "effective_fg_pct_MEDIO": "visitor_effective_fg_pct_MEDIO",
                            "3pa_rate_MEDIO": "visitor_3pa_rate_MEDIO",
                            "fta_rate_MEDIO": "visitor_fta_rate_MEDIO",
                            "orb_pct_MEDIO": "visitor_orb_pct_MEDIO",
                            "drb_pct_MEDIO": "visitor_drb_pct_MEDIO",
                            "trb_pct_MEDIO": "visitor_trb_pct_MEDIO",
                            "ast_pct_MEDIO": "visitor_ast_pct_MEDIO",
                            "stl_pct_MEDIO": "visitor_stl_pct_MEDIO",
                            "blk_pct_MEDIO": "visitor_blk_pct_MEDIO",
                            "tov_pct_MEDIO": "visitor_tov_pct_MEDIO",
                            "off_rate_MEDIO": "visitor_off_rate_MEDIO",
                            "def_rate_MEDIO": "visitor_def_rate_MEDIO"
                            },  
                            inplace = True) 
#JOIN
df_1_joined = df_1_local.merge(df_1_visitante, on = "ID Partido", how = "left" )

Resultados_clasificacion_final = Resultados_clasificacion_final.merge(df_1_joined, on = "ID Partido", how = "left" )
Resultados_clasificacion_final = Resultados_clasificacion_final.drop_duplicates()

Resultados_clasificacion_final.to_csv("input.csv", header=True, index=False)
