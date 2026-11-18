"""Convierte una pregunta en números para la red neuronal (bolsa de palabras).

Solo usa NumPy: lo comparten el entrenamiento y el asistente de la página.
"""
import re
import unicodedata

import numpy as np


def palabras(texto):
    """Minúsculas, sin tildes y separado en palabras."""
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return re.findall(r"[a-z0-9]+", texto)


def crear_vocabulario(frases):
    """Lista ordenada con todas las palabras que aparecen en las frases."""
    return sorted({p for f in frases for p in palabras(f)})


def vectorizar(texto, vocabulario):
    """Vector de 0 y 1: 1 si la palabra del vocabulario está en el texto."""
    presentes = set(palabras(texto))
    return np.array([1.0 if p in presentes else 0.0 for p in vocabulario], dtype=np.float32)
