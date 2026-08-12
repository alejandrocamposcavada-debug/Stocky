import sqlite3
import subprocess
import os

conexion = sqlite3.connect("stock.db")
cursor = conexion.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS stock (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        precio_USD REAL NOT NULL
    )
"""
)

version = 1.2

def mostrar_estadisticas():
    cursor.execute("SELECT SUM(cantidad * precio_USD), SUM(cantidad), AVG(precio_USD) FROM stock")
    total_valor, total_unidades, precio_promedio = cursor.fetchone()

    if total_valor is None:
        print("\n⚠️ El inventario está vacío. No hay estadísticas disponibles.\n")
        return

    print("\n--- ESTADÍSTICAS DEL INVENTARIO ---")
    print(f"💵 Valor total en stock: ${total_valor:.2f}")
    print(f"📦 Total de unidades: {int(total_unidades)}")
    print(f"🏷️ Precio promedio por producto: ${precio_promedio:.2f}")
    print("-----------------------------------\n")
    


def eliminar_producto():
    id_producto = int(pedir_numero("Ingrese el ID del producto a eliminar: "))

    cursor.execute("DELETE FROM stock WHERE id = ?", (id_producto,))
    if cursor.rowcount == 0:
        print(f"\n❌ No se encontró un producto con ID {id_producto}.\n")
    else:
        conexion.commit()
        print(f"\n✅ Producto con ID {id_producto} eliminado correctamente.\n")

def mostrar_inventario():
    cursor.execute("SELECT * FROM stock")
    productos = cursor.fetchall()

    if not productos:
        print("\n⚠️ El inventario está vacío.\n")
        return

    print("\n--- INVENTARIO ACTUAL ---")
    for id, nombre, cantidad, precio in productos:
        print(
            f"ID: {id} | Producto: {nombre} | Cantidad: {cantidad} | Precio: ${precio:.2f}"
        )
    print("-------------------------\n")

def pedir_numero(mensaje):
    while True:
        entrada = input(mensaje)
        try:
            numero = float(entrada)
            if numero < 0:
                print("❌ Error: Ingrese números positivos.")
                continue
            return numero
        except ValueError:
            print("❌ Error: Ingrese números enteros o decimales.")

def modificar_producto():
    id_producto = int(pedir_numero("Ingrese el ID del producto a modificar: "))
    nueva_cantidad = int(pedir_numero("Ingrese la nueva cantidad: "))
    nuevo_precio = pedir_numero("Ingrese el nuevo precio en USD: ")

    cursor.execute(
        """UPDATE stock SET cantidad = ?, precio_USD = ? WHERE id = ?""",
        (nueva_cantidad, nuevo_precio, id_producto),
    )
    if cursor.rowcount == 0:
        print(f"\n❌ No se encontró un producto con ID {id_producto}.\n")
    else:
        conexion.commit()
        print(f"\n✅ Producto con ID {id_producto} modificado correctamente.\n")

def bucle_principal():
    print("-----------------------------------")
    print(f"Bienvenido a Stocky v{version}")
    print("-----------------------------------\n")

    while True:
        print("1. Agregar un producto.")
        print("2. Mostrar los productos.")
        print("3. Modificar un producto.")
        print("4. Limpiar la pantalla.")
        print("5. Eliminar un producto.")
        print("6. Mostrar Valor total del inventario.")
        print("7. Salir.")
        opcion = input("¿Qué opción desea realizar?: ")

        if opcion == "1":
            nombre_producto = input(
                "¿Qué nombre desea ponerle a su producto?: "
            )
            cantidad = int(
                pedir_numero(f"¿Cuántas unidades tiene de {nombre_producto}?: ")
            )
            precio = pedir_numero(
                f"¿Cuál es el precio en USD de {nombre_producto}?: "
            )

            cursor.execute(
                """INSERT INTO stock (nombre, cantidad, precio_USD) VALUES (?, ?, ?)""",
                (nombre_producto, cantidad, precio),
            )
            conexion.commit() 
            print(f"\n✅ Producto registrado: {nombre_producto} | Cantidad: {cantidad} | Precio: ${precio:.2f}\n")

        elif opcion == "2":
            mostrar_inventario()

        elif opcion == "3":
            modificar_producto()

        elif opcion == "4":
            subprocess.run(["cls" if os.name == "nt" else "clear"], check=True)
            print("\n🧹 Pantalla limpiada.\n")

        elif opcion == "5":
            eliminar_producto()

        elif opcion == "6":
            mostrar_estadisticas()


        elif opcion == "7":
            print("\n¡Gracias por usar Stocky! 👋")
            break

        else:
            print("❌ Opción no válida. Intente de nuevo.\n")

bucle_principal()
conexion.commit()
conexion.close()