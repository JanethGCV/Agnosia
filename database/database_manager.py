import mysql.connector
from mysql.connector import Error
import hashlib
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='gesture_game_db',
                user='root',  # Cambia por tu usuario de MySQL
                password=''   # Cambia por tu contraseña de MySQL
            )
            self.cursor = self.connection.cursor(dictionary=True)
        except Error as e:
            print(f"Error conectando a MySQL: {e}")
            self.connection = None

    def crear_usuario(self, username, email, password):
        if not self.connection:
            return False
        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            query = """
            INSERT INTO usuarios (username, email, password, es_admin) 
            VALUES (%s, %s, %s, %s)
            """
            # Por defecto, los nuevos usuarios no son administradores
            self.cursor.execute(query, (username, email, hashed_password, False))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error creando usuario: {e}")
            return False

    def validar_login(self, email, password):
        if not self.connection:
            return None

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        query = "SELECT * FROM usuarios WHERE email = %s AND password = %s"
        self.cursor.execute(query, (email, hashed_password))
        return self.cursor.fetchone()

    def guardar_partida(self, usuario_id, puntuacion, fecha=None):
        if not self.connection:
            return False

        if fecha is None:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        query = """
        INSERT INTO partidas (usuario_id, puntuacion, fecha) 
        VALUES (%s, %s, %s)
        """
        try:
            self.cursor.execute(query, (usuario_id, puntuacion, fecha))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error guardando partida: {e}")
            return False

    def obtener_estadisticas_usuario(self, usuario_id):
        if not self.connection:
            return None

        query = """
        SELECT 
            COUNT(*) AS total_partidas,
            COALESCE(AVG(puntuacion), 0) AS promedio_puntuacion,
            COALESCE(MAX(puntuacion), 0) AS maximo_puntaje,
            COALESCE(MIN(puntuacion), 0) AS minimo_puntaje
        FROM partidas 
        WHERE usuario_id = %s
        """
        self.cursor.execute(query, (usuario_id,))
        return self.cursor.fetchone()

    def obtener_puntajes(self, usuario_id):
        if not self.connection:
            return []

        query = "SELECT puntuacion, fecha FROM partidas WHERE usuario_id = %s ORDER BY fecha"
        self.cursor.execute(query, (usuario_id,))
        return self.cursor.fetchall()

    def obtener_usuarios(self):
        if not self.connection:
            return []

        query = "SELECT id, username FROM usuarios"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def __del__(self):
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()