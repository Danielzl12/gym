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

## Siguiente fase
Chatbot para el administrador con una red neuronal simple (TensorFlow/Keras) que responda preguntas como miembros activos, ingresos de membresías o clientes que han venido.
