from database.connection import get_connection
from database.connection import insert_integrante
from database.connection import insert_instrumento
from database.connection import insert_melodia
from database.connection import assign_instrumento_melodia
from database.create_database import create_database

def main():
    while True:
        cursor = get_connection()

        print("############################################")
        print("### Sistema de Gestión de Ecos del Valle ###")
        print("############################################\n\n")

        print("1. Crear base de datos")
        print("2. Ingresar un integrante")
        print("3. Ingresar un instrumento")
        print("4. Ingresar una melodía")
        print("5. Asignar instrumento y melodía a un integrante")
        print("6. Salir\n")

        choice = input("Selecciona una opción (1-6): ")

        if choice == '1':
            create_database()
            break

        elif choice == '2':
            nombre = input("Ingrese el nombre del integrante: ")
            rol = input("Ingrese el rol del integrante: ")
            data = (nombre, rol)
            insert_integrante(cursor, data)
            break
        
        elif choice == '3':
            nombre = input("Ingrese el nombre del instrumento: ")
            tipo = input("Ingrese el tipo del instrumento: ")
            data = (nombre, tipo)
            insert_instrumento(cursor, data)
            break

        elif choice == '4':
            titulo = input("Ingrese el título de la melodía: ")
            genero = input("Ingrese el género de la melodía: ")
            data = (titulo, genero)
            insert_melodia(cursor, data)
            break

        elif choice == '5':
            integrante_id = input("Ingrese el ID del integrante: ")
            instrumento_id = input("Ingrese el ID del instrumento: ")
            melodia_id = input("Ingrese el ID de la melodía: ")
            puesto = input("Ingrese el puesto del integrante en la melodía: ")
            data = (integrante_id, instrumento_id, melodia_id, puesto)
            assign_instrumento_melodia(cursor, data)
            break

        elif choice == '6':
            cursor.close()     
            print("Conexión cerrada.\n")
            print("Saliendo del sistema...")
            break


if __name__ == "__main__":
    main()
