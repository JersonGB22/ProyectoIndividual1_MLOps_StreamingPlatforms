# Importación de las librerías necesarias
import pandas as pd
from fastapi import FastAPI

# Importación de datos
df_platform=pd.read_csv("https://github.com/JersonGB22/ProyectoIndividualN1/blob/main/Datasets/platform_transformation.csv")
# Instanciamos la clase FastAPI para construir la aplicación de Interfaz de Consultas
app=FastAPI()

@app.get("/")
def bienvenida():
    return "Bienvenid@s a mi Proyecto Individual Nº1: Machine Learning Operations (MLOps)"

# Película con mayor duración según año, plataforma y tipo de duración
@app.get("/max_duration/{year}/{platform}/{duration_type}")
def get_max_duration(year:int, platform:str,duration_type:str):
    df=df_platform.copy()
    df=df[(df.id.str[0]==platform[0])&(df.release_year==year)&(df.duration_type==duration_type)]
    if df.shape[0]>0:
        return df.title[df.duration_int.idxmax()]
    else:
        return "Sin Datos"
