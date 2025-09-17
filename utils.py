"""
Módulo con utilidades varias para la aplicación
"""
import re
import tkinter.messagebox as messagebox

def validar_email(email):
    """Valida el formato de un email"""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

def validar_campos_contacto(nombre, apellido, telefono, email):
    """Valida que todos los campos obligatorios estén completos"""
    if not nombre.strip():
        messagebox.showwarning("Validación", "El nombre es obligatorio")
        return False
    if not apellido.strip():
        messagebox.showwarning("Validación", "El apellido es obligatorio")
        return False
    if not telefono.strip():
        messagebox.showwarning("Validación", "El teléfono es obligatorio")
        return False
    if not email.strip():
        messagebox.showwarning("Validación", "El email es obligatorio")
        return False
    if not validar_email(email):
        messagebox.showwarning("Validación", "El formato del email no es válido")
        return False
    return True