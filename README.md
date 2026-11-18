# GymBarrio

Sistema web para administrar el gimnasio del barrio: quién entrena, qué plan tiene y cuándo se le vence.
Proyecto de Taller de Programación - Fase II (prototipo funcional).

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


## Base de datos
Las tablas están en el schema `gym` (ver `db/schema.sql`). Solo pueden usar el sistema los correos que estén en la tabla `gym.admins`:

```sql
insert into gym.admins (email) values ('correo@ejemplo.com');
```

El administrador crea su cuenta desde la pantalla de ingreso y luego se agrega su correo a esa tabla.

## Manejo de errores
Si falla la conexión, la sesión vence o el usuario no tiene permiso, la aplicación muestra un mensaje claro y no se cierra.

## Siguiente fase
Chatbot para el administrador con una red neuronal simple (TensorFlow/Keras) que responda preguntas como miembros activos, ingresos de membresías o clientes que han venido.
