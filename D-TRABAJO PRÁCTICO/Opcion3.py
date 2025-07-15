import json
import os
from datetime import datetime

# Archivos JSON
LIBROS_FILE = 'libros.json'
SOCIOS_FILE = 'socios.json'
PRESTAMOS_FILE = 'prestamos.json'

# Funciones auxiliares
def cargar_datos(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_datos(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def obtener_nuevo_id(lista):
    if lista:
        return max(item['id'] for item in lista) + 1
    else:
        return 1

# Gestión de Libros
def registrar_libro():
    libros = cargar_datos(LIBROS_FILE)
    libro = {
        "id": obtener_nuevo_id(libros),
        "titulo": input("Título: "),
        "autor": input("Autor: "),
        "editorial": input("Editorial: "),
        "anio": input("Año de Publicación: "),
        "genero": input("Género: "),
        "cantidad": int(input("Cantidad Disponible: "))
    }
    libros.append(libro)
    guardar_datos(LIBROS_FILE, libros)
    print("Libro registrado exitosamente.")

def editar_libro():
    libros = cargar_datos(LIBROS_FILE)
    id_libro = int(input("ID de Libro a editar: "))
    libro = next((l for l in libros if l['id'] == id_libro), None)
    if libro:
        print(f"Editando {libro['titulo']}")
        libro['titulo'] = input(f"Título [{libro['titulo']}]: ") or libro['titulo']
        libro['autor'] = input(f"Autor [{libro['autor']}]: ") or libro['autor']
        libro['editorial'] = input(f"Editorial [{libro['editorial']}]: ") or libro['editorial']
        libro['anio'] = input(f"Año [{libro['anio']}]: ") or libro['anio']
        libro['genero'] = input(f"Género [{libro['genero']}]: ") or libro['genero']
        libro['cantidad'] = int(input(f"Cantidad [{libro['cantidad']}]: ") or libro['cantidad'])
        guardar_datos(LIBROS_FILE, libros)
        print("Libro actualizado.")
    else:
        print("Libro no encontrado.")

def eliminar_libro():
    libros = cargar_datos(LIBROS_FILE)
    id_libro = int(input("ID de Libro a eliminar: "))
    libros = [l for l in libros if l['id'] != id_libro]
    guardar_datos(LIBROS_FILE, libros)
    print("Libro eliminado (si existía).")

# Gestión de Socios
def registrar_socio():
    socios = cargar_datos(SOCIOS_FILE)
    socio = {
        "id": obtener_nuevo_id(socios),
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "fecha_nacimiento": input("Fecha de Nacimiento (YYYY-MM-DD): "),
        "direccion": input("Dirección: "),
        "email": input("Correo Electrónico: "),
        "telefono": input("Teléfono: ")
    }
    socios.append(socio)
    guardar_datos(SOCIOS_FILE, socios)
    print("Socio registrado exitosamente.")

def editar_socio():
    socios = cargar_datos(SOCIOS_FILE)
    id_socio = int(input("ID de Socio a editar: "))
    socio = next((s for s in socios if s['id'] == id_socio), None)
    if socio:
        print(f"Editando {socio['nombre']} {socio['apellido']}")
        socio['nombre'] = input(f"Nombre [{socio['nombre']}]: ") or socio['nombre']
        socio['apellido'] = input(f"Apellido [{socio['apellido']}]: ") or socio['apellido']
        socio['fecha_nacimiento'] = input(f"Fecha Nacimiento [{socio['fecha_nacimiento']}]: ") or socio['fecha_nacimiento']
        socio['direccion'] = input(f"Dirección [{socio['direccion']}]: ") or socio['direccion']
        socio['email'] = input(f"Email [{socio['email']}]: ") or socio['email']
        socio['telefono'] = input(f"Teléfono [{socio['telefono']}]: ") or socio['telefono']
        guardar_datos(SOCIOS_FILE, socios)
        print("Socio actualizado.")
    else:
        print("Socio no encontrado.")

def eliminar_socio():
    socios = cargar_datos(SOCIOS_FILE)
    id_socio = int(input("ID de Socio a eliminar: "))
    socios = [s for s in socios if s['id'] != id_socio]
    guardar_datos(SOCIOS_FILE, socios)
    print("Socio eliminado (si existía).")

# Gestión de Préstamos
def registrar_prestamo():
    prestamos = cargar_datos(PRESTAMOS_FILE)
    libros = cargar_datos(LIBROS_FILE)
    socios = cargar_datos(SOCIOS_FILE)

    id_socio = int(input("ID del Socio: "))
    id_libro = int(input("ID del Libro: "))
    
    socio = next((s for s in socios if s['id'] == id_socio), None)
    libro = next((l for l in libros if l['id'] == id_libro), None)

    if not socio:
        print("Socio no encontrado.")
        return
    if not libro:
        print("Libro no encontrado.")
        return
    if libro['cantidad'] <= 0:
        print("No hay copias disponibles.")
        return

    costo = float(input("Costo del préstamo (0 si no aplica): "))
    prestamo = {
        "id": obtener_nuevo_id(prestamos),
        "id_socio": id_socio,
        "id_libro": id_libro,
        "fecha_prestamo": datetime.today().strftime('%Y-%m-%d'),
        "costo": costo,
        "fecha_devolucion": None,
        "estado": "En Curso"
    }
    prestamos.append(prestamo)
    libro['cantidad'] -= 1  # Reducir cantidad disponible
    guardar_datos(PRESTAMOS_FILE, prestamos)
    guardar_datos(LIBROS_FILE, libros)
    print("Préstamo registrado exitosamente.")

def registrar_devolucion():
    prestamos = cargar_datos(PRESTAMOS_FILE)
    libros = cargar_datos(LIBROS_FILE)

    id_prestamo = int(input("ID del Préstamo: "))
    prestamo = next((p for p in prestamos if p['id'] == id_prestamo and p['estado'] == "En Curso"), None)

    if prestamo:
        prestamo['fecha_devolucion'] = datetime.today().strftime('%Y-%m-%d')
        prestamo['estado'] = "Devuelto"
        libro = next((l for l in libros if l['id'] == prestamo['id_libro']), None)
        if libro:
            libro['cantidad'] += 1
        guardar_datos(PRESTAMOS_FILE, prestamos)
        guardar_datos(LIBROS_FILE, libros)
        print("Devolución registrada exitosamente.")
    else:
        print("Préstamo no encontrado o ya devuelto.")

# Búsqueda de Libros
def buscar_libros():
    libros = cargar_datos(LIBROS_FILE)
    print("Búsqueda avanzada: puede dejar campos vacíos")
    titulo = input("Título contiene: ").lower()
    autor = input("Autor contiene: ").lower()
    genero = input("Género contiene: ").lower()
    editorial = input("Editorial contiene: ").lower()

    resultados = []
    for libro in libros:
        if (titulo in libro['titulo'].lower() and
            autor in libro['autor'].lower() and
            genero in libro['genero'].lower() and
            editorial in libro['editorial'].lower()):
            resultados.append(libro)

    if resultados:
        for l in resultados:
            print(f"\nID: {l['id']}, Título: {l['titulo']}, Autor: {l['autor']}, Editorial: {l['editorial']}, Año: {l['anio']}, Género: {l['genero']}, Disponible: {l['cantidad']}")
    else:
        print("No se encontraron libros con esos criterios.")

# Reportes
def reporte_prestamos_por_socio():
    prestamos = cargar_datos(PRESTAMOS_FILE)
    id_socio = int(input("ID de Socio: "))
    filtrados = [p for p in prestamos if p['id_socio'] == id_socio]
    mostrar_prestamos(filtrados)

def reporte_prestamos_por_libro():
    prestamos = cargar_datos(PRESTAMOS_FILE)
    id_libro = int(input("ID de Libro: "))
    filtrados = [p for p in prestamos if p['id_libro'] == id_libro]
    mostrar_prestamos(filtrados)

def reporte_prestamos_por_fecha():
    prestamos = cargar_datos(PRESTAMOS_FILE)
    fecha_inicio = input("Fecha inicio (YYYY-MM-DD): ")
    fecha_fin = input("Fecha fin (YYYY-MM-DD): ")
    filtrados = [p for p in prestamos if fecha_inicio <= p['fecha_prestamo'] <= fecha_fin]
    mostrar_prestamos(filtrados)

def mostrar_prestamos(prestamos):
    if prestamos:
        for p in prestamos:
            print(f"\nID: {p['id']}, Socio ID: {p['id_socio']}, Libro ID: {p['id_libro']}, Fecha Préstamo: {p['fecha_prestamo']}, Estado: {p['estado']}")
    else:
        print("No se encontraron préstamos.")

# Menú principal
def menu():
    while True:
        print("\n--- Sistema de Biblioteca ---")
        print("1. Registrar libro")
        print("2. Editar libro")
        print("3. Eliminar libro")
        print("4. Registrar socio")
        print("5. Editar socio")
        print("6. Eliminar socio")
        print("7. Registrar préstamo")
        print("8. Registrar devolución")
        print("9. Buscar libros")
        print("10. Reporte préstamos por socio")
        print("11. Reporte préstamos por libro")
        print("12. Reporte préstamos por fecha")
        print("0. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_libro()
        elif opcion == "2":
            editar_libro()
        elif opcion == "3":
            eliminar_libro()
        elif opcion == "4":
            registrar_socio()
        elif opcion == "5":
            editar_socio()
        elif opcion == "6":
            eliminar_socio()
        elif opcion == "7":
            registrar_prestamo()
        elif opcion == "8":
            registrar_devolucion()
        elif opcion == "9":
            buscar_libros()
        elif opcion == "10":
            reporte_prestamos_por_socio()
        elif opcion == "11":
            reporte_prestamos_por_libro()
        elif opcion == "12":
            reporte_prestamos_por_fecha()
        elif opcion == "0":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()
