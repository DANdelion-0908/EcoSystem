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

        print(f"Connection to {conn.database} successful")

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get Cursor
    cur: mariadb.Cursor = conn.cursor()
    return cur

def insert_member(cursor: mariadb.Cursor, data: tuple) -> None:
    """Insertar datos en la tabla integrante.
    
    Args:
        cursor (mariadb.Cursor): Cursor de la base de datos.
        data (tuple): Datos a insertar.

    Returns:
        None
    """
    try:
        cursor.execute(
            "INSERT INTO integrante (nombre, rol) VALUES (?, ?)", (data[0], data[1])
        )
    
        print(f"Integrante {data[0]} agregado correctamente.")

    except mariadb.Error as e:
        print(f"Ocurrió un error al insertar al integrante: {e}")

def insert_instrument(cursor: mariadb.Cursor, data: tuple) -> None:
    """Insertar datos en la tabla instrumento.

    Args:
        cursor (mariadb.Cursor): Cursor de la base de datos.
        data (tuple): Datos a insertar.

    Returns:
        None
    """

    try:
        cursor.execute(
            "INSERT INTO instrumento (nombre, tipo) VALUES (?,?)", (data[0], data[1])
        )

        print(f"Instrumento {data[0]} agregado correctamente.")

    except mariadb.Error as e:
        print(f"Ocurrió un error al insertar al instrumento: {e}")

def insert_melody(cursor: mariadb.Cursor, data: tuple) -> None:
    """Insertar datos en la tabla melodia.

    Args:
        cursor (mariadb.Cursor): Cursor de la base de datos.
        data (tuple): Datos a insertar.

    Returns:
        None
    """

    try:
        cursor.execute(
            "INSERT INTO melodia (titulo, genero) VALUES (?,?)", (data[0], data[1])
        )

        print(f"Melodía {data[0]} agregada correctamente.")

    except mariadb.Error as e:
        print(f"Ocurrió un error al insertar la melodía: {e}")

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
            "INSERT INTO integrante_instrumento_melodia (integrante_id, instrumento_id, melodia_id, puesto) VALUES (?, ?, ?, ?)",  (data[0], data[1], data[2], data[3])
        )

        print(f"Asignación de instrumento {data[1]} y melodía {data[2]} a integrante {data[0]} con el puesto {data[3]} realizada correctamente.")

    except mariadb.Error as e:
        print(f"Ocurrió un error al asignar el instrumento y la melodía: {e}")
