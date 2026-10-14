from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def export_pdf(data):

    headers = ["ID", "Producto", "Categoría", "Precio ($)", "Ventas (Unid)"]

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

    col_widths = [40, 160, 100, 80, 80]

    pdf_table = Table([header_paragraphs] + data_paragraphs, colWidths=col_widths, repeatRows=1)

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

    doc.build(story)

    print("\n[EXITO] Archivo 'reporte_ejecutivo_ventas.pdf' generado correctamente")