#!/usr/bin/env python3
"""
Punto de entrada principal del Sistema ABM de Contactos
"""
import tkinter as tk
from gui import App

def main():
    """Función principal que inicia la aplicación"""
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()