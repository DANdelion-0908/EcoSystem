from database.connection import get_connection
from database.connection import insert_member
from database.connection import insert_instrument
from database.connection import insert_melody
from database.connection import assign_instrument_member_melody
from database.create_database import create_database
import mariadb

def main():
    while True:
        cursor: mariadb.Cursor = get_connection()

        print("############################################")
        print("### Sistema de Gestión de Ecos del Valle ###")
        print("############################################\n\n")

        print("1. Crear base de datos")
        print("2. Ingresar un integrante")
        print("3. Ingresar un instrumento")
        print("4. Ingresar una melodía")
        print("5. Asignar instrumento y melodía a un integrante")
        print("6. Salir\n")

        choice: str = input("Selecciona una opción (1-6): ")

        if choice == '1':           # Extraño los switch case...
            create_database()
            break

        elif choice == '2':
            name: str = input("Ingrese el nombre del integrante: ")
            role: str = input("Ingrese el rol del integrante: ")
            member_data: tuple[str, str] = (name, role)
            insert_member(cursor, member_data)
            break
        
        elif choice == '3':
            name: str = input("Ingrese el nombre del instrumento: ")
            instrument_type: str = input("Ingrese el tipo del instrumento: ")
            instrument_data: tuple[str, str] = (name, instrument_type)
            insert_instrument(cursor, instrument_data)
            break

        elif choice == '4':
            title: str = input("Ingrese el título de la melodía: ")
            genre: str = input("Ingrese el género de la melodía: ")
            melody_data: tuple[str, str] = (title, genre)
            insert_melody(cursor, melody_data)
            break

        elif choice == '5':
            member_id: str = input("Ingrese el ID del integrante: ")
            instrument_id: str = input("Ingrese el ID del instrumento: ")
            melody_id: str = input("Ingrese el ID de la melodía: ")
            position: str = input("Ingrese el puesto del integrante en la melodía: ")
            assignment_data: tuple[str, str, str, str] = (member_id, instrument_id, melody_id, position)
            assign_instrument_member_melody(cursor, assignment_data)
            break

        elif choice == '6':
            cursor.close()
            print("Conexión cerrada.\n")
            print("Saliendo del sistema...")
            break


if __name__ == "__main__":
    main()
