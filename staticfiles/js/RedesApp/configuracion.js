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

$(function() {
    function update() {
        $.ajax({  
            type: "POST",  
            url: "update_datos",
            headers: {'X-CSRFToken': csrftoken },
            data:{},
            success: function(data) {
                $('#cant_mensajes_recibidos').text('Mensajes Recibidos: '+data.cant_mensajes_recibidos);
                $('#mensaje_por_minuto').text('Mensajes/min: '+data.mensaje_por_minuto);
                $('#cant_topicos').text('Cantidad de topicos: '+data.cant_topicos);
                $('#cant_topicos_activos').text('Topicos activos: '+data.cant_topicos_activos);
            }
        })
    }
    setInterval(update, 2000);
    update();
});

setTimeout(function() {
    location.reload();
  }, 15000);