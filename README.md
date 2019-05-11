# ST0263-Project3 - Analítica de texto

## Instalación y ejecución
Para ejecutar el Notebook se requiere Spark 2.4.0 y las siguientes librerías de Python:
* gensim
* matplotlib
* sklearn
* tqdm
* pandas

Descargar el dataset https://www.kaggle.com/snapcrack/all-the-news y procesarlo con el script one_file.py. Este dataset debe cargarse a HDFS, y luego en una tabla llamada ‘articles_all_csv’.

## CRISP-DM
### Entendimiento del negocio 
Con el crecimiento de la cantidad de contenido disponible la búsqueda de contenido es una necesidad de importancia en el mundo real. Para el caso de  las noticias se propone crear buscadores que funcionen a partir de palabras clave y similaridad semántica.

### Comprensión de los datos
El dataset comprende tres archivos CSV, compuestos por diversos artículos de diferentes periódicos y websites entre 2015 y 2016. Para cada artículo se tienen id,  titulo, contenido, autor, url y fecha de publicación. Se identifica la existencia de filas nulas y algunos contenidos que empiezan y terminan por fin de línea.

### Preparación de datos
Para nuestro objetivo solo se hacen necesarias las columnas título, contenido y fecha.  Se realizan las siguientes operaciones:

#### Preprocesado con Script en Pandas:
* Unificar los tres CSV en uno 
* Eliminar los fin de línea que aparecían al comienzo del contenido de algunos artículos 
* Tomar solo las 3 columnas relevantes para nuestro trabajo: Id, titulo, contenido y generar el dataset que se usará en spark (articles_all.csv)

#### Preprocesado con PySpark 
* Eliminar filas que contienen algún valor nulo.
* Convertir la columna contenido en una lista de palabras-
* Eliminar signos de puntuación y números de ambos lados de cada palabra-
* Eliminar stopwords y palabras con longitud menor a uno.

### Modelado
Los datos se adaptan la estructura de búsqueda índice inverso, que asocia una palabra con los artículos en que más veces ocurre. Posteriormente, se hace clustering de los artículos. Para esta tarea se usan los siguientes modelos:

* Se entrena una Red Neuronal que codifica cada artículo en un vector 20-dimensional, capturando significado de modo que artículos con temas similares tengan representaciones cercanas, técnica conocida como Doc2Vec. En el entrenamiento se itera 20 veces sobre todo el dataset y usa un learning rate decreciente que empieza en 0.025.
* Se agrupan estos vectores en 20 clusters usando K-means.
* Como los clusters obtenidos con  K-means son 20-dimensionales, se usan las técnicas de reducción de dimensionalidad Principal Component Analysis y t-Distributed Stochastic Neighbor Embedding para poner los artículos en un espacio 2D. 

### Evaluación
#### Evaluar similaridad de algunos artículos con Cosine Similarity
Se muestrean artículos aleatorios y se verifica manualmente que la similaridad coseno entre sus vectores se corresponda con cuán similar es la temática de los artículos. 
#### Elegir número de clusters para el algoritmo K-means
Se ejecutó k-means, variando el parámetro k entre 2 y 40 con paso 2. La siguiente gráfica muestra el valor de la función de costo de k-means en función del número de clusters con que se entrenaba. Finalmente, se escogió usar 20 clusters.
![kmeans](/images/kmeans.png?raw=true "kmeans")

#### Análisis de las 20 palabras más distintivas de cada cluster.
Para que estas palabras fueran realmente representativas del cluster se descartan las que tienen menos de 1.500 o más de 200.000 ocurrencias en todos los artículos. La intuición detrás de esto es que las palabras con menos ocurrencias no representaban el significado del cluster y las que tenían más, por aparecer en múltiples clusters, no son distintivas. 

Tanto 1.500 como 200.000 son parámetros ajustados experimentalmente. 

A continuación las 20 palabras más representativas de cada cluster: 

| Cluster |                                                                                                  Most Distinctive Words                                                                                                 |
|:-------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|    0    | ["schools","transgender","campus","scalia","abortion","gorsuch","faculty","teachers","justices","devos","colleges","antonin","legislature","students","abortions","charter","bathrooms","clinics","school’s","court’s"] |
|    1    |         ["outbreak","fda","zika","virus","symptoms","patients","genetic","mosquitoes","infected","disease","clinical","mosquito","treatments","autism","vaccine","cdc","diet","bacteria","diseases","infection"]        |
|    2    |            ["roosevelt","nafta","mexicans","vox","conservatism","gingrich","nixon","romney","elites","coal","populist","pruitt","populism","tpp","reagan","inaugural","reader","mitt","bannon","nationalism"]           |
|    3    |         ["france’s","pen","cent","theresa","brexit","netherlands","merkel","european","britain’s","chancellor","bloc","parliament","eu","britain","labour","macron","cameron","referendum","le","parliamentary"]        |
|    4    |           ["missile","iran","tillerson","korea","putin’s","ballistic","xi","nuclear","sanctions","iran’s","korean","ukraine","taiwan","nato","missiles","pyongyang","jong","netanyahu","korea’s","peninsula"]           |
|    5    |               ["scored","coach","yankees","championship","tournament","ball","nfl","players","knicks","nba","giants","league","player","jets","curry","yards","quarterback","warriors","mets","patriots"]               |
|    6    |                      ["songs","music","album","lyrics","comedy","episodes","pop","show’s","movie","film","episode","jazz","comic","movies","musical","band","films","song","characters","broadway"]                     |
|    7    |            ["realdonaldtrump","kaine","lewandowski","debates","melania","gingrich","conway","msnbc","biden","hannity","pac","carson","palin","pence","jeb","sexist","weiner","hillary’s","kellyanne","mate"]            |
|    8    |              ["apple","uber","apps","apple’s","iphone","yahoo","motors","startup","tesla","acquisition","merger","musk","inc","software","microsoft","samsung","smartphone","antitrust","android","google"]             |
|    9    |                ["stocks","economists","crude","inflation","wells","fed","monetary","index","stimulus","exports","dow","bonds","mnuchin","imports","dollar","reserve","nasdaq","securities","fargo","s&p"]               |
|    10   |             ["bail","shooter","jurors","felony","patrol","cop","inmates","sheriff’s","officer","police","custody","shooting","firearm","sheriff","cops","hernandez","nypd","shootings","officers","fatally"]            |
|    11   |                ["solar","species","hurricane","birds","storm","weather","arctic","warming","mars","fish","moon","ocean","winds","nasa","scientists","snow","planet","temperatures","temperature","earth"]               |
|    12   |        ["cartel","brussels","belgian","manchester","airport","rio","attackers","swedish","turkey’s","migrant","migrants","turkish","sweden","coup","duterte","istanbul","detained","erdogan","asylum","attacker"]       |
|    13   |                 ["comey","nsa","hacking","server","schiff","fbi","abedin","cia","comey’s","collusion","fbi’s","leaks","mueller","flynn’s","nunes","flynn","yates","kislyak","intelligence","classified"]                |
|    14   |           ["airstrikes","civilians","iraqi","casualties","afghan","rebel","mosul","aleppo","taliban","rebels","assad","fighters","raqqa","baghdad","syrian","bashar","sunni","militants","syria’s","kurdish"]           |
|    15   |     ["repealing","aca","obamacare","caucuses","margin","repeal","insurers","delegate","sanders’s","medicaid","kasich","filibuster","caucus","medicare","ryan’s","gop’s","delegates","turnout","premiums","contests"]    |
|    16   |         ["firearms","dakota","mateen","demonstrators","guns","deportation","dhs","policing","ferguson","gun","rouge","shootings","nypd","sanctuary","orlando","tribe","protesters","baton","refuge","pipeline"]         |
|    17   |          ["o’reilly","cosby","boycott","espn","milo","actress","gawker","trans","academy","harassment","feminist","ailes","awards","celebrities","yiannopoulos","oscar","sexist","instagram","anthem","makeup"]         |
|    18   |              ["cream","restaurant","designer","fashion","art","painting","chicken","design","taste","listing","wedding","beer","restaurants","museum","cooking","wine","cheese","kitchen","coffee","meal"]              |
|    19   |          ["israeli","islam","jesus","holy","egypt","palestinian","palestinians","francis","pope","jerusalem","christians","israel’s","jews","cuban","cuba","catholic","castro","jewish","holocaust","egyptian"]         


#### Imagenes de los clusters generados
##### Con Principal Component Analysis
![pca](/images/pca.png?raw=true "pca")

##### Con t-Distributed Stochastic Neighbor Embedding 
![tsne](/images/tsne.png?raw=true "tsne")

### Despliegue

El desarrollo del proyecto se realizó en Databricks.

## Integrantes y sus contribuciones

### Juan José Suárez Estrada - jsuare32@eafit.edu.co
Declaro que participé en las siguientes etapas del proyecto, y que todas estas son de autoría propia:
* Estructuración del desarrollo bajo la metodología CRISP-DM
* Limpieza y carga de datos
* Cálculo del Índice Inverso
* Entrenamiento y evaluación de Doc2Vec
* Clusterización de los artículos con k-Means
* Visualización de los clusters usando t-SNE y PCA

### Juan Manuel Ciro Restrepo - jcirore@eafit.edu.co
Declaro que participé en las siguientes etapas del proyecto, y que todas estas son de autoría propia:
* Estructuración del desarrollo bajo la metodología CRISP-DM
* Limpieza y carga de datos
* Cálculo del Índice Inverso
* Entrenamiento y evaluación de Doc2Vec
* Clusterización de los artículos con k-Means
* Visualización de los clusters usando t-SNE y PCA

