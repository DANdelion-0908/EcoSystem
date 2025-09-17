from database.connection import get_connection, insert_member, insert_instrument, insert_melody, assign_instrument_member_melody, get_all_members, get_all_instruments, get_all_melodies, get_members_by_melody, delete_relations
from database.create_database import create_database
from controller.verifications import check_mandatory_positions_filled, recommend_member_for_position
import mariadb, os

def main():
    cursor: mariadb.Cursor = get_connection()
    
    while True:

        print("############################################")
        print("### Sistema de Gestión de Ecos del Valle ###")
        print("############################################")

        print("\n1. Opciones de administración")
        print("2. Opciones de inserción")
        print("3. Opciones de consulta")
        print("4. Salir\n")

        choice: str = input("Selecciona una opción (1-4): ")

        if choice == '1':           # Extraño los switch case...

            while True:

                print("##################################")
                print("### Opciones de administración ###")
                print("##################################\n")

                print("\n1. Crear la base de datos")
                print("2. Eliminar relaciones de integrantes, instrumentos y melodías")
                print("3. Volver al menú principal\n")

                admin_choice: str = input("Selecciona una opción (1-3): ")

                if admin_choice == '1':
                    create_database()

                elif admin_choice == '2':
                    delete_relations(cursor)

                elif admin_choice == '3':
                    break

        elif choice == '2':
            while True:

                print("#############################")
                print("### Opciones de inserción ###")
                print("#############################\n")

                print("\n1. Insertar un nuevo integrante")
                print("2. Insertar un nuevo instrumento")
                print("3. Insertar una nueva melodía")
                print("4. Asignar un instrumento y una melodía a un integrante")
                print("5. Volver al menú principal\n")

                sub_choice: str = input("Selecciona una opción (1-5): ")

                if sub_choice == '1':
                    name: str = input("Ingrese el nombre del integrante: ")
                    main_position: str = input("Ingrese el puesto principal del integrante: ")
                    role: str = input("Ingrese el rol del integrante: ")
                    print()

                    member_data: tuple[str, str, str] = (name, main_position, role)
                    insert_member(cursor, member_data)

                elif sub_choice == '2':
                    name: str = input("Ingrese el nombre del instrumento: ")
                    family: str = input("Ingrese la familia del instrumento: ")
                    print()

                    instrument_data: tuple[str, str] = (name, family)
                    insert_instrument(cursor, instrument_data)

                elif sub_choice == '3':        
                    name: str = input("Ingrese el título de la melodía: ")
                    genre: str = input("Ingrese el género de la melodía: ")
                    print()

                    melody_data: tuple[str, str] = (name, genre)
                    insert_melody(cursor, melody_data)

                elif sub_choice == '4':
                    member_id: str = input("Ingrese el ID del integrante: ")
                    instrument_id: str = input("Ingrese el ID del instrumento: ")
                    melody_id: str = input("Ingrese el ID de la melodía: ")
                    member_position: str = input("Ingrese el puesto del integrante en la melodía: ")
                    print()

                    assignment_data: tuple[str, str, str, str] = (member_id, instrument_id, melody_id, member_position)
                    assign_instrument_member_melody(cursor, assignment_data)

                elif sub_choice == '5':
                    break

        elif choice == '3':

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
                        print(f"ID: {member[0]}, Nombre: {member[1]}, Puesto Principal: {member[2]}, Rol: {member[3]}")
                    print()

                elif sub_choice == "2":
                    instruments = get_all_instruments(cursor)

                    if not instruments:
                        print("\nNo hay instrumentos registrados.\n")

                    print("\nLista de Instrumentos:")

                    for instrument in instruments:
                        print(f"ID: {instrument[0]}, Nombre: {instrument[1]}, Familia: {instrument[2]}")
                    print()

                elif sub_choice == "3":
                    melodies = get_all_melodies(cursor)

                    if not melodies:
                        print("\nNo hay melodías registradas.\n")

                    print("\nLista de Melodías:")

                    for melody in melodies:
                        print(f"ID: {melody[0]}, Nombre: {melody[1]}, Género: {melody[2]}")
                    print()

                elif sub_choice == "4":
                    melody_id: str = input("Ingrese el ID de la melodía: ")
                    members_in_melody = get_members_by_melody(cursor, melody_id)
                    all_members = get_all_members(cursor)

                    if not members_in_melody:
                        print(f"\nNo hay integrantes registrados para la melodía con ID {melody_id}.\n")

                    else:
                        try:
                            print(f"\nIntegrantes que participan en la melodía {members_in_melody[1]['melody']}:")

                            for member_id, dmember_details in members_in_melody.items():
                                print(f"ID Integrante: {member_id}, Nombre: {dmember_details['member']}, Instrumento: {dmember_details['instrument']}, Puesto: {dmember_details['member_positions']}")
                            print()

                            for member in all_members:
                                if member[0] not in members_in_melody:
                                    members_in_melody[member[0]] = {"member": member[1], "main": member[2], "melody": None, "instrument": None, "member_positions": None}

                            filled_positions = check_mandatory_positions_filled(members_in_melody)
                            recommendations = recommend_member_for_position(members_in_melody, filled_positions)

                            for position, assigned_members in recommendations.items():
                                if assigned_members:
                                    print(f"{position}: {', '.join(assigned_members)}")
                                else:
                                    print(f"{position}: Ninguno")

                        except KeyError:
                            print(f"\nNo hay integrantes registrados para la melodía con ID {melody_id}.\n")

                elif sub_choice == "5":
                    print()
                    break

        elif choice == '4':
            cursor.close()
            print("Conexión cerrada.")
            print("Saliendo del sistema...")
            os._exit(0)
            break

if __name__ == "__main__":
    main()
