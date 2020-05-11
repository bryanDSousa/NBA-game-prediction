import os
import pandas as pd 
import numpy as np
import warnings

warnings.filterwarnings(action='ignore')

premios = pd.read_csv("Extraccion/Premios_10_05_20/Premios_10_05_20.csv")
AWS =  pd.read_csv("Script_seleccion_jugadores/AWS_TOP30.csv")
WP =  pd.read_csv("Script_seleccion_jugadores/WP_TOP30.csv")
sueldos = pd.read_csv("Extraccion/Sueldos/sueldos_jugadores.csv")
seasons = [2018, 2019]
li = []
for season in seasons:
    df_Premios = premios[(premios["año"] == season) & (premios["award"] == "Most Valuable Player")]
    df_Premios = df_Premios.sort_values(by=['puntos'], ascending = False)
    maximo = len(df_Premios)
    df_Premios = df_Premios.head(maximo)
    df_Premios["Posicion"] = np.arange(1,maximo + 1,1)
    df_Premios = df_Premios[["Posicion", "nombre", "año"]]
    #"nombre": "premios"
    df_Premios.rename(columns = {"nombre": "Premios", "año": "Season"}, inplace = True)

    df_AWS = AWS[AWS["Season"] == season ]
    df_AWS = df_AWS.sort_values(by=['AWS_MEAN'], ascending = False)
    df_AWS = df_AWS.head(maximo)
    df_AWS["Posicion"] = np.arange(1,maximo + 1,1)
    df_AWS = df_AWS[["Posicion", "Name"]]
    #"Name": "AWS"
    df_AWS.rename(columns = {"Name": "AWS"}, inplace = True)

    df_joined = df_Premios.merge(df_AWS, on = "Posicion", how = "left")
    #df_joined['Premios-AWS'] = np.where(df_joined['Premios'] == df_joined['AWS'], True, False)

    df_WP = WP[WP["Season"] == season ]
    df_WP = df_WP.sort_values(by=['WP_MEAN'], ascending = False)
    df_WP = df_WP.head(maximo)
    df_WP["Posicion"] = np.arange(1,maximo + 1,1)
    df_WP = df_WP[["Posicion", "Name"]]
    #"Name": "WP"
    df_WP.rename(columns = {"Name": "WP"}, inplace = True)
    df_joined = df_joined.merge(df_WP, on = "Posicion", how = "left")

    df_Defensivo = premios[(premios["año"] == season) & (premios["award"] == "Defensive Player of the Year")]
    df_Defensivo = df_Defensivo.sort_values(by=['puntos'], ascending = False)
    df_Defensivo = df_Defensivo.head(maximo)
    df_Defensivo["Posicion"] = np.arange(1,len(df_Defensivo) + 1,1)
    df_Defensivo = df_Defensivo[["Posicion", "nombre"]]
    #"nombre": "premios"
    df_Defensivo.rename(columns = {"nombre": "Defensivo"}, inplace = True)

    df_joined = df_joined.merge(df_Defensivo, on = "Posicion", how = "left")

    df_sueldos = sueldos[sueldos["Temporada"] == season]
    df_sueldos = df_sueldos.sort_values(by=['Sueldo'], ascending = False)
    df_sueldos = df_sueldos.head(maximo)
    df_sueldos["Posicion"] = np.arange(1,maximo + 1,1)
    df_sueldos = df_sueldos[["Posicion", "Nombre"]]
    df_sueldos["Nombre"] = df_sueldos["Nombre"].str.split().str[1] + "," + df_sueldos["Nombre"].str.split().str[0]
    df_sueldos.rename(columns = {"Nombre": "Sueldos"}, inplace = True)

    df_joined = df_joined.merge(df_sueldos, on = "Posicion", how = "left")
    aux_AWS = 0
    aux_WP = 0
    i = 0
    for jugador in df_joined["Premios"]:
        i = i + 1
        if(jugador in df_joined["AWS"].tolist()):
            aux_AWS = aux_AWS + 1 
        if(jugador in df_joined["WP"].tolist()):
            aux_WP = aux_WP + 1

    print("AWS", aux_AWS, "aciertos de", maximo, "respecto a premio MVP")
    print("WP", aux_WP, "aciertos de", maximo, "respecto a premio MVP")

    aux_AWS = 0
    aux_WP = 0
    
    for jugador in df_joined["Sueldos"]:
        i = i + 1
        if(jugador in df_joined["AWS"].tolist()):
            aux_AWS = aux_AWS + 1 
        if(jugador in df_joined["WP"].tolist()):
            aux_WP = aux_WP + 1

    print("AWS", aux_AWS, "aciertos de", maximo, "respecto a sueldos")
    print("WP", aux_WP, "aciertos de", maximo, "respecto a sueldos")

    aux_AWS = 0
    aux_WP = 0
    i = 0
    for jugador in df_joined["Defensivo"]:
        i = i + 1
        if(jugador in df_joined["AWS"].tolist()):
            aux_AWS = aux_AWS + 1 
        if(jugador in df_joined["WP"].tolist()):
            aux_WP = aux_WP + 1

    print("AWS", aux_AWS, "aciertos de", maximo, "respecto a premio Defensivo")
    print("WP", aux_WP, "aciertos de", maximo, "respecto a premio Defensivo")

    li.append(df_joined)

df_final = pd.concat(li, axis=0, ignore_index=True)
df_final.to_csv("valoracion_AWS_WP.csv", header=True, index=False)

# Genera un DF con las posiciones, y los jugadores que ocupan cada puesto según las diferentes métricas:
# - AWS
# - WP 
# - Votos para el All Star (premios)
# - Sueldo
# Después itera sobre los jugadores de la lista de premios, si el jugador está en la lista de AWS / WP suma 1 a su score
# Lo mismo para el sueldo. 
# Tengo la sensación de que WP tienen un cierto sesgo hacia los jugadores ofensivos frente a los defensivos (opinión personal)