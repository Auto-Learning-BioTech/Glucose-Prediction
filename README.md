# Glucose-Prediction
---
#### Members
1. *Christian Aguilar* - *A01024157*
2. *Cesar Valladares* - *A01023506*
3. *Jorge De la Vega* - *A01650285*
4. *Saul Enrique Labra* - *A01020725*
5. *Alfredo Quintero* - *A01337630*
---
### Abstract
This project is for the "Aprendizaje Automatico" class at itesm. It consists of a web application that will allow us to upload csv information on glucose measurements and make predictions on such. 
Una aplicacion web con un modelo para entrenar donde se puede predecir el nivel de glucosa basado en algunos factores como si se ha comido o no, cuanto ejercicio se hace, etc. Consiste de dos endpoints, uno para subir mediciones de metodo POST y otro para obtener predicciones de metodo GET.

### Introduccion
La diabetes es una enfermedad la cual occure cuando la glucosa en la sangre es demasiado alta. La glucosa en la sangre es nuestra principal fuente de energia la cual proviene de lo que comemos. La insulina es una hormona creada por el pancreas que ayuda a que la glucosa se inyecte a las celulas de nuestro cuerpo. Las personas con diabetes utilizan inyecciones de insulina para ayudar a su cuerpo a manejar este proceso.
Existen medidores de insulina que inyecta automaticamente despues de medir los niveles de glucosa si es necesario. Estos niveles de glucosa se pueden predecir si se tiene la informacion de comidas y ejercicio de forma precisa

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
Activar el directorio .env
```
source .env/bin/activate
```
Iniciar variable de entorno
```
export FLASK_APP=src
```
Correr la aplicacion flask
```
flask run
```
---
#### Docker
Clonar repositorio y correr
```
docker-compose up
```
o
```
docker build .
```

### Endpoints Documentation

Primero deberemos entrenar el modelo, para esto debemos hacer (nota: utilizar Postman https://www.postman.com/): 
-petición POST a http://localhost:5000/datasets
-form data llamado data_file con el csv a entrenar

Para llamar una predicción:
-Petición GET a http://localhost:5000/prediction?hour=<int:0-23>
-La variable hour para predecir el nivel de glucosa a cierta hora

