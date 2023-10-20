import re

from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import variables


def validar_datos_usuario(datos):
    errores = {}
    # Validaciones del formato del nombre de usuario
    if User.objects.filter(username__iexact=datos['usuario']).exists():
        errores['usuario1'] = "El nombre de usuario ya existe."
    if len(datos['usuario']) < 4 or len(datos['usuario']) > 15:
        errores['usuario2'] = "El nombre de usuario no posee la longitud " \
                            "correcta."
    if not datos['usuario'][0].isalpha():
        errores['usuario3'] = "El nombre de usuario debe comenzar con una " \
                            "letra."
    if not re.match('^[a-z0-9_@+.-]+$', datos['usuario']):
        errores['usuario4'] = "El nombre de usuario solo puede tener " \
                            "n&uacute;meros, letras o los caracteres _, @, +," \
                            " ., -."
    # Validaciones del formato de correo electronico
    if not re.match("[^@]+@[^@]+\.[^@]+", datos['email']):
        errores['email'] = "El correo electronico debe tener un formato valido."
    # Validaciones del formato de password
    if len(datos['password']) < 8 or len(datos['password']) > 15:
        errores['password1'] = "La contrase&ntilde;a debe poseer entre 8 y 15 " \
                                "caracteres."
    if not re.match('^(?=.*[a-zA-Z].+$)', datos['password']):
        errores['password2'] = "La contrase&ntilde;a debe poseer al menos una" \
                                " letra."
    if not any(char.isdigit() for char in datos.get('password')):
        errores['password3'] = "La contrase&ntilde;a debe poseer al menos un " \
                                "n&uacute;mero."
    if not re.match('(?:[^`!@#$%^&*\-_=+.]*[`!@#$%^&*\-_=+.])', datos['password']):
        errores['password4'] = "La contrase&ntilde;a solo puede tener los " \
                                "siguientes caracteres especiales: !, @, #, $, " \
                                " %, ^, &, *, -, _, =, +, . o ?."
    # Validacion de password igual a repassword
    if datos['password'] != datos['repassword']:
        errores['repassword'] = "Las contase&ntilde;as deben coincidir." 
    return errores


@login_required(login_url='/')
def configuracion(request):
    # Vista (Template) de configuracion de la aplicacion
    context = RequestContext(request)
    lista_usuarios = User.objects.all()
    grafana = variables.objects.get(pk=1)
    nodered = variables.objects.get(pk=2)
    paginator = Paginator(lista_usuarios, 5)
    pagina = request.GET.get('pagina')
    usuarios = paginator.get_page(pagina)
    context = {
        'usuarios':usuarios,
        'grafanaURL':grafana.valor,
        'noderedURL':nodered.valor
    }
    return render(request,'configuracion.html',context)


def existe_username(request):
    if  request.method == "POST" and is_ajax(request):
        username = request.POST.get('usuario', None)
        data = {
            'existe': User.objects.filter(username__iexact=username).exists()
        }
        return JsonResponse(data)


def crear_usuario(request):
    if request.method == "POST" and is_ajax(request):
        datos = request.POST
        errores = validar_datos_usuario(datos)
        data = {}
        if len(errores) > 0:
            data['ModalTitulo'] = "El usuario no ha sido creado " \
                                    "correctamente"
            data['ModalResultado'] = "La operación no se ha realizado. " \
                                    "Se han producido los siguientes errores:\n"
            data['errores'] = errores
        else:
            usuario = User.objects.create_user(
                datos['usuario'],
                datos['email'],
                datos['password']
            )
            usuario.first_name = datos['nombre']
            usuario.last_name = datos['apellido']
            usuario.save()
            data['ModalTitulo'] = "El usuario ha sido creado satisfactoriamente"
            data['ModalResultado'] = "La operación se ha realizado " \
                                    "correctamente. Presione cerrar para " \
                                    "continuar."
        return JsonResponse(data)


