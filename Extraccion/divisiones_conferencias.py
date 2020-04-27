import pandas as pd
import os 
import numpy as np

boardsframe_equipos = pd.DataFrame(index=np.arange(1, 31), columns=["Conferencia", "Division", "Equipo"])

boardsframe_equipos.loc[1] = ["Toronto Raptors", "Atlantic Division", "Este"]
boardsframe_equipos.loc[2] = ["Boston Celtics", "Atlantic Division", "Este"]
boardsframe_equipos.loc[3] = ["Philadelphia 76ers", "Atlantic Division", "Este"]
boardsframe_equipos.loc[4] = ["Brooklyn Nets", "Atlantic Division", "Este"]
boardsframe_equipos.loc[5] = ["New York Knicks", "Atlantic Division", "Este"]
boardsframe_equipos.loc[6] = ["Milwaukee Bucks", "Central Division", "Este"]
boardsframe_equipos.loc[7] = ["Indiana Pacers", "Central Division", "Este"]
boardsframe_equipos.loc[8] = ["Chicago Bulls", "Central Division", "Este"]
boardsframe_equipos.loc[9] = ["Detroit Pistons", "Central Division", "Este"]
boardsframe_equipos.loc[10] = ["Cleveland Cavaliers", "Central Division", "Este"]
boardsframe_equipos.loc[11] = ["Miami Heat", "Southeast Division", "Este"]
boardsframe_equipos.loc[12] = ["Orlando Magic", "Southeast Division", "Este"]
boardsframe_equipos.loc[13] = ["Washington Wizards", "Southeast Division", "Este"]
boardsframe_equipos.loc[14] = ["Charlotte Hornets", "Southeast Division", "Este"]
boardsframe_equipos.loc[15] = ["Atlanta Hawks", "Southeast Division", "Este"]
boardsframe_equipos.loc[16] = ["Denver Nuggets", "Northwest Division", "Oeste"]
boardsframe_equipos.loc[17] = ["Utah Jazz", "Northwest Division", "Oeste"]
boardsframe_equipos.loc[18] = ["Oklahoma City Thunder", "Northwest Division", "Oeste"]
boardsframe_equipos.loc[19] = ["Portland Trail Blazers", "Northwest Division", "Oeste"]
boardsframe_equipos.loc[20] = ["Minnesota Timberwolves", "Northwest Division", "Oeste"]
boardsframe_equipos.loc[21] = ["Los Angeles Lakers", "Pacific Division", "Oeste"]
boardsframe_equipos.loc[22] = ["Los Angeles Clippers", "Pacific Division", "Oeste"]
boardsframe_equipos.loc[23] = ["Sacramento Kings", "Pacific Division", "Oeste"]
boardsframe_equipos.loc[24] = ["Phoenix Suns", "Pacific Division", "Oeste"]
boardsframe_equipos.loc[25] = ["Golden State Warriors", "Pacific Division", "Oeste"]
boardsframe_equipos.loc[26] = ["Houston Rockets", "Southwest Division", "Oeste"]
boardsframe_equipos.loc[27] = ["Dallas Mavericks", "Southwest Division", "Oeste"]
boardsframe_equipos.loc[28] = ["Memphis Grizzlies", "Southwest Division", "Oeste"]
boardsframe_equipos.loc[29] = ["New Orleans Pelicans", "Southwest Division", "Oeste"]
boardsframe_equipos.loc[30] = ["San Antonio Spurs", "Southwest Division", "Oeste"]
directorio = "divisiones"

try:
    os.stat(directorio)
except:
    os.mkdir(directorio)
    
os.chdir(directorio)

nombre_fichero='divisiones.csv'
boardsframe_equipos.to_csv(nombre_fichero, header=True, index=False)
os.chdir("..")

#import
#rename del boadframe de divisiones para local
#join
#rename del boadframe de divisiones para visitante
#join
