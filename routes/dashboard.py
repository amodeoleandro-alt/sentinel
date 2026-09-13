from functools import wraps
from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user

from models import Usuario

dashboard_bp = Blueprint("dashboard", __name__)


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.es_admin():
            abort(403)
        return f(*args, **kwargs)
    return wrapper


@dashboard_bp.route("/")
@dashboard_bp.route("/inicio")
@login_required
def inicio():
    return render_template("inicio.html")


@dashboard_bp.route("/camaras")
@login_required
def camaras():
    # Los datos de cámaras se obtienen dinámicamente vía /api/camaras (fetch),
    # no se hardcodean en la plantilla.
    return render_template("camaras.html")


@dashboard_bp.route("/grabaciones")
@login_required
def grabaciones():
    return render_template("grabaciones.html")


@dashboard_bp.route("/ajustes")
@login_required
def ajustes():
    return render_template("ajustes.html")


@dashboard_bp.route("/perfil")
@login_required
def perfil():
    return render_template("perfil.html")


@dashboard_bp.route("/administracion")
@login_required
@admin_required
def administracion():
    usuarios = Usuario.query.order_by(Usuario.fecha_creacion.desc()).all()
    return render_template("admin.html", usuarios=usuarios)
