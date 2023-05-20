from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Sum
from .models import MQTTdef

@login_required(login_url='/')
def to_redes(request):
    #import pudb;pudb.set_trace()
    lista_topicos = MQTTdef.objects.all()
    cant_topicos = len(lista_topicos)
    cant_topicos_activos = len(MQTTdef.objects.filter(status=True))
    cant_mensajes_recibidos = MQTTdef.objects.aggregate(Sum('cant_mensajes'))
    mensajes_por_minuto = MQTTdef.objects.aggregate(Sum('mensajes_minuto'))
    paginator = Paginator(lista_topicos, 5)
    pagina = request.GET.get('pagina')
    topicos = paginator.get_page(pagina)
    context = {
        'topicos':topicos,
        'cant_mensajes_recibidos': cant_mensajes_recibidos['cant_mensajes__sum'],
        'mensaje_por_minuto': mensajes_por_minuto['mensajes_minuto__sum'],
        'cant_topicos': cant_topicos,
        'cant_topicos_activos': cant_topicos_activos,
    }
    return render(request,'redes.html',context)

def update_datos(request):
    if  request.method == "POST" and request.is_ajax():
        lista_topicos = MQTTdef.objects.all()
        cant_topicos = len(lista_topicos)
        cant_topicos_activos = len(MQTTdef.objects.filter(status=True))
        cant_mensajes_recibidos = MQTTdef.objects.aggregate(Sum('cant_mensajes'))
        mensajes_por_minuto = MQTTdef.objects.aggregate(Sum('mensajes_minuto'))
        data = {
            'cant_mensajes_recibidos': cant_mensajes_recibidos['cant_mensajes__sum'],
            'mensaje_por_minuto': mensajes_por_minuto['mensajes_minuto__sum'],
            'cant_topicos': cant_topicos,
            'cant_topicos_activos': cant_topicos_activos,
        }
        return JsonResponse(data)

