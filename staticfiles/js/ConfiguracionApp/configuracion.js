// Funciones hechas en javascript para el template/vista de configuracion

// Funcion para tener el token CSRF
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

// Funcion para copiar el contenido del formulario de creacion de usuario
// al de validacion
function CopiarFomularioCrearUsuario() {
    datosRegistro = {};
    $.each($('#registroUsuario').serializeArray(),function(i,campo){
        datosRegistro[campo.name]=campo.value;
    });
    $('#usernameVR').val(datosRegistro.usuario);
    $('#firstNameVR').val(datosRegistro.nombre);
    $('#lastNameVR').val(datosRegistro.apellido);
    $('#emailVR').val(datosRegistro.correo);
};

// Funciones para validar los campos requeridos para la creacion de usuarios
function validarNombreUsuarioCrear(usuario){
    var array=[false,false,false,false];
    // Verifica si el nombre de usuario existe
    $.ajax({  
        type: "POST",  
        url: "existe_username",
        headers: {'X-CSRFToken': csrftoken },
        data: {
            'usuario': usuario,
        },
        success: function(data) {
            if(data.existe) {
                $($($('#reqUsuario ul li')[0]).children()[0]).css(
                    'display','inline');
                $($($('#reqUsuario ul li')[0]).children()[1]).css(
                    'display','contents');
                $($('#reqUsuario ul li')[0]).removeClass(
                    'req-aproved').addClass('req');
            }
            else{
                $($($('#reqUsuario ul li')[0]).children()[1]).css(
                    'display','inline');
                $($($('#reqUsuario ul li')[0]).children()[0]).css(
                    'display','contents');
                $($('#reqUsuario ul li')[0]).removeClass(
                    'req').addClass('req-aproved');
            }
        }
    })
    // Verifica el largo del nombre de usuario
    if(usuario.length > 3 && usuario.length < 16) {
        $($($('#reqUsuario ul li')[1]).children()[1]).css('display','inline');
        $($($('#reqUsuario ul li')[1]).children()[0]).css('display','contents');
        $($('#reqUsuario ul li')[1]).removeClass('req').addClass('req-aproved');
        array[1]=true;
    }
    else{
        $($($('#reqUsuario ul li')[1]).children()[0]).css('display','inline');
        $($($('#reqUsuario ul li')[1]).children()[1]).css('display','contents');
        $($('#reqUsuario ul li')[1]).removeClass('req-aproved').addClass('req');
        array[1]=false;
    }
    // Verifica que el nombre de usuario comience con una letra
    if(usuario.match(/^[A-Za-z]/)) {
        $($($('#reqUsuario ul li')[2]).children()[1]).css('display','inline');
        $($($('#reqUsuario ul li')[2]).children()[0]).css('display','contents');
        $($('#reqUsuario ul li')[2]).removeClass('req').addClass('req-aproved');
        array[2]=true;
    }
    else{
        $($($('#reqUsuario ul li')[2]).children()[0]).css('display','inline');
        $($($('#reqUsuario ul li')[2]).children()[1]).css('display','contents');
        $($('#reqUsuario ul li')[2]).removeClass('req-aproved').addClass('req');
        array[2]=false;
    }
    // Los nombres de usuario solo pueden contener caracteres alfanumericos 
    // y caracteres especiales _, @, +, . y - en Django
    if(usuario.match(/^[a-z0-9_@+.-]+$/i)) {
        $($($('#reqUsuario ul li')[3]).children()[1]).css('display','inline');
        $($($('#reqUsuario ul li')[3]).children()[0]).css('display','contents');
        $($('#reqUsuario ul li')[3]).removeClass('req').addClass('req-aproved');
        array[3]=true;
    }
    else{
        $($($('#reqUsuario ul li')[3]).children()[0]).css('display','inline');
        $($($('#reqUsuario ul li')[3]).children()[1]).css('display','contents');         
        $($('#reqUsuario ul li')[3]).removeClass('req-aproved').addClass('req');
        array[3]=false;
    }
    if(array[1]==true && array[2]==true && array[3]==true){
        return true;
    }else{
        return false;
    }
};

function validarEmailUsuarioCrear(email){
    //  Valida el formato del string de correo electronico 
    var validar;
    if(email.match(/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/)){
        $($($('#reqEmail ul li')[0]).children()[1]).css('display','inline');
        $($($('#reqEmail ul li')[0]).children()[0]).css('display','contents')         
        $($('#reqEmail ul li')[0]).removeClass('req').addClass('req-aproved');
        validar = true;
    }
    else{
        $($($('#reqEmail ul li')[0]).children()[0]).css('display','inline');
        $($($('#reqEmail ul li')[0]).children()[1]).css('display','contents')         
        $($('#reqEmail ul li')[0]).removeClass('req-aproved').addClass('req');
        validar = false;
    }
    return validar;
};

