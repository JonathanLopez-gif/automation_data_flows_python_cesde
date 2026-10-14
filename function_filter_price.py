from tabulate import tabulate

def filter_price(data):

    headers = ["ID", "Producto", "Categoría", "Precio ($)", "Ventas (Unid)"]

    alignments = ("center", "left", "center", "right", "right")

    print(f"\n=== PRODUCTOS CON PRECIO SUPERIOR A $100 ({len(data)} PRODUCTOS) ===")

    print(tabulate(data, headers=headers, tablefmt="fancy_grid", colalign=alignments))