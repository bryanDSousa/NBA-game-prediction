import os
import pandas as pd 
import numpy as np
import warnings

warnings.filterwarnings(action='ignore')

def list_diff(list1, list2):
    return(list(set(list1) - set(list2)))

premios = pd.read_csv("Extraccion/Premios_10_05_20/Premios_10_05_20.csv")
AWS =  pd.read_csv("Script_seleccion_jugadores/docus15.05/jugadores_AWS_temp.csv")
WP =  pd.read_csv("Script_seleccion_jugadores/docus15.05/jugadores_WP_temp.csv")
WP_adj =  pd.read_csv("Script_seleccion_jugadores/docus15.05/jugadores_WP_adj_temp.csv")

sueldos = pd.read_csv("Extraccion/Sueldos/sueldos_jugadores.csv")
seasons = [2018, 2019]
li = []
for season in seasons:
    df_Premios = premios[(premios["año"] == season) & (premios["award"] == "Most Valuable Player")]
    df_Premios = df_Premios.sort_values(by=['puntos'], ascending = False)
    maximo = len(df_Premios)
    df_Premios = df_Premios.head(maximo)
    df_Premios["Posicion"] = np.arange(1,maximo + 1,1)
    df_Premios = df_Premios[["Posicion", "nombre", "puntos", "primero"]]
    #"nombre": "premios"
    df_Premios.rename(columns = {"nombre": "Premios", "puntos": "puntos_MVP"}, inplace = True)

    df_AWS = AWS[AWS["Season"] == season ]
    df_AWS = df_AWS.sort_values(by=['AWS_temp'], ascending = False)
    df_AWS = df_AWS
    df_AWS["Posicion"] = np.arange(1,len(df_AWS) + 1,1)
    df_AWS = df_AWS[["Posicion", "Name", "AWS_temp"]]
    #"Name": "AWS"
    df_AWS.rename(columns = {"Name": "AWS"}, inplace = True)

    df_joined = df_Premios.merge(df_AWS, on = "Posicion", how = "right")
    #df_joined['Premios-AWS'] = np.where(df_joined['Premios'] == df_joined['AWS'], True, False)

    df_WP = WP[WP["Season"] == season ]
    df_WP = df_WP.sort_values(by=['WP_season'], ascending = False)
    df_WP["Posicion"] = np.arange(1,len(df_WP) + 1,1)
    df_WP = df_WP[["Posicion", "Name", "Season", "WP_season"]]
    #"Name": "WP"
    df_WP.rename(columns = {"Name": "WP"}, inplace = True)
    df_joined = df_joined.merge(df_WP, on = "Posicion", how = "right")

    df_WP_adj = WP_adj[WP["Season"] == season ]
    df_WP_adj = df_WP_adj.sort_values(by=['WP_adj_season'], ascending = False)
    df_WP_adj["Posicion"] = np.arange(1,len(df_WP_adj) + 1,1)
    df_WP_adj = df_WP_adj[["Posicion", "Name", "WP_adj_season"]]
    #"Name": "WP"
    df_WP_adj.rename(columns = {"Name": "WP_adj"}, inplace = True)
    df_joined = df_joined.merge(df_WP_adj, on = "Posicion", how = "right")


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
    df_sueldos = df_sueldos
    df_sueldos["Posicion"] = np.arange(1,len(df_sueldos) + 1,1)
    df_sueldos = df_sueldos[["Posicion", "Nombre"]]
    df_sueldos["Nombre"] = df_sueldos["Nombre"].str.split().str[1] + "," + df_sueldos["Nombre"].str.split().str[0]
    df_sueldos.rename(columns = {"Nombre": "Sueldos"}, inplace = True)

    df_joined = df_joined.merge(df_sueldos, on = "Posicion", how = "left")
    aux_AWS = 0
    aux_WP = 0
    aux_WP_adj = 0
    i = 0
    for jugador in df_joined["Premios"]:
        i = i + 1
        if(jugador in df_joined["AWS"].head(30).tolist()):
            aux_AWS = aux_AWS + 1 
        if(jugador in df_joined["WP"].head(30).tolist()):
            aux_WP = aux_WP + 1 
        if(jugador in df_joined["WP_adj"].head(30).tolist()):
            aux_WP_adj = aux_WP_adj + 1
    print("###########", season ,"###########")
    print("AWS", aux_AWS, "aciertos de", maximo, "respecto a premio MVP")
    print("WP", aux_WP, "aciertos de", maximo, "respecto a premio MVP")
    print("WP_adj", aux_WP_adj, "aciertos")

    aux_AWS = 0
    aux_WP = 0
    
    for jugador in df_joined["Sueldos"]:
        i = i + 1
        if(jugador in df_joined["AWS"].tolist()):
            aux_AWS = aux_AWS + 1 
        if(jugador in df_joined["WP"].tolist()):
            aux_WP = aux_WP + 1

    print("AWS", aux_AWS, "aciertos de", 30, "respecto a sueldos")
    print("WP", aux_WP, "aciertos de", 30, "respecto a sueldos")

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

    print("######## AWS ############")
    print("Votados para el MVP que no aparecen en AWS")
    print("\t", list_diff(df_joined["Premios"].tolist(), df_joined["AWS"].tolist()))
    diff_AWS = list_diff(df_joined["Premios"].tolist(), df_joined["AWS"].tolist())
    puntos_faltantes_primero = 0
    puntos_faltantes = 0
    for jugador in diff_AWS:
        #print(jugador,  int(df_joined[df_joined["Premios"] == jugador]["puntos"]))
        try:
            puntos_faltantes_primero = puntos_faltantes + int(df_joined[df_joined["Premios"] == jugador]["primero"])
            puntos_faltantes = puntos_faltantes + int(df_joined[df_joined["Premios"] == jugador]["Posicion"])
        except:
            puntos_faltantes_primero = puntos_faltantes_primero
            puntos_faltantes = puntos_faltantes
    print("\t", "Puntos faltantes (votado en primer puesto):", puntos_faltantes_primero)
    print("\t", "Puntos faltantes (suma de las posiciones no presentes):", puntos_faltantes)

    print("######## WP ############")
    print("Votados para el MVP que no aparecen en WP")
    print("\t", list_diff(df_joined["Premios"].tolist(), df_joined["WP"].tolist()))
    diff_WP = list_diff(df_joined["Premios"].tolist(), df_joined["WP"].tolist())
    puntos_faltantes_primero = 0
    puntos_faltantes = 0
    for jugador in diff_WP:
        #print(jugador,  int(df_joined[df_joined["Premios"] == jugador]["puntos"]))
        try:
            puntos_faltantes_primero = puntos_faltantes_primero + int(df_joined[df_joined["Premios"] == jugador]["primero"])
            puntos_faltantes = puntos_faltantes + int(df_joined[df_joined["Premios"] == jugador]["Posicion"])
        except:
            puntos_faltantes_primero = puntos_faltantes_primero
            puntos_faltantes = puntos_faltantes
    print("\t", "Puntos faltantes (votado en primer puesto):", puntos_faltantes_primero)
    print("\t", "Puntos faltantes (suma de las posiciones no presentes):", puntos_faltantes)


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
# Tengo la sensación de que WP tienen un cierto sesgo hacia los jugadores ofensivos frente a los defensivos (opinión personal), 
# pero la escogería por dos motivos:
# a) siendo las dos listas que salen buenas, creo que es mejor la de WP 
# b) más allá de la opinión, contempla más datos que el AWS.
