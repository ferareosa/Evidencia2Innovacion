"""
Módulo Principal de la Interfaz Gráfica
"""
import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from models import Contacto
from forms import FormularioContacto, FormularioBusqueda

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema ABM de Contactos")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Instancia de la base de datos
        self.db = Database()
        
        # Configurar la interfaz
        self.configurar_interfaz()
        
        # Cargar contactos iniciales
        self.actualizar_lista_contactos()
        
        # Manejar cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def configurar_interfaz(self):
        """Configura todos los elementos de la interfaz gráfica"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid para expansión
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="Gestión de Contactos", font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, pady=(0, 10))
        
        # Formulario de contacto
        self.formulario = FormularioContacto(main_frame, self.db, self.actualizar_lista_contactos)
        self.formulario.frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Formulario de búsqueda
        self.busqueda = FormularioBusqueda(main_frame, self.buscar_contacto)
        self.busqueda.frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Lista de contactos
        columns = ("ID", "Nombre", "Apellido", "Teléfono", "Email")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", selectmode="browse")
        
        # Configurar columnas
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.W)
        
        self.tree.column("ID", width=50)
        self.tree.column("Nombre", width=120)
        self.tree.column("Apellido", width=120)
        self.tree.column("Teléfono", width=100)
        self.tree.column("Email", width=180)
        
        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        scrollbar.grid(row=3, column=1, sticky=(tk.N, tk.S), pady=(0, 10))
        
        # Botones de acción adicionales
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, pady=10)
        
        ttk.Button(btn_frame, text="Modificar Contacto", command=self.cargar_seleccionado).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Eliminar Contacto", command=self.eliminar_seleccionado).pack(side=tk.LEFT, padx=5)
        
        # Evento de selección en la tabla
        self.tree.bind("<Double-1>", self.cargar_seleccionado)

    def buscar_contacto(self, texto_busqueda):
        """Busca contactos según el texto ingresado"""
        if not texto_busqueda:
            self.actualizar_lista_contactos()
            return
            
        # Buscar en todos los campos
        resultados = []
        for campo in ["nombre", "apellido", "telefono", "email"]:
            resultados.extend(self.db.buscar_contacto(campo, texto_busqueda))
        
        # Eliminar duplicados
        resultados_unicos = []
        ids_vistos = set()
        for contacto in resultados:
            if contacto[0] not in ids_vistos:
                resultados_unicos.append(contacto)
                ids_vistos.add(contacto[0])
        
        self.mostrar_contactos(resultados_unicos)

    def cargar_seleccionado(self, event=None):
        """Carga el contacto seleccionado en el formulario"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Selección", "Debe seleccionar un contacto")
            return
            
        item = self.tree.item(seleccion[0])
        valores = item['values']
        
        contacto = Contacto(
            id=valores[0],
            nombre=valores[1],
            apellido=valores[2],
            telefono=valores[3],
            email=valores[4]
        )
        
        self.formulario.cargar_contacto(contacto)

    def eliminar_seleccionado(self):
        """Elimina el contacto seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Selección", "Debe seleccionar un contacto para eliminar")
            return
            
        item = self.tree.item(seleccion[0])
        valores = item['values']
        id_contacto = valores[0]
        
        confirmacion = messagebox.askyesno(
            "Confirmar eliminación", 
            f"¿Está seguro de que desea eliminar a {valores[1]} {valores[2]}?"
        )
        
        if confirmacion:
            if self.db.eliminar_contacto(id_contacto):
                messagebox.showinfo("Éxito", "Contacto eliminado correctamente")
                self.formulario.limpiar()
                self.actualizar_lista_contactos()

    def actualizar_lista_contactos(self):
        """Actualiza la lista de contactos en la interfaz"""
        contactos = self.db.listar_contactos()
        self.mostrar_contactos(contactos)

    def mostrar_contactos(self, contactos):
        """Muestra los contactos en la tabla"""
        # Limpiar tabla existente
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insertar nuevos datos
        for contacto in contactos:
            self.tree.insert("", tk.END, values=contacto)

    def on_closing(self):
        """Maneja el cierre de la aplicación"""
        self.db.cerrar_conexion()
        self.root.destroy()