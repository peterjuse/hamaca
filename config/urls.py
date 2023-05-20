"""hamaca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import login, logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',login, {'template_name':'login.html'},name='login'),
    path('salir',logout,{'next_page':'/'},name="salir"),
    path('hamaca/',include('HomeApp.urls')),
    path('hamaca/monitor/',include('MonitorApp.urls')),
    path('hamaca/control/',include('ControlApp.urls')),
    path('hamaca/redes/',include('RedesApp.urls')), 
    path('hamaca/procesamiento/',include('ProcesamientoApp.urls')),
    path('hamaca/configuracion/',include('ConfiguracionApp.urls')),   
]
