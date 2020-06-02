# Glucose-Prediction
---
#### Miembros
1. *Alfredo Quintero* - *A01337630*
2. *Cesar Valladares* - *A01023506*
3. *Jorge De la Vega* - *A01650285*
4. *Saul Enrique Labra* - *A01020725*
5. *Christian Aguilar* - *A01024157*
---
### Resumen
Este proyecto fue desarrollado para la clase de "Aprendizaje Automático" impartida en el ITESM. Consiste en un API y una aplicación Android que le permitirá al usuario hacer predicciones de sus niveles de glucosa mediante técnicas de machine learning y tener un registro histórico de estas mediciones.

### Planteamiento del problema
La diabetes es una enfermedad la cual occure cuando la glucosa en la sangre es demasiado alta. La glucosa en la sangre es nuestra principal fuente de energia la cual proviene de lo que comemos. La insulina es una hormona creada por el pancreas que ayuda a que la glucosa se inyecte a las celulas de nuestro cuerpo. Las personas con diabetes utilizan inyecciones de insulina para ayudar a su cuerpo a manejar este proceso. Si el nivel de glucosa en la sangre es demasiado alta se pueden presentar situaciones de riesgo en las que el paciente pueda perder incluso la vista o gangrena de extremidades por lo que nuestra tarea es ayudar a mitigar este riesgo.

### Objetivo
El objetivo de este proyecto es ser una ayuda para los pacientes que padecen de diabetes mediante alertas oportunas que les prevengan de una alta subida de nivel de glucosa en la sangre antes de que esto ocurra para que puedan tomar medidas pertinentes antes de que se genere una situación de riesgo mas grave contra su salud. Se generará en este proyecto una solución de software que empleará técnicas de machine learning y de desarrollo de aplicaciones móviles para lograr el objetivo.

### Solución
Para lograr cumplir con el objetivo del proyecto se optó por desarrollar una aplicación móvil para sistemas Android que recabará datos de los niveles de glucosa de un determinado paciente de manera periódica en intervalos prestablecidos de tiempo. Estos datos provendran de un dispositivo medidor de glucosa automático que el paciente deberá portar todo el tiempo y con la información recabada se entrenará de manera diaria un algoritmo de machine learning que emplea regresiones para predecir en un futuro los niveles de glucosa en la sangre esperados de ese mismo paciente a una determinada hora. El paciente será capaz de ver en la aplicación tanto el histórico de sus mediciones de glucosa a lo largo del tiempo como también contará con una notificación que le será enviada en caso de que la predicción de nivel de glucosa para la próxima hora se salga de los parámetros saludables.

La parte del procesamiento de la información para entrenar los modelos de machine learning se hará dentro de un API y la información que se genere se almacenará en una base de datos alojada en la nube, teniendo registros separados por usuario para predicciones específicas por paciente. Las alertas se generarán por medio del servicio de notificaciones de Firebase Messaging Services usando un token generado por cada dispositivo como identificador.

### Alcance
El alcance final del proyecto es contar con una aplicación completamente funcional que informe al usuario sobre sus niveles de glucosa a lo largo del tiempo y que reciba las notificaciones oportunas basandose en un modelo entrenado de forma individual por usuario contanto con un perfil al que pueda acceder con un nombre de usuario y una contraseña.

### Arquitectura
<p align="center">
  <img width="769" alt="Screen Shot 2020-06-01 at 13 49 09" src="https://user-images.githubusercontent.com/27737295/83443049-b9af6b00-a40e-11ea-9088-a2c0c5f592d4.png">
</p>

### Tecnologías
- Android
- Firebase Cloud Messaging
- API (flask)
- Cloud Firestore 
- Google Cloud Platform 

Este proyecto utiliza una aplicación en Android la cual envia los registros de glucosa a una API. La API se encarga de guardar un registro en una base de datos en la nube cada hora. El API obtiene datos de la base de datos diariamente para mantenerse entrenado. Si la API predice un nivel de glucosa mayor a 200 mg/dl, se envia una alerta al servicio en la nube de Firebase Cloud Messaging que envia una notificación a la aplicación en Android. La aplicación en el dispositivo mostrará una gráfica con el registro historico de sus datos. 

### Dataset
Se utilizó una serie de datasets que representan varias acciones que toman pacientes que padecen de diabetes. Los datos incluyen mediciones de glucosa, tiempos de comida, tiempos de ejercicio, etc. De aquí se obtiene la información que en un futuro sería obtenida de un medidor automático de glucosa.

