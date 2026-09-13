# CamMonitor — MVP Sistema de Monitoreo de Cámaras (Hikvision-ready)

MVP full-stack para la entrega de avance de proyecto final. Implementa autenticación con roles,
dashboard con cámaras y grabaciones simuladas, y panel de administración — todo con datos
reales fluyendo Frontend → Backend → Base de Datos.

## Stack

- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript (fetch API, sin recargas de página en las
  vistas internas de datos)
- **Backend:** Python + Flask (Blueprints: `auth`, `dashboard`, `api`)
- **Base de datos:** SQLite en desarrollo → MySQL en producción (mismo código, cambia solo la config)
- **Autenticación:** Flask-Login + sesiones con expiración por inactividad
- **Contraseñas:** hash con `bcrypt` (nunca texto plano)

## 1. Cómo instalar

```bash
python3 -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # Completar SECRET_KEY (y datos de MySQL si aplica)
```

## 2. Cómo crear la base de datos

```bash
python seed.py
```

Esto crea las tablas (`usuarios`, `camaras`, `grabaciones`, `logs`) y carga datos de ejemplo:

| Correo | Contraseña | Rol |
|---|---|---|
| admin@demo.com | Admin1234 | administrador |
| usuario@demo.com | Usuario1234 | usuario |

## 3. Cómo ejecutar

```bash
python app.py
```

La app queda disponible en `http://127.0.0.1:5000`.

## 4. Flujos implementados (requisito de integración End-to-End)

- **Flujo de Usuarios:** `/registro` envía el formulario al backend → se valida → se hashea la
  contraseña con bcrypt → se persiste en `usuarios` → login posterior validado contra ese hash.
- **Flujo de Datos del Negocio:** las vistas `/camaras`, `/grabaciones` y `/administracion` no
  tienen datos hardcodeados: hacen `fetch()` a `/api/camaras`, `/api/grabaciones` y `/api/usuarios`,
  que ejecutan un `SELECT` real contra la base y devuelven JSON, renderizado dinámicamente sin
  recargar la página.

## 5. Roles y permisos

- **Usuario:** ve cámaras y grabaciones, edita su propio perfil.
- **Administrador:** además accede a `/administracion` (listar, buscar, cambiar rol, activar/
  desactivar y eliminar usuarios vía `/api/usuarios`).

Para crear un nuevo rol: agregar el valor en `models.Usuario.rol`, actualizar el decorador
`admin_required` en `routes/dashboard.py` / `routes/api.py` si el nuevo rol necesita reglas
propias, y sumar la opción en el `<select>` de `templates/admin.html`.

## 6. Cómo cambiar SQLite por MySQL

1. En AlwaysData (u otro proveedor), crear la base MySQL y un usuario con permisos.
2. Completar en `.env`: `FLASK_ENV=production`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_NAME`.
3. `config.py` ya arma el `SQLALCHEMY_DATABASE_URI` de MySQL automáticamente con esos valores
   (usa `PyMySQL` como driver, incluido en `requirements.txt`).
4. Ejecutar `python seed.py` una vez apuntando a la base de producción para crear tablas y datos
   iniciales.

## 7. Cómo agregar nuevas cámaras

Mientras se usan datos simulados: insertar filas en la tabla `camaras` (por ejemplo, extendiendo
`seed.py` o vía un futuro endpoint de administración). El frontend no requiere cambios: `/camaras`
lee dinámicamente todo lo que exista en la tabla a través de `/api/camaras`.

## 8. Cómo conectar la API de Hikvision (siguiente iteración)

El proyecto ya está desacoplado para este reemplazo:

1. Crear `services/hikvision_service.py` con las llamadas reales a la API/SDK de Hikvision
   (autenticación, listado de dispositivos, streams, grabaciones).
2. En `routes/api.py`, reemplazar las consultas `Camara.query.all()` / `Grabacion.query...` por
   llamadas a `hikvision_service` (o combinarlas: cámaras registradas en la BD + estado en vivo
   desde Hikvision).
3. En `templates/camaras.html`, cambiar la fuente de la imagen simulada por el stream real (por
   ejemplo, un `<video>` o un proxy MJPEG/RTSP-a-HLS) sin tocar el resto de la lógica de la página.

## 9. Cómo desplegar en AlwaysData

1. Subir el proyecto (Git o FTP/SFTP) a tu cuenta de AlwaysData.
2. Crear la base de datos MySQL desde el panel de AlwaysData y anotar host/usuario/clave.
3. Configurar las variables de entorno de producción (`.env` o panel de "Environment variables").
4. Configurar el sitio Python/WSGI de AlwaysData apuntando a `app:create_app()` (usando un
   `wsgi.py` que invoque `app = create_app("production")` si el panel lo requiere).
5. Instalar dependencias: `pip install -r requirements.txt --user`.
6. Ejecutar `python seed.py` una vez para crear las tablas.
7. Reiniciar la aplicación desde el panel de AlwaysData.

## Estructura del proyecto

```
proyecto_camaras/
├── app.py                 # Application factory
├── config.py               # Config dev (SQLite) / prod (MySQL)
├── extensions.py            # db, login_manager
├── models.py                # Usuario, Camara, Grabacion, Log
├── seed.py                  # Crea tablas + datos de ejemplo
├── requirements.txt
├── .env.example
├── routes/
│   ├── auth.py               # login, registro, logout
│   ├── dashboard.py          # páginas (inicio, cámaras, grabaciones, ajustes, perfil, admin)
│   └── api.py                # endpoints JSON (cámaras, grabaciones, usuarios)
├── templates/                # Jinja2 + Bootstrap 5
├── static/
│   ├── css/style.css
│   ├── js/main.js            # sidebar toggle + auto-logout por inactividad
│   └── img/camara_placeholder.svg
└── database/                 # app.db (SQLite, se genera con seed.py)
```

## Pendiente para próximas iteraciones (fuera del alcance de este avance)

- Recuperación de contraseña por correo (código de 6 dígitos con expiración).
- Persistencia de preferencias de Ajustes (tema/idioma) por usuario.
- Envío de correo real (Flask-Mail) para notificaciones.
- Protección CSRF explícita en formularios (Flask-WTF) y rate-limiting contra fuerza bruta.
- Integración real con Hikvision (ver punto 8).
