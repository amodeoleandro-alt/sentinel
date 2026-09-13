from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
import bcrypt

from extensions import db
from models import Usuario, Log

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.inicio"))

    if request.method == "POST":
        correo = request.form.get("correo", "").strip().lower()
        password = request.form.get("password", "")

        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario and bcrypt.checkpw(password.encode("utf-8"), usuario.password_hash.encode("utf-8")):
            if not usuario.activo:
                flash("Tu cuenta está deshabilitada. Contactá a un administrador.", "danger")
                return redirect(url_for("auth.login"))

            login_user(usuario)
            session.permanent = True
            usuario.ultimo_login = datetime.utcnow()
            db.session.add(Log(usuario_id=usuario.id, accion="Inicio de sesión", ip=request.remote_addr))
            db.session.commit()

            return redirect(url_for("dashboard.inicio"))

        flash("Correo o contraseña incorrectos.", "danger")

    return render_template("login.html")


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.inicio"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        correo = request.form.get("correo", "").strip().lower()
        password = request.form.get("password", "")
        confirmar = request.form.get("confirmar", "")

        errores = []
        if not nombre or not apellido:
            errores.append("Nombre y apellido son obligatorios.")
        if len(password) < 8:
            errores.append("La contraseña debe tener al menos 8 caracteres.")
        if password != confirmar:
            errores.append("Las contraseñas no coinciden.")
        if Usuario.query.filter_by(correo=correo).first():
            errores.append("Ya existe una cuenta registrada con ese correo.")

        if errores:
            for e in errores:
                flash(e, "danger")
            return render_template("register.html", nombre=nombre, apellido=apellido, correo=correo)

        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            password_hash=password_hash,
            rol="usuario",
        )
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("Cuenta creada correctamente. Ya podés iniciar sesión.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/logout")
@login_required
def logout():
    db.session.add(Log(usuario_id=current_user.id, accion="Cierre de sesión", ip=request.remote_addr))
    db.session.commit()
    logout_user()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("auth.login"))
