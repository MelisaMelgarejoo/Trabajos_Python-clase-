import json
import os
from datetime import datetime

# Archivos donde se guardarán los datos
PACIENTES_FILE = 'pacientes.json'
MEDICOS_FILE = 'medicos.json'

# Funciones de utilidad
def cargar_datos(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_datos(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def calcular_edad(fecha_nacimiento_str):
    nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d")
    hoy = datetime.today()
    edad = hoy.year - nacimiento.year - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))
    return edad

# Gestión de Médicos
def listar_medicos():
    medicos = cargar_datos(MEDICOS_FILE)
    print("\n--- Lista de Médicos ---")
    for medico in medicos:
        print(f"{medico['nombre']} {medico['apellido']} - Especialidad: {medico['especialidad']}")

def registrar_medico():
    medicos = cargar_datos(MEDICOS_FILE)
    nombre = input("Nombre del médico: ")
    apellido = input("Apellido del médico: ")
    especialidad = input("Especialidad: ")
    medico = {"nombre": nombre, "apellido": apellido, "especialidad": especialidad}
    medicos.append(medico)
    guardar_datos(MEDICOS_FILE, medicos)
    print("Médico registrado exitosamente.")

# Gestión de Pacientes
def obtener_nuevo_id_paciente(pacientes):
    if not pacientes:
        return 1
    else:
        return max(p['historia_clinica'] for p in pacientes) + 1

def registrar_paciente():
    pacientes = cargar_datos(PACIENTES_FILE)
    historia_clinica = obtener_nuevo_id_paciente(pacientes)
    documento = input("Documento de Identidad: ")
    apellido = input("Apellido: ")
    nombre = input("Nombre: ")
    fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ")
    nacionalidad = input("Nacionalidad: ")
    
    paciente = {
        "historia_clinica": historia_clinica,
        "documento": documento,
        "apellido": apellido,
        "nombre": nombre,
        "fecha_nacimiento": fecha_nacimiento,
        "nacionalidad": nacionalidad,
        "historias": []
    }
    pacientes.append(paciente)
    guardar_datos(PACIENTES_FILE, pacientes)
    print(f"Paciente registrado exitosamente. Nº Historia Clínica: {historia_clinica}")

def editar_paciente():
    pacientes = cargar_datos(PACIENTES_FILE)
    documento = input("Ingrese el Documento del paciente a editar: ")
    paciente = next((p for p in pacientes if p['documento'] == documento), None)
    if paciente:
        print(f"Editando paciente {paciente['nombre']} {paciente['apellido']}")
        paciente['apellido'] = input(f"Apellido [{paciente['apellido']}]: ") or paciente['apellido']
        paciente['nombre'] = input(f"Nombre [{paciente['nombre']}]: ") or paciente['nombre']
        paciente['fecha_nacimiento'] = input(f"Fecha Nacimiento [{paciente['fecha_nacimiento']}]: ") or paciente['fecha_nacimiento']
        paciente['nacionalidad'] = input(f"Nacionalidad [{paciente['nacionalidad']}]: ") or paciente['nacionalidad']
        guardar_datos(PACIENTES_FILE, pacientes)
        print("Paciente actualizado.")
    else:
        print("Paciente no encontrado.")

def eliminar_paciente():
    pacientes = cargar_datos(PACIENTES_FILE)
    documento = input("Ingrese el Documento del paciente a eliminar: ")
    pacientes = [p for p in pacientes if p['documento'] != documento]
    guardar_datos(PACIENTES_FILE, pacientes)
    print("Paciente eliminado (si existía).")

# Historias Clínicas
def agregar_historia_clinica():
    pacientes = cargar_datos(PACIENTES_FILE)
    documento = input("Documento de paciente para agregar historia clínica: ")
    paciente = next((p for p in pacientes if p['documento'] == documento), None)
    if paciente:
        fecha = input("Fecha de atención (YYYY-MM-DD): ")
        enfermedad = input("Enfermedad/afección: ")
        medico = input("Médico tratante: ")
        observaciones = input("Observaciones: ")
        
        historia = {
            "fecha": fecha,
            "enfermedad": enfermedad,
            "medico": medico,
            "observaciones": observaciones
        }
        paciente['historias'].append(historia)
        guardar_datos(PACIENTES_FILE, pacientes)
        print("Historia clínica agregada.")
    else:
        print("Paciente no encontrado.")

# Búsquedas
def buscar_paciente():
    pacientes = cargar_datos(PACIENTES_FILE)
    print("\nCriterios de búsqueda:")
    print("1. Por apellido y/o nombre")
    print("2. Por rango de fechas de atención")
    print("3. Por enfermedad/afección")
    print("4. Por médico que lo trató")
    print("5. Por nacionalidad")
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        term = input("Ingrese apellido y/o nombre: ").lower()
        resultados = [p for p in pacientes if term in p['apellido'].lower() or term in p['nombre'].lower()]
    elif opcion == "2":
        fecha_inicio = input("Fecha inicio (YYYY-MM-DD): ")
        fecha_fin = input("Fecha fin (YYYY-MM-DD): ")
        resultados = []
        for p in pacientes:
            for h in p['historias']:
                if fecha_inicio <= h['fecha'] <= fecha_fin:
                    resultados.append(p)
                    break
    elif opcion == "3":
        enfermedad = input("Ingrese enfermedad/afección: ").lower()
        resultados = []
        for p in pacientes:
            for h in p['historias']:
                if enfermedad in h['enfermedad'].lower():
                    resultados.append(p)
                    break
    elif opcion == "4":
        medico = input("Ingrese nombre del médico tratante: ").lower()
        resultados = []
        for p in pacientes:
            for h in p['historias']:
                if medico in h['medico'].lower():
                    resultados.append(p)
                    break
    elif opcion == "5":
        nacionalidad = input("Ingrese nacionalidad: ").lower()
        resultados = [p for p in pacientes if nacionalidad in p['nacionalidad'].lower()]
    else:
        print("Opción inválida.")
        return

    if resultados:
        for paciente in resultados:
            edad = calcular_edad(paciente['fecha_nacimiento'])
            print(f"\nPaciente: {paciente['nombre']} {paciente['apellido']} - Edad: {edad} años")
            print(f"Documento: {paciente['documento']} - Nacionalidad: {paciente['nacionalidad']}")
            for historia in paciente['historias']:
                print(f"  Historia Clínica - Fecha: {historia['fecha']}, Enfermedad: {historia['enfermedad']}, Médico: {historia['medico']}")
    else:
        print("No se encontraron pacientes.")

# Menú principal
def menu():
    while True:
        print("\n--- Instituto Médico Las Luciérnagas ---")
        print("1. Registrar nuevo paciente")
        print("2. Editar paciente existente")
        print("3. Eliminar paciente")
        print("4. Agregar historia clínica a un paciente")
        print("5. Buscar pacientes")
        print("6. Registrar médico")
        print("7. Listar médicos")
        print("0. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_paciente()
        elif opcion == "2":
            editar_paciente()
        elif opcion == "3":
            eliminar_paciente()
        elif opcion == "4":
            agregar_historia_clinica()
        elif opcion == "5":
            buscar_paciente()
        elif opcion == "6":
            registrar_medico()
        elif opcion == "7":
            listar_medicos()
        elif opcion == "0":
            print("Saliendo del sistema.")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    menu()
