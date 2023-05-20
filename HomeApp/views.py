from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from ConfiguracionApp.models import variables


@login_required(login_url='/')
def to_nodered_control(request):
    # Hacer lo necesario para el set de variables
    context = RequestContext(request)
    nodered = variables.objects.get(pk=2)
    context = {
        'noderedURL':nodered.valor
    }
    return render(request,'nodered1.html',context)
