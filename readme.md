<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

# <h1 align=center> **PROYECTO INDIVIDUAL N°1: Machine Learning Operations (MLOps)** </h1>

<p align="center">
  <img src="https://user-images.githubusercontent.com/67664604/217914153-1eb00e25-ac08-4dfa-aaf8-53c09038f082.png" height="300" width="auto" style="max-width: 50%;" />
  <img src="ConsignasProyecto/src/image_platforms.jpg" height="300" width="auto" style="max-width: 50%;" />
</p>
<center>

*Bienvenid@s a la presentación de mi primer proyecto de la carrera de Data Science, el cual fue realizado durante la etapa de Labs del bootcamp [Henry](https://www.soyhenry.com/carrera-data-science)*

</center>

# **Descripción**:

Este proyecto individual tiene como objetivo simular el papel de `Data Scientist` en una startup que se dedica a la agregación de plataformas de streaming. El objetivo es desarrollar consultas de películas y un sistema de recomendación basado en `Machine Learning` que, hasta ahora, no ha podido ser implementado debido a la falta de madurez en los datos. Para llevar a cabo este proyecto, se necesitará realizar tareas de `Data Engineer` para la recolección y tratamiento de los datos, así como el entrenamiento del modelo de Machine Learning y finalmente, implementarlo en el mundo real con la metodología de `DevOps`.

***Se recomienda encarecidamente al lector revisar los notebooks y el script asociados en los enlaces proporcionados en las etapas del proyecto. Estos archivos contienen explicaciones exhaustivas y comentarios detallados que describen cada paso de la realización del proyecto.***

# **Etapa I: Transformaciones**
**Consignas:**  

+ Generar campo **`id`**: Cada id se compondrá de la primera letra del nombre de la plataforma, seguido del show_id ya presente en los datasets (ejemplo para títulos de Amazon = **`as123`**)
+ Los valores nulos del campo rating deberán reemplazarse por el string “**`G`**” (corresponde al maturity rating: “general for all audiences”
+ De haber fechas, deberán tener el formato **`AAAA-mm-dd`**
+ Los campos de texto deberán estar en **minúsculas**, sin excepciones
+ El campo ***duration*** debe convertirse en dos campos: **`duration_int`** y **`duration_type`**. El primero será un integer y el segundo un string indicando la unidad de medición de duración: min (minutos) o season (temporadas).

**Resolución de la consignas:**

Las transformaciones requeridas por las [especificaciones del proyecto](https://github.com/JersonGB22/ProyectoIndividualN1/blob/main/ConsignasProyecto/ConsignaReadme.md) corresponden a la fase de ETL (Extract, Transform and Load), que se llevó a cabo en un archivo Jupyter Notebook llamado [transformaciones.ipynb](https://github.com/JersonGB22/ProyectoIndividualN1/blob/main/transformaciones.ipynb), utilizando los archivos CSV presentes en la carpeta [Datasets](https://github.com/JersonGB22/ProyectoIndividualN1/tree/main/Datasets). Durante esta fase, también se calculó el puntaje promedio de los usuarios para cada película y se imputaron la mayoría de valores faltantes en los campos `duration_int` y `duration_type` utilizando la columna `rating`. Además, se realizó un tratamiento adicional en la variable rating y se realizó una reagrupación. Se emplearon las librerías Pandas y NumPy. Finalmente, el dataframe resultante se exportó a un [archivo CSV](https://raw.githubusercontent.com/JersonGB22/ProyectoIndividualN1/main/Datasets/platform_transformation.csv) alojado en la carpeta Datasets para ser utilizado en la etapa de implementación de los endpoints que se consumirán en la API.

# **Etapa II: Desarrollo API**
**Consignas:** 
Creas 6 funciones para disponibilizar los datos de la empresa usando el framework ***FastAPI***
+ Película (sólo película, no serie, ni documentales, etc) con mayor duración según año, plataforma y tipo de duración. La función debe llamarse get_max_duration(year, platform, duration_type) y debe devolver sólo el string del nombre de la película.
+ Cantidad de películas (sólo películas, no series, ni documentales, etc) según plataforma, con un puntaje mayor a XX en determinado año. La función debe llamarse get_score_count(platform, scored, year) y debe devolver un int, con el total de películas que cumplen lo solicitado.
+ Cantidad de películas (sólo películas, no series, ni documentales, etc) según plataforma. La función debe llamarse get_count_platform(platform) y debe devolver un int, con el número total de películas de esa plataforma. Las plataformas deben llamarse amazon, netflix, hulu, disney.
+ Actor que más se repite según plataforma y año. La función debe llamarse get_actor(platform, year) y debe devolver sólo el string con el nombre del actor que más se repite según la plataforma y el año dado.
+ La cantidad de contenidos/productos (todo lo disponible en streaming) que se publicó por país y año. La función debe llamarse prod_per_county(tipo,pais,anio) deberia devolver el tipo de contenido (pelicula,serie,documental) por pais y año en un diccionario con las variables llamadas 'pais' (nombre del pais), 'anio' (año), 'pelicula' (tipo de contenido).
+ La cantidad total de contenidos/productos (todo lo disponible en streaming, series, documentales, peliculas, etc) según el rating de audiencia dado (para que publico fue clasificada la pelicula). La función debe llamarse get_contents(rating) y debe devolver el numero total de contenido con ese rating de audiencias.

**Resolución de la consignas:**

En esta etapa del proyecto, hemos creado los seis endpoints que se nos han asignado mediante el uso de las librerías pandas y FastAPI en el archivo [main.py](https://github.com/JersonGB22/ProyectoIndividualN1/blob/main/main.py). Además, hemos incluido algunas observaciones importantes que es necesario tomar en cuenta. En cada función, se han considerado los casos en los que los argumentos no están presentes en el dataframe establecido, y se han proporcionado instrucciones sobre qué argumentos deben ser ingresados. En los casos en que la función no devuelva nada debido a los filtros aplicados, el dataframe respectivo se retornará con la cadena de texto "Sin Datos" para evitar errores y mejorar la visualización de las funciones.

# **Etapa III: Análisis Exploratorio de los Datos (EDA)**

**Consigna:**
Ya los datos están limpios, ahora es tiempo de investigar las relaciones que hay entre las variables de los datasets, ver si hay outliers o anomalías (que no tienen que ser errores necesariamente :eyes: ), y ver si hay algún patrón interesante que valga la pena explorar en un análisis posterior.  Sabes que puedes apoyarte en librerías como _pandas profiling, sweetviz, autoviz_, entre otros y sacar de allí tus conclusiones

**Resolución de la consigna:**

En la primera etapa del proyecto, se generó un dataset denominado `platform_transformation`. En base a este archivo en esta etapa se realizó un [EDA inicial](https://huknt1mctoiumyo41mctaq.on.drv.tw/ArchivosHTML/ReportEDA_PlatformStreaming.html), se utilizó la librería ydata-profiling (antes llamada pandas-profiling). Posteriormente, se llevó a cabo un EDA más detallado, se detectaron outliers, se analizaron las distribuciones de las variables numéricas y se revisaron las frecuencias de las variables categóricas mediante el uso de las librerías matplotlib y seaborn. Adicionalmente, se realizaron transformaciones necesarias para el sistema de recomendación basado en contenido, como la eliminación de columnas innecesarias, la imputación de valores faltantes y el preprocesamiento de texto, el cual es una tarea de procesamiento del lenguaje natural (NLP) que se llevó a cabo con las librerías regex y nltk. Finalmente, se exportó el dataframe generado en un archivo CSV denominado [movies_transformation_ML](https://raw.githubusercontent.com/JersonGB22/ProyectoIndividualN1/main/Datasets/movies_transformation_ML.csv), el cual se utilizará en la etapa de Machine Learning.

En el archivo correspondiente a esta etapa [EDA&ETL(ML).ipynb](https://github.com/JersonGB22/ProyectoIndividualN1/blob/main/EDA%26ETL(ML).ipynb), donde se encuentra todo lo antes descrito, también se incluye un "bonus track" que contiene el EDA y ETL necesarios en caso de que se hubiese requerido implementar un sistema de recomendación basado en filtro colaborativo en el proyecto.

# **Etapa IV: Machine Learning (ML)**
 **Consigna:**
 Realizar un modelo de machine learning para armar un sistema de recomendación de películas. Éste consiste en recomendar películas a los usuarios basándose en películas similares, por lo que se debe encontrar la similitud de puntuación entre esa película y el resto de películas, se ordenarán según el score y devolverá una lista de Python con 5 valores, cada uno siendo el string del nombre de las películas con mayor puntaje, en orden descendente. Debe ser deployado como una función adicional de la API anterior y debe llamarse get_recommendation(titulo: str).

**Resolución de la consigna:**

En la etapa de construcción del modelo de machine learning, utilizamos el archivo [MachineLearning.ipynb](https://github.com/JersonGB22/ProyectoIndividualN1/blob/main/MachineLearning.ipynb) y la biblioteca "scikit-learn" (sklearn). Primero, cargamos el conjunto de datos `movies_transformation_ML`, y luego creamos una matriz de características utilizando la clase "CountVectorizer". A continuación, entrenamos y transformamos el modelo, lo que resultó en un vector. Luego, utilizamos la clase "cosine_similarity" para calcular la matriz de similitud. Además, construimos una función para obtener una lista de índices de las películas con mayor puntaje en orden descendente en relación a una película específica. Esta función se aplicó a la columna `label` para obtener las listas correspondientes a cada película, lo que nos permitió hacer recomendaciones personalizadas de manera más rápida y efectiva en el endpoint 7 de la API.

Finalmente, exportamos el dataframe resultante a un archivo CSV denominado [movies_ML_API.csv](https://raw.githubusercontent.com/JersonGB22/ProyectoIndividualN1/main/Datasets/movies_ML_API.csv), el cual se utilizó para realizar la función encomendada `get_recommendation`, en el archivo `main.py`, la cual recibe el nombre de una película y devuelve las 5 más parecidas a esta en orden descendente. También valida el argumento `titulo` y proporciona instrucciones sobre los argumentos necesarios para su uso, al igual que las otras seis funciones.

# **Etapa V: Deployment**
 **Consigna:**
 Conoces sobre Render y tienes un tutorial de Render que te hace la vida mas fácil. También podrías usar Railway, pero ten en cuenta que con este si necesitas dockerización.

 **Resolución de la consigna:**

Para hacer el deployment de nuestro proyecto, se utilizó Render, un servicio de alojamiento en la nube para aplicaciones web. En nuestro archivo `main.py`, se encuentran los siete endpoints que hemos desarrollado utilizando la biblioteca FastAPI y Pandas. Cada endpoint tiene una función asociada que realiza la tarea correspondiente, como la recuperación de datos de un conjunto de datos, el procesamiento de datos y la generación de recomendaciones personalizadas. Antes de hacer el deployment en Render, es importante crear un archivo [requirements.txt](https://raw.githubusercontent.com/JersonGB22/ProyectoIndividualN1/main/requirements.txt) que especifique las bibliotecas y versiones utilizadas en nuestro proyecto. Esto asegura que Render pueda instalar las mismas bibliotecas en su servidor, lo que garantiza la compatibilidad de versiones y evita problemas de incompatibilidad que puedan surgir durante el deployment.

Una vez que hemos creado el archivo `requirements.txt`, podemos seguir las instrucciones de Render para hacer el deployment de nuestro proyecto. Render nos proporciona una URL para acceder a nuestra aplicación, lo que nos permite probar y verificar que todo funciona como se espera.
## Pasos para hacer el deployment de nuestro proyecto en Render:
- Iniciar un repositorio Git en la carpeta de tu proyecto local, utilizando el comando: `git init`.
- Crear un nuevo repositorio en GitHub para el proyecto.
- Vincular tu repositorio local de Git con tu repositorio en GitHub, con el siguiente comando: `git remote add origin <URL de tu repositorio en GitHub>`
- Realizar un commit de los cambios en tu proyecto y un push de los cambios a tu repositorio en GitHub, con los siguientes comandos respectivamente: `git add`, `git commit -m "Descripción del commit"` y `git push -u origin master`.
- Crear una nueva aplicación en Render. Iniciar sesión en Render y hacer clic en el botón "Add a New Service". Seleccionar el tipo de servicio "Web Service" y seguir las instrucciones para configurar la aplicación.
- Vincular la aplicación de Render con el repositorio de GitHub. En la sección de configuración de la aplicación en Render, haz clic en "Link to GitHub" y selecciona el repositorio que acabas de crear.
- Hacer un deploy de la aplicación en Render. En la sección de configuración de la aplicación en Render, hacer clic en el botón "Deploy". Render se encargará de clonar el repositorio de GitHub y desplegar tu aplicación en línea.
- Verificar que la aplicación está funcionando correctamente. 
## [URL de la aplicación web](https://jersonbgb-project-n1-henry.onrender.com/)

- Nota: Para acceder a la documentación de la API, visite la siguiente URL en su navegador: <https://jersonbgb-project-n1-henry.onrender.com/docs>. Al hacerlo, se abrirá la página de documentación interactiva, la cual le permitirá explorar todos los endpoints disponibles y probarlos en tiempo real.
La documentación interactiva ha sido generada automáticamente por FastAPI, y en ella encontrará una descripción detallada de cada uno de los endpoints, así como de los parámetros que aceptan y los esquemas de respuesta. De esta manera, podrá tener un mayor entendimiento sobre el funcionamiento de la API y cómo utilizarla de manera efectiva.

# **Tecnologías utilizadas:**
| Technology | Documentation |
|------------|---------------|
| Visual Studio Code (VSC) | https://code.visualstudio.com/docs |
| Python | https://docs.python.org/3/ |
| Render | https://render.com/docs |
| Git | https://git-scm.com/doc |
| GitHub | https://docs.github.com/en |
| Pandas | https://pandas.pydata.org/docs/ |
| Scikit-learn (sklearn) | https://scikit-learn.org/stable/documentation.html |
| FastAPI | https://fastapi.tiangolo.com/ |
| Uvicorn | https://www.uvicorn.org/ |
| NumPy | https://numpy.org/doc/ |
| Ydata-Profiling | https://ydata-profiling.ydata.ai/docs/master/index.html |
| Matplotlib | https://matplotlib.org/stable/contents.html |
| Seaborn | https://seaborn.pydata.org/ |
| NLTK | https://www.nltk.org/ |
| Regex (expresiones regulares) | https://docs.python.org/3/library/re.html |


<p>
  <img src="https://code.visualstudio.com/assets/favicon.ico" height="100" width="auto" style="max-width: 50%;" />
  <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" height="100" width="auto" style="max-width: 50%;" />
  <img src="https://images.g2crowd.com/uploads/product/image/large_detail/large_detail_477db83f729d63210139ec7cd29c1351/render-render.png" height="100" width="auto" style="max-width: 50%;" />
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Git_icon.svg/1200px-Git_icon.svg.png" height="100" width="auto" style="max-width: 50%;" />
  <img src="https://github.com/fluidicon.png" height="100" width="auto" style="max-width: 50%;" />
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Pandas_logo.svg/2560px-Pandas_logo.svg.png" height="100" width="auto" style="max-width: 50%;" />
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Scikit_learn_logo_small.svg/640px-Scikit_learn_logo_small.svg.png" height="100" width="auto" style="max-width: 50%;" />
  <img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" height="100" width="auto" style="max-width: 50%;" />
  <img src="https://raw.githubusercontent.com/tomchristie/uvicorn/master/docs/uvicorn.png" height="100" width="auto" style="max-width: 50%;" />
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/NumPy_logo_2020.svg/1200px-NumPy_logo_2020.svg.png" height="100" width="auto" style="max-width: 50%;" />
  <img src="https://camo.githubusercontent.com/350907f8f83a7a83e678cfdd24b85ecc3948a2cc469a86c61d2db7e393246626/68747470733a2f2f6173736574732e79646174612e61692f6f73732f79646174612d70726f66696c696e675f626c61636b2e706e67" height="100" width="auto" style="max-width: 50%;" />
  <img src="https://d33wubrfki0l68.cloudfront.net/e33fd6f372aa5d51e7b0de4bd763bd983251881e/4b0f4/blog/customising-matplotlib/matplot_title_logo.png" height="100" width="auto" style="max-width: 50%;" />
  <img src="https://seaborn.pydata.org/_static/logo-wide-lightbg.svg" height="80" width="auto" style="max-width: 50%;" />
  <img src="https://miro.medium.com/v2/resize:fit:592/0*zKRz1UgqpOZ4bvuA" height="80" width="auto" style="max-width: 50%;" />
  <img src="https://www.freecodecamp.org/news/content/images/2023/02/regexpy.png" height="80" width="auto" style="max-width: 50%;" />
</p>

# **Datos del Autor:**
## ***Jerson Brayan Gimenes Beltrán***

### **Correo electrónico:** jerson.gimenesbeltran@gmail.com
