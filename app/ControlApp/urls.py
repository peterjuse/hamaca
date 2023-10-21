from django.urls import path
from . import views

app_name = 'ControlApp'
urlpatterns = [ 
    path('', views.to_nodered_recipes,name='noderedrecipes'),
]