def get_datos_usuario(request):
    if  request.method == "POST" and is_ajax(request):
        user_id = request.POST.get('id_usuario',None)
        import pudb; pudb.set_trace()
        if user_id and (user_id == str(request.user.id) or request.user.is_superuser):
            usuario = User.objects.get(pk=user_id)
            data = {
                'up_username': usuario.username,
                'up_nombre':usuario.first_name,
                'up_apellido':usuario.last_name,
                'up_correo':usuario.email,
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error':'Usted no posee privilegios para editar el usuario'})


def update_service_url(request):
    if  request.method == "POST" and is_ajax(request):
        grafana_url = request.POST.get('grafana_url',None)
        nodered_url = request.POST.get('nodered_url',None)
        if nodered_url:
            nodered = variables.objects.get(pk=2)
            nodered.valor = nodered_url
            nodered.save()
        else:
            grafana = variables.objects.get(pk=1)
            grafana.valor = grafana_url
            grafana.save()
        data = {}
        return JsonResponse(data)


def editar_usuario(request):
    if request.method == "POST" and is_ajax(request):
        datos = request.POST
        errores = {}
        data = {}
        passw = datos.get('pass',None)
        usuario = User.objects.get(username=datos.get('usuario'))
        if usuario and passw is not None:
            if usuario.check_password(passw):
                # Validaciones del formato de correo electronico
                if datos.get('email'):
                    if not re.match("[^@]+@[^@]+\.[^@]+", datos.get('email')):
                        errores['email'] = "El correo electronico debe tener un formato valido."
                if datos.get('password'):
                    # Validaciones del formato de password
                    if len(datos.get('password')) < 8 or len(datos.get('password')) > 15:
                        errores['password1'] = "La contrase&ntilde;a debe poseer entre 8 y 15 " \
                                                "caracteres."
                    if not re.match('^(?=.*[a-zA-Z].+$)', datos.get('password')):
                        errores['password2'] = "La contrase&ntilde;a debe poseer al menos una" \
                                                " letra."
                    if not any(char.isdigit() for char in datos.get('password')):
                        errores['password3'] = "La contrase&ntilde;a debe poseer al menos un " \
                                                "n&uacute;mero."
                    if not re.match('(?:[^`!@#$%^&*\-_=+.]*[`!@#$%^&*\-_=+.])', datos.get('password')):
                        errores['password4'] = "La contrase&ntilde;a solo puede tener los " \
                                                "siguientes caracteres especiales: !, @, #, $, " \
                                                " %, ^, &, *, -, _, =, +, . o ?."
                    # Validacion de password igual a repassword
                    if datos.get('password') != datos.get('repassword'):
                        errores['repassword'] = "Las contase&ntilde;as deben coincidir."
            else:
                errores['same_password']= "La contrase&ntilde;a del usuario no es correcta"
            if not errores:
                if datos.get('nombre') == usuario.first_name:
                    usuario.first_name = datos.get('nombre')
                if datos.get('apellido') == usuario.last_name:
                    usuario.last_name = datos.get('apellido')
                if datos.get('email') == usuario.email:
                    usuario.email = datos.get('email')
                if datos.get('password') and datos.get('password') == usuario.password:
                    usuario.set_password(datos.get('password'))
                usuario.save()        
                data['ModalTitulo'] = "El usuario ha sido editado satisfactoriamente"
                data['ModalResultado'] = "La operación se ha realizado " \
                                    "correctamente. Presione cerrar para " \
                                    "continuar."
            else:
                data['ModalTitulo'] = "El usuario no ha sido editado " \
                                    "correctamente"
                data['ModalResultado'] = "La operación no se ha realizado. " \
                                    "Se han producido los siguientes errores:\n"
                data['errores'] = errores
    return JsonResponse(data)


def borrar_usuario(request):
    if request.method == "POST" and is_ajax(request):
        datos = request.POST
        data = {}
        errores = {}
        password = datos.get('password',None)
        usuario = User.objects.get(pk=datos.get('id_usuario'))
        if usuario and password is not None:
            if not usuario.check_password(password):
                errores['same_password']= "La contrase&ntilde;a del usuario no es correcta"
            if not errores:
                usuario.delete()
                data['ModalTitulo'] = "El usuario ha sido eliminado satisfactoriamente"
                data['ModalResultado'] = "La operación se ha realizado " \
                                    "correctamente. Presione cerrar para " \
                                    "continuar."
            else:
                data['ModalTitulo'] = "El usuario no ha sido eliminado "
                data['ModalResultado'] = "La operación no se ha realizado. " \
                                    "Se han producido los siguientes errores:\n"
                data['errores'] = errores
    return JsonResponse(data)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
