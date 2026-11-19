# GymBarrio

Sistema web para administrar el gimnasio del barrio: quién entrena, qué plan tiene y cuándo se le vence.
Proyecto de Taller de Programación: prototipo funcional de gestión y asistente con inteligencia artificial.

## Funcionalidades (administrador)
- Inicio de sesión del administrador
- Clientes: crear, listar y eliminar (con validaciones)
- Planes: diario, mensual, trimestral (se pueden crear más)
- Membresías: registrar y renovar, con fecha de vencimiento y estado (activa / vencida)
- Pagos: se registra uno automáticamente por cada membresía
- Asistencia: registrar la entrada de clientes con membresía activa
- Inicio: resumen (clientes, miembros activos, entradas de hoy, ingresos del mes)
- Asistente: chatbot con red neuronal que responde preguntas de balance

## Tecnologías
- Lenguaje: Python 3 con Flask
- Base de datos y autenticación: Supabase (PostgreSQL)
- Inteligencia artificial: red neuronal entrenada con Keras y usada con NumPy
- Despliegue: Vercel

## Estructura
```
app.py                Rutas de la aplicación (Flask)
db.py                 Conexión con Supabase
balance.py            Cálculos del balance (inicio y asistente)
asistente.py          Respuestas del asistente según la intención
ia/                   Red neuronal: frases, entrenamiento, modelo y pruebas
templates/            Páginas HTML (Jinja) y estilos
db/schema.sql         Tablas y seguridad de la base de datos
requirements.txt      Dependencias de Python
.env.example          Ejemplo de variables de entorno
docs/evidencias/      Capturas de funcionamiento
```


## Aplicación en línea
GymBarrio está desplegado y funcionando en Vercel: https://gymbarrio.vercel.app

Usuario de prueba (administrador):
- Correo: `admin@gymbarrio.com`
- Contraseña: `Admin12345`

## Base de datos
Las tablas están en el schema `gym` (ver `db/schema.sql`). Solo pueden usar el sistema los correos que estén en la tabla `gym.admins`:

```sql
insert into gym.admins (email) values ('correo@ejemplo.com');
```

El administrador crea su cuenta desde la pantalla de ingreso y luego se agrega su correo a esa tabla.

## Manejo de errores
Si falla la conexión, la sesión vence o el usuario no tiene permiso, la aplicación muestra un mensaje claro y no se cierra.

## Resumen de la primera fase: prototipo de gestión
**Estado: completada.** Se construyó el sistema que usa el administrador para gestionar el gimnasio.

**Qué se hizo**
- **Base de datos** en Supabase (PostgreSQL), en el schema `gym`: planes, clientes, membresías, pagos, asistencias y administradores, con sus relaciones y restricciones (documento único, valores positivos).
- **Seguridad:** solo los correos registrados en `gym.admins` pueden leer o escribir datos (Row Level Security). Las credenciales no están en el repositorio: se configuran como variables de entorno.
- **Aplicación en Python (Flask):** login, cinco pantallas con menú de navegación, validaciones en los formularios y mensajes de error claros cuando algo falla.
- **Reglas del negocio:** cada membresía calcula su vencimiento según el plan y registra su pago; solo entra el cliente con membresía activa.
- **Despliegue** en Vercel y **datos de prueba** (clientes, membresías y asistencias ficticios).
- **Trabajo en equipo:** el desarrollo quedó repartido en commits de los tres integrantes sobre el mismo repositorio.
- **Pruebas:** se verificó el flujo completo (login, crear cliente, documento duplicado, membresía, asistencia y resumen) y que un usuario sin permiso no puede leer ni escribir.

**Decisiones frente a la ficha técnica**

