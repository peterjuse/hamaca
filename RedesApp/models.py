from django.db import models

class MQTTdef(models.Model):
    nombre = models.CharField(max_length=200, help_text="")
    status = models.BooleanField(default=True)
    cant_mensajes = models.PositiveIntegerField(default=0)
    mensajes_minuto = models.PositiveIntegerField(default=0)
    payload = models.TextField()
    hora = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    