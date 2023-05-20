import re
import os
import sys
import paho.mqtt.client as mqtt
from rfc3339 import rfc3339
from datetime import datetime, timezone, timedelta
from influxdb import InfluxDBClient

def on_connect(client, userdata, flags, rc):  # callback al conectarse al broker
    cliente.subscribe("#")  # Subscripcion a # para recibir todos los topicos
    from .models import MQTTdef
    topicos = MQTTdef.objects.all()
    for topico in topicos:
        diferencia = datetime.now(timezone.utc) - topico.hora
        if  diferencia.total_seconds >= 86400:
            topico.status = False
            topico.save()

def on_message(client, userdata, msg):  # callback al recibir un mensaje
    global bd
    global sensoresString
    #print("Topico: " + msg.topic + " Mensaje:" + str(msg.payload))
    topico = msg.topic

    # Aqui almaceno en BD el mensaje segun topico
    from .models import MQTTdef
    if MQTTdef.objects.filter(nombre=msg.topic).exists():
        bd_topic = MQTTdef.objects.get(nombre=msg.topic)
        bd_topic.cant_mensajes += 1
        bd_topic.payload = msg.payload.decode('utf-8')
        inicio_minuto = datetime.now(timezone.utc).replace(second=0, microsecond=0)
        fin_minuto = datetime.now(timezone.utc).replace(second=0, microsecond=0) + timedelta(seconds=60)
        if (inicio_minuto < bd_topic.hora) and (bd_topic.hora < fin_minuto):
            bd_topic.mensajes_minuto += 1
        else:
            bd_topic.mensajes_minuto = 1
        bd_topic.hora = datetime.now()
        bd_topic.save()
    else:
        bd_topic = MQTTdef(nombre=msg.topic,cant_mensajes=1, mensajes_minuto=1,payload=msg.payload.decode('utf-8'))
        bd_topic.save()

    topico = topico.split('/')
    ubicacion = topico[0]
    medida = topico[1]
    if ubicacion == 'Indoor':
        dispositivo = 'RPi3Javier'
    elif ubicacion == 'Seguridad':
        dispositivo = 'RPi3Peter'
    else:
        dispositivo = 'Arduino+iBookG4'
    payload = msg.payload.decode('utf-8')
    if ubicacion == 'Seguridad' and medida == 'Pantalla':
        nombre_sensor = 'LCD-16x2'
        variable = payload
        hora = rfc3339(datetime.now())
    elif ubicacion == 'Indoor' and medida == 'Buzzer' and \
        (payload == 'ON' or payload == 'OFF'):
        nombre_sensor = 'BUZZER'
        variable = payload
        hora = rfc3339(datetime.now())
    elif medida == 'Bombillos' and (payload == 'ON' or payload == 'OFF'):
        nombre_sensor = 'LED-BLANCO'
        variable = payload
        hora = rfc3339(datetime.now())
    else:
        payload = payload.replace('\n','').split(' - Hora: ')
        try:
            hora = rfc3339(datetime.strptime(payload[1],'%Y-%m-%d %H:%M:%S.%f'))
        except ValueError:  
            hora = rfc3339(datetime.strptime(payload[1],'%Y-%m-%d %H:%M:%S'))
        sensor = payload[0].split(': ')
        nombre_sensor = sensor[0]
        variable = sensor[1]
        if nombre_sensor not in sensoresString:
            if nombre_sensor == 'DHT11' and variable=='Error de lectura':
                variable = 'ERROR'
            else:
                variable = re.sub('[^0-9,.]','',
                    variable[variable.find(': ')+1:])
        if nombre_sensor == 'RASPICAM':
            variable = variable.replace('Persona detectada = ','')
    json = [{
            "measurement":medida,
            "tags": {
                "host": dispositivo,
                "region": ubicacion 
            },
            "fields": {
                "sensor": nombre_sensor,
                "variable": variable
            },
            "time": hora
        }]
    try:
        bd.write_points(json)
        #print('Insercion realizadsa correctamente')
    except Exception as e:
        print('Error al insertar dato')
    


sensoresString = [
                  'HC-SR501','LED-ROJO','LED-VERDE',
                  'LED-BLANCO','LED-RGB','MFRC522',
                  'RASPICAM','LCD-16x2','BUZZER','SG90'
                  ]
 
#if __name__ == '__main__':            
bd = InfluxDBClient(host='127.0.0.1',port=8086, username='gateway', 
                        password='MedicionesIoTDB',database='SensorData')
cliente = mqtt.Client("HAMACA")  
cliente.on_connect = on_connect  # callback de conexion
cliente.on_message = on_message  # callback al recibir un mensaje
cliente.connect('127.0.0.1')