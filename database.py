"""
Módulo para manejo de la base de datos SQLite
"""
import sqlite3
import os
import tkinter.messagebox as messagebox

class Database:
    def __init__(self, db_name='contactos.db'):
        APP_DIR = os.path.join(os.getenv("APPDATA"), "ContactosApp")
        os.makedirs(APP_DIR, exist_ok=True)
        self.db_name = os.path.join(APP_DIR , db_name)
        self.conn = None
        self.cursor = None
        self.conectar()
        self.crear_tabla()

    def conectar(self):
        """Establece conexión con la base de datos SQLite"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {e}")

    def crear_tabla(self):
        """Crea la tabla Contactos si no existe"""
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Contactos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    telefono TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Error de base de datos", f"No se pudo crear la tabla: {e}")

    def insertar_contacto(self, contacto):
        """Inserta un nuevo contacto en la base de datos"""
        try:
            self.cursor.execute(
                "INSERT INTO Contactos (nombre, apellido, telefono, email) VALUES (?, ?, ?, ?)",
                (contacto.nombre, contacto.apellido, contacto.telefono, contacto.email)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El email ya existe en la base de datos")
            return False
        except sqlite3.Error as e:
            messagebox.showerror("Error de base de datos", f"No se pudo insertar el contacto: {e}")
            return False

    def listar_contactos(self):
        """Obtiene todos los contactos de la base de datos"""
        try:
            self.cursor.execute("SELECT * FROM Contactos")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Error de base de datos", f"No se pudieron recuperar los contactos: {e}")
            return []

    def modificar_contacto(self, contacto):
        """Modifica un contacto existente"""
        try:
            self.cursor.execute(
                "UPDATE Contactos SET nombre=?, apellido=?, telefono=?, email=? WHERE id=?",
                (contacto.nombre, contacto.apellido, contacto.telefono, contacto.email, contacto.id)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El email ya existe en la base de datos")
            return False
        except sqlite3.Error as e:
            messagebox.showerror("Error de base de datos", f"No se pudo modificar el contacto: {e}")
            return False

    def eliminar_contacto(self, id_contacto):
        """Elimina un contacto de la base de datos"""
        try:
            self.cursor.execute("DELETE FROM Contactos WHERE id=?", (id_contacto,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Error de base de datos", f"No se pudo eliminar el contacto: {e}")
            return False

    def buscar_contacto(self, campo, valor):
        """Busca contactos según un criterio"""
        try:
            query = f"SELECT * FROM Contactos WHERE {campo} LIKE ?"
            self.cursor.execute(query, (f'%{valor}%',))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Error de base de datos", f"No se pudo realizar la búsqueda: {e}")
            return []

    def cerrar_conexion(self):
        """Cierra la conexión con la base de datos"""
        if self.conn:
            self.conn.close()