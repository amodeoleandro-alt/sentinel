from datetime import datetime
from flask_login import UserMixin
from extensions import db


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default="usuario")  # 'usuario' | 'administrador'
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    ultimo_login = db.Column(db.DateTime, nullable=True)
    activo = db.Column(db.Boolean, default=True)

    def es_admin(self):
        return self.rol == "administrador"


class Camara(db.Model):
    """Entidad principal del negocio. En el MVP los datos son simulados;
    luego se reemplazan por la integración real con la API de Hikvision."""
    __tablename__ = "camaras"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    ubicacion = db.Column(db.String(120), nullable=False)
    estado = db.Column(db.String(20), nullable=False, default="activa")  # activa | inactiva
    imagen_url = db.Column(db.String(255), nullable=False)


class Grabacion(db.Model):
    __tablename__ = "grabaciones"

    id = db.Column(db.Integer, primary_key=True)
    camara_id = db.Column(db.Integer, db.ForeignKey("camaras.id"), nullable=False)
    fecha = db.Column(db.String(20), nullable=False)
    hora = db.Column(db.String(20), nullable=False)
    duracion = db.Column(db.String(20), nullable=False)
    archivo = db.Column(db.String(255), nullable=False)

    camara = db.relationship("Camara")


class Log(db.Model):
    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)
    accion = db.Column(db.String(255), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    ip = db.Column(db.String(45), nullable=True)
