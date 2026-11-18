"""Conexión con Supabase usando su API REST (PostgREST) y su autenticación."""
import os
import requests

URL = os.environ.get("SUPABASE_URL", "")
KEY = os.environ.get("SUPABASE_KEY", "")
SCHEMA = "gym"  # las tablas del gimnasio están en este schema


class ErrorBD(Exception):
    """Error al hablar con la base de datos."""

    def __init__(self, mensaje, codigo=None):
        super().__init__(mensaje)
        self.codigo = codigo


class SesionVencida(Exception):
    """El token del administrador ya no sirve."""


def _cabeceras(token):
    return {
        "apikey": KEY,
        "Authorization": "Bearer " + token,
        "Accept-Profile": SCHEMA,
        "Content-Profile": SCHEMA,
        "Prefer": "return=representation",
    }


def _revisar(respuesta):
    if respuesta.status_code in (401, 403):
        raise SesionVencida()
    if respuesta.status_code >= 400:
        try:
            datos = respuesta.json()
        except ValueError:
            datos = {}
        raise ErrorBD(datos.get("message", "Error en la base de datos"), datos.get("code"))
    return respuesta


def _llamar(metodo, url, **kwargs):
    try:
        return metodo(url, timeout=10, **kwargs)
    except requests.RequestException:
        raise ErrorBD("No hay conexión con el servidor.")


def ingresar(email, clave):
    """Inicia sesión y devuelve el token de acceso."""
    r = _llamar(requests.post, URL + "/auth/v1/token?grant_type=password",
                headers={"apikey": KEY}, json={"email": email, "password": clave})
    if r.status_code >= 400:
        raise ErrorBD("Correo o contraseña incorrectos.")
    return r.json()["access_token"]


def crear_cuenta(email, clave):
    r = _llamar(requests.post, URL + "/auth/v1/signup",
                headers={"apikey": KEY}, json={"email": email, "password": clave})
    if r.status_code >= 400:
        raise ErrorBD(r.json().get("msg", "No se pudo crear la cuenta."))


def consultar(tabla, token, filtros=None):
    """SELECT. Ejemplo: consultar("clientes", token, {"select": "*", "order": "nombre"})"""
    r = _llamar(requests.get, f"{URL}/rest/v1/{tabla}", headers=_cabeceras(token), params=filtros or {})
    return _revisar(r).json()


def insertar(tabla, datos, token):
    r = _llamar(requests.post, f"{URL}/rest/v1/{tabla}", headers=_cabeceras(token), json=datos)
    return _revisar(r).json()[0]


def eliminar(tabla, id_registro, token):
    r = _llamar(requests.delete, f"{URL}/rest/v1/{tabla}", headers=_cabeceras(token),
                params={"id": "eq." + str(id_registro)})
    _revisar(r)
