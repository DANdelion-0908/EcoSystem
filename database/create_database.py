from database.connection import get_connection

def create_database():
    """Crear la base de datos de Ecos del Valle."""
    cur = get_connection()
    cur.execute("USE ecos;")

    cur.execute("""CREATE TABLE IF NOT EXISTS member(
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(100) NOT NULL,
                    main_position VARCHAR(100) NOT NULL,
                    role VARCHAR(100) NOT NULL);"""
                )

    cur.execute("""CREATE TABLE IF NOT EXISTS instrument(
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(100) NOT NULL,
                    family VARCHAR(100) NOT NULL);"""
                )

    cur.execute("""CREATE TABLE IF NOT EXISTS melody(
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL,
                genre VARCHAR(100) NOT NULL);"""
            )

    cur.execute("""CREATE TABLE IF NOT EXISTS member_instrument_melody(
                member_id INT,
                instrument_id INT,
                melody_id INT,
                member_positions VARCHAR(100) NOT NULL,
                FOREIGN KEY (member_id) REFERENCES member(id),
                FOREIGN KEY (instrument_id) REFERENCES instrument(id),
                FOREIGN KEY (melody_id) REFERENCES melody(id));"""
            )

    print("Se han creado las tablas 'member', 'instrument', 'melody' y 'member_instrument_melody' correctamente\n")
