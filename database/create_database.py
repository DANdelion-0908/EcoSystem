from database.connection import get_connection

def create_database():
    """Crear la base de datos de Ecos del Valle."""
    cur = get_connection()
    cur.execute("USE ecos;")

    cur.execute("""CREATE TABLE IF NOT EXISTS integrante(
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    nombre VARCHAR(100) NOT NULL,
                    rol VARCHAR(100) NOT NULL);"""
                )

    cur.execute("""CREATE TABLE IF NOT EXISTS instrumento(
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    nombre VARCHAR(100) NOT NULL,
                    tipo VARCHAR(100) NOT NULL);"""
                )

    cur.execute("""CREATE TABLE IF NOT EXISTS melodia(
                id INT PRIMARY KEY AUTO_INCREMENT,
                titulo VARCHAR(100) NOT NULL,
                genero VARCHAR(100) NOT NULL);"""
            )

    cur.execute("""CREATE TABLE IF NOT EXISTS integrante_instrumento_melodia(
                integrante_id INT,
                instrumento_id INT,
                melodia_id INT,
                puesto VARCHAR(100) NOT NULL,
                FOREIGN KEY (integrante_id) REFERENCES integrante(id),
                FOREIGN KEY (instrumento_id) REFERENCES instrumento(id),
                FOREIGN KEY (melodia_id) REFERENCES melodia(id));"""
            )
    
    print("Se han creado la base de datos 'ecos' y las tablas 'integrante', 'instrumento', 'melodia' e 'integrante_instrumento_melodia' correctamente.")
    