from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from ConfiguracionApp.models import variables


@login_required(login_url='/')
def to_grafana(request):
    # Hacer lo necesario para el set de variables
    context = RequestContext(request)
    grafana = variables.objects.get(pk=1)
    context = {
        'grafanaURL':grafana.valor
    }
    return render(request,'grafana.html',context)