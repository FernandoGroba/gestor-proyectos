import flet as ft
import db
import generate_pdf

def main (page: ft.Page):
    page.title= "Gestor de Proyectos Freelance"
    page.window.width=1000
    page.window.height= 700

    db.init_db()

    def cargar_lista(filtro= "todas"):
        lista.controls.clear()
        proyectos=db.list_proyectos(filtro)
        for p in proyectos:
            lista.controls.append(ft.ListTile(
                title=ft.Text(p["nombre"]),
                subtitle=ft.Text(f"{p['cliente']} - {p['horas']} hs - ${int(p['valor_hora'] * p['horas']):,}"),
                data=p["id"],
                on_click=edita_proyecto,
            ))
        page.update()
        
            

    lista = ft.ListView(expand=True, spacing=5)
    filtro = ft.Dropdown(
        label="Filtro",
        value="todas",
        options=[
            ft.DropdownOption("todas", "Todas"),
            ft.DropdownOption("0", "Pendientes"),
            ft.DropdownOption("1", "Aprobadas")
        ],
        on_select=lambda e: cargar_lista(e.control.value),

    
    )
    columna_izquierda = ft.Column(
            controls = [filtro, lista],
            expand=True,
    )


    campo_cliente = ft.TextField(label="Cliente")
    campo_nombre = ft.TextField(label="Nombre del proyecto")
    campo_descripcion = ft.TextField(label="Descripcion", multiline=True)
    campo_tarifa = ft.Dropdown(label="Tarifa", options=[
        ft.DropdownOption("8000", "A - $8.000"),
        ft.DropdownOption("10650", "B - $10.650"),
    ])
    campo_horas = ft.TextField(label="Horas")
    check_aprobado = ft.Checkbox(label="Aprobado")
    etiqueta_total = ft.Text("Total: $0")

    editing_id = None

    def nuevo_proyecto(e):
        nonlocal editing_id
        editing_id = None
        campo_nombre.value = ""
        campo_cliente.value = ""
        campo_descripcion.value = ""
        campo_tarifa.value = ""
        campo_horas.value = "" 
        check_aprobado.value = False
        etiqueta_total.value = "Total: $0"
        page.update()

    def guardar_proyecto(e):
        nonlocal editing_id
        try:
            horas = float(campo_horas.value)
            valor_hora = float(campo_tarifa.value)
        except (TypeError, ValueError):
            etiqueta_total.value = "Error: tarifa y horas deben ser números"
            page.update()
            return
        datos = {
            "nombre" : campo_nombre.value,
            "descripcion" : campo_descripcion.value,
            "cliente" : campo_cliente.value,
            "valor_hora" : valor_hora,
            "horas" : horas,
            "aprobado" : 1 if check_aprobado.value else 0,
        }  
        if editing_id is None:
            db.insertar_proyecto(datos)
        else:
            db.update_proyecto(editing_id, datos)
        cargar_lista(filtro.value)
        nuevo_proyecto(e)
        page.update()

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
        check_aprobado.value = bool(proyecto["aprobado"])
        total = int(proyecto["valor_hora"] * proyecto["horas"])
        etiqueta_total.value = f"Total: ${total:,}"
        page.update()    
              


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

    def eliminar_proyecto(e):
        nonlocal editing_id
        if editing_id is None:
            etiqueta_total.value = "Error: selecciona un proyecto primero"
            page.update()
            return

        def confirmar(e):
            db.eliminar_proyecto(editing_id)
            page.pop_dialog()
            nuevo_proyecto(e)
            cargar_lista(filtro.value)

        dialogo = ft.AlertDialog(
            title=ft.Text("Eliminar proyecto"),
            content=ft.Text("¿Seguro que querés eliminar este proyecto?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.pop_dialog()),
                ft.FilledButton("Eliminar", on_click=confirmar),
            ],
        )
        page.show_dialog(dialogo)

    boton_guardar = ft.FilledButton("Guardar", on_click=guardar_proyecto)
    boton_nuevo = ft.OutlinedButton("Nuevo", on_click=nuevo_proyecto)
    boton_eliminar = ft.OutlinedButton("Eliminar", on_click=eliminar_proyecto)
    boton_pdf = ft.OutlinedButton("Generar PDF", on_click=generar_pdf)

    columna_derecha = ft.Column(
        controls=[
            campo_nombre,
            campo_cliente,
            campo_descripcion,
            campo_tarifa,
            campo_horas,
            check_aprobado,
            etiqueta_total,
            ft.Row(controls=[boton_guardar, boton_nuevo, boton_eliminar, boton_pdf]),
        ],
        expand=True,
    )
    cargar_lista()
    page.add(
        ft.Row(
            controls=[
                columna_izquierda,
                columna_derecha
            ]
        )
    )


ft.run(main)

    