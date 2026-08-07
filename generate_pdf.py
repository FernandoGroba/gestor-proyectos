from datetime import date
import os
import re
from pathlib import Path

from fpdf import FPDF
from fpdf.fonts import FontFace
from PIL import Image

BASE_DIR = Path(__file__).parent
RUTA_LOGO = BASE_DIR / "assets" / "img_presupuesto.png"

AZUL = (31, 56, 100)
GRIS_CLARO = (240, 240, 240)

ANCHO_LOGO = 40


def generate_pdf(proyecto):
    total = proyecto["valor_hora"] * proyecto["horas"]

    ancho, alto = Image.open(RUTA_LOGO).size
    alto_logo = ANCHO_LOGO * alto / ancho

    pdf = FPDF()
    pdf.set_margins(15, 15, 15)
    pdf.add_page()

    pdf.image(RUTA_LOGO, x=15, y=12, w=ANCHO_LOGO)

    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(*AZUL)
    pdf.set_y(12 + (alto_logo - 8) / 2)
    pdf.cell(0, 8, "PRESUPUESTO", align="R", ln=True)

    y_divisor = 12 + alto_logo + 6
    pdf.set_draw_color(*AZUL)
    pdf.set_line_width(0.8)
    pdf.line(15, y_divisor, 195, y_divisor)

    pdf.set_y(y_divisor + 8)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, f"Cliente: {proyecto['cliente']}", ln=True)
    pdf.cell(0, 7, f"Fecha: {date.today().strftime('%d/%m/%Y')}", ln=True)
    pdf.cell(0, 7, f"Proyecto: {proyecto['nombre']}", ln=True)
    pdf.ln(8)

    datos_tabla = [
        ["Descripcion", "Horas", "Valor hora ($)", "Subtotal ($)"],
        [proyecto["descripcion"], f"{proyecto['horas']:g}", f"{proyecto['valor_hora']:,.0f}", f"{total:,.0f}"],
        ["", "", "TOTAL", f"{total:,.0f}"],
    ]

    with pdf.table(
        col_widths=(80, 20, 30, 30),
        text_align=("LEFT", "CENTER", "RIGHT", "RIGHT"),
        headings_style=FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=AZUL),
        borders_layout="INTERNAL",
        line_height=7,
        v_align="TOP",
    ) as tabla:
        for i, fila in enumerate(datos_tabla):
            fila_row = tabla.row()
            if i == len(datos_tabla) - 1:
                fila_row.style = FontFace(emphasis="BOLD", fill_color=GRIS_CLARO)
            for dato in fila:
                fila_row.cell(dato)

    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*AZUL)
    pdf.cell(0, 8, f"Total: $ {total:,.0f}", ln=True, align="R")
    pdf.set_text_color(0, 0, 0)

    carpeta = Path(os.getenv("FLET_APP_STORAGE_DATA", str(BASE_DIR))) / "presupuestos"
    carpeta.mkdir(parents=True, exist_ok=True)
    nombre_archivo = re.sub(r'[<>:"/\\|?*]', "_", proyecto["nombre"])
    ruta = carpeta / f"presupuesto_{nombre_archivo}.pdf"
    pdf.output(ruta)
    return ruta