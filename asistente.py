"""Respuestas del asistente: la red neuronal entiende la pregunta y aquí se calcula el dato."""
import balance


def _pesos(valor):
    return "${:,}".format(int(valor)).replace(",", ".")


def responder(intencion, token, fecha):
    if intencion == "saludo":
        return "¡Hola! Soy el asistente de GymBarrio. Pregúntame por el balance del gimnasio."
    if intencion == "ayuda":
        return ("Puedo decirte: cuántos clientes hay, cuántos miembros activos, "
                "cuántos vinieron hoy, cuánto dinero entró este mes y qué membresías vencen pronto.")
    if intencion == "total_clientes":
        return "Hay {} clientes registrados.".format(balance.total_clientes(token))
    if intencion == "miembros_activos":
        return "Hay {} miembros con membresía activa.".format(balance.miembros_activos(token, fecha))
    if intencion == "entradas_hoy":
        return "Hoy han entrado {} clientes.".format(balance.entradas_hoy(token, fecha))
    if intencion == "ingresos_mes":
        return "Este mes han entrado {} por membresías.".format(_pesos(balance.ingresos_mes(token, fecha)))
    if intencion == "por_vencer":
        lista = balance.por_vencer(token, fecha)
        if not lista:
            return "Ninguna membresía vence en los próximos 7 días."
        return "Vencen en los próximos 7 días: " + "; ".join(
            "{} ({})".format(nombre, vence) for nombre, vence in lista) + "."
    return "No entendí la pregunta. Escribe «ayuda» para ver lo que puedo responder."
