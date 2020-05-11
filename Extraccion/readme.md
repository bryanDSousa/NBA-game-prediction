# Extracción de datos:  

La extracción de los datos se lleva a cabo realizando scrapping a distintos endpoints mediante Python empleando las librerías `request`, para realizar las peticiones y `Pandas` para recopilar la información en DataFrames, principalmente. El proceso se basa en descomponer mediante la función "Split" la respuesta del endpoint para recopilar la información útil y desechar el resto, también se llevan a cabo en estos procesos unas transformaciones mínimas en los datos y uniones de DataFrames cuando es necesario, para dar lugar a ficheros csv que contengan la información que necesitamos para el análisis. 
Mayoritariamente extraemos la información de www.basketballreference.com. También consumimos información de data.nba.net, de www.shrpsports.com y www.geodatos.net.    

## Extractores: 

**1.	StatsJugadoresV2.py:**  
Extrae la información para cada jugador de sus estadísticas en cada partido desde 2010 a 2020. Se realiza una llamada para obtener el calendario del equipo, que nos devuelve las URL del boxscore de cada partido. Iterativamente realizamos dichas llamadas y recogemos los siguientes datos:

      * MP: Minutos jugados
      * FG: Tiros de campos anotados
      * FGA: Tiros de campo intentados
      * FG%: Porcentaje de tiros de campo
      * 3P: Triples anotados
      * 3PA: Triples intentados
      * 3P%: Porcentaje de triples
      * FT: Tiros libres anotados
      * FTA: Tiros libres intentados
      * FT%: Porcentaje de tiros libres
      * ORB: Rebotes ofensivos
      * DRB: Rebotes defensivos
      * TRB: Rebotes totales
      * AST: Asistencias
      * STL: Recuperaciones
      * BLK: Tapones
      * TOV: Pérdidas
      * PF: Faltas personales
      * PTS: Puntos
      * +/-: Más menos (marcador parcial con el jugador en pista)
      * TS% -- True Shooting Percentage
      * eFG% -- Effective Field Goal Percentage
      * 3PAr -- 3-Point Attempt Rate
      * FTr -- Free Throw Attempt Rate
      * ORB% -- Offensive Rebound Percentage
      * DRB% -- Defensive Rebound Percentage
      * TRB% -- Total Rebound Percentage
      * AST% -- Assist Percentage
      * STL% -- Steal Percentage
      * BLK% -- Block Percentage
      * TOV% -- Turnover Percentage
      * USG% -- Usage Percentage
      * ORtg -- Offensive Rating
      * DRtg -- Defensive Rating
      * BPM -- Box Plus/Minus

**2.	StatsJugadoresV2_h1.py:**  
Extrae la información para cada jugador de sus estadísticas al descanso en cada partido desde 2010 a 2020. Se realiza una llamada para obtener el calendario del equipo, que nos devuelve las URL del boxscore de cada partido. En el mismo python se agrupa por partido y equipo para dar lugar a un DF en el formato requerido por el modelo. Iterativamente realizamos las llamadas a basketball-reference y recogemos los siguientes datos:

      * FG: Tiros de campos anotados
      * FGA: Tiros de campo intentados
      * FG%: Porcentaje de tiros de campo
      * 3P: Triples anotados
      * 3PA: Triples intentados
      * 3P%: Porcentaje de triples
      * FT: Tiros libres anotados
      * FTA: Tiros libres intentados
      * FT%: Porcentaje de tiros libres
      * ORB: Rebotes ofensivos
      * DRB: Rebotes defensivos
      * TRB: Rebotes totales
      * AST: Asistencias
      * STL: Recuperaciones
      * BLK: Tapones
      * TOV: Pérdidas
      * PF: Faltas personales
      * PTS: Puntos

**3.	ResultadosClasificacionV2.py:**  
Realiza una serie de llamadas a www.shrpsports.com para obtener la clasificación en todas las fechas posibles desde octubre de 2009 a abril de 2020, cada fila recoge los datos referentes a la clasificación de un equipo en una fecha. Los campos obtenidos son: 

    * Fecha (mes y día)
    * Año
    * Temporada
    * Equipo 
    * Posición de conferencia
    * Victorias
    * Derrotas
    * Porcentaje victorias / derrotas
    * Diferencia con el líder de conferencia
    * Victorias como local
    * Derrotas como Local
    * Victorias intra-división 
    * Derrotas intra-división 
    * Victorias intra-conferencia 
    * Derrotas intra-conferencia
    * Victorias inter-conferencia 
    * Derrotas inter-conferencia

    Realizamos a su vez las mismas llamadas que realizamos en StatsJugadoresV2.py para obtener los mismos datos que obtenemos en ese extractor a nivel de equipo, tanto visitante como local, además de otras como resultado y un flag de Local (True/False). Después declaramos un diccionario que mapee la nomenclatura de shrpsports.com y la de basketball-reference.com para poder unir los DataFrames. Lo haremos realizando un join de la clasificación para el equipo visitante y otro para el local, después de haber filtrado convenientemente los datos para poder realizar esta unión. El DF resultante tiene todos los datos que hemos mencionado tanto para el equipo visitante como para el equipo local.   

        Nota: La unión mencionada se realiza de dos formas distintas, una para generar un fichero con los datos de la clasificación de los equipos antes del partido y otra para obtener los datos de la clasificación después del mismo. 

