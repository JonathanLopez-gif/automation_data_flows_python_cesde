import openpyxl
from tabulate import tabulate
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# 1. Cargar el archivo Excel (load_workbook) y seleccionar la hoja activa (active)
wb = openpyxl.load_workbook("ventas_tecnologia_v2.xlsx", data_only=True)
sheet = wb.active

# 2. Leer datos dinámicamente (iter_rows)
data = []
for row in sheet.iter_rows(min_row=2, values_only=True):
    data.append(list(row))

# 3. Mostrar en consola (tabulate)
headers = ["ID", "Producto", "Categoría", "Precio ($)", "Ventas (Unid)"]
alignments = ("center", "left", "center", "right", "right")

print(f"\n=== REPORTE DE VENTAS EN CONSOLA ({len(data)} PRODUCTOS) ===")
print(tabulate(data, headers=headers, tablefmt="fancy_grid", colalign=alignments))

# 4. Generar el informe en PDF (ReportLab)

# 4.1. Crear documento base
doc = SimpleDocTemplate("reporte_ejecutivo_ventas.pdf", pagesize=letter)
styles = getSampleStyleSheet()

# 4.2. Estilos personalizados
title_style = ParagraphStyle(
    "TitleStyle", 
    parent=styles["Title"],
    fontName="Helvetica-Bold", 
    fontSize=18,
    textColor=colors.HexColor("#1A365D"), 
    spaceAfter=10
)
body_style = ParagraphStyle(
    "BodyStyle",
    parent=styles["Normal"],
    fontSize=9
)
header_style = ParagraphStyle(
    "HeaderStyle",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=10,
    textColor=colors.whitesmoke,
    alignment=1
)

# 4.3. Lista story (carrito de compras)
story = [
    Paragraph("Informe Ejecutivo de Ventas Tecno", title_style),
    Paragraph(f"<b>Total de Productos Procesados:</b> {len(data)}", body_style),
    # Espacio vertical de 12 puntos (ancho y alto)
    Spacer(1, 12) 
]

# 4.4. Convertir celdas a Paragraph
header_paragraphs = [Paragraph(f"<b>{h}</b>", header_style) for h in headers]
data_paragraphs = [
    [
        Paragraph(str(r[0]), ParagraphStyle("C", parent=body_style, alignment=1)),
        Paragraph(str(r[1]), ParagraphStyle("L", parent=body_style, alignment=0)),
        Paragraph(str(r[2]), ParagraphStyle("C", parent=body_style, alignment=1)),
        Paragraph(f"${r[3]:,.2f}", ParagraphStyle("R", parent=body_style, alignment=2)),
        Paragraph(str(r[4]), ParagraphStyle("R", parent=body_style, alignment=2))
    ]
    for r in data
]

# 4.5. Configurar anchos y tabla
col_widths = [40, 160, 100, 80, 80]
pdf_table = Table([header_paragraphs] + data_paragraphs, colWidths=col_widths, repeatRows=1)

# 4.6. Aplicar estilo visual con TableStyle
pdf_table.setStyle(TableStyle([
    # Color de fondo del encabezado
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1A365D")), 
    # Alineación vertical de todas las celdas
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), 
    # Dibuja bordes alrededor de todas las celdas
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")), 
    # Alterna colores de fondo para las filas de datos
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]) 
]))

story.append(pdf_table)

# 4.7. Compilar PDF
doc.build(story)

print("\n[EXITO] Archivo 'reporte_ejecutivo_ventas.pdf' generado correctamente.")


