"""Cálculos del balance del gimnasio. Los usan el resumen de inicio y el asistente."""
from datetime import timedelta

import db


def total_clientes(token):
    return len(db.consultar("clientes", token, {"select": "id"}))


def _vigentes(token, fecha):
    """Membresías que todavía no vencen."""
    return db.consultar("membresias", token, {
        "fecha_vencimiento": "gte." + fecha.isoformat(),
        "select": "cliente_id,fecha_vencimiento,clientes(nombre)"})


def miembros_activos(token, fecha):
    return len({m["cliente_id"] for m in _vigentes(token, fecha)})


def entradas_hoy(token, fecha):
    return len(db.consultar("asistencias", token, {
        "fecha_hora": "gte." + fecha.isoformat() + "T00:00:00-05:00", "select": "id"}))


def quienes_hoy(token, fecha):
    """Nombres de los clientes que entraron hoy (sin repetir)."""
    entradas = db.consultar("asistencias", token, {
        "fecha_hora": "gte." + fecha.isoformat() + "T00:00:00-05:00",
        "select": "fecha_hora,clientes(nombre)", "order": "fecha_hora"})
    nombres = []
    for e in entradas:
        if e["clientes"]["nombre"] not in nombres:
            nombres.append(e["clientes"]["nombre"])
    return nombres


def entradas_mes(token, fecha):
    return len(db.consultar("asistencias", token, {
        "fecha_hora": "gte." + fecha.replace(day=1).isoformat() + "T00:00:00-05:00", "select": "id"}))


def ingresos_mes(token, fecha):
    pagos = db.consultar("pagos", token, {
        "fecha": "gte." + fecha.replace(day=1).isoformat(), "select": "valor"})
    return sum(p["valor"] for p in pagos)


def por_vencer(token, fecha, dias=7):
    """Clientes cuya última membresía vence en los próximos días: [(nombre, fecha)]."""
    limite = (fecha + timedelta(days=dias)).isoformat()
    ultima = {}  # la membresía que más tarde vence de cada cliente
    for m in _vigentes(token, fecha):
        if m["cliente_id"] not in ultima or m["fecha_vencimiento"] > ultima[m["cliente_id"]][1]:
            ultima[m["cliente_id"]] = (m["clientes"]["nombre"], m["fecha_vencimiento"])
    return sorted((v for v in ultima.values() if v[1] <= limite), key=lambda v: v[1])
