"""Revisa que el modelo guardado entienda las frases de prueba.

    python -m ia.pruebas
"""
from ia.frases import FRASES_DE_PRUEBA
from ia.red import entender

aciertos = total = 0
for intencion, frases in FRASES_DE_PRUEBA.items():
    for frase in frases:
        obtenida, seguridad = entender(frase)
        total += 1
        aciertos += obtenida == intencion
        print("{:<5} {:<45} -> {} ({:.0%})".format(
            "OK" if obtenida == intencion else "FALLA", frase, obtenida, seguridad))

for rara in ["cual es la capital de francia", "asdf qwer"]:
    print("{:<5} {:<45} -> {}".format("", rara, entender(rara)[0]))

print("\nAciertos: {}/{}".format(aciertos, total))
assert aciertos == total, "El modelo falló alguna frase"