function validarPasswordUsuarioCrear(password){
    var array = [false,false,false,false];
    // Validacion de la longitud del password
    if(password.length > 7 && password.length < 16){
        $($($('#reqPassword ul li')[0]).children()[1]).css('display','inline');
        $($($('#reqPassword ul li')[0]).children()[0]).css('display','contents');         
        $($('#reqPassword ul li')[0]).removeClass('req').addClass('req-aproved');
        array[0] = true;
    }
    else{
        $($($('#reqPassword ul li')[0]).children()[0]).css('display','inline');
        $($($('#reqPassword ul li')[0]).children()[1]).css('display','contents');         
        $($('#reqPassword ul li')[0]).removeClass('req-aproved').addClass('req');
        array[0] = false;
    }
    // Validacion de tener al menos una letra mayuscula
    if(password.match(/^(?=.*[A-Z]).+$/)){
        $($($('#reqPassword ul li')[1]).children()[1]).css('display','inline');
        $($($('#reqPassword ul li')[1]).children()[0]).css('display','contents');         
        $($('#reqPassword ul li')[1]).removeClass('req').addClass('req-aproved');
        array[1] = true;
    }
    else{
        $($($('#reqPassword ul li')[1]).children()[0]).css('display','inline');
        $($($('#reqPassword ul li')[1]).children()[1]).css('display','contents');         
        $($('#reqPassword ul li')[1]).removeClass('req-aproved').addClass('req');
        array[1] = false;
    }
    // Validacion de tener al menos un numero
    if(password.match(/^(?=.*[\d]).+$/)){
        $($($('#reqPassword ul li')[2]).children()[1]).css('display','inline');
        $($($('#reqPassword ul li')[2]).children()[0]).css('display','contents');         
        $($('#reqPassword ul li')[2]).removeClass('req').addClass('req-aproved');
        array[2] = true;
    }
    else{
        $($($('#reqPassword ul li')[2]).children()[0]).css('display','inline');
        $($($('#reqPassword ul li')[2]).children()[1]).css('display','contents');         
        $($('#reqPassword ul li')[2]).removeClass('req-aproved').addClass('req');
        array[2] = false;
    }
    // Validacion de tener al menos un caracter especial
    if(password.match(/(?:[^`!@#$%^&*\-_=+.]*[`!@#$%^&*\-_=+.])/)){
        $($($('#reqPassword ul li')[3]).children()[1]).css('display','inline');
        $($($('#reqPassword ul li')[3]).children()[0]).css('display','contents');         
        $($('#reqPassword ul li')[3]).removeClass('req').addClass('req-aproved');
        array[3] = true;
    }
    else{
        $($($('#reqPassword ul li')[3]).children()[0]).css('display','inline');
        $($($('#reqPassword ul li')[3]).children()[1]).css('display','contents');         
        $($('#reqPassword ul li')[3]).removeClass('req-aproved').addClass('req');
        array[3] = false;
    }
    if(array[0]==true && array[1]==true && array[2]==true && array[3]==true){
        return true;
    }else{
        return false;
    }
};

function revalidarPasswordUsuarioCrear(repassword,password){
    // El campo de password debe ser igual
    var validar;
    if(repassword == password){
        $($($('#reqRePassword ul li')[0]).children()[1]).css('display','inline');
        $($($('#reqRePassword ul li')[0]).children()[0]).css('display','contents')         
        $($('#reqRePassword ul li')[0]).removeClass('req').addClass('req-aproved');
        validar = true;
    }
    else{
        $($($('#reqRePassword ul li')[0]).children()[0]).css('display','inline');
        $($($('#reqRePassword ul li')[0]).children()[1]).css('display','contents')         
        $($('#reqRePassword ul li')[0]).removeClass('req-aproved').addClass('req');
        validar = false;
    }
    return validar;
};

// Funcion para comunicar la creacion de usuario
function crearUsuario(){
    datosRegistro = {};
    $.each($('#registroUsuario').serializeArray(),function(i,campo){
        datosRegistro[campo.name]=campo.value;
    });
    $.ajax({  
        type: "POST",  
        url: "crear_usuario",
        headers: {'X-CSRFToken': csrftoken },
        data: {
            'usuario': datosRegistro.usuario,
            'nombre': datosRegistro.nombre,
            'apellido': datosRegistro.apellido,
            'email': datosRegistro.correo,
            'password': datosRegistro.password,
            'repassword': datosRegistro.repassword,
        },
        success: function(data) {
            //  Cerrando modal actual, mostrando modal resultado
            $('#modalValidarRegistroUsuario').modal('hide');
            $('#modalResultadoCrearUsuario').modal();
            $('#UsuarioCreadoStatus').text(data.ModalTitulo);
            $('#msgModalCrearUsuarioRes').text(data.ModalResultado);
            // Si se encuentran errores se despliegan en el modal
            if(data.errores){
                $('#msgModalCrearUsuarioRes').append(
                    '<ul id="listaErrores"></ul>');
                $.each(data.errores, function(i,val) {
                    $('#listaErrores').append('<li>'+val+'</li>');
                });
                $('#msgModalCrearUsuarioRes').append(
                    '<p>Presione cerrar para continuar.</p>');
            }
            // Borrado del formulario inicial
            $('#registroUsuario')[0].reset();
            $('#botonCrear').attr("disabled", true);
        }
    })
}

function rstModalRes(modal){   
    $('#'+modal.id+' .modal-dialog .modal-content .modal-header h5').text('');
    $('#'+modal.id+' .modal-dialog .modal-content .modal-body p').empty();
    validarNombreUsuarioCrear('');
    validarEmailUsuarioCrear('');
    validarPasswordUsuarioCrear('');
    revalidarPasswordUsuarioCrear(' ');
    location.reload();
}

function abrirModalEditarUsuario(userid){
    $.ajax({  
        type: "POST",  
        url: "get_datos_usuario",
        headers: {'X-CSRFToken': csrftoken },
        data: {
            'id_usuario': userid,
        },
        success: function(data) {
            if(!data.hasOwnProperty("error")){
                $('input[name=up_usuario]').val(data['up_username']);
                $('input[name=up_nombre]').val(data['up_nombre']);
                $('input[name=up_apellido]').val(data['up_apellido']);
                $('input[name=up_correo]').val(data['up_correo']);
                $("#modalEditarUsuario").modal('show');
            }else{
                alert(data['error']);
            }
        }
    });
}

function abrirModalBorrarUsuario(userid){
    $("#modalSeguroBorrarUsuario").modal('show');
    useridBorrar =  userid
}

// Funcion para guardar URL de grafana
function guardarGrafanaURL(){
    var nuevaurl = $("#grafanaurl").text()
    $.ajax({  
        type: "POST",  
        url: "update_service_url",
        headers: {'X-CSRFToken': csrftoken },
        data: {
            'grafana_url': nuevaurl,
        },
        success: function(data) {
            location.reload();
        }
    })
}

// Funcion para guardar URL de Node-RED
function guardarNodeREDURL(){
    var nuevaurl = $("#noderedurl").text()
    $.ajax({  
        type: "POST",  
        url: "update_service_url",
        headers: {'X-CSRFToken': csrftoken },
        data: {
            'nodered_url': nuevaurl,
        },
        success: function(data) {
            location.reload();
        }
    })
}

//  Funcion para guardar el valor del formulario de edicion de usuario
var datosEdicion = {}
function CopiarFomularioEditarUsuario(){
    $.each($('#edicionUsuario').serializeArray(),function(i,campo){
        datosEdicion[campo.name]=campo.value;
    });
    datosEdicion["up_usuario"]=$("input[name='up_usuario']").val()
}

// Funcion para comunicar la edicion del usuario
function editarUsuario(){
    pass = $("#validarPasswordEditarUsuario").val(),
    $.ajax({  
        type: "POST",  
        url: "editar_usuario",
        headers: {'X-CSRFToken': csrftoken },
        data: {
            'pass': pass,
            'usuario': datosEdicion.up_usuario,
            'nombre': datosEdicion.up_nombre,
            'apellido': datosEdicion.up_apellido,
            'email': datosEdicion.up_correo,
            'password': datosEdicion.up_contrasena,
            'repassword': datosEdicion.up_contrasenavalidate,
        },
        success: function(data) {
            //  Cerrando modal actual, mostrando modal resultado
            $('#modalValidarEditarUsuario').modal('hide');
            $('#modalResultadoEditarUsuario').modal();
            $('#UsuarioEditadoStatus').text(data.ModalTitulo);
            $('#msgModalEditarUsuarioRes').text(data.ModalResultado);
            // Si se encuentran errores se despliegan en el modal
            if(data.errores){
                $('#msgModalEditarUsuarioRes').append(
                    '<ul id="listaErrores"></ul>');
                $.each(data.errores, function(i,val) {
                    $('#listaErrores').append('<li>'+val+'</li>');
                });
                $('#msgModalEditarUsuarioRes').append(
                    '<p>Presione cerrar para continuar.</p>');
            }
            // Borrado del formulario inicial
            // $('#registroUsuario')[0].reset();
            // $('#botonCrear').attr("disabled", true);
        }
    })
}

var useridBorrar;

// Funcion para comunicar el borrado de un usuario
function borrarUsuario(){
    $.ajax({  
        type: "POST",  
        url: "borrar_usuario",
        headers: {'X-CSRFToken': csrftoken },
        data: {
            'id_usuario': useridBorrar,
            'password': $('#validarPasswordBorarUsuario').val(),
        },
        success: function(data) {
            //  Cerrando modal actual, mostrando modal resultado
            $('#modalValidarBorrarUsuario').modal('hide');
            $('#modalResultadoBorrarUsuario').modal();
            $('#UsuarioBorrarStatus').text(data.ModalTitulo);
            $('#msgModalBorrarUsuarioRes').text(data.ModalResultado);
            // Si se encuentran errores se despliegan en el modal
            if(data.errores){
                $('#msgModalBorrarUsuarioRes').append(
                    '<ul id="listaErrores"></ul>');
                $.each(data.errores, function(i,val) {
                    $('#listaErrores').append('<li>'+val+'</li>');
                });
                $('#msgModalBorrarUsuarioRes').append(
                    '<p>Presione cerrar para continuar.</p>');
            }
        }
    });
}

var habilitarBotonCrearUsuario = [false,false,false,false]
// var habilitarBotonEditarUsuario = [false,false,false]

$(document).ready(function(){
    // Validaciones dentro del modal de crear usuario
    $("#usuario").on('input',function(event){
        var usuario = $('#usuario').val();
        habilitarBotonCrearUsuario[0] = validarNombreUsuarioCrear(usuario);
    });
    $('#usuario').focusin(function(){
        var popup = document.getElementById("reqUsuario");
        popup.classList.toggle("show");
        for(i=0;i<3;i++){
            $($($('#reqUsuario ul li')[i]).children()[0]).show();
            $($($('#reqUsuario ul li')[i]).children()[1]).show();
        }
    });
    $('#usuario').focusout(function(){
        var popup = document.getElementById("reqUsuario");
        popup.classList.toggle("show");
        for(i=0;i<3;i++){
            $($($('#reqUsuario ul li')[i]).children()[0]).hide();
            $($($('#reqUsuario ul li')[i]).children()[1]).hide();
        }
    });

    $("#email").on('input',function(event){
        var email = $("#email").val();
        habilitarBotonCrearUsuario[1] = validarEmailUsuarioCrear(email);
    });
    $('#email').focusin(function(){
        var popup = document.getElementById('reqEmail');
        popup.classList.toggle("show");
        $($($('#reqEmail ul li')[0]).children()[0]).show();
    });
    $("#email").focusout(function(){
        var popup = document.getElementById('reqEmail');
        popup.classList.toggle("show"); 
        $($($('#reqEmail ul li')[0]).children()[0]).show();
    });

    $("#password").on('input',function(event){
        var password = $("#password").val();
        habilitarBotonCrearUsuario[2] = validarPasswordUsuarioCrear(password);
    });
    $('#password').focusin(function(){
        var popup = document.getElementById('reqPassword');
        popup.classList.toggle("show");
        $($($('#reqPassword ul li')[0]).children()[0]).show();
    });
    $("#password").focusout(function(){
        var popup = document.getElementById('reqPassword');
        popup.classList.toggle("show"); 
        $($($('#reqPassword ul li')[0]).children()[0]).show();
    });

    $("#repassword").on('input',function(event){
        var repassword = $("#repassword").val();
        var password = $("#password").val();
        habilitarBotonCrearUsuario[3] = revalidarPasswordUsuarioCrear(
            repassword,password);
        if(habilitarBotonCrearUsuario[0] == true && 
            habilitarBotonCrearUsuario[1] == true && 
            habilitarBotonCrearUsuario[2] == true && 
            habilitarBotonCrearUsuario[3] == true) {
            $('#botonCrear').removeAttr("disabled");
        }
        else{
            $('#botonCrear').attr("disabled", true);
        }
    });
    $('#repassword').focusin(function(){
        var popup = document.getElementById('reqRePassword');
        popup.classList.toggle("show");
        $($($('#reqRePassword ul li')[0]).children()[0]).show();
    });
    $("#repassword").focusout(function(){
        var popup = document.getElementById('reqRePassword');
        popup.classList.toggle("show"); 
        $($($('#reqRePassword ul li')[0]).children()[0]).show();
    });
});


