"""
Script de inicialización de la base de datos.
Crea las tablas y carga datos de ejemplo (usuario admin + cámaras/grabaciones simuladas).

Uso:
    python seed.py
"""
import bcrypt
from app import create_app
from extensions import db
from models import Usuario, Camara, Grabacion


def hash_password(plain):
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def run():
    app = create_app()
    with app.app_context():
        db.create_all()

        if not Usuario.query.filter_by(correo="admin@demo.com").first():
            admin = Usuario(
                nombre="Admin",
                apellido="Sistema",
                correo="admin@demo.com",
                password_hash=hash_password("Admin1234"),
                rol="administrador",
            )
            user = Usuario(
                nombre="Usuario",
                apellido="Demo",
                correo="usuario@demo.com",
                password_hash=hash_password("Usuario1234"),
                rol="usuario",
            )
            db.session.add_all([admin, user])
            print("Usuarios de ejemplo creados:")
            print("  admin@demo.com / Admin1234  (rol: administrador)")
            print("  usuario@demo.com / Usuario1234  (rol: usuario)")

        if Camara.query.count() == 0:
            camaras = [
                Camara(nombre="Cámara 1 - Entrada", ubicacion="Puerta principal",
                       estado="activa", imagen_url="/static/img/camara_placeholder.svg"),
                Camara(nombre="Cámara 2 - Estacionamiento", ubicacion="Playa de estacionamiento",
                       estado="activa", imagen_url="/static/img/camara_placeholder.svg"),
                Camara(nombre="Cámara 3 - Depósito", ubicacion="Depósito trasero",
                       estado="inactiva", imagen_url="/static/img/camara_placeholder.svg"),
                Camara(nombre="Cámara 4 - Oficinas", ubicacion="Planta alta",
                       estado="activa", imagen_url="/static/img/camara_placeholder.svg"),
            ]
            db.session.add_all(camaras)
            db.session.commit()
            print("Cámaras simuladas creadas.")

            grabaciones = [
                Grabacion(camara_id=camaras[0].id, fecha="2026-07-01", hora="08:15", duracion="00:12:30", archivo="rec_001.mp4"),
                Grabacion(camara_id=camaras[0].id, fecha="2026-07-02", hora="14:40", duracion="00:05:10", archivo="rec_002.mp4"),
                Grabacion(camara_id=camaras[1].id, fecha="2026-07-02", hora="09:00", duracion="00:20:00", archivo="rec_003.mp4"),
                Grabacion(camara_id=camaras[3].id, fecha="2026-07-03", hora="18:22", duracion="00:08:45", archivo="rec_004.mp4"),
            ]
            db.session.add_all(grabaciones)
            print("Grabaciones simuladas creadas.")

        db.session.commit()
        print("Base de datos inicializada correctamente.")


if __name__ == "__main__":
    run()
