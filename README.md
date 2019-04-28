# Instalación y ejecución
Para ejecutar el Notebook se requiere Spark 2.4.0 y las siguientes librerías de Python
* gensim
* matplotlib
* sklearn
* tqdm
* pandas

Descargar el dataset https://www.kaggle.com/snapcrack/all-the-news y procesarlo con el script one_file.py. Este dataset debe cargarse a HDFS, y luego en una tabla llamada ‘articles_all_csv’.

# CRISP-DM
## Entendimiento del negocio 
Con el crecimiento de la cantidad de contenido disponible la búsqueda de contenido es una necesidad de importancia en el mundo real. Para el caso de  las noticias se propone crear buscadores que funcionen a partir de palabras clave y similaridad semántica.

## Comprensión de los datos
El dataset comprende tres archivos CVS, compuestos por diversos artículos de diferentes periódicos y websites entre 2015 y 2016. Para cada artículo se tienen id,  titulo, contenido, autor, url y fecha de publicación. Se identifica la existencia de filas nulas y algunos contenidos que empiezan y terminan por fin de línea.

Las siguientes gráficas dan una idea de algunos de estos campos:


## Preparación de datos
Para nuestro objetivo solo se hacen necesarias las columnas título, contenido y fecha.  Se realizan las siguientes operaciones:

### Preprocesado con Script en Pandas:
* Unificar los tres CVS en uno 
* Eliminar los fin de línea que aparecían al comienzo del contenido de algunos artículos 
* Tomar solo las 3 columnas relevantes para nuestro trabajo: Id, titulo, contenido y generar el dataset que se usará en spark (articles_all.csv)

### Preprocesado con PySpark 
* Eliminar filas que contienen algún valor nulo.
* Convertir la columna contenido en una lista de palabras-
* Eliminar signos de puntuación y números de ambos lados de cada palabra-
* Eliminar stopwords y palabras con longitud menor a uno.

## Modelado
Los datos se adaptan la estructura de búsqueda índice inverso, que asocia una palabra con los artículos en que más veces ocurre. Posteriormente, se hace clustering de los artículos. Para esta tarea se usan los siguientes modelos:

* Se entrena una Red Neuronal que codifica cada artículo en un vector 20-dimensional, capturando significado de modo que artículos con temas similares tengan representaciones cercanas, técnica conocida como Doc2Vec. En el entrenamiento se itera 20 veces sobre todo el dataset y usa un learning rate decreciente que empieza en 0.025.
* Se agrupan estos vectores en 20 clusters usando K-means.
* Como los clusters obtenidos con  K-means son 20-dimensionales, se usan las técnicas de reducción de dimensionalidad Principal Component Analysis y t-Distributed Stochastic Neighbor Embedding para poner los artículos en un espacio 2D. 


## Evaluación
### Evaluar similaridad de algunos artículos con Cosine Similarity
Se muestrean artículos aleatorios y se verifica manualmente que la similaridad coseno entre sus vectores se corresponda con cuán similar es la temática de los artículos. 
### Elegir número de clusters para el algoritmo K-means
Se ejecutó k-means, variando el parámetro k entre 2 y 40 con paso 2. La siguiente gráfica muestra el valor de la función de costo de k-means en función del número de clusters con que se entrenaba. Finalmente, se escogió usar 20 clusters.

[img:images/elbownotelbow.png]

### Análisis de las 20 palabras que más ocurren en cada cluster.
Para que estas palabras fueran realmente representativas del cluster se realizan las siguientes operaciones:
* Eliminar las palabras con menos de 1.500 o más de 200.000 ocurrencias en todos los artículos. La intuición detrás de esto es que las palabras con menos ocurrencias no representaban el significado del cluster y las que tenían más, por aparecer en múltiples clusters, no lo identificaban. 

Tanto 1.500 como 200.000 son parámetros ajustados experimentalmente. 

A continuación las 20 palabras más representativas de cada cluster: 

[img:images/palabras_clusters.png]

### Imagenes de los clusters generados
## Con Principal Component Analysis

[img:images/pca.png]

## Con t-Distributed Stochastic Neighbor Embedding 

[img:images/t_sne.png]