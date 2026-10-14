import openpyxl
from tabulate import tabulate
import function_see_full_catalog
import function_filter_price
import function_search_by_id
import function_export_pdf

wb = openpyxl.load_workbook("ventas_tecnologia_v2.xlsx", data_only=True)

sheet = wb.active

data = []

for row in sheet.iter_rows(min_row=2, values_only=True):
        data.append(list(row))

data_1 = []

for row in sheet.iter_rows(min_row=2, values_only=True):
    price = row[3]

    if price > 100:
        data_1.append(list(row))

# Menú interactivo
while True:
    print("=" * 50)
    print("MENU PRINCIPAL - VENTAS TECNO")
    print("=" * 50)
    print("1. Ver catálogo completo")
    print("2. Filtrar por precio (> $100)")
    print("3. Buscar por ID")
    print("4. Exportar informe PDF")
    print("5. Salir del programa")

    option = input("\nSeleccione una opción: ").strip()

    match option:

        case "1": 
            function_see_full_catalog.see_full_catalog(data)

        case "2": 
            function_filter_price.filter_price(data_1)

        case "3": 
            function_search_by_id.search_by_id(data)

        case "4": 
            function_export_pdf.export_pdf(data)

        case "5": 
            print("\nSaliendo del programa ...")
            break

        case _:
            print("\n[ADVERTENCIA] Opción inválida. Selecciona un número del 1 al 5")
