from tabulate import tabulate

def see_full_catalog(data):

    headers = ["ID", "Producto", "Categoría", "Precio ($)", "Ventas (Unid)"]

    alignments = ("center", "left", "center", "right", "right")

    print(f"\n=== REPORTE DE VENTAS EN CONSOLA ({len(data)} PRODUCTOS) ===")

    print(tabulate(data, headers=headers, tablefmt="fancy_grid", colalign=alignments))