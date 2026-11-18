"""Frases de ejemplo para entrenar la red neuronal.

Cada clave es una intención (lo que el administrador quiere saber) y cada
lista son maneras distintas de preguntarlo. Para mejorar el asistente basta
con agregar más frases y volver a entrenar.
"""

INTENCIONES = {
    "saludo": [
        "hola", "buenas", "buenos dias", "buenas tardes", "buenas noches",
        "hey", "que tal", "hola como estas", "saludos", "hola asistente",
        "buen dia", "hola buenas", "gracias", "muchas gracias", "chao",
    ],
    "ayuda": [
        "ayuda", "que puedes hacer", "que sabes hacer", "como funciona",
        "que te puedo preguntar", "que preguntas entiendes", "necesito ayuda",
        "para que sirves", "que opciones tengo", "ayudame",
        "dime que puedes responder", "como te uso", "que haces",
    ],
    "total_clientes": [
        "cuantos clientes tengo", "cuantos clientes hay", "total de clientes",
        "cuantas personas estan registradas", "cuantos clientes estan registrados",
        "numero de clientes", "cuantos usuarios tiene el gimnasio",
        "cuantos inscritos hay", "cantidad de clientes registrados",
        "dime el total de clientes", "cuantos clientes tiene el gimnasio",
        "cuantas personas hay inscritas", "total de personas registradas",
    ],
    "miembros_activos": [
        "cuantos miembros activos hay", "cuantos clientes tienen membresia activa",
        "miembros activos", "cuantas membresias estan vigentes",
        "cuantos tienen la membresia al dia", "cuantos clientes estan activos",
        "cuantas personas tienen plan vigente", "dime los miembros activos",
        "cuantos socios activos tenemos", "cuantas membresias activas hay",
        "numero de miembros con membresia vigente", "cuantos estan al dia con su plan",
        "clientes con membresia vigente",
    ],
    "entradas_hoy": [
        "cuantos clientes vinieron hoy", "cuantas personas han venido hoy",
        "asistencias de hoy", "cuantos entraron hoy al gimnasio",
        "cuantos clientes han asistido hoy", "cuantas entradas hubo hoy",
        "cuanta gente vino hoy", "personas que llegaron hoy",
        "cuantos asistieron hoy", "dime las asistencias de hoy",
        "cuantos han entrenado hoy", "cuantas visitas hubo hoy",
        "cuantos clientes han llegado hoy",
    ],
    "ingresos_mes": [
        "cuanto dinero hemos recibido este mes", "ingresos del mes",
        "cuanto se ha ganado este mes", "cuanto han pagado en membresias este mes",
        "dinero recaudado este mes", "cuanto hemos facturado en el mes",
        "ventas de membresias del mes", "cuanta plata entro este mes",
        "dime los ingresos de este mes", "cuanto dinero han dejado las membresias",
        "balance de ingresos del mes", "cuanto vendimos este mes",
        "total de pagos del mes",
    ],
    "por_vencer": [
        "que membresias vencen pronto", "quienes estan por vencer",
        "membresias proximas a vencer", "a quien se le vence la membresia",
        "que clientes vencen esta semana", "membresias por vencer",
        "quien tiene la membresia a punto de vencerse", "vencimientos proximos",
        "que planes se vencen en estos dias", "clientes con membresia por terminar",
        "a quienes les toca renovar", "quienes deben renovar pronto",
        "membresias que se acaban pronto",
    ],
}

# Frases que NO están en el entrenamiento, para medir qué tan bien generaliza.
FRASES_DE_PRUEBA = {
    "saludo": ["hola buenos dias", "buenas como vas", "hey hola"],
    "ayuda": ["que cosas puedo preguntarte", "explicame que haces", "necesito que me ayudes"],
    "total_clientes": ["cuantos clientes tenemos registrados", "numero total de inscritos", "dime cuantas personas hay registradas"],
    "miembros_activos": ["cuantos miembros tienen membresia vigente", "numero de socios activos", "cuantas membresias estan activas"],
    "entradas_hoy": ["cuantas personas entraron hoy", "dime cuantos vinieron hoy al gimnasio", "asistencia de hoy"],
    "ingresos_mes": ["cuanto dinero entro este mes", "dime los ingresos por membresias del mes", "cuanta plata hemos recibido en el mes"],
    "por_vencer": ["que membresias se vencen esta semana", "quienes tienen que renovar pronto", "membresias que estan por terminar"],
}
