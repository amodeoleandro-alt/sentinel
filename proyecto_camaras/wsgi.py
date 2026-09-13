"""
Punto de entrada WSGI para desplegar en AlwaysData (o cualquier hosting con Python WSGI).

En el panel de AlwaysData, al crear el sitio tipo "Python WSGI" hay que apuntar
"Application path" a este archivo (por ejemplo: /proyecto_camaras/wsgi.py)
y el objeto que exporta se llama "application".
"""
import os

os.environ.setdefault("FLASK_ENV", "production")

from app import create_app

application = create_app("production")
