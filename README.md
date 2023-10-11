

<p align="center">
    <img src="http://www.ucv.ve/typo3temp/pics/6b94159b4e.png" alt="UCV Logo" width="150px" style="margin-left: 30px;">
    <img src="http://computacion.ciens.ucv.ve/escueladecomputacion/img/layout_publico/encabezado/logo_ciencias.jpg" alt="Facultad de Ciencias Logo" width="150px" style="margin-left:30px">
    <img src="http://computacion.ciens.ucv.ve/escueladecomputacion/img/layout_publico/encabezado/logo_encabezado_nuevo.jpg" alt="Facultad de Ciencias Logo" width="150px">
</p>


# Herramienta de Automatización, Monitoreo y Analisis de Componentes y Artefactos (HAMACA)

Este es el repositorio de la aplicación "Herramienta de Automatización, Monitoreo y Analisis de Componentes y Artefactos" (HAMACA) como parte del desarrollo e investigación realizado para el Trabajo Especial de Grado, con el fin de ser un framework para laboratorios de IoT y entorno de ourebas y desarollos en el area de la automatización de procesos. Ademas este repositorio tambien contiene las configuraciones de herramientas integradas a este proyecto.

# Requsitos previos
Como requisitos previos para correr esta aplicación se sugiere la utlización de un ambiente virtual en python. Estos se pueden crear de la siguiente forma:

Tener instalado y activo postgresql.
Tener instalado mosquitto.
Ambiente de python con librerias del proyecto.
Variables de entorno necesarias para el proyecto
Stack de Nginx configurado y activo para el despligue en caso de estar en ambiente de producción.


# Como correr este proyecto

Con la base de datos Postgresql y el broker mosquitto como servicios activos, se puede proceder a correr este proyecto.

Lo primero es ubicarse en la carpeta docker_stack que contine los archivos de docker, docker compose y los archivos de configuración de las aplicaciones del stack utilizado por el proyecto. Se debe correr en el siguiente orden:

1. Correr el archivo Dockerfile para obtener la imagen de node-red modificada que contine los plugins necesarios para los flujos y la pestaña de actuadores. Para ello haremos uso del comando docker build . -t node-red-teg.
2. Correr el archivo de docker-compose para levantar la base de datos InfluxDB, la aplicación de Grafana y la apliación de Node-Red modificada, a traves del comando docker-compose up.
3. Levantado el ambiente de python con sus dependencias, se hace lo suigiente. En caso de ser la primera ejecución cargar en la base de datos de postgres los modelos requeridos de la apliación haciendo uso del comando python manage.py migrate y luego llenando la data incial requerida por la app con el comando python manage.py loaddata <fixture>, donde fixture son los archivos.json de cada modulo que sirven de fixture dentro del desarollo. Aparte se necesita crear un usuario administrador de la aplicación haciendo uso del comando django-admin createuser <nombre de usuario> con el que se iniciara la app por primera vez.
5. Si ya se ha corrido los pasos del framework django anteriormente yya se puede correr la apliación haciendo uso del comando python manage.py runserver <host>. Con ello la aplicación web se levantara junto a todos los modulos desarrollados. 
6. Si es la primera vez que se levanta el ambiente de la app será necesario ajustar los paneles iniciales de las apliaciones de grafana, node-red y la configuración de influxdb de forma que todos los componentes se comuniquen de manera adecuda. 