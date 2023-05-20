from django.db import models

class variables(models.Model):
    nombre = models.CharField(max_length=50, help_text="El nombre de la variable global de la aplicacion")
    valor = models.TextField()

    def __str__(self):
        return self.nombre
