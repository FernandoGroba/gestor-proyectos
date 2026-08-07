# Gestor de Proyectos Freelance

Aplicación de escritorio para gestionar proyectos de programación freelance: carga de proyectos, seguimiento de aprobación y generación de presupuestos en PDF con tu marca.

## Funcionalidades

- Alta, edición y borrado de proyectos con confirmación.
- Filtro de la lista por estado: todas, pendientes, aprobadas.
- Datos por proyecto: cliente, nombre, descripción, tarifa, horas y estado de aprobación.
- Cálculo automático del total (`valor_hora * horas`).
- Generación de presupuesto en PDF por proyecto, con logo, encabezado y tabla de totales.
- Tarifas configurables guardadas en la base de datos (`tarifa_a`, `tarifa_b`).

## Tecnologías

- **Python 3.13**
- **Flet 0.86** — interfaz de escritorio
- **SQLite** — persistencia (`proyectos.db`)
- **fpdf2 2.8.7** — generación de PDF
- **Pillow** — procesamiento de la imagen del logo

## Cómo correr en desarrollo

1. Creá y activá el entorno virtual:

```
python -m venv .venv
.venv\Scripts\activate
```

2. Instalá las dependencias:

```
pip install flet fpdf2 pillow
```

3. Corré la app:

```
flet run main.py
```

## Estructura del proyecto

```
main.py            Aplicación Flet: ventana, lista, formulario y eventos
db.py              Capa de datos: conexión a SQLite y consultas
generate_pdf.py    Generación del presupuesto en PDF
assets/
  img_presupuesto.png   Logo que aparece en el PDF
proyectos.db       Base de datos (se crea automáticamente)
```

## Dónde se guardan los datos

La app usa el directorio de datos de la aplicación (`FLET_APP_STORAGE_DATA`):

- En desarrollo: `.flet/storage/data/`
- Empaquetada: la carpeta de datos del usuario en su sistema operativo

Ahí se guardan tanto la base de datos como la carpeta `presupuestos/` con los PDFs generados (un PDF por proyecto, con el nombre del proyecto como nombre de archivo).

## Base de datos

Tabla `proyecto`:

| Campo        | Tipo    | Descripción                          |
|--------------|---------|--------------------------------------|
| id           | INTEGER | Identificador único (autoincremental) |
| nombre       | TEXT    | Nombre del proyecto                  |
| descripcion  | TEXT    | Descripción del trabajo              |
| cliente      | TEXT    | Cliente                              |
| valor_hora   | REAL    | Tarifa aplicada                      |
| horas        | REAL    | Horas estimadas                      |
| aprobado     | INTEGER | 0 = pendiente, 1 = aprobado          |

Tabla `config`: pares clave/valor (por ahora `tarifa_a` y `tarifa_b`).

## Empaquetado (próximamente)

Se planea distribuir un único ejecutable `gestor.exe` que, en su primera ejecución, cree un acceso directo en el escritorio del usuario. La app es exclusivamente para Windows/PC.
