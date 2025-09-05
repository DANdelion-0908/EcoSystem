# Module Imports
import mariadb, sys, os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    """Establecer conexión a la base de datos de Ecos del Valle.
    
    Returns:
        cur (mariadb.Cursor): Cursor de la base de datos.
    """
    try:
        conn = mariadb.connect(
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
    cur = conn.cursor()
    return cur

def insert_integrante(cursor: mariadb.Cursor, data: tuple):
    """Insertar datos en la tabla integrante.
    
    Args:
        cursor (mariadb.Cursor): Cursor de la base de datos.
        data (tuple): Datos a insertar.
    """
    try:
        cursor.execute(
            "INSERT INTO integrante (nombre, rol) VALUES (?, ?)", data[0], data[1]
        )
    
        print(f"Integrante {data[0]} agregado correctamente.")

    except mariadb.Error as e:
        print(f"Ocurrió un error al insertar al integrante: {e}")

def insert_instrumento(cursor: mariadb.Cursor, data: tuple):
    """Insertar datos en la tabla instrumento.

    Args:
        cursor (mariadb.Cursor): Cursor de la base de datos.
        data (tuple): Datos a insertar.
    """

    try:
        cursor.execute(
            "INSERT INTO instrumento (nombre, tipo) VALUES (?,?)", data[0], data[1]
        )

        print(f"Instrumento {data[0]} agregado correctamente.")

    except mariadb.Error as e:
        print(f"Ocurrió un error al insertar al instrumento: {e}")

def insert_melodia(cursor: mariadb.Cursor, data: tuple):
    pass

def assign_instrumento_melodia(cursor: mariadb.Cursor, data: dict):
    pass
