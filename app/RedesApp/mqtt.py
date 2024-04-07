import os
import json
import paho.mqtt.client as mqtt

from rfc3339 import rfc3339
from datetime import datetime, timezone, timedelta
from influxdb import InfluxDBClient

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from time import sleep

def on_connect(client, userdata, flags, rc):  # callback al conectarse al broker
    sleep(.25)
    cliente.subscribe("#")  # Subscripcion a # para recibir todos los topicos
    from .models import MQTTdef
    topicos = MQTTdef.objects.all()
    for topico in topicos:
        diferencia = datetime.now(timezone.utc) - topico.hora
        if diferencia.total_seconds() >= 86400:
            topico.status = False
            topico.save()


def on_message(client, userdata, msg):  # callback al recibir un mensaje
    from .models import MQTTdef
    
    global bd
    global sensoresString

    try:
        topico = msg.topic
        payload = json.loads(msg.payload)
        # # Aqui almaceno en BD el mensaje segun topico
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
            bd_topic = MQTTdef(
                nombre=msg.topic,
                cant_mensajes=1,
                mensajes_minuto=1,
                payload=msg.payload.decode('utf-8')
            )
            bd_topic.save()
        try:
            hora = rfc3339(datetime.strptime(payload['date'],'%Y-%m-%d %H:%M:%S.%f'))
        except ValueError:
            try:
                hora = rfc3339(datetime.strptime(payload['date'],'%Y-%m-%d %H:%M:%S'))
            except ValueError:
                try:
                    hora = rfc3339(datetime.strptime(payload['date'],'%Y-%m-%dT%H:%M:%SZ'))
                except ValueError:
                    hora = rfc3339(datetime.strptime(payload['date'],'%Y-%m-%dT%H:%M:%S.%fZ'))
        except Exception as e:
            print(f'ocurrio el siguiente error con parseando la fecha:\n{e}')
        medicion = {
            "measurement":payload["measurement_type"],
            "tags": {
                "host": payload["host_device"],
                "region": payload["location"]
            },
            "fields": {
                "sensor": payload["sensor"],
                "valor": payload["value"]
            },
            "time": hora
        }
        try:
            print(f"Topico: {topico} - Medicion: {medicion}")
            write_api.write(bucket=bucket, record=medicion)
            print('Insercion realizada correctamente')
        except Exception as e:
            print(f'Ocurrió un error al insertar dato:\n{e}')
    except json.decoder.JSONDecodeError:
        pass


"""" codigo hardcoded de dispositivos para el onsmessage
# topico = topico.split('/')
        # ubicacion = topico[0]
        # medida = topico[1]
        # if ubicacion == 'Indoor':
        #     dispositivo = 'RPi3Javier'
        # elif ubicacion == 'Seguridad':
        #     dispositivo = 'RPi3Peter'
        # else:
        #     dispositivo = 'Arduino+iBookG4'
        # payload = msg.payload.decode('utf-8')
        # if ubicacion == 'Seguridad' and medida == 'Pantalla':
        #     nombre_sensor = 'LCD-16x2'
        #     variable = payload
        #     hora = rfc3339(datetime.now())
        # elif ubicacion == 'Indoor' and medida == 'Buzzer' and \
        #     (payload == 'ON' or payload == 'OFF'):
        #     nombre_sensor = 'BUZZER'
        #     variable = payload
        #     hora = rfc3339(datetime.now())
        # elif medida == 'Bombillos' and (payload == 'ON' or payload == 'OFF'):
        #     nombre_sensor = 'LED-BLANCO'
        #     variable = payload
        #     hora = rfc3339(datetime.now())
        # else:
        #     payload = payload.replace('\n','').split(' - Hora: ')
        #     try:
        #         hora = rfc3339(datetime.strptime(payload[1],'%Y-%m-%d %H:%M:%S.%f'))
        #     except ValueError:  
        #         hora = rfc3339(datetime.strptime(payload[1],'%Y-%m-%d %H:%M:%S'))
        #     sensor = payload[0].split(': ')
        #     nombre_sensor = sensor[0]
        #     variable = sensor[1]
        #     if nombre_sensor not in sensoresString:
        #         if nombre_sensor == 'DHT11' and variable=='Error de lectura':
        #             variable = 'ERROR'
        #         else:
        #             variable = re.sub('[^0-9,.]','',
        #                 variable[variable.find(': ')+1:])
        #     if nombre_sensor == 'RASPICAM':
        #         variable = variable.replace('Persona detectada = ','')
"""


#if __name__ == '__main__':            
# bd = InfluxDBClient(
#     host='localhost',
#     port=8086,
#     username='gateway',
#     password='MedicionesIoTDB',
#     database='SensorData'
# )
url = 'http://localhost:8086'
bucket = 'SensorData'
client = InfluxDBClient(
    url=url,
    #token= 'nLUGvTKJnLsL94YTr-H2Ms-N_0BZPoKj9G_i7ImqmWlZCQ2HLXg3Aywb7byo5T3m5psCip9CSUw-pjxplgV7FA==',
    token=os.getenv("INFLUXDB_TOKEN"),
    org='hamaca'
)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()


cliente = mqtt.Client("HAMACA")  
cliente.on_connect = on_connect  # callback de conexion
cliente.on_message = on_message  # callback al recibir un mensaje
cliente.connect('127.0.0.1')