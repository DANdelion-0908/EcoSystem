from database.connection import get_connection, insert_member, insert_instrument, insert_melody, assign_instrument_member_melody, get_all_members, get_all_instruments, get_all_melodies, get_members_by_melody
from database.create_database import create_database
import mariadb, os

MANDATORY_POSITIONS = [
    "Piccolo", 
    "Tiple", 
    "Centro", 
    "Bajo", 
    "Piccolo segundo", 
    "Tiple segundo", 
    "Bajo tenor",
    "Batería"]

def check_mandatory_positions_filled(melody_id: str, members_in_melody: dict) -> bool:
    """Verifica si todos los puestos obligatorios han sido llenados para una melodía específica.

    Args:
        melody_id (str): ID de la melodía a verificar.
        members_in_melody (dict): Miembros asignados a la melodía.

    Returns:
        bool: True si todos los puestos obligatorios están llenos, False en caso contrario.
    """
    positions_filled = {position: False for position in MANDATORY_POSITIONS}

    for member_details in members_in_melody.values():
        if member_details['puesto'].capitalize() in MANDATORY_POSITIONS:
            positions_filled[member_details['puesto'].capitalize()] = True

        if all(positions_filled.values()):
            print(f"\nTodos los puestos obligatorios para la melodía con ID {melody_id} han sido llenados.\n")
            return True

    for position, filled in positions_filled.items():
        if not filled:
            print(f"No se ha llenado el puesto '{position}' para la melodía {members_in_melody[1]['melodia']}.")
        
    return False

def main():
    cursor: mariadb.Cursor = get_connection()
    
    while True:

        print("############################################")
        print("### Sistema de Gestión de Ecos del Valle ###")
        print("############################################")

        print("\n1. Crear base de datos")
        print("2. Ingresar un integrante")
        print("3. Ingresar un instrumento")
        print("4. Ingresar una melodía")
        print("5. Asignar instrumento y melodía a un integrante")
        print("6. Opciones de consulta")
        print("7. Salir\n")

        choice: str = input("Selecciona una opción (1-7): ")

        if choice == '1':           # Extraño los switch case...
            create_database()

        elif choice == '2':
            name: str = input("Ingrese el nombre del integrante: ")
            role: str = input("Ingrese el rol del integrante: ")
            print()

            member_data: tuple[str, str] = (name, role)
            insert_member(cursor, member_data)
        
        elif choice == '3':
            name: str = input("Ingrese el nombre del instrumento: ")
            instrument_type: str = input("Ingrese el tipo del instrumento: ")
            print()

            instrument_data: tuple[str, str] = (name, instrument_type)
            insert_instrument(cursor, instrument_data)

        elif choice == '4':
            title: str = input("Ingrese el título de la melodía: ")
            genre: str = input("Ingrese el género de la melodía: ")
            print()

            melody_data: tuple[str, str] = (title, genre)
            insert_melody(cursor, melody_data)

        elif choice == '5':
            member_id: str = input("Ingrese el ID del integrante: ")
            instrument_id: str = input("Ingrese el ID del instrumento: ")
            melody_id: str = input("Ingrese el ID de la melodía: ")
            position: str = input("Ingrese el puesto del integrante en la melodía: ")
            print()

            assignment_data: tuple[str, str, str, str] = (member_id, instrument_id, melody_id, position)
            assign_instrument_member_melody(cursor, assignment_data)

        elif choice == '6':

            while True:

                print("\n############################")
                print("### Opciones de consulta ###")
                print("############################")

                print("\n1. Ver todos los integrantes")
                print("2. Ver todos los instrumentos")
                print("3. Ver todas las melodías")
                print("4. Ver miembros que participan en una melodía específica")
                print("5. Volver al menú principal\n")

                sub_choice: str = input("Selecciona una opción (1-5): ")

                if sub_choice == "1":
                    members = get_all_members(cursor)

                    if not members:
                        print("\nNo hay integrantes registrados.\n")
                    
                    print("\nLista de Integrantes:")
                    
                    for member in members:
                        print(f"ID: {member[0]}, Nombre: {member[1]}, Rol: {member[2]}")
                    print()

                elif sub_choice == "2":
                    instruments = get_all_instruments(cursor)

                    if not instruments:
                        print("\nNo hay instrumentos registrados.\n")

                    print("\nLista de Instrumentos:")

                    for instrument in instruments:
                        print(f"ID: {instrument[0]}, Nombre: {instrument[1]}, Tipo: {instrument[2]}")
                    print()

                elif sub_choice == "3":
                    melodies = get_all_melodies(cursor)

                    if not melodies:
                        print("\nNo hay melodías registradas.\n")

                    print("\nLista de Melodías:")

                    for melody in melodies:
                        print(f"ID: {melody[0]}, Título: {melody[1]}, Género: {melody[2]}")
                    print()

                elif sub_choice == "4":
                    melody_id: str = input("Ingrese el ID de la melodía: ")
                    members_in_melody = get_members_by_melody(cursor, melody_id)

                    if not members_in_melody:
                        print(f"\nNo hay integrantes registrados para la melodía con ID {melody_id}.\n")

                    else:
                        print(f"\nIntegrantes que participan en la melodía {members_in_melody[1]['melodia']}:")

                        for member_id, dmember_details in members_in_melody.items():
                            print(f"ID Integrante: {member_id}, Nombre: {dmember_details['integrante']}, Instrumento: {dmember_details['instrumento']}, Puesto: {dmember_details['puesto']}")
                        print()

                        check_mandatory_positions_filled(melody_id, members_in_melody)

        elif choice == '7':
            cursor.close()
            print("Conexión cerrada.")
            print("Saliendo del sistema...")
            os._exit(0)
            break

if __name__ == "__main__":
    main()
