#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", 
        "config.settings.development")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No fue posible importar Django. ¿Esta seguro que esta instalado y "
            "esta disponible la variavle de entorno PYTHONPATH? ¿No ha "
            "olvidado activar el entorno virtual?"
        ) from exc
    execute_from_command_line(sys.argv)
