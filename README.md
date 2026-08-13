# Gestor de Proyectos Freelance

Aplicación de escritorio para gestionar proyectos de programación freelance: carga de proyectos, seguimiento de estado, edición y borrado, y generación de presupuestos en PDF con tu marca.

## Funcionalidades

- Alta y edición de proyectos desde un formulario (Guardar / Nuevo proyecto).
- Cada proyecto de la lista es una **tarjeta** con iconos para **editar** y **borrar**.
- Borrado con diálogo de confirmación.
- Estado del proyecto como **dropdown** de colores: Aprobado (verde), Pendiente (amarillo), No Aprobado (rojo).
- Filtro de la lista por estado: todas, pendientes, aprobadas.
- Cálculo automático del total (`valor_hora * horas`) que se actualiza al cargar horas y tarifa.
- Generación de presupuesto en PDF **por proyecto**, con logo, encabezado y tabla de totales. Cada PDF se guarda dentro de la carpeta `presupuestos/`, con el **nombre del proyecto** como nombre de archivo.
- Tarifas configurables guardadas en la base de datos (`tarifa_a`, `tarifa_b`).
- Layout de dos paneles: formulario a la izquierda (altura fija) y lista de proyectos a la derecha (scroll interno).

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
main.py            Aplicación Flet: ventana, lista de tarjetas, formulario y eventos
db.py              Capa de datos: conexión a SQLite, consultas y migración automática
generate_pdf.py    Generación del presupuesto en PDF con logo y tabla
assets/
  img_presupuesto.png   Logo que aparece en el PDF
presupuestos/           PDFs generados (uno por proyecto)
```

## Dónde se guardan los datos

La app usa el directorio de datos de la aplicación (`FLET_APP_STORAGE_DATA`):

- En desarrollo: `.flet/storage/data/`
- Empaquetada: la carpeta de datos del usuario en su sistema operativo

**Migración automática:** la primera vez que se abre la app (o al empaquetar), si la base de datos existe en la carpeta del proyecto (`proyectos.db`) y aún no existe en el storage, se copia automáticamente. A partir de ahí la app usa la copia del storage.

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
| aprobado     | INTEGER | 0 = No aprobado, 1 = Aprobado, 2 = Pendiente |

Tabla `config`: pares clave/valor (por ahora `tarifa_a` y `tarifa_b`).

Funciones disponibles en `db.py`: `init_db`, `insertar_proyecto`, `list_proyectos(filtro)`, `get_proyecto(id)`, `update_proyecto(id, datos)`, `eliminar_proyecto(id)`, `get_config`, `set_config`.

## Empaquetado

La app está pensada para Windows. Se planea distribuir un único ejecutable `gestor.exe` que, en su primera ejecución, cree un acceso directo en el escritorio del usuario.

## Créditos del look & feel

El rediseño visual (tema oscuro con acento verde petróleo, layout de dos paneles y cards) fue basado en assets de `desing/`.
