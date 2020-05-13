# Glucose-Prediction
---
#### Members
1. *Alfredo Quintero* - *A01337630*
2. *Cesar Valladares* - *A01023506*
3. *Jorge De la Vega* - *A01650285*
4. *Saul Enrique Labra* - *A01020725*
5. *Christian Aguilar* - *A01024157*
---
### Abstract
This project is for the "Aprendizaje Automatico" class at itesm. It consists of a web application that will allow us to upload csv information on glucose measurements and make predictions on such.
Una aplicacion web con un modelo para entrenar donde se puede predecir el nivel de glucosa basado en algunos factores como si se ha comido o no, cuanto ejercicio se hace, etc. Consiste de dos endpoints, uno para subir mediciones de metodo POST y otro para obtener predicciones de metodo GET.

### Introduccion
La diabetes es una enfermedad la cual occure cuando la glucosa en la sangre es demasiado alta. La glucosa en la sangre es nuestra principal fuente de energia la cual proviene de lo que comemos. La insulina es una hormona creada por el pancreas que ayuda a que la glucosa se inyecte a las celulas de nuestro cuerpo. Las personas con diabetes utilizan inyecciones de insulina para ayudar a su cuerpo a manejar este proceso.
Existen medidores de insulina que inyecta automaticamente despues de medir los niveles de glucosa si es necesario. Estos niveles de glucosa se pueden predecir si se tiene la informacion de comidas y ejercicio de forma precisa

### Definición del Proyecto 
México es uno de los paises con mayor número de personas obsesas en el mundo, por lo tanto, cuenta con un indice alto en diabetes. La diabetes al ser una enfermedad delicada, es tambien silenciosa. El objetivo de este proyecto es hacer una aplicación móvil que monitoree los niveles de glucosa de un usuario constantemente. El proposito es que los usuarios obtengan en su aplicación los niveles constantes de glucosa, y reciba una notificación si el usuario tiene sus niveles muy altos indicando una probable enfermedad grave que ponga en peligro su vida. Para obtener datos precisos, se cuenta con una API entrenando de forma constante para saber cuando notificar al usuario, mientras que los datos se mantienen almacenados en una nube. La API notificará a Firebase el nivel alto de glucosa, por lo que la aplicación en Android recibirá una alerta. El alcance final del proyecto es contar con una aplicación completamente funcional que informe al usuario sobre su estado de salud. 

### Arquitectura
<p align="center">
  <img width="461" alt="Screen Shot 2020-05-12 at 20 57 44" src="https://user-images.githubusercontent.com/27737295/81772227-effe6800-94aa-11ea-96e0-d7cef20b455b.png">
</p>

### Tecnologías
- Android
- Firebase
- API (flask)
- Base de datos en la nube

Este proyecto utiliza una aplicación en Android la cual envia los registros de glucosa a una API. La API se encarga de guardar un registro en una base de datos en la nube cada hora. La base de datos le envía a la API datos con los que se mantiene entrenando constantemenete. Si la API recibe un nivel de glucosa mayor a 200, se envia una alerta a Firebasla cual envia una notificación a la aplicación en Android. La aplicación en el dispositivo mostrará una gráfica con el registro historico de sus datos. 

### Dataset
Se utilizaron dos datasets diferentes:
1. Una encuesta de personas que se admitieron a un hospital con problemas de glucosa y diabetes
2. Una serie de datasets que representan varias acciones que toman pacientes que padecen de diabetes. Los datos incluyen mediciones de glucosa, tiempos de comida, tiempos de ejercicio, etc.

### API
Se desarrollo una API con Flask debido a su lenguaje de programacion de python del cual utilizamos varias librerias de datos.

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

### Endpoints Documentation

Primero deberemos entrenar el modelo, para esto debemos hacer (nota: utilizar Postman https://www.postman.com/):
-petición POST a http://localhost:5000/datasets
-form data llamado data_file con el csv a entrenar

Para llamar una predicción:
-Petición GET a http://localhost:5000/prediction?hour=<int:0-23>
-La variable hour para predecir el nivel de glucosa a cierta hora

