import pandas as pd

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, FactorRange, HoverTool
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.sampledata.commits import data
from bokeh.transform import jitter
from bokeh.models.formatters import DatetimeTickFormatter
from influxdb import InfluxDBClient, DataFrameClient
from math import pi


@login_required(login_url='/')
def to_procesamiento(request):
    # cliente = InfluxDBClient(host='127.0.0.1',port=8086, username='gateway',
    #                     password='MedicionesIoTDB',database='SensorData')
    # # Query de obtencion de las ubicaciones
    # res = cliente.query('SHOW TAG VALUES WITH KEY="region"')
    # cliente.close()
    # ubicaciones = set()
    # for i in res:
    #     ubicaciones.add(i[0]['value'])

    # plot = figure(plot_height=300, sizing_mode='scale_width',
    #                 tools="pan,wheel_zoom,box_zoom,reset")
    # x = []
    # y = []
    # script, div = components(plot)

    # context = {
    #     'ubicaciones':sorted(ubicaciones),
    #     'script': script,
    #     'div': div,
    # }   
    return render(request,'procesamiento.html')#,context)


def obtener_ubicaciones(request):
    if  request.method == "POST" and is_ajax(request):
        ubicacion = request.POST.get('ubicacion')
        cliente = InfluxDBClient(host='127.0.0.1',port=8086, username='gateway',
                                password='MedicionesIoTDB',database='SensorData')
        #Query de obtencion de los dispositivos de una determinada ubicacion
        respuesta = cliente.query("SHOW TAG VALUES WITH KEY=host WHERE region='" + 
                                    ubicacion + "'")
        cliente.close()
        dispositivos = set()
        for i in respuesta:
            dispositivos.add(i[0]['value'])
    data = {
        'lista':sorted(dispositivos),
    }
    return JsonResponse(data)   


def obtener_dispositivos(request):
    if  request.method == "POST" and is_ajax(request):
        dispositivo = request.POST.get('dispositivo')
        cliente = InfluxDBClient(host='127.0.0.1',port=8086, username='gateway',
                                password='MedicionesIoTDB',database='SensorData')
        #Query de obtencion de los dispositivos de una determinada ubicacion
        respuesta = cliente.query("SHOW MEASUREMENTS WHERE host='" + dispositivo +"'")        
        cliente.close()
        mediciones = set()
        for i in respuesta:
            for j in i:
                mediciones.add(j['name'])
    data = {
        'lista':sorted(mediciones),
    }
    return JsonResponse(data)     


def obtener_mediciones(request):
    if  request.method == "POST" and is_ajax(request):
        # Query de obtencion de los datos de una medicion
        dispositivo = request.POST.get('dispositivo')
        medicion = request.POST.get('medicion')
        cliente = DataFrameClient(host='127.0.0.1',port=8086, username='gateway',
                                password='MedicionesIoTDB',database='SensorData')                            
        respuesta = cliente.query("select time,variable from "+ medicion +
                                " where host='" + dispositivo + 
                                "' and time < now() and time > now()-7d")
        cliente.close()
        df = respuesta[medicion]
        df.index = pd.to_datetime(df.index)
        df.replace(to_repace = "Error", value = df["variable"].mean())
        plot = figure(plot_height=300, sizing_mode='scale_width',title=medicion, toolbar_location="right")
        x = df.index
        y = df.variable
        plot.line(x, y, line_width=4)
        hover = HoverTool(
            tooltips = [
                ("Fecha", "$index{%d-%m-%Y %H:%M:%S.%3N}"),
                ("Medicion", "$variable")
            ],
            formatters={
                'Date': 'datetime',
                'variable' : 'printf',
            },
        )
        plot.add_tools(hover)
        plot.xaxis.formatter=DatetimeTickFormatter(
            seconds = ["%Y-%m-%d %H:%M:%S"],
            minsec = ["%Y-%m-%d %H:%M:%S"],
            minutes = ["%Y-%m-%d %H:%M:%S"],
            hourmin = ["%Y-%m-%d %H:%M:%S"],
            hours=["%Y-%m-%d %H:%M:%S"],
            days=["%Y-%m-%d %H:%M:%S"],
            months=["%Y-%m-%d %H:%M:%S"],
            years=["%Y-%m-%d %H:%M:%S"],
        )
        plot.xaxis.major_label_orientation = pi/3
        script, div = components(plot)
        data = {
           'script': script,
           'div': div,
        }   
        return JsonResponse(data)  


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
