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

## Tecnologías
- Lenguaje: Python 3 con Flask
- Base de datos y autenticación: Supabase (PostgreSQL)
- Despliegue: Vercel

## Estructura
```
app.py                Rutas de la aplicación (Flask)
db.py                 Conexión con Supabase
templates/            Páginas HTML (Jinja) y estilos
db/schema.sql         Tablas y seguridad de la base de datos
requirements.txt      Dependencias de Python
.env.example          Ejemplo de variables de entorno
docs/evidencias/      Capturas de funcionamiento
```


## Demo en línea
Aplicación desplegada en Vercel: https://gymbarrio.vercel.app

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
- **Despliegue** en Vercel y **datos de demostración** para probar el sistema.
- **Trabajo en equipo:** el desarrollo quedó repartido en commits de los tres integrantes sobre el mismo repositorio.
- **Pruebas:** se verificó el flujo completo (login, crear cliente, documento duplicado, membresía, asistencia y resumen) y que un usuario sin permiso no puede leer ni escribir.

**Decisiones frente a la ficha técnica**

| Ficha técnica | Lo que se implementó | Por qué |
|---|---|---|
| Frontend en HTML, CSS y JavaScript con API REST en Node.js | Python con Flask, que genera las páginas | Menos piezas, más sencillo para el tiempo disponible y el mismo lenguaje que usará la inteligencia artificial |
| Asistencia e ingresos como fase posterior | Se incluyeron de forma mínima | El asistente de la segunda fase necesita responder cuántos clientes han venido y cuánto dinero ha ingresado |

## Segunda fase: asistente con inteligencia artificial
**Estado: en desarrollo.**

**Objetivo.** Agregar al sistema un chatbot para el administrador que responda preguntas de balance del gimnasio, por ejemplo: ¿cuántos miembros activos tengo?, ¿cuánto dinero ingresó este mes por membresías?, ¿cuántos clientes han venido hoy?, ¿qué membresías vencen pronto?

**Cómo funciona**
```
Administrador escribe la pregunta
        -> Chatbot (nueva pantalla de la aplicación)
        -> Red neuronal: identifica qué quiere saber (la intención)
        -> La aplicación consulta la base de datos y calcula el dato
        -> Respuesta con el dato real
```
La red neuronal no inventa números: solo entiende la pregunta. El dato sale siempre de la base de datos, así la respuesta es exacta y siempre está actualizada.

**La red neuronal.** Es una red propia, local, que no depende de servicios externos ni de claves de API. Sigue la arquitectura de la guía (entrada, capa oculta con ReLU y capa de salida):
- **Entrada:** la pregunta convertida en un vector de palabras.
- **Capa oculta:** neuronas con ReLU.
- **Salida:** una neurona por intención con Softmax. La guía usa una sola salida con Sigmoid porque su problema es de sí o no; aquí hay varias intenciones posibles.
- **Entrenamiento:** frases de ejemplo escritas por el equipo para cada intención, con pérdida de entropía cruzada y descenso del gradiente. El modelo entrenado se guarda en un archivo dentro del repositorio.

| Paso de la guía | Cómo se hace en el proyecto |
|---|---|
| Preparar los datos | Frases de ejemplo etiquetadas por intención |
| Crear la red | Capa oculta ReLU y salida Softmax |
| Configurar y entrenar | Propagación hacia adelante, pérdida y retropropagación |
| Realizar una predicción | Probabilidad de cada intención para una pregunta nueva |
| Guardar el modelo | Archivo con los pesos de la red |
| Integrarlo a la herramienta | Ruta del chatbot en la aplicación Flask |

**Por qué se entrena con NumPy y no con TensorFlow/Keras.** La guía propone TensorFlow y Keras. El equipo mantuvo la misma red y los mismos pasos, pero cambió la herramienta de entrenamiento por NumPy, por estas razones:
1. **Despliegue.** La aplicación funciona en Vercel, cuyas funciones de Python permiten hasta 500 MB. TensorFlow, una vez empaquetado, ocupa alrededor de 2 GB según lo reportado por usuarios de Vercel, así que no se puede desplegar ahí. La alternativa era montar un servidor aparte solo para la IA: más piezas y más complejidad para el tiempo disponible.
2. **Tamaño del problema.** El modelo es pequeño (un vocabulario de unos cientos de palabras y pocas neuronas). Un framework completo sobra: con NumPy entrena en segundos y predecir es solo multiplicar matrices.
3. **Comprensión.** Al programar a mano la propagación hacia adelante y la retropropagación se ve cada paso que Keras hace internamente, que es justo el flujo de datos de la entrada a la predicción que la guía quiere que se entienda.

**Avance**
- [ ] Frases de ejemplo por intención
- [ ] Entrenamiento y modelo guardado
- [ ] Pantalla del chatbot e integración con la base de datos
- [ ] Pruebas y evidencias
