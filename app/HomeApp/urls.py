from django.urls import path
# from django.contrib.auth.decorators import login_required

from . import views

app_name = 'HomeApp'
urlpatterns = [ 
    path('home', views.to_nodered_control,name='noderedcontrol'),
]