| Ficha técnica | Lo que se implementó | Por qué |
|---|---|---|
| Frontend en HTML, CSS y JavaScript con API REST en Node.js | Python con Flask, que genera las páginas | Menos piezas, más sencillo para el tiempo disponible y el mismo lenguaje que usará la inteligencia artificial |
| Asistencia e ingresos como fase posterior | Se incluyeron de forma mínima | El asistente de la segunda fase necesita responder cuántos clientes han venido y cuánto dinero ha ingresado |

## Segunda fase: asistente con inteligencia artificial
**Estado: completada.** Está en la página, en el menú **Asistente**.

**Objetivo.** Un chatbot para el administrador que responde preguntas de balance del gimnasio, por ejemplo: ¿cuántos miembros activos tengo?, ¿cuánto dinero ingresó este mes por membresías?, ¿cuántos clientes han venido hoy?, ¿qué membresías vencen pronto?

**Cómo funciona**
```
Administrador escribe la pregunta
        -> Red neuronal: identifica qué quiere saber (la intención)
        -> La aplicación consulta la base de datos y calcula el dato
        -> Respuesta con el dato real
```
La red neuronal no inventa números: solo entiende la pregunta. El dato sale siempre de la base de datos, así que la respuesta es exacta y está al día. Si la red no está segura de qué se preguntó, responde que no entendió en lugar de adivinar.

**La red neuronal.** Es una red propia y local, sin servicios externos ni claves de API. Sigue la arquitectura de la guía:
- **Entrada:** la pregunta convertida en un vector de palabras (sin tildes ni mayúsculas).
- **Capa oculta:** 16 neuronas con ReLU.
- **Salida:** una neurona por intención con Softmax (10 intenciones: saludo, ayuda, total de clientes, miembros activos, entradas de hoy, quiénes entraron hoy, entradas del mes, salidas, ingresos del mes y membresías por vencer). La guía usa una sola salida con Sigmoid porque su problema es de sí o no; aquí hay varias intenciones posibles.
- **Entrenamiento:** 144 frases de ejemplo escritas por el equipo, pérdida de entropía cruzada y optimizador Adam.
- **Resultado:** 100 % en las frases de entrenamiento y 31 de 31 aciertos en frases nuevas que la red nunca vio (`python -m ia.pruebas`).

| Paso de la guía | Cómo se hizo en el proyecto |
|---|---|
| Preparar los datos | Frases de ejemplo por intención (`ia/frases.py`) |
| Crear la red | Capa oculta ReLU y salida Softmax con Keras (`ia/entrenar.py`) |
| Configurar y entrenar | `compile` y `fit` de Keras |
| Realizar una predicción | Probabilidad de cada intención para una pregunta nueva (`ia/red.py`) |
| Guardar el modelo | Pesos en `ia/modelo.json` |
| Integrarlo a la herramienta | Ruta `/asistente` en la aplicación Flask |

**Keras para entrenar, NumPy para usar la red.** El equipo usó la tecnología de la guía, Keras con TensorFlow, para crear y entrenar la red en el computador. La página en línea, en cambio, no usa TensorFlow: lee los pesos guardados y calcula la predicción con NumPy. Motivos:
1. **Límite de Vercel.** Lo probamos: al desplegar una app de prueba con `tensorflow-cpu` (la versión más liviana), Vercel rechazó el despliegue con el error `LAMBDA_SIZE_EXCEEDED` (paquete de 1388 MB frente al máximo de 500 MB). NumPy pesa unos 60 MB.
2. **Mismo resultado.** Con los mismos pesos, Keras y NumPy dan la misma probabilidad (diferencia menor a 0,0000001), porque la predicción solo son dos multiplicaciones de matrices, una activación ReLU y un Softmax.
3. **Más simple.** Un solo despliegue, sin un servidor aparte para la IA.

**Si se quiere mejorar el asistente.** Se agregan frases en `ia/frases.py` (o una intención nueva con su respuesta en `asistente.py`) y se vuelve a entrenar en el computador con `pip install -r ia/requirements-entrenamiento.txt` y `python -m ia.entrenar`. Eso actualiza `ia/modelo.json`.
