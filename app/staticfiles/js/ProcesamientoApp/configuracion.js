// Funciones hechas en javascript para el template/vista de procesamiento

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

function seleccionar_ubicacion(value){
    $.ajax({  
        type: "POST",  
        url: "obtener_ubicaciones",
        headers: {'X-CSRFToken': csrftoken },
        data: {
            'ubicacion': value,
        },
        success: function(data) {
            $('#columndispositivo').removeAttr('hidden');
            $('#dispositivoslista').empty();
            $('#medicioneslista').empty();
            $('#medicioneslista').append('<option value="Selecionar" label="Selecionar"></option>');
            $('#dispositivoslista').append('<option value="Selecionar" label="Selecionar"></option>');
            $.each(data.lista,function(i,val){
                $('#dispositivoslista').append('<option value="' + val + '" label="'+ val +'"></option>');
            });
        }
    })
}

function seleccionar_dispositivo(value){
    $.ajax({  
        type: "POST",  
        url: "obtener_dispositivos",
        headers: {'X-CSRFToken': csrftoken },
        data: {
            'dispositivo': value,
        },
        success: function(data) {
            $('#columnmedicion').removeAttr('hidden');
            $('#medicioneslista').empty();
            $('#medicioneslista').append('<option value="Selecionar" label="Selecionar"></option>');
            $.each(data.lista,function(i,val){
                $('#medicioneslista').append('<option value="' + val + '" label="'+ val +'"></option>');
            });
        }
    })
}

function seleccionar_medicion(value){
    $.ajax({  
        type: "POST",  
        url: "obtener_mediciones",
        headers: {'X-CSRFToken': csrftoken },
        data: {
            'dispositivo': $('#dispositivoslista').val(),
            'medicion': value,
        },
        success: function(data) {
            $('#procedimientoOptimizacion').removeAttr('hidden');
            $('#bokeh_graph').html(data.div);
            $("head").append(data.script)
        }
    })
}