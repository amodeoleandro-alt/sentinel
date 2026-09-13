from flask import Blueprint, jsonify, request, abort
from flask_login import login_required, current_user
import bcrypt

from extensions import db
from models import Camara, Grabacion, Usuario

api_bp = Blueprint("api", __name__, url_prefix="/api")


def admin_required():
    if not current_user.es_admin():
        abort(403)


# ---------- Cámaras (Flujo de Datos del Negocio: Frontend -> Backend -> SELECT -> DB) ----------

@api_bp.route("/camaras", methods=["GET"])
@login_required
def listar_camaras():
    camaras = Camara.query.all()
    return jsonify([
        {
            "id": c.id,
            "nombre": c.nombre,
            "ubicacion": c.ubicacion,
            "estado": c.estado,
            "imagen_url": c.imagen_url,
        }
        for c in camaras
    ])


# ---------- Grabaciones ----------

@api_bp.route("/grabaciones", methods=["GET"])
@login_required
def listar_grabaciones():
    grabaciones = Grabacion.query.join(Camara).all()
    return jsonify([
        {
            "id": g.id,
            "camara": g.camara.nombre,
            "fecha": g.fecha,
            "hora": g.hora,
            "duracion": g.duracion,
            "archivo": g.archivo,
        }
        for g in grabaciones
    ])


# ---------- Administración de usuarios (CRUD) ----------

@api_bp.route("/usuarios", methods=["GET"])
@login_required
def listar_usuarios():
    admin_required()
    q = request.args.get("q", "").strip().lower()
    query = Usuario.query
    if q:
        query = query.filter(
            db.or_(
                Usuario.nombre.ilike(f"%{q}%"),
                Usuario.apellido.ilike(f"%{q}%"),
                Usuario.correo.ilike(f"%{q}%"),
            )
        )
    usuarios = query.order_by(Usuario.fecha_creacion.desc()).all()
    return jsonify([
        {
            "id": u.id,
            "nombre": u.nombre,
            "apellido": u.apellido,
            "correo": u.correo,
            "rol": u.rol,
            "activo": u.activo,
            "fecha_creacion": u.fecha_creacion.strftime("%Y-%m-%d %H:%M") if u.fecha_creacion else None,
            "ultimo_login": u.ultimo_login.strftime("%Y-%m-%d %H:%M") if u.ultimo_login else None,
        }
        for u in usuarios
    ])


@api_bp.route("/usuarios/<int:usuario_id>", methods=["PUT"])
@login_required
def editar_usuario(usuario_id):
    admin_required()
    usuario = Usuario.query.get_or_404(usuario_id)
    data = request.get_json(silent=True) or {}

    if "rol" in data and data["rol"] in ("usuario", "administrador"):
        usuario.rol = data["rol"]
    if "activo" in data:
        usuario.activo = bool(data["activo"])
    if "password" in data and data["password"]:
        usuario.password_hash = bcrypt.hashpw(
            data["password"].encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    db.session.commit()
    return jsonify({"ok": True})


@api_bp.route("/usuarios/<int:usuario_id>", methods=["DELETE"])
@login_required
def eliminar_usuario(usuario_id):
    admin_required()
    if usuario_id == current_user.id:
        return jsonify({"ok": False, "error": "No podés eliminar tu propia cuenta."}), 400
    usuario = Usuario.query.get_or_404(usuario_id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"ok": True})
