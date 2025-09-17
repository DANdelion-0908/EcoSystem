# Module Imports
import mariadb, sys, os
from dotenv import load_dotenv

load_dotenv()

def get_connection() -> mariadb.Cursor:
    """Establecer conexión a la base de datos de Ecos del Valle.
    
    Returns:
        cur (mariadb.Cursor): Cursor de la base de datos.
    """
    try:
        conn: mariadb.Connection = mariadb.connect(
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            host=os.getenv("DATABASE_HOST"),
            port=3306,
            database=os.getenv("DATABASE_NAME")
        )

        conn.autocommit = True

        print(f"Connection to {conn.database} successful\n")

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}\n")
        sys.exit(1)

    # Get Cursor
    cur: mariadb.Cursor = conn.cursor()
    return cur

def insert_member(cursor: mariadb.Cursor, data: tuple) -> None:
    """Insertar datos en la tabla member.
    
    Args:
        cursor (mariadb.Cursor): Cursor de la base de datos.
        data (tuple): Datos a insertar.

    Returns:
        None
    """
    try:
        cursor.execute(
            "INSERT INTO member (name, main_position, role) VALUES (?, ?, ?)", (data[0], data[1], data[2])
        )
    
        print(f"Integrante {data[0]} agregado correctamente.\n")

    except mariadb.Error as e:
        print(f"Ocurrió un error al insertar al integrante: {e}\n")

def insert_instrument(cursor: mariadb.Cursor, data: tuple) -> None:
    """Insertar datos en la tabla instrument.

    Args:
        cursor (mariadb.Cursor): Cursor de la base de datos.
        data (tuple): Datos a insertar.

    Returns:
        None
    """

    try:
        cursor.execute(
            "INSERT INTO instrument (name, family) VALUES (?,?)", (data[0], data[1])
        )

        print(f"Instrumento {data[0]} agregado correctamente.\n")

    except mariadb.Error as e:
        print(f"Ocurrió un error al insertar al instrumento: {e}\n")

def insert_melody(cursor: mariadb.Cursor, data: tuple) -> None:
    """Insertar datos en la tabla melody.

    Args:
        cursor (mariadb.Cursor): Cursor de la base de datos.
        data (tuple): Datos a insertar.

    Returns:
        None
    """

    try:
        cursor.execute(
            "INSERT INTO melody (name, genre) VALUES (?,?)", (data[0], data[1])
        )

        print(f"Melodía {data[0]} agregada correctamente.\n")

    except mariadb.Error as e:
        print(f"Ocurrió un error al insertar la melodía: {e}\n")

def assign_instrument_member_melody(cursor: mariadb.Cursor, data: tuple) -> None:
    """Asignar un instrumento y una melodía a un integrante.

    Args:
        cursor (mariadb.Cursor): Cursor de la base de datos.
        data (tuple): Datos a insertar.

    Returns:
        None
    """
    try:
        cursor.execute(
            "INSERT INTO member_instrument_melody (member_id, instrument_id, melody_id, member_positions) VALUES (?, ?, ?, ?)",  (data[0], data[1], data[2], data[3])
        )

        print(f"Asignación de instrumento {data[1]} y melodía {data[2]} a integrante {data[0]} con el puesto {data[3]} realizada correctamente.\n")

    except mariadb.Error as e:
        print(f"Ocurrió un error al asignar el instrumento y la melodía: {e}\n")

def get_all_members(cursor: mariadb.Cursor) -> list[tuple]:
    """Obtener todos los integrantes de la base de datos.

    Args:
        cursor (mariadb.Cursor): Cursor de la base de datos.

    Returns:
        list[tuple]: Lista de tuplas con los datos de los integrantes.
    """
    try:
        cursor.execute("SELECT * FROM member")
        members: list[tuple] = cursor.fetchall()
        return members

    except mariadb.Error as e:
        print(f"Ocurrió un error al obtener los integrantes: {e}\n")
        return []

def get_all_instruments(cursor: mariadb.Cursor) -> list[tuple]:
    """Obtener todos los instrumentos de la base de datos.

    Args:
        cursor (mariadb.Cursor): Cursor de la base de datos.

    Returns:
        list[tuple]: Lista de tuplas con los datos de los instrumentos.
    """
    try:
        cursor.execute("SELECT * FROM instrument")
        instruments: list[tuple] = cursor.fetchall()
        return instruments

    except mariadb.Error as e:
        print(f"Ocurrió un error al obtener los instrumentos: {e}\n")
        return []

def get_all_melodies(cursor: mariadb.Cursor) -> list[tuple]:
    """Obtener todas las melodías de la base de datos.

    Args:
        cursor (mariadb.Cursor): Cursor de la base de datos.

    Returns:
        list[tuple]: Lista de tuplas con los datos de las melodías.
    """
    try:
        cursor.execute("SELECT * FROM melody")
        melodies: list[tuple] = cursor.fetchall()
        return melodies

    except mariadb.Error as e:
        print(f"Ocurrió un error al obtener las melodías: {e}\n")
        return []

    except mariadb.Error as e:
        print(f"Ocurrió un error al obtener las melodías: {e}\n")
        return []

def get_members_by_melody(cursor: mariadb.Cursor, melody_id: str) -> dict:
    """Obtener todos los miembros y su relación con una determinada canción.
    Si participan, se muestra su puesto, de lo contrario, None.

    Args:
        cursor (mariadb.Cursor): Cursor de la base de datos.
        melody_id (str): ID de la melodía para filtrar las relaciones.

    Returns:
        dict: Diccionario con los datos de las relaciones.
    """
    try:
        cursor.execute(f"""
            SELECT m.id AS member_id,
                m.name AS member, 
                m.main_position AS main,
                mel.name AS melody, 
                ins.name AS instrument, 
                mim.member_positions 
            FROM member_instrument_melody mim 
            JOIN member m ON mim.member_id = m.id JOIN 
            instrument ins ON mim.instrument_id = ins.id JOIN 
            melody mel ON mim.melody_id = mel.id 
            WHERE mel.id = ?;
        """, (melody_id,))

        relations: dict = {}

        for (member_id, member, main, melody, instrument, member_positions) in cursor.fetchall():
            relations[member_id] = {
                "member": member,
                "melody": melody,
                "instrument": instrument,
                "main": main,
                "member_positions": member_positions
            }
        
        return relations

    except mariadb.Error as e:
        print(f"Ocurrió un error al obtener las relaciones: {e}\n")
        return {}

def delete_relations(cursor: mariadb.Cursor) -> None:
    """Eliminar todas las relaciones de la tabla member_instrument_melody.

    Args:
        cursor (mariadb.Cursor): Cursor de la base de datos.

    Returns:
        None
    """
    try:
        cursor.execute("TRUNCATE TABLE member_instrument_melody")
        print("Todas las relaciones eliminadas correctamente.\n")

    except mariadb.Error as e:
        print(f"Ocurrió un error al eliminar las relaciones: {e}\n")
