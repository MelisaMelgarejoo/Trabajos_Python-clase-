import json
import os
from datetime import datetime

# Archivos donde se guardarán los datos
CLIENTES_FILE = 'clientes.json'
COMPROBANTES_FILE = 'comprobantes.json'

# Funciones auxiliares
def cargar_datos(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_datos(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def completar_numero(num, largo):
    return str(num).zfill(largo)

def buscar_cliente(cuit):
    clientes = cargar_datos(CLIENTES_FILE)
    return next((cliente for cliente in clientes if cliente['cuit'] == cuit), None)

def cliente_existe(cuit):
    return buscar_cliente(cuit) is not None

def comprobante_existe(tipo, punto_venta, numero):
    comprobantes = cargar_datos(COMPROBANTES_FILE)
    for c in comprobantes:
        if (c['tipo'] == tipo and c['punto_venta'] == punto_venta and c['numero'] == numero):
            return True
    return False

# Gestión de Clientes
def registrar_cliente():
    clientes = cargar_datos(CLIENTES_FILE)
    cuit = input("CUIT/CUIL: ")
    if cliente_existe(cuit):
        print("El cliente ya existe.")
        return
    apellido = input("Apellido: ")
    nombre = input("Nombre: ")
    domicilio = input("Domicilio: ")
    cliente = {"cuit": cuit, "apellido": apellido, "nombre": nombre, "domicilio": domicilio}
    clientes.append(cliente)
    guardar_datos(CLIENTES_FILE, clientes)
    print("Cliente registrado.")

def editar_cliente():
    clientes = cargar_datos(CLIENTES_FILE)
    cuit = input("CUIT/CUIL del cliente a editar: ")
    cliente = next((c for c in clientes if c['cuit'] == cuit), None)
    if cliente:
        print(f"Editando cliente {cliente['nombre']} {cliente['apellido']}")
        cliente['apellido'] = input(f"Apellido [{cliente['apellido']}]: ") or cliente['apellido']
        cliente['nombre'] = input(f"Nombre [{cliente['nombre']}]: ") or cliente['nombre']
        cliente['domicilio'] = input(f"Domicilio [{cliente['domicilio']}]: ") or cliente['domicilio']
        guardar_datos(CLIENTES_FILE, clientes)
        print("Cliente actualizado.")
    else:
        print("Cliente no encontrado.")

def eliminar_cliente():
    clientes = cargar_datos(CLIENTES_FILE)
    cuit = input("CUIT/CUIL del cliente a eliminar: ")
    clientes = [c for c in clientes if c['cuit'] != cuit]
    guardar_datos(CLIENTES_FILE, clientes)
    print("Cliente eliminado (si existía).")

# Gestión de Comprobantes
def registrar_comprobante():
    comprobantes = cargar_datos(COMPROBANTES_FILE)
    
    fecha = input("Fecha (YYYY-MM-DD): ")
    tipo = input("Tipo de Comprobante (A/B/C): ").upper()
    punto_venta = completar_numero(input("Punto de Venta (4 cifras): "), 4)
    numero = completar_numero(input("Número de Comprobante (8 cifras): "), 8)

    if comprobante_existe(tipo, punto_venta, numero):
        print("Ya existe un comprobante con esos datos.")
        return
    
    cuit_cliente = input("CUIT/CUIL del Cliente: ")
    cliente = buscar_cliente(cuit_cliente)
    if not cliente:
        print("Cliente no encontrado. Regístrelo primero.")
        return
    
    detalles = []
    total_importe = 0
    item_num = 1
    while True:
        producto = input(f"Producto Ítem {item_num}: ")
        cantidad = int(input("Cantidad: "))
        precio_unitario = float(input("Precio Unitario: "))
        if precio_unitario <= 0:
            print("El precio unitario debe ser mayor que 0.")
            continue
        total_item = cantidad * precio_unitario
        detalles.append({
            "item_numero": item_num,
            "producto": producto,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "total": total_item
        })
        total_importe += total_item
        otro = input("¿Agregar otro ítem? (s/n): ").lower()
        if otro != 's':
            break
        item_num += 1
    
    comprobante = {
        "fecha": fecha,
        "tipo": tipo,
        "punto_venta": punto_venta,
        "numero": numero,
        "importe_total": total_importe,
        "cliente": cliente,
        "detalles": detalles
    }
    comprobantes.append(comprobante)
    guardar_datos(COMPROBANTES_FILE, comprobantes)
    print("Comprobante registrado exitosamente.")

# Listados
def listar_comprobantes_por_cliente():
    comprobantes = cargar_datos(COMPROBANTES_FILE)
    cuit = input("Ingrese CUIT/CUIL del Cliente: ")
    filtrados = [c for c in comprobantes if c['cliente']['cuit'] == cuit]
    mostrar_comprobantes(filtrados)

def listar_comprobantes_por_fecha():
    comprobantes = cargar_datos(COMPROBANTES_FILE)
    fecha_inicio = input("Fecha inicio (YYYY-MM-DD): ")
    fecha_fin = input("Fecha fin (YYYY-MM-DD): ")
    filtrados = [c for c in comprobantes if fecha_inicio <= c['fecha'] <= fecha_fin]
    mostrar_comprobantes(filtrados)

def listar_comprobantes_por_producto():
    comprobantes = cargar_datos(COMPROBANTES_FILE)
    producto = input("Nombre del producto: ").lower()
    filtrados = []
    for c in comprobantes:
        for d in c['detalles']:
            if producto in d['producto'].lower():
                filtrados.append(c)
                break
    mostrar_comprobantes(filtrados)

def mostrar_comprobantes(comprobantes):
    if comprobantes:
        for c in comprobantes:
            print("\n--- Comprobante ---")
            print(f"Fecha: {c['fecha']}")
            print(f"Tipo: {c['tipo']}, Punto de Venta: {c['punto_venta']}, Número: {c['numero']}")
            print(f"Cliente: {c['cliente']['nombre']} {c['cliente']['apellido']} ({c['cliente']['cuit']})")
            print(f"Importe Total: ${c['importe_total']:.2f}")
            print("Detalles:")
            for d in c['detalles']:
                print(f"  Ítem {d['item_numero']}: {d['producto']} x{d['cantidad']} - ${d['precio_unitario']} c/u - Total: ${d['total']}")
    else:
        print("No se encontraron comprobantes.")

# Menú principal
def menu():
    while True:
        print("\n--- La Nave Nodriza ---")
        print("1. Registrar cliente")
        print("2. Editar cliente")
        print("3. Eliminar cliente")
        print("4. Registrar comprobante")
        print("5. Listar comprobantes por cliente")
        print("6. Listar comprobantes por rango de fechas")
        print("7. Listar comprobantes por producto")
        print("0. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_cliente()
        elif opcion == "2":
            editar_cliente()
        elif opcion == "3":
            eliminar_cliente()
        elif opcion == "4":
            registrar_comprobante()
        elif opcion == "5":
            listar_comprobantes_por_cliente()
        elif opcion == "6":
            listar_comprobantes_por_fecha()
        elif opcion == "7":
            listar_comprobantes_por_producto()
        elif opcion == "0":
            print("Saliendo del sistema.")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    menu()
