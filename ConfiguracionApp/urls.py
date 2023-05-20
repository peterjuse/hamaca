from django.urls import path

from . import views

app_name = 'ConfiguracionApp'
urlpatterns = [ 
    path('', views.configuracion,name='configuracion'),
    path('existe_username',views.existe_username,name='existe_username'),
    path('crear_usuario',views.crear_usuario,name='crear_usuario'),
    path('get_datos_usuario',views.get_datos_usuario,name='get_datos_usuario'),
    path('update_service_url',views.update_service_url,name='update_service_url'),
    path('editar_usuario',views.editar_usuario,name='editar_usuario'),
    path('borrar_usuario',views.borrar_usuario,name='borrar_usuario'),
]