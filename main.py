# Importación de las librerías necesarias
import pandas as pd
from fastapi import FastAPI

# Importación de datos
df_platform=pd.read_csv(r"https://raw.githubusercontent.com/JersonGB22/ProyectoIndividualN1/main/Datasets/platform_transformation.csv")
df_ml=pd.read_csv(r"https://raw.githubusercontent.com/JersonGB22/ProyectoIndividualN1/main/Datasets/movies_ML_API.csv")

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
@app.get("/get_max_duration/{anio}/{plataforma}/{dtype}")
def get_max_duration(anio:int, plataforma:str,dtype:str):
    if plataforma not in ["amazon","disney","hulu","netflix"]:
        return {"Nombre de plataforma incorrecta. Datos correctos":["amazon","disney","hulu","netflix"]}
    else:
        df=df_platform[df_platform.id.str[0]==plataforma[0]]
        if anio not in df.release_year.to_list():
            return {"Año de estreno inválido. Rango correcto":f"[{df.release_year.min()};{df.release_year.max()}]"}
        else:
            if dtype not in ["min","season"]:
                return {"Tipo de duración inválido. Datos correctos":["min","season"]}
            else:
                df=df[(df.type=="movie")&~(df.listed_in.str.contains("documentar"))&(df.release_year==anio)&(df.duration_type==dtype)]
                if df.shape[0]>0:
                    return {"pelicula":df.title[df.duration_int.idxmax()]}
                else:
                     return "Sin Datos"
                
# Función 2: Cantidad de películas (solo películas) por plataforma con un puntaje mayor a XX en determinado año
@app.get("/get_score_count/{plataforma}/{scored}/{anio}")
def get_score_count(plataforma:str,scored:float,anio:int):
    if plataforma not in ["amazon","disney","hulu","netflix"]:
        return {"Nombre de plataforma incorrecta. Datos correctos":["amazon","disney","hulu","netflix"]}
    else:
        df=df_platform[df_platform.id.str[0]==plataforma[0]]
        if anio not in df.release_year.to_list():
            return {"Año de estreno inválido. Rango correcto":f"[{df.release_year.min()};{df.release_year.max()}]"}
        else:
            df=df[(df.type=="movie")&~(df.listed_in.str.contains("documentar"))&(df.score>scored)&(df.release_year==anio)]
            if df.shape[0]>0:
                return {"plataforma":plataforma,"cantidad":df.shape[0],"anio":anio,"score":scored}
            else:
                return "Sin Datos"

# Función 3: Cantidad de películas (sólo películas) según plataforma
@app.get("/get_count_platform/{plataforma}")
def get_count_platform(plataforma:str):
    if plataforma not in ["amazon","disney","hulu","netflix"]:
        return {"Nombre de plataforma incorrecta. Datos correctos":["amazon","disney","hulu","netflix"]}
    else:
        df=df_platform[(df_platform.id.str[0]==plataforma[0])&(df_platform.type=="movie")&~(df_platform.listed_in.str.contains("documentar"))]
        return {"plataforma":plataforma,"peliculas":df.shape[0]}

# Función 4: Actor que más se repite según plataforma y año
# En este caso se devolverá una lista de actores, ya que puede darse el caso de múltiples empates
@app.get("/get_actor/{plataforma}/{anio}")
def get_actor(plataforma:str,anio:int):
    if plataforma not in ["amazon","disney","hulu","netflix"]:
        return {"Nombre de plataforma incorrecta. Datos correctos":["amazon","disney","hulu","netflix"]}
    else:
        df=df_platform[df_platform.id.str[0]==plataforma[0]]
        if anio not in df.release_year.to_list():
            return {"Año de estreno inválido. Rango correcto":f"[{df.release_year.min()};{df.release_year.max()}]"}
        else:
            df=df[df.release_year==anio].dropna(subset="cast")
            if df.shape[0]>0:
                se=df.cast.str.split(", ").explode().value_counts()
                df_actor=se[se==se.max()].reset_index()
                return {"plataforma":plataforma,"anio":anio,"actor":df_actor["index"].to_list(),"apariciones":df_actor["cast"].to_list()[0]}
            else:
                return "Sin Datos"

#Función 5: Cantidad de contenidos/productos (todo lo disponible en streaming) que se publicó por país y año
# Observación: existen varios contenidos que se realizaron en más de un país, por lo que estos también se considerarán en su conteo
@app.get("/prod_per_county/{tipo}/{pais}/{anio}")
def prod_per_county(tipo:str,pais:str,anio:int):
    if tipo not in ["pelicula","serie","documental"]:
        return {"Tipo de contenido inválido. Datos correctos":["pelicula","serie","documental"]}
    else:
        if tipo=="pelicula":
            df=df_platform[(df_platform.type=="movie")&~(df_platform.listed_in.str.contains("documentar"))]
        elif tipo=="serie":
            df=df_platform[(df_platform.type=="tv show")&~(df_platform.listed_in.str.contains("documentar"))]
        else:
            df=df_platform[df_platform.listed_in.str.contains("documentar")]
        if pais not in df[df.country.notnull()].country.unique():
            return {"Nombre de país inválido. Datos de ejemplo correctos":list(df[df.country.notnull()].country.unique())[:10]}
        else:
            if anio not in df.release_year.to_list():
                return {"Año de estreno inválido. Rango correcto":f"[{df.release_year.min()};{df.release_year.max()}]"}
            else:
                df=df[(df.country.str.contains(pais,na=False))&(df.release_year==anio)]
                s="(es)" if tipo=="documental" else "(s)"
                return {"pais":pais,"anio":anio,"peliculas":f"{df.shape[0]} {tipo}{s}"}

# Función 6: Cantidad total de contenidos/productos (todo lo disponible en streaming) según el rating de audiencia
@app.get("/get_contents/{rating}")
def get_contents(rating:str):
    if rating not in df_platform.rating.unique():
        return {"Rating de audiencia incorrecto. Datos correctos":list(df_platform.rating.unique())}
    else:
        return {"rating":rating,"contenido":df_platform[df_platform.rating==rating].shape[0]}

# Función 7: 5 películas con mayor puntaje (más similares) a una específica en orden descendente
@app.get("/get_recomendation/{title}")
def get_recommendation(title: str):
    if title not in df_ml.title.tolist():
        return {"Nombre de la película incorrecto. Datos de ejemplos correctos":list(df_ml.title)[:10]}
    else:
        indices=eval(df_ml[df_ml.title==title].index_movie.iloc[0])
        return {"recomendacion":list(df_ml.title.iloc[indices].values)}