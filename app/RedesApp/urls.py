from django.urls import path

from . import views

app_name = 'RedesApp'
urlpatterns = [
    path('', views.to_redes,name='redes'),
    path('update_datos',views.update_datos,name='update_datos'),
    #path('update_table',views.update_table,name='update_table'),
]