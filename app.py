"""GymBarrio - sistema de gestión de membresías para el administrador."""
import os
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from functools import wraps

from flask import Flask, render_template, request, redirect, session, flash

import asistente
import balance
import db
from ia import red

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
    token = session["token"]
    fecha = hoy()
    return render_template("inicio.html", total_clientes=balance.total_clientes(token),
                           miembros_activos=balance.miembros_activos(token, fecha),
                           entradas_hoy=balance.entradas_hoy(token, fecha),
                           ingresos_mes=balance.ingresos_mes(token, fecha))



# ---------- Clientes ----------
@app.route("/clientes", methods=["GET", "POST"])
@requiere_login
def clientes():
    token = session["token"]
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        documento = request.form.get("documento", "").strip()
        if len(nombre) < 3:
            flash("El nombre es muy corto.", "error")
        elif not (documento.isdigit() and 5 <= len(documento) <= 12):
            flash("El documento debe tener entre 5 y 12 números.", "error")
        else:
            try:
                db.insertar("clientes", {
                    "nombre": nombre,
                    "documento": documento,
                    "telefono": request.form.get("telefono", "").strip() or None,
                    "email": request.form.get("email", "").strip() or None,
                }, token)
                flash("Cliente guardado.", "ok")
            except db.ErrorBD as e:
                if e.codigo == "23505":
                    flash("Ya existe un cliente con ese documento.", "error")
                else:
                    raise
        return redirect("/clientes")
    lista = db.consultar("clientes", token, {"select": "*", "order": "nombre"})
    return render_template("clientes.html", clientes=lista)


@app.route("/clientes/<int:id_cliente>/eliminar", methods=["POST"])
@requiere_login
def eliminar_cliente(id_cliente):
    db.eliminar("clientes", id_cliente, session["token"])
    flash("Cliente eliminado.", "ok")
    return redirect("/clientes")


# ---------- Planes ----------
@app.route("/planes", methods=["GET", "POST"])
@requiere_login
def planes():
    token = session["token"]
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        duracion = request.form.get("duracion", "")
        precio = request.form.get("precio", "")
        if not nombre:
            flash("Escribe el nombre del plan.", "error")
        elif not (duracion.isdigit() and int(duracion) > 0):
            flash("La duración debe ser un número de días mayor a 0.", "error")
        elif not precio.isdigit():
            flash("El precio debe ser un número sin negativos.", "error")
        else:
            db.insertar("planes", {"nombre": nombre, "duracion_dias": int(duracion), "precio": int(precio)}, token)
            flash("Plan guardado.", "ok")
        return redirect("/planes")
    lista = db.consultar("planes", token, {"select": "*", "order": "duracion_dias"})
    return render_template("planes.html", planes=lista)


@app.route("/planes/<int:id_plan>/eliminar", methods=["POST"])
@requiere_login
def eliminar_plan(id_plan):
    try:
        db.eliminar("planes", id_plan, session["token"])
        flash("Plan eliminado.", "ok")
    except db.ErrorBD:
        flash("No se puede eliminar: el plan tiene membresías.", "error")
    return redirect("/planes")


# ---------- Membresías ----------
@app.route("/membresias", methods=["GET", "POST"])
@requiere_login
def membresias():
    token = session["token"]
    if request.method == "POST":
        id_cliente = request.form.get("cliente", "")
        id_plan = request.form.get("plan", "")
        inicio_texto = request.form.get("inicio", "")
        try:
            inicio_fecha = date.fromisoformat(inicio_texto)
        except ValueError:
            flash("La fecha de inicio no es válida.", "error")
            return redirect("/membresias")
        if not (id_cliente.isdigit() and id_plan.isdigit()):
            flash("Selecciona un cliente y un plan.", "error")
            return redirect("/membresias")

        plan = db.consultar("planes", token, {"id": "eq." + id_plan, "select": "*"})
        if not plan:
            flash("El plan no existe.", "error")
            return redirect("/membresias")
        plan = plan[0]
        vence = inicio_fecha + timedelta(days=plan["duracion_dias"])

        membresia = db.insertar("membresias", {
            "cliente_id": int(id_cliente),
            "plan_id": plan["id"],
            "fecha_inicio": inicio_fecha.isoformat(),
            "fecha_vencimiento": vence.isoformat(),
        }, token)
        # Cada membresía registra su pago
        db.insertar("pagos", {"membresia_id": membresia["id"], "valor": plan["precio"],
                              "fecha": hoy().isoformat()}, token)
        flash("Membresía registrada.", "ok")
        return redirect("/membresias")

    lista = db.consultar("membresias", token, {
        "select": "id,fecha_inicio,fecha_vencimiento,clientes(nombre),planes(nombre)",
        "order": "fecha_vencimiento.desc",
    })
    for m in lista:
        m["activa"] = m["fecha_vencimiento"] >= hoy().isoformat()
    return render_template(
        "membresias.html",
        membresias=lista,
        clientes=db.consultar("clientes", token, {"select": "id,nombre", "order": "nombre"}),
        planes=db.consultar("planes", token, {"select": "*", "order": "duracion_dias"}),
        hoy=hoy().isoformat(),
    )


# ---------- Asistencia ----------
@app.route("/asistencia", methods=["GET", "POST"])
@requiere_login
def asistencia():
    token = session["token"]
    if request.method == "POST":
        id_cliente = request.form.get("cliente", "")
        if not id_cliente.isdigit():
            flash("Selecciona un cliente.", "error")
            return redirect("/asistencia")
        # Solo entra quien tenga una membresía vigente
        vigentes = db.consultar("membresias", token, {
            "cliente_id": "eq." + id_cliente,
            "fecha_vencimiento": "gte." + hoy().isoformat(),
            "select": "id", "limit": 1,
        })
        if not vigentes:
            flash("Este cliente no tiene membresía activa.", "error")
        else:
            db.insertar("asistencias", {"cliente_id": int(id_cliente)}, token)
            flash("Entrada registrada.", "ok")
        return redirect("/asistencia")
    lista = db.consultar("asistencias", token, {
        "select": "fecha_hora,clientes(nombre)", "order": "fecha_hora.desc", "limit": 30,
    })
    for a in lista:
        a["fecha_hora"] = datetime.fromisoformat(a["fecha_hora"]).astimezone(
            ZoneInfo("America/Bogota")).strftime("%Y-%m-%d %H:%M")
    return render_template(
        "asistencia.html",
        asistencias=lista,
        clientes=db.consultar("clientes", token, {"select": "id,nombre", "order": "nombre"}),
    )


# ---------- Asistente (chatbot con red neuronal) ----------
@app.route("/asistente", methods=["GET", "POST"])
@requiere_login
def asistente_chat():
    if request.method == "POST":
        pregunta = request.form.get("pregunta", "").strip()
        if not pregunta:
            flash("Escribe una pregunta.", "error")
        elif len(pregunta) > 200:
            flash("La pregunta es muy larga (máximo 200 caracteres).", "error")
        else:
            intencion, _seguridad = red.entender(pregunta)
            respuesta = asistente.responder(intencion, session["token"], hoy())
            # La conversación se guarda en la sesión (solo los últimos 8 mensajes)
            chat = session.get("chat", []) + [["yo", pregunta], ["asistente", respuesta]]
            session["chat"] = chat[-8:]
        return redirect("/asistente")
    return render_template("asistente.html", chat=session.get("chat", []))
