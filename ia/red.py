"""Usa la red ya entrenada para entender una pregunta. Solo necesita NumPy."""
import json
import os

import numpy as np

from ia.lenguaje import vectorizar

_RUTA = os.path.join(os.path.dirname(__file__), "modelo.json")
UMBRAL = 0.5  # si la red no está segura, responde que no entendió

with open(_RUTA, encoding="utf-8") as f:
    _m = json.load(f)
INTENCIONES = _m["intenciones"]
_VOCABULARIO = _m["vocabulario"]
_W1, _B1 = np.array(_m["w1"]), np.array(_m["b1"])
_W2, _B2 = np.array(_m["w2"]), np.array(_m["b2"])


def probabilidades(pregunta):
    """Propagación hacia adelante: entrada -> ReLU -> Softmax."""
    x = vectorizar(pregunta, _VOCABULARIO)
    oculta = np.maximum(0, x @ _W1 + _B1)
    salida = oculta @ _W2 + _B2
    e = np.exp(salida - salida.max())
    return e / e.sum()


def entender(pregunta):
    """Devuelve (intención, seguridad). Si no está segura, la intención es 'desconocida'."""
    if not any(vectorizar(pregunta, _VOCABULARIO)):
        return "desconocida", 0.0  # ninguna palabra conocida: no hay nada que clasificar
    p = probabilidades(pregunta)
    i = int(np.argmax(p))
    if p[i] < UMBRAL:
        return "desconocida", float(p[i])
    return INTENCIONES[i], float(p[i])
