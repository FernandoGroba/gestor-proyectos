import flet as ft
import db
import generate_pdf

# ── Paleta del wireframe ──
CYAN       = "#00d4d4"
VERDE      = "#4ade80"
AMARILLO   = "#facc15"
ROJO       = "#f87171"
GRIS_FONDO = "#3a3a3a"
GRIS_PANEL = "#2d2d2d"
GRIS_INPUT = "#2a2a2a"


def main(page: ft.Page):
    page.title = "Gestor de Proyectos Freelance"
    page.window.width = 1000
    page.window.height = 700
    page.padding = 24
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = GRIS_FONDO
    page.scroll = ft.ScrollMode.AUTO

    db.init_db()
    editing_id = None

    # ── Campos del formulario ──
    campo_nombre = ft.TextField(
        label="Nombre del Proyecto",
        bgcolor=GRIS_INPUT,
        border_color=CYAN,
        focused_border_color=CYAN,
        color="white",
        label_style=ft.TextStyle(color="white"),
    )
    campo_cliente = ft.TextField(
        label="Cliente",
        bgcolor=GRIS_INPUT,
        border_color=CYAN,
        focused_border_color=CYAN,
        color="white",
        label_style=ft.TextStyle(color="white"),
    )
    campo_tarifa = ft.Dropdown(
        label="Tarifa",
        options=[
            ft.DropdownOption(key="8000",  text="A - $8.000"),
            ft.DropdownOption(key="10650", text="B - $10.650"),
        ],
        bgcolor=GRIS_INPUT,
        border_color=CYAN,
        focused_border_color=CYAN,
        color="white",
        label_style=ft.TextStyle(color="white"),
        expand=True,
    )
    campo_horas = ft.TextField(
        label="Horas",
        bgcolor=GRIS_INPUT,
        border_color=CYAN,
        focused_border_color=CYAN,
        color="white",
        label_style=ft.TextStyle(color="white"),
        expand=True,
    )
    campo_descripcion = ft.TextField(
        label="Descripcion",
        multiline=True,
        min_lines=4,
        max_lines=4,
        bgcolor=GRIS_INPUT,
        border_color=CYAN,
        focused_border_color=CYAN,
        color="white",
        label_style=ft.TextStyle(color="white"),
    )

    campo_estado = ft.Dropdown(
        label="Estado",
        value="1",
        options=[
            ft.DropdownOption(key="1", text="Aprobado",     style=ft.ButtonStyle(text_style=ft.TextStyle(color=VERDE))),
            ft.DropdownOption(key="2", text="Pendiente",    style=ft.ButtonStyle(text_style=ft.TextStyle(color=AMARILLO))),
            ft.DropdownOption(key="0", text="No Aprobado",  style=ft.ButtonStyle(text_style=ft.TextStyle(color=ROJO))),
        ],
        bgcolor=GRIS_INPUT,
        border_color=CYAN,
        focused_border_color=CYAN,
        color="white",
        label_style=ft.TextStyle(color="white"),
        expand=True,
    )

    etiqueta_total = ft.Text("Total: $0", size=16, weight=ft.FontWeight.BOLD, color="white")

    # ── Panel derecho: filtro + lista ──
    filtro_dropdown = ft.Dropdown(
        label="Filtrar por estado",
        value="todas",
        options=[
            ft.DropdownOption(key="todas", text="Todas"),
            ft.DropdownOption(key="2",     text="Pendientes"),
            ft.DropdownOption(key="1",     text="Aprobadas"),
            ft.DropdownOption(key="0",     text="No Aprobadas"),
        ],
        on_select=lambda e: cargar_lista(e.control.value),
        bgcolor=GRIS_INPUT,
        border_color=CYAN,
        focused_border_color=CYAN,
        color="white",
        label_style=ft.TextStyle(color="white"),
        width=220,
    )

    lista = ft.ListView(expand=True, spacing=0)

    # ── Funciones ──
    def estado_info(valor):
        if valor == 1:
            return "Aprobado", VERDE
        if valor == 2:
            return "Pendiente", AMARILLO
        return "No Aprobado", ROJO

    def crear_tarjeta(p):
        estado_txt, estado_color = estado_info(p["aprobado"])
        total = int(p["valor_hora"] * p["horas"])

        lineas = [l.strip() for l in (p["descripcion"] or "").split("\n") if l.strip()]
        bullets = [ft.Text(f"• {l}", color="white", size=13) for l in lineas]

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(p["nombre"], size=20, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.EDIT_OUTLINED,
                            icon_color=CYAN,
                            data=p["id"],
                            on_click=edita_proyecto,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE,
                            icon_color=ROJO,
                            data=p["id"],
                            on_click=eliminar_proyecto_por_id,
                        ),
                    ], spacing=4),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Row([
                    ft.Text(p["cliente"], color="white70", size=13),
                    ft.Text("•", color="white70", size=13),
                    ft.Text(f"${total:,}", color="white70", size=13),
                    ft.Text("•", color="white70", size=13),
                    ft.Text(f"$/h {int(p['valor_hora']):,}", color="white70", size=13),
                    ft.Text("•", color="white70", size=13),
                    ft.Text(estado_txt, color=estado_color, weight=ft.FontWeight.BOLD, size=13),
                ], spacing=6, wrap=True),
                ft.Text("Descripción del proyecto es hacer:", color="white", size=13),
                ft.Column(bullets, spacing=2) if bullets else ft.Container(),
            ], spacing=6),
            bgcolor=GRIS_PANEL,
            border=ft.Border.all(1, CYAN),
            border_radius=12,
            padding=16,
            margin=ft.Margin.only(bottom=10),
            data=p["id"],
            on_click=edita_proyecto,
        )

    def cargar_lista(filtro="todas"):
        lista.controls.clear()
        for p in db.list_proyectos(filtro):
            lista.controls.append(crear_tarjeta(p))
        page.update()

    def limpiar_form():
        nonlocal editing_id
        editing_id = None
        campo_nombre.value = ""
        campo_cliente.value = ""
        campo_descripcion.value = ""
        campo_tarifa.value = ""
        campo_horas.value = ""
        campo_estado.value = "1"
        etiqueta_total.value = "Total: $0"
        page.update()

    def nuevo_proyecto(e):
        limpiar_form()

    def guardar_proyecto(e):
        nonlocal editing_id
        try:
            horas = float(campo_horas.value or 0)
            valor_hora = float(campo_tarifa.value or 0)
        except (TypeError, ValueError):
            etiqueta_total.value = "Error: tarifa y horas deben ser números"
            page.update()
            return

        datos = {
            "nombre": campo_nombre.value,
            "descripcion": campo_descripcion.value,
            "cliente": campo_cliente.value,
            "valor_hora": valor_hora,
            "horas": horas,
            "aprobado": int(campo_estado.value),
        }

        if editing_id is None:
            db.insertar_proyecto(datos)
        else:
            db.update_proyecto(editing_id, datos)

        cargar_lista(filtro_dropdown.value)
        nuevo_proyecto(e)

    def edita_proyecto(e):
        nonlocal editing_id
        proyecto = db.get_proyecto(e.control.data)
        if proyecto is None:
            return
        editing_id = proyecto["id"]
        campo_nombre.value = proyecto["nombre"]
        campo_cliente.value = proyecto["cliente"]
        campo_descripcion.value = proyecto["descripcion"]
        campo_tarifa.value = str(int(proyecto["valor_hora"]))
        campo_horas.value = str(proyecto["horas"])
        campo_estado.value = str(proyecto["aprobado"])
        total = int(proyecto["valor_hora"] * proyecto["horas"])
        etiqueta_total.value = f"Total: ${total:,}"
        page.update()

    def eliminar_proyecto_por_id(e):
        pid = e.control.data

        def confirmar(e):
            db.eliminar_proyecto(pid)
            page.pop_dialog()
            cargar_lista(filtro_dropdown.value)
            nonlocal editing_id
            if editing_id == pid:
                limpiar_form()

        dialogo = ft.AlertDialog(
            title=ft.Text("Eliminar proyecto", color="white"),
            content=ft.Text("¿Seguro que querés eliminar este proyecto?", color="white70"),
            bgcolor=GRIS_PANEL,
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.pop_dialog()),
                ft.FilledButton("Eliminar", bgcolor=ROJO, on_click=confirmar),
            ],
        )
        page.show_dialog(dialogo)

    def generar_pdf(e):
        nonlocal editing_id
        if editing_id is None:
            etiqueta_total.value = "Error: selecciona un proyecto primero"
            page.update()
            return
        proyecto = db.get_proyecto(editing_id)
        ruta = generate_pdf.generate_pdf(proyecto)
        etiqueta_total.value = f"PDF guardado en:\n{ruta}"
        page.update()

    # ── Botones ──
    def pill(text, bg, fg, on_click):
        return ft.ElevatedButton(
            text,
            bgcolor=bg,
            color=fg,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20),
                padding=ft.Padding.symmetric(horizontal=16, vertical=12),
            ),
            on_click=on_click,
        )

    boton_nuevo  = pill("Nuevo proyecto", CYAN,     "black", nuevo_proyecto)
    boton_guardar = pill("Guardar",        VERDE,    "black", guardar_proyecto)
    boton_pdf    = pill("Generar PDF",    AMARILLO, "black", generar_pdf)

    # ── Layout izquierdo ──
    columna_izquierda = ft.Column(
        controls=[
            campo_nombre,
            campo_cliente,
            ft.Row(                           
                [campo_tarifa, campo_horas],
                spacing=10,
                expand=True,                 
            ),
            campo_descripcion,
            ft.Text("Estado", color="white", weight=ft.FontWeight.BOLD, size=14),
            campo_estado,
            etiqueta_total,
            ft.Row(
                [boton_nuevo, boton_guardar],
                spacing=8,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [boton_pdf],
                spacing=8,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        spacing=12,
        height=580,
    )

    panel_izquierdo = ft.Container(
        content=columna_izquierda,
        border=ft.Border.all(1.5, CYAN),
        border_radius=16,
        padding=20,
        bgcolor=GRIS_PANEL,
        width=340,
    )

    panel_derecho = ft.Container(
        content=ft.Column([
            ft.Row([filtro_dropdown], alignment=ft.MainAxisAlignment.START),
            lista,
        ], spacing=12, height=580),
        border=ft.Border.all(1.5, CYAN),
        border_radius=16,
        padding=20,
        bgcolor=GRIS_PANEL,
        width=560,
    )

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    cargar_lista()
    page.add(
        ft.Container(
            content=ft.Row(
                controls=[panel_izquierdo, panel_derecho],
                spacing=20,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            width=1040,
            height=600,
        )
    )


ft.run(main)