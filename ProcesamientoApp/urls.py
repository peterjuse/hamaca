from django.urls import path
from . import views

app_name = 'ProcesamientoApp'
urlpatterns = [ 
    path('', views.to_procesamiento,name='procesamiento'),
    path('obtener_ubicaciones',views.obtener_ubicaciones,name='obtener_ubicaciones'),
    path('obtener_dispositivos',views.obtener_dispositivos,name='obtener_dispositivos'),
    path('obtener_mediciones',views.obtener_mediciones,name='obtener_mediciones'),
]