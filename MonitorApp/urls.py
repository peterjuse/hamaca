from django.urls import path
# from django.contrib.auth.decorators import login_required

from . import views

app_name = 'MonitorApp'
urlpatterns = [ 
    path('', views.to_grafana,name='grafana'),
]