### API
Se desarrollo una API con Flask debido a su lenguaje de programacion de python fácil de usar del cual se usaron las siguientes librerias de datos.


### Puntos de entrada
**Formato de peticiones:**
/punto de entrada | Método | Tipo | Valor si elemento fué regresado con éxito.

/ | GET | null | "1": 
Este endpoint no recibe parámetros y regresa un '1' como muestra de que el API está corriendo

/**initialize_firebase**| POST | Form-data | "Initialized":
Este endpoint contiene un json con las credenciales para utilizar el servicio de Firebase. 

  Parámetros: 
  - "credentials" (archivo .json con las credenciales de Firebase)

/**register_user** | POST | Form-data | "registered":
Este endpoint se encarga de registrar un usuario en la base de datos, su funcionamiento consiste en revisar si el usuario existe en la base de datos, si el usuario no existe se permite el registro del usuario y sus datos terminan en la base de datos.

Parámetros:
- "username"(str) 
- "device_token"(str)

/**update_device_token** | POST | Form-data | "updated":
Este endpoint se encarga de actualizar el device token de cada usuario. Los tokens cambian si la aplicación se reinstala. 

Parámetros:
- "username"(str)
- "device_token"(str)

/**insert_json_db** | POST | JSON | "ok":
Este endpoint inserta un conjunto de datos en un json y se sube a la base de datos a la información especifica de cada usuario (username). 
Este json se enviará a la base de datos al final del día para mantener un control de la información de cada usuario. 

Parámetros:
- "username"(str)
- "data_file"(.json file with meassures)

/**new_meassurement** | POST | JSON | "ok":
Este endpoint se encarga de hacer una nueva medición a cada usuario de glucosa. 

Parámetros:
- "username"(str)
- "year"(int)
- "month"(int)
- "day"(int)
- "hour"(int)
- "level"(int)

/**set_user_model** | POST | JSON | "exp_arr updated":
Este endpoint se encarga de actualizar los valores de la función polinomial que medirá la glucosa. 

Parámetros:
- "username"(str)
- "exp_arr"(int array)

/**user_predict** | POST | Form-data | "ok": 
Este endpoint obtiene la predicción de un usuario en una hora específica del día. 

Parámetros:
- "username"(str) 
- "hour"(int)

/**get_history** | POST | Form-data | "retrieved":
Este endpoint obtiene los datos de un usuario específico de los ultimos seis meses. 

Parámetros:
- "username"(str)

Para hacer predicciones se debe seguir el siguiente proceso

Primero deberemos entrenar el modelo, para esto debemos hacer (nota: utilizar Postman https://www.postman.com/):
-petición POST a http://localhost:5000/datasets
-form data llamado data_file con el csv a entrenar

Para llamar una predicción:
-Petición GET a http://localhost:5000/prediction?hour=<int:0-23>
-La variable hour para predecir el nivel de glucosa a cierta hora


### Dependencias
- Flask
- pandas
- numpy
- matplotlib
- scipy
- joblib
- threadpoolctl
- tzlocal
- firebase-admin
- grpcio
- scikit-learn

### Instalacion
#### Native
Clonar repositorio
```
git clone https://github.com/Auto-Learning-BioTech/Glucose-Prediction.git
```
Cambiar de directorio
```
cd Glucose-Prediction
```
---
#### Docker
Crear un build del Dockerfile
```
docker build -t flaskapp .
```
Correr (Port: 5000)
```
docker run -p 5000:5000 flaskapp
```
O correr como un background process
```
docker run -p 5000:5000 -d flaskapp
```

Solicite las credenciales del proyecto a uno de los miembros del equipo.

### Base de datos
<p align="center">
<img width="500" alt="Screen Shot 2020-06-01 at 20 01 27" src="https://user-images.githubusercontent.com/27737295/83468574-c3eb5c80-a442-11ea-9310-7d00ecd74b90.png">
</p>

Est proyecto utiliza el servicio Cloud Firestore de Firebase. Este servicio es una base de datos no relacional basada en documentos similares a JSON. Se realiza una validación automatica de datos y cuenta con escalabilidad automática. 
La base de datos cuenta con dos colecciones: Users y Data. Este proyecto utiliza la base para insertar y recuperar datos históricos y la distinción se hace por usuarios individuales. 

- Users: continene tres atributos: username, device_token y exp_arr. El primero, username, es el id del dispositivo, se caracteriza por ser el nombre de usuario. El segundo, device_token, es el dispositivo Android que el usuario se encuentre utilizando, de esta forma se permite el envio de notificaciones a cada usuario. Finalmente exp_arr contiene los coeficientes de la función polinomial que se utiliza para predecir la glucosa.
- Data: contiene siete atributos: id, year, month, day, hour, username_fk.id de los registros en la colección 'data' se compone del año, mes, día y nombre de usuario concatenados en un strings. Además del id, se tienen los siguientes atributos:  día, nivel de glucosa, hora, mes, nombre del usuario y año. 

### Servicio en la nube
<p align="center">
  <img width="700" alt="Screen Shot 2020-06-02 at 18 20 55" src="https://user-images.githubusercontent.com/27737295/83579142-163d8380-a4fe-11ea-9e2b-552c12e78f77.png">

</p>

La API de este proyecto se encuentra desplegada en Google Cloud Platform (GCP). La API se encuentra dentro de un contenedor de Docker en forma de imagen con una etiqueta que distingue cada versión de la otra. La imagen del contenedor se encuentra en un registro dentro de GCP para que Google Kubernetes Enginee (GKE) pueda descargar y correr la imagen. Para correr la imagen, se cuenta con un cluster GKE con dos nodos. Para desplegar la aplicación en el cluster GKE, se establece una comunicación con el sistema de administracion de clusters de Kubernetes. Debido a que Kubernetes representa las aplicaciones como Pods, en esta implementación se tiene un Pod que contiene solo el contenedor de nuestra imagen. Finalmente, la aplicación está expuesta en el puerto 5000, pues se crea una IP externa y cuenta con un balanceador de carga, mientras que el contenedor se encuentra en el target port 5000. Es necesario hacer esta división de puertos debido a que los contenedores que corren en GKE no cuentan con direcciones IP externas, por lo tanto no son accesibles a internet. 

Para desplegar la API se debe tener los siguientes requisitos: un proyecto de GCP creado, tener habilitado Kubernetes Engine API y haber seleccionado el proyecto que se desee utilizar. Además, debe tener instalado el SDK de Google Cloud en su dispositivo y tener Docker instalado en su sistema. Finalmente debe contar con kubectl ya que se utiliza para comunicarse con Kubernetes. 
```
gcloud components install kubectl
```
Clonar repositorio
```
git clone https://github.com/Auto-Learning-BioTech/Glucose-Prediction.git
```
Cambiar de directorio
```
cd Glucose-Prediction
```
Añada la variable de ambiente PROJECT_ID al ID del proyecto de Google Cloud (project-id). La variable PROJECT_ID se utilizará para asociar la imagen del contenedor con el contenedor de registro del proyecto. 
```
export PROJECT_ID=project-id
```
Construya la imagen del contenedor de esta aplicación y aplique una etiqueta para distinguir, en este caso se usará v1. 
```
docker build -t gcr.io/${PROJECT_ID}/flaskapp:v1 .
```
Configure la herramienta de linea de comandos de Docker para autenticar el contenedor de registro. Ojo, solo se debe hacer la primera vez que realice este tipo de configuración.
```
gcloud auth configure-docker
```
Ahora puede cargar la imagen al contenedor de registro:
```
docker push gcr.io/${PROJECT_ID}/flaskapp:v1
```
Deberá elegir la zona que desee utilizar en su project ID y en Compute Engine. 
```
gcloud config set project $PROJECT_ID
gcloud config set compute/zone us-central1-a 
```
Cree un cluter de dos nodos de nombre glucose-cluster.
```
gcloud container clusters create glucose-cluster --num-nodes=2
```
Suba su aplicación al cluster GKE.
```
kubectl create deployment glucose-cluster --image=gcr.io/${PROJECT_ID}/flaskapp:v1
```
Finalmente, suba su aplicación a internet.
```
kubectl expose deployment glucose-cluster --type=LoadBalancer --port 5000 --target-port 5000
```
Escriba el siguiente comando para ver su IP externa y el puerto designado. 
```
kubectl get service
```
--- 
**Para subir nuevas versiones del sistema siga los siguientes pasos.**

Construya una nueva imagen de Docker con la etiqueta v2, que simboliza la versión numero dos de su aplicación. 
```
docker build -t gcr.io/${PROJECT_ID}/flaskapp:v2 .
```
Suba la imagen al contenedor de registro. 
```
docker push gcr.io/${PROJECT_ID}/flaskapp:v2  
```
Aplique una actualización al despliegue actual con la nueva imagen:
```
kubectl set image deployment/glucose-cluster flaskapp=gcr.io/${PROJECT_ID}/flaskapp:v2
```
Para mayor información visite Google Cloud Kubernetes Engine Documentation o visite el siguiente link: https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app. 



