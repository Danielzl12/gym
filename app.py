"""GymBarrio - sistema de gestión de membresías para el administrador."""
import os
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from functools import wraps

from flask import Flask, render_template, request, redirect, session, flash

import db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "clave-solo-para-desarrollo")


def hoy():
    """Fecha de hoy en Colombia (el servidor puede estar en otra zona horaria)."""
    return datetime.now(ZoneInfo("America/Bogota")).date()


@app.template_filter("pesos")
def pesos(valor):
    return "${:,}".format(int(valor)).replace(",", ".")


def requiere_login(vista):
    """Solo deja entrar si el administrador inició sesión."""
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if not session.get("token"):
            return redirect("/")
        try:
            return vista(*args, **kwargs)
        except db.SesionVencida:
            session.clear()
            flash("Tu sesión terminó o no tienes permiso. Ingresa de nuevo.", "error")
            return redirect("/")
        except db.ErrorBD as e:
            flash(str(e), "error")
            return redirect("/inicio")
    return envoltura


# ---------- Login ----------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        clave = request.form.get("clave", "")
        if "@" not in email or len(clave) < 6:
            flash("Escribe un correo válido y una contraseña de mínimo 6 caracteres.", "error")
            return redirect("/")
        try:
            if request.form.get("accion") == "crear":
                db.crear_cuenta(email, clave)
                flash("Cuenta creada. Ya puedes ingresar.", "ok")
                return redirect("/")
            session["token"] = db.ingresar(email, clave)
            return redirect("/inicio")
        except db.ErrorBD as e:
            flash(str(e), "error")
            return redirect("/")
    return render_template("login.html")


@app.route("/salir")
def salir():
    session.clear()
    return redirect("/")


@app.route("/inicio")
@requiere_login
def inicio():
    return render_template("inicio.html")
