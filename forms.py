"""
Módulo con formularios para altas, bajas y modificaciones
"""
import tkinter as tk
from tkinter import ttk, messagebox
from models import Contacto
import utils

class FormularioContacto:
    def __init__(self, parent, db, on_guardar_callback=None):
        self.parent = parent
        self.db = db
        self.on_guardar_callback = on_guardar_callback
        self.contacto = None
        
        # Variables para los campos de entrada
        self.id_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.apellido_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.email_var = tk.StringVar()
        
        self.crear_formulario()
    
    def crear_formulario(self):
        """Crea el formulario de contacto"""
        self.frame = ttk.Frame(self.parent, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid para expansión
        self.frame.columnconfigure(1, weight=1)
        
        # Campos de entrada
        
        ttk.Label(self.frame, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(self.frame, textvariable=self.nombre_var).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        
        ttk.Label(self.frame, text="Apellido:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(self.frame, textvariable=self.apellido_var).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        
        ttk.Label(self.frame, text="Teléfono:").grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Entry(self.frame, textvariable=self.telefono_var).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        
        ttk.Label(self.frame, text="Email:").grid(row=4, column=0, sticky=tk.W, pady=2)
        ttk.Entry(self.frame, textvariable=self.email_var).grid(row=4, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        
        # Botones de acción
        btn_frame = ttk.Frame(self.frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Guardar", command=self.guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.cancelar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar).pack(side=tk.LEFT, padx=5)
    
    def guardar(self):
        """Guarda el contacto (alta o modificación)"""
        nombre = self.nombre_var.get().strip()
        apellido = self.apellido_var.get().strip()
        telefono = self.telefono_var.get().strip()
        email = self.email_var.get().strip()
        
        if not utils.validar_campos_contacto(nombre, apellido, telefono, email):
            return
        
        if self.contacto and self.contacto.id:
            # Modificación
            self.contacto.nombre = nombre
            self.contacto.apellido = apellido
            self.contacto.telefono = telefono
            self.contacto.email = email
            
            if self.db.modificar_contacto(self.contacto):
                messagebox.showinfo("Éxito", "Contacto modificado correctamente")
                self.limpiar()
                if self.on_guardar_callback:
                    self.on_guardar_callback()
        else:
            # Alta
            nuevo_contacto = Contacto(None, nombre, apellido, telefono, email)
            if self.db.insertar_contacto(nuevo_contacto):
                messagebox.showinfo("Éxito", "Contacto agregado correctamente")
                self.limpiar()
                if self.on_guardar_callback:
                    self.on_guardar_callback()
    
    def cancelar(self):
        """Cancela la operación y limpia el formulario"""
        self.limpiar()
    
    def limpiar(self):
        """Limpia todos los campos del formulario"""
        self.contacto = None
        self.id_var.set("")
        self.nombre_var.set("")
        self.apellido_var.set("")
        self.telefono_var.set("")
        self.email_var.set("")
    
    def cargar_contacto(self, contacto):
        """Carga un contacto existente en el formulario para modificación"""
        self.contacto = contacto
        self.id_var.set(contacto.id)
        self.nombre_var.set(contacto.nombre)
        self.apellido_var.set(contacto.apellido)
        self.telefono_var.set(contacto.telefono)
        self.email_var.set(contacto.email)


class FormularioBusqueda:
    def __init__(self, parent, on_buscar_callback=None):
        self.parent = parent
        self.on_buscar_callback = on_buscar_callback
        self.buscar_var = tk.StringVar()
        
        self.crear_formulario()
    
    def crear_formulario(self):
        """Crea el formulario de búsqueda"""
        self.frame = ttk.Frame(self.parent, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Configurar grid para expansión
        self.frame.columnconfigure(1, weight=1)
        
        ttk.Label(self.frame, text="Buscar:").grid(row=0, column=0, sticky=tk.W)
        buscar_entry = ttk.Entry(self.frame, textvariable=self.buscar_var)
        buscar_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        buscar_entry.bind("<KeyRelease>", self.buscar)
    
    def buscar(self, event=None):
        """Ejecuta la búsqueda según el texto ingresado"""
        if self.on_buscar_callback:
            self.on_buscar_callback(self.buscar_var.get().strip())