

<p align="center">
    <img src="http://www.ucv.ve/typo3temp/pics/6b94159b4e.png" alt="UCV Logo" width="150px" style="margin-left: 150px;">
    <img src="http://computacion.ciens.ucv.ve/escueladecomputacion/img/layout_publico/encabezado/logo_ciencias.jpg" alt="Facultad de Ciencias Logo" width="150px" style="margin-left:150px">
    <img src="http://computacion.ciens.ucv.ve/escueladecomputacion/img/layout_publico/encabezado/logo_encabezado_nuevo.jpg" alt="Facultad de Ciencias Logo" width="150px">
</p>


# Herramienta de Automatización, Monitoreo y Analisis de Componentes y Artefactos (HAMACA)

## Introducción 
Este es el repositorio de la aplicación "Herramienta de Automatización, Monitoreo y Analisis de Componentes y Artefactos" (HAMACA), que tiene como fin el de ser un framework para laboratorios de IoT y entorno de purebas y desarollos en el area de la automatización de procesos. Ademas este repositorio tambien contiene las configuraciones de herramientas integradas a este proyecto.

Este proyecto academico se realiza como parte del desarrollo e investigación realizado para el Trabajo Especial de Grado para la [Escuela de Computación](http://computacion.ciens.ucv.ve/escueladecomputacion/) de la [Facultad de Ciencias](http://www.ciens.ucv.ve/ciens/) de la [Universidad Central de Venezuela](http://www.ucv.ve/).

## Requsitos previos
Como requisitos previos para correr esta aplicación se necesita tener primero las siguientes aplicaciones instaladar. 

### Docker
Este proyecto usa las imagenes docker de varias integraciones. Se anexa la [documentación oficial](https://docs.docker.com/get-docker/) para realizar la instalación según sea requerido.

### Python
Esta webapp esta desarrollada en el lenguaje de programación Python en su version 3.10. Esta es [la página oficial del lenguaje](https://www.python.org/) y su [sección de descargas](https://www.python.org/downloads/) en caso de que no se posea en el sistema operativo

### Postgresql
La aplicación web requiere para su funcionamiento y el almacenamiento de data referente a si misma la base de datos postgresql. En este [link oficial](https://www.postgresql.org/download/) con los instaladores y las instrucciones para poder instalarlo en los diversos dispositivos disponibles. Se requiere que una vez instalado el sistema manejador, crear una base de datos de nombre `hamaca` y un usuario gateway con el cual se pueda conectar la app a ella al momento de hacer las migraciones de los modelos de django a la base de datos.

### Mosquitto
Mosquitto es la implementación del protocolo MQTT que se utiliza en este trabajo de investigación. Tiene la capacidad de actuar como cliente y broker. Se deja link a la [documentación oficial](https://mosquitto.org/download/) para su instalación. Tambien es posible utilizar cualquier otra implementación del protocolo MQTT sea local o en la nube. 

### Nginx
En el caso de querer desplegar esto en el modo de ambiente de producción tambien se requiere tener el Stack de Nginx configurado y activo. [Se puede seguir la guía de instalación oficial](https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-open-source/) según la plataforma deseada


Se recomienda el [tutorial de DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04) para configurar todo el proceso de Nginx y Django en ambiente de producción.

## Instalación
Se sugiere la utlización de un ambiente virtual en python. Estos se pueden crear de la siguiente forma:

```bash
python -m venv hamaca-env
```

El proyecto requiere ciertas variables de entorno para poder funcioinar. Se recomienda el uso de un archivo `.env` en el cual se inicialicen esas variables. La lista es la siguiente

```bash
export DJANGO_SECRET_KEY=
export DJANGO_SETTINGS_MODULE=
export DJANGO_DB_NAME=
export DJANGO_DB_USER=
export DJANGO_DB_PASSWORD=
export DJANGO_DB_HOST=
export DJANGO_DB_PORT=
```

Una vez llenas esas variables de entorno se pueden cargar usando el comando
```bash
source .env
```

Lo primero es ubicarse en la carpeta docker_stack que contine los archivos de docker, docker compose y los archivos de configuración de las aplicaciones del stack utilizado por el proyecto. A continuación estan la serie de pasos para poder tener el ambiente desplegado.

1. Correr el archivo Dockerfile para obtener la imagen de node-red modificada que contine los plugins necesarios para los flujos y la pestaña de actuadores. Para ello haremos uso del comando: 
```bash 
docker build . -t node-red-teg 
``` 

2. Se procede a levantar el ambiente de python con sus dependencias. Se hace de la suguiente forma: 
En Windows, ejecuta:
```bash
hamaca-env\Scripts\activate
```
En Unix o MacOS, ejecuta:
```bash
source hamaca-env/bin/activate
```
Para poder instalar las dependencias necesarias y que se encuentran listadas en el archivo `requirements.txt` hacemos uso del comando:
```python
pip install -r requirements.txt
```

3. Con la base de datos Postgresql como servicio activo pasamos a cargar en la base de datos de postgres los modelos requeridos de la apliación. Esto se hace de la suigiente manera:
```bash
python manage.py migrate
```
 
4. Luego llenando la data incial requerida por la app, donde fixture son los archivos.json de cada modulo. Se hace con el comando 
```bash
python manage.py loaddata <directorio del modulo>/<fixture> 
``` 

5. Aparte se necesita crear un usuario administrador de la aplicación con el que se iniciara la app por primera vez. Esto se hace usando del comando 
 ```bash
django-admin createuser <nombre de usuario>
```

6. Si es la primera vez que se levanta el ambiente de la app será necesario ajustar los paneles iniciales de las apliaciones de grafana, la configuración de influxdb como fuente de datos en grafana como se muestra en la figura. 

  <img src="https://images.ctfassets.net/o7xu9whrs0u9/5bTkzeL0eGHSDnJAEep4j8/5e1e717658472b6b5e5f5f8e45734c4e/Grafana_and_InfluxDB_connection_setup.png" alt="InfluxDB connection in Grafana">

## Como correr este proyecto

Antes de poder correr la webapp es necesario levantar todos los elementos dockerizados con el fin que se muestren todas las integraciones que usa el proyecto. Esto se hace de la siguiente forma: ubicandonos en la carpeta `docker_stack` se encuentra el archivo de docker-compose para levantar la base de datos InfluxDB, la aplicación de Grafana y la apliación de Node-Red modificada, a traves del comando:
```bash 
docker-compose up 
```
si deseamos no ver el log de las interfaces podemos agregarle el parametro 	`-d` para utilizar la consola en modo detached.

Luego tener levantadas todas las imagenes de las integraciones, con el entorno de python aun activo procedemos a hacer lo siguiente: 

```bash
python manage.py runserver <host>
``` 
Con ello la aplicación web se levantara junto a todos los modulos desarrollados. 