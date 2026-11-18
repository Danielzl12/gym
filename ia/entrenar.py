"""Entrena la red neuronal con Keras y guarda sus pesos en ia/modelo.json.

Se ejecuta UNA vez en el computador (no en Vercel):
    pip install -r ia/requirements-entrenamiento.txt
    python -m ia.entrenar

Keras/TensorFlow solo se usan aquí. La página usa los pesos guardados con NumPy.
"""
import json
import os

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import numpy as np
import keras

from ia.frases import INTENCIONES, FRASES_DE_PRUEBA
from ia.lenguaje import crear_vocabulario, vectorizar

RUTA_MODELO = os.path.join(os.path.dirname(__file__), "modelo.json")

keras.utils.set_random_seed(42)  # para que el resultado se pueda repetir

# 1. Preparar los datos
nombres = list(INTENCIONES)
frases, etiquetas = [], []
for i, nombre in enumerate(nombres):
    for frase in INTENCIONES[nombre]:
        frases.append(frase)
        etiquetas.append(i)

vocabulario = crear_vocabulario(frases)
X = np.array([vectorizar(f, vocabulario) for f in frases])
y = keras.utils.to_categorical(etiquetas, num_classes=len(nombres))

# 2. Crear la red: entrada -> capa oculta (ReLU) -> salida (Softmax)
modelo = keras.Sequential([
    keras.layers.Input(shape=(len(vocabulario),)),
    keras.layers.Dense(16, activation="relu"),
    keras.layers.Dense(len(nombres), activation="softmax"),
])

# 3. Configurar y entrenar
modelo.compile(optimizer=keras.optimizers.Adam(0.01),
               loss="categorical_crossentropy", metrics=["accuracy"])
historia = modelo.fit(X, y, epochs=150, batch_size=8, verbose=0)
print("Precisión en entrenamiento: {:.1%}".format(historia.history["accuracy"][-1]))

# 4. Probar con frases que la red nunca vio
aciertos = total = 0
for i, nombre in enumerate(nombres):
    for frase in FRASES_DE_PRUEBA[nombre]:
        pred = int(np.argmax(modelo.predict(vectorizar(frase, vocabulario)[None, :], verbose=0)))
        total += 1
        aciertos += pred == i
        if pred != i:
            print("  Falló:", frase, "->", nombres[pred])
print("Precisión en frases nuevas: {}/{} ({:.1%})".format(aciertos, total, aciertos / total))

# 5. Guardar el modelo (pesos en JSON para leerlos con NumPy)
w1, b1, w2, b2 = modelo.get_weights()
with open(RUTA_MODELO, "w", encoding="utf-8") as f:
    json.dump({
        "intenciones": nombres,
        "vocabulario": vocabulario,
        "w1": np.round(w1, 5).tolist(), "b1": np.round(b1, 5).tolist(),
        "w2": np.round(w2, 5).tolist(), "b2": np.round(b2, 5).tolist(),
    }, f, ensure_ascii=False)
print("Modelo guardado en", RUTA_MODELO)
