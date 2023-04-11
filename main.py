# Importación de las librerías necesarias
import pandas as pd
from fastapi import FastAPI

# Importación de datos
df_platform=pd.read_csv(r"https://raw.githubusercontent.com/JersonGB22/ProyectoIndividualN1/main/Datasets/platform_transformation.csv")
# Instanciamos la clase FastAPI para construir la aplicación de Interfaz de Consultas
app=FastAPI()

# Creación del endpoint de bienvenida
@app.get("/")
def bienvenida():
    return "Bienvenid@s a mi Proyecto Individual Nº1: Machine Learning Operations (MLOps)"

# Creación de los endpoints
"""
Observaciones:
- En relación a la identificación de los tipos de contenidos visuales en las plataformas de Streaming, se debe mencionar que existen 
  una gran variedad de tipos y que en los datasets no se encuentra un campo que los mencione explícitamente. Por lo tanto, se han 
  establecido únicamente 3 tipos: películas, series y documentales. Para determinar estos tipos, se utilizarán los campos "type" y 
  "listed_in", ambos sin valores nulos. El campo "type" cuenta con dos valores: "movie" y "tv show", que corresponden a películas y
  series respectivamente. No obstante, para identificar el tercer tipo, documentales, se verificará si el campo "listed_in" contiene 
  el string "documentar" (singular: documentary, plural: documentaries). De esta manera se obtendrán los 3 tipos de contenido.

- El tipo de contenido "película" solo puede tener como "duration_type"="min", ya que las películas según el data frame y de manera general
  no pueden tener "season", pero de todas maneras se considerará el argumento duration_type de la función 1.
"""

# Función 1: Película (solo película) con mayor duración según año, plataforma y tipo de duración
@app.get("/max_duration/{year}/{platform}/{duration_type}")
def get_max_duration(year:int, platform:str,duration_type:str):
    if platform not in ["amazon","disney","hulu","netflix"]:
        return "Nombre de plataforma incorrecta. Datos correctos: amazon,disney,hulu,netflix"
    else:
        df=df_platform[df_platform.id.str[0]==platform[0]]
        if year not in df.release_year.to_list():
            return f"Año de estreno inválido. Rango correcto: [{df.release_year.min()};{df.release_year.max()}]"
        else:
            if duration_type not in ["min","season"]:
                return "Tipo de duración inválido. Datos correctos: min,season"
            else:
                df=df[(df.type=="movie")&~(df.listed_in.str.contains("documentar"))&(df.release_year==year)&(df.duration_type==duration_type)]
                if df.shape[0]>0:
                    return df.title[df.duration_int.idxmax()]
                else:
                     return "Sin Datos"

# Función 2: Cantidad de películas (solo películas) por plataforma con un puntaje mayor a XX en determinado año
@app.get("/score_count/{platform}/{scored}/{year}")
def get_score_count(platform:str,scored:float,year:int):
    if platform not in ["amazon","disney","hulu","netflix"]:
        return "Nombre de plataforma incorrecta. Datos correctos: amazon,disney,hulu,netflix"
    else:
        df=df_platform[df_platform.id.str[0]==platform[0]]
        if year not in df.release_year.to_list():
            return f"Año de estreno inválido. Rango correcto: [{df.release_year.min()};{df.release_year.max()}]"
        else:
            df=df[(df.type=="movie")&~(df.listed_in.str.contains("documentar"))&(df.score>scored)&(df.release_year==year)]
            if df.shape[0]>0:
                return df.shape[0]
            else:
                return "Sin Datos"

# Función 3: Cantidad de películas (sólo películas) según plataforma
@app.get("/count_platform/{platform}")
def get_count_platform(platform:str):
    if platform not in ["amazon","disney","hulu","netflix"]:
        return "Nombre de plataforma incorrecta. Datos correctos: amazon,disney,hulu,netflix"
    else:
        df=df_platform[(df_platform.id.str[0]==platform[0])&(df_platform.type=="movie")&~(df_platform.listed_in.str.contains("documentar"))]
        return df.shape[0]

# Función 4: Actor que más se repite según plataforma y año
# En este caso se devolverá una lista de actores, ya que puede darse el caso de múltiples empates
@app.get("/actor/{platform}/{year}")
def get_actor(platform:str,year:int):
    if platform not in ["amazon","disney","hulu","netflix"]:
        return "Nombre de plataforma incorrecta. Datos correctos: amazon,disney,hulu,netflix"
    else:
        df=df_platform[df_platform.id.str[0]==platform[0]]
        if year not in df.release_year.to_list():
            return f"Año de estreno inválido. Rango correcto: [{df.release_year.min()};{df.release_year.max()}]"
        else:
            df=df[df.release_year==year].dropna(subset="cast")
            if df.shape[0]>0:
                se=df.cast.str.split(", ").explode().value_counts()
                df_actor=se[se==se.max()].reset_index()
                return df_actor["index"].str.title().to_list()
            else:
                return "Sin Datos"

#Función 5: Cantidad de contenidos/productos (todo lo disponible en streaming) que se publicó por país y año
# Observación: existen varios contenidos que se realizaron en más de un país, por lo que estos también se considerarán en su conteo
@app.get("/count_county/{tipo}/{pais}/{anio}")
def prod_per_county(tipo:str,pais:str,anio:int):
    if tipo not in ["pelicula","serie","documental"]:
        return "Tipo de contenido inválido. Datos correctos: ",["pelicula","serie","documental"]
    else:
        if tipo=="pelicula":
            df=df_platform[(df_platform.type=="movie")&~(df_platform.listed_in.str.contains("documentar"))]
        elif tipo=="serie":
            df=df_platform[(df_platform.type=="tv show")&~(df_platform.listed_in.str.contains("documentar"))]
        else:
            df=df_platform[df_platform.listed_in.str.contains("documentar")]
        if pais not in df[df.country.notnull()].country.unique():
            return "Nombre de país inválido. Datos de ejemplo correctos",list(df[df.country.notnull()].country.unique())[:10]
        else:
            if anio not in df.release_year.to_list():
                return f"Año de estreno inválido. Rango correcto: [{df.release_year.min()};{df.release_year.max()}]"
            else:
                df=df[(df.country.str.contains(pais,na=False))&(df.release_year==anio)]
                return {"Tipo de contenido":tipo,"País":pais,"Año":anio,"Cantidad de publicaciones":df.shape[0]}

# Función 6: 
@app.get("/rating/{rating}")
def get_contents(rating:str):
    pass