**4.	DNP.py:**  
Recoge los jugadores que no jugaron en el cada partido. Se realizan llamadas para obtener el calendario y después llamadas para obtener el boxscore de cada partido. Se recoge el nombre y el equipo del jugador que no jugó, así como el ID de partido. Esta información servirá para crear una variable true/false en el DataFrame que usemos como entrada del modelo de predicción que indique si el jugador estrella participó en el encuentro. 

 **5. Premios.py:**   
Recoge los jugadores que han recibido votos para recibir el premio MVP (premio a mejor jugador del año) desde 2010 hasta 2020. Se registra el nombre del jugador, el número de votos en primera posición, los puntos obtenidos, los puntos máximos y el share de éstos. Esta información nos servirá para actuar como contraste al análisis de las estadísticas individuales.  

**6.	Distancias.py:**   
Mediante llamadas a www.geodatos.net obtenemos las distancias entre las ciudades de todos los equipos que componen la NBA. Realizamos las llamadas iterando sobre la misma lista de equipos (que se relacionan con la ciudad mediante un diccionario) dos veces, bajo la condición de que el equipo no sea el mismo. Obtenemos así la distancia de Equipo A a Equipo B en kilómetros. Del mismo modo que en el extractor **DNP.py**, nos servirá como una variable más para el modelo de predicción, como distancia recorrida por el equipo visitante.  

**7.	Evolucion.py:**  
Obtendrá estadísticas totales de cada equipo en cada temporada para realizar un análisis sobre la evolución en el baloncesto NBA desde 1990 hasta 2020. La fuente de estos datos es www.basketball-reference.com. 

    * FG: Tiros de campos anotados
    * FGA: Tiros de campo intentados
    * FG%: Porcentaje de tiros de campo
    * 3P: Triples anotados
    * 3PA: Triples intentados
    * 3P%: Porcentaje de triples
    * FT: Tiros libres anotados
    * FTA: Tiros libres intentados
    * FT%: Porcentaje de tiros libres
    * ORB: Rebotes ofensivos
    * DRB: Rebotes defensivos
    * TRB: Rebotes totales
    * AST: Asistencias
    * STL: Recuperaciones
    * BLK: Tapones
    * TOV: Pérdidas
    * PF: Faltas personales
    * PTS: Puntos

# Generación del fichero de entrada:

Una vez extraida la información necesaria el objetivo es generar un fichero que sirva de input al modelo predictivo aunando toda esta información. 

El fichero final queremos que contenga la siguiente información:  

| Información | Extractor |
| -- | -- |
| Clasificación antes del partido (posición, rachas, etc.) | ResultadosClasificacionV2.py |
| Estadisticas al descanso | StatsJugadoresV2_h1.py |
| Suma de los sueldos del equipo | sueldos.py |
| AWS |  StatsJugadoresV2.py |
| WP  | StatsJugadoresV2.py y ResultadosClasificacionV2.py |
| Divisiones y conferencias | - |


En este paso aprovecharemos para eliminar toda la información duplicada o innecesaria y para adaptar toda la información al formato local / visitante. 

Además de los campos obtenidos directamente de la web se realizan transformaciones para obtener los siguientes:

* **Ultimos10Victorias**: las victorias conseguidas en los últimos diez partidos * jugados (se realiza un rolling sum y join para el equipo local y visitante)
* **Ultimos10Derrotas**: las derrotas conseguidas en los últimos diez partidos  jugados (se realiza un rolling sum y join para el equipo local y visitante)
* **Sueldo**: La suma del sueldo del equipo en la temporada (agrupación por equipo y temporada, y join para el equipo local y visitante)
* **Division**: división a la que eprtenece el equipo (join para el equipo local y visitante))
* **Conferencia**: conferencia a la que pertenece el equipo (join para el equipo local y visitante))  

* **AWS_MEDIO_AGRUPADO**: La medida AWS será explicada más adelante, una vez calculada para cada jugador, hacemos un rolling mean y un shift, para obtener la media hasta antes del partido del jugador en la temporada, posteriormente se agrupan por equipo y se realiza el join, obteniendo una valoración conjunta de los jugadores que participan en el encuentro por equipo. 
* **WP_MEDIO_AGRUPADO**: Se trata de una medida análoga al AWS 

De este modo el fichero de entrada al modelo contiene una gran cantidad de información, mucho más rica que la tabla de estadísticas en la que se recogen habitualmente los desempeños a nivel individual y colectivo de cada partido. El fichero que generamos incluye gran variedad de fuentes y campos obtenidos a través de operativas complejas.  

