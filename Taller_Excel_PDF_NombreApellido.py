import openpyxl
from tabulate import tabulate
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

wb = openpyxl.load_workbook("ventas_tecnologia_v2.xlsx", data_only=True)
sheet = wb.active

data = []

for row in sheet.iter_rows(min_row=2, values_only=True):
    data.append(list(row))

# Calcular las métricas
total_units = sum(r[4] for r in data)

average_price = (sum(r[3] for r in data) / len(data) if data else 0)

# Mostrar en consola (tabulate)
headers = ["ID", "Producto", "Categoría", "Precio ($)", "Ventas (Unid)"]
alignments = ("center", "left", "center", "right", "right")

print(f"\n=== REPORTE DE VENTAS EN CONSOLA ({len(data)} PRODUCTOS) ===")
print(tabulate(data, headers=headers, tablefmt="fancy_grid", colalign=alignments))

# Mostrar las métricas al final de la consola
print("\n=== RESUMEN DE MÉTRICAS ===")
print(f"Total de Unidades Vendidas: {total_units}")
print(f"Precio Promedio de los Productos: ${average_price:,.2f}")

# Generar el informe en PDF (ReportLab)

doc = SimpleDocTemplate("reporte_ejecutivo_ventas.pdf", pagesize=letter)
styles = getSampleStyleSheet()

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
summary_label_style = ParagraphStyle(
    "SummaryLabelStyle",
    parent=body_style,
    fontName="Helvetica-Bold",
    alignment=1
)
summary_number_style = ParagraphStyle(
    "SummaryNumberStyle",
    parent=body_style,
    fontName="Helvetica-Bold",
    alignment=2,
)

story = [
    Paragraph("Informe Ejecutivo de Ventas Tecno", title_style),
    Paragraph(f"<b>Total de Productos Procesados:</b> {len(data)}", body_style),
    Spacer(1, 12) 
]

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

# Agregar resumen de métricas al final del PDF
summary_row = [
    Paragraph("RESUMEN DE MÉTRICAS", summary_label_style),
    "",
    "",
    Paragraph(f"Total de Unidades Vendidas: {total_units}", summary_number_style),
    Paragraph(f"Precio Promedio de los Productos: ${average_price:,.2f}", summary_number_style)
]

col_widths = [40, 160, 100, 80, 80]
pdf_table = Table([header_paragraphs] + data_paragraphs + [summary_row], colWidths=col_widths, repeatRows=1)

pdf_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1A365D")), 
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), 
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")), 
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
    # Combina las tres primeras columnas de la fila de resumen en una sola celda
    ("SPAN", (0, -1), (2, -1)),
    # Color especial para la fila de resumen
    ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#E2E8F0")),
    # Linea de separación más gruesa para la fila de resumen
    ("LINEABOVE", (0, -1), (-1, -1), 1, colors.HexColor("#1A365D")),
    # Espaciado interno para la fila de resumen
    ("TOPPADDING", (0, -1), (-1, -1), 7),
    ("BOTTOMPADDING", (0, -1), (-1, -1), 7)
]))

story.append(pdf_table)

doc.build(story)

print("\n[EXITO] Archivo 'reporte_ejecutivo_ventas.pdf' generado correctamente.")


