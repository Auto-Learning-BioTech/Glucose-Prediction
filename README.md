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
  <img width="500" alt="Screen Shot 2020-05-31 at 19 57 32" src="https://user-images.githubusercontent.com/27737295/83367209-   0c3e4800-a379-11ea-967e-ed1b8096a4b8.png">
</p>

### Tecnologías
- Android
- Firebase Cloud Messaging
- API (flask)
- Cloud Firestore 

Este proyecto utiliza una aplicación en Android la cual envia los registros de glucosa a una API. La API se encarga de guardar un registro en una base de datos en la nube cada hora. El API obtiene datos de la base de datos diariamente para mantenerse entrenado. Si la API predice un nivel de glucosa mayor a 200 mg/dl, se envia una alerta al servicio en la nube de Firebase Cloud Messaging que envia una notificación a la aplicación en Android. La aplicación en el dispositivo mostrará una gráfica con el registro historico de sus datos. 

### Dataset
Se utilizó una serie de datasets que representan varias acciones que toman pacientes que padecen de diabetes. Los datos incluyen mediciones de glucosa, tiempos de comida, tiempos de ejercicio, etc. De aquí se obtiene la información que en un futuro sería obtenida de un medidor automático de glucosa.

### API
Se desarrollo una API con Flask debido a su lenguaje de programacion de python fácil de usar del cual se usaron las siguientes librerias de datos.

### Dependencias
- Flask
- pandas
- numpy
- sklearn
- matplotlib

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
### Base de datos
Est proyecto utiliza el servicio Cloud Firestore de Firebase. Este servicio es una base de datos no relacional basada en documentos similares a JSON. Se realiza una validación automatica de datos y cuenta con escalabilidad automática. 
La base de datos cuenta con dos colecciones: Users y Data. Este proyecto utiliza la base para insertar y recuperar datos históricos y la distinción se hace por usuarios individuales. 

- Users: continene tres atributos: username, device_token y exp_arr. El primero, username, es el id del dispositivo, se caracteriza por ser el nombre de usuario. El segundo, device_token, es el dispositivo Android que el usuario se encuentre utilizando, de esta forma se permite el envio de notificaciones a cada usuario. Finalmente exp_arr se encarga de guardar el modelo por usuario. De esta manera se sabe que exponentes utilizar en la funcion polinomial que mide la glucosa. 
- Data: contiene siete atributos: id, year, month, day, hour, username_fk. El id se identifica mediante una combinación entre la llave independiente de cada usuario, el nombre del usuario (username) y la hora. Además contiene el día, nivel de glucosa, hora, mes, nombre del usuario y año. 

<p align="center">
  <img width="500" alt="Screen Shot 2020-05-30 at 23 12 26" src="https://user-images.githubusercontent.com/27737295/83344380-857f6180-a2cb-11ea-8a5d-baabd1de09ed.png">
</p>


### Puntos de entrada
**Formato de peticiones:**
/punto de entrada | Método | Tipo | Valor si elemento fué regresado con éxito.

/**GET** | GET | null | "1": 
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

/**insert_csv_db** | POST | Form-data | "ok":
Este endpoint inserta un conjunto de datos en un CSV y se sube a la base de datos a la información especifica de cada usuario (username). 
Este csv se enviará a la base de datos al final del día para mantener un control de la información de cada usuario. 

Parámetros:
- "username"(str)
- "data_file"(.csv file with meassures)

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

/**datasets** | POST:
Este enpoint recibe como parámetro en el cuerpo de la solicitud el csv que se usará para entrenar el modelo

Parámetros:
- data_file:<str:'filename.csv'>

/**prediction?hour=<int:0-23>** | GET:
Este endpoint recibe como parámetro un entero con rango de 0 a 23 para predecir el nivel de glucosa a cierta hora del día

Parámetros:
- hour:<int: 0-23>

/**insert** | POST:
Este endpoint recibe como parámetros la fecha y valor de la medición de glucosa a insertar en el csv temporalmente estático, todo se introduce en el cuerpo de la solicitud

  Parámetros:
  - hour:<int: 0-23>
  - glucose:<int: >
  - day:<int: 1-31>
  - month:<int: 1-12>
  - filename:<str: 'filename.csv'>

Para hacer predicciones se debe seguir el siguiente proceso

Primero deberemos entrenar el modelo, para esto debemos hacer (nota: utilizar Postman https://www.postman.com/):
-petición POST a http://localhost:5000/datasets
-form data llamado data_file con el csv a entrenar

Para llamar una predicción:
-Petición GET a http://localhost:5000/prediction?hour=<int:0-23>
-La variable hour para predecir el nivel de glucosa a cierta hora

