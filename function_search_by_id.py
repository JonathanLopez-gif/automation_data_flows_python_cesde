from tabulate import tabulate

def search_by_id(data):

    headers = ["ID", "Producto", "Categoría", "Precio ($)", "Ventas (Unid)"]
    
    alignments = ("center", "left", "center", "right", "right")

    try:
        entered_id = int(input("Ingrese el ID del producto que desea buscar: "))

        row_found = next((r for r in data if r[0] == entered_id), None)

        if row_found:
            print(f"\n=== PRODUCTO ENCONTRADO: ID {entered_id} ===")
            # tabulate necesita una lista de listas, por lo que pasamos [row_found]
            print(tabulate([row_found], headers=headers, tablefmt="fancy_grid", colalign=alignments))
        else:
            print(f"\n[ADVERTENCIA] No existe un producto con el ID {entered_id}")

    except ValueError:
        print("\n[ERROR] Por favor, ingrese un ID válido (número entero)")

