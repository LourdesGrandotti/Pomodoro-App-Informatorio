#Menu desplegable de selección de tarea

import tkinter as tk
from tkinter import ttk
from datetime import datetime

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas con Cronómetro")
        self.root.geometry("400x300")  

        # Variable para almacenar la tarea actual
        self.tarea_actual = tk.StringVar(value="Ninguna tarea")
        self.tiempo_cronometrado = tk.StringVar(value="00:00:00")
        self.tiempo_inicio = None
        self.cronometro_activo = False

        # Botón principal para desplegar opciones
        self.boton_opciones = ttk.Button(
            root,
            text="Desplegar Opciones",
            command=self.mostrar_ventana_opciones
        )
        self.boton_opciones.pack(pady=20)

        # Etiqueta para mostrar la tarea actual y el tiempo
        self.etiqueta_tarea = ttk.Label(
            root,
            textvariable=self.tarea_actual,
            font=("Helvetica", 12)
        )
        self.etiqueta_tarea.pack(pady=10)

        self.etiqueta_tiempo = ttk.Label(
            root,
            textvariable=self.tiempo_cronometrado,
            font=("Consolas", 16)
        )
        self.etiqueta_tiempo.pack(pady=5)

    def mostrar_ventana_opciones(self):
        # Crear ventana emergente
        ventana_opciones = tk.Toplevel(self.root)
        ventana_opciones.title("Opciones")
        ventana_opciones.geometry("300x200")
        ventana_opciones.resizable(False, False)

        # Etiqueta de bienvenida
        ttk.Label(ventana_opciones, text="Selecciona una opción:", font=("Helvetica", 10)).pack(pady=10)

        # Botón para agregar tarea
        ttk.Button(
            ventana_opciones,
            text="Agregar Tarea",
            command=self.agregar_tarea
        ).pack(pady=5)

        # Botón para iniciar cronómetro
        ttk.Button(
            ventana_opciones,
            text="Iniciar Cronómetro",
            command=self.iniciar_cronometro
        ).pack(pady=5)

        # Botón para ver estadísticas
        ttk.Button(
            ventana_opciones,
            text="Ver Estadísticas",
            command=self.ver_estadisticas
        ).pack(pady=5)

        # Botón para cerrar la ventana emergente
        ttk.Button(
            ventana_opciones,
            text="Cerrar",
            command=ventana_opciones.destroy
        ).pack(pady=10)

    def agregar_tarea(self):
        # Ventana para ingresar la tarea
        ventana_tarea = tk.Toplevel(self.root)
        ventana_tarea.title("Agregar Tarea")
        ventana_tarea.geometry("300x200")
        ventana_tarea.resizable(False, False)

        ttk.Label(ventana_tarea, text="Nombre de la tarea:").pack(pady=10)
        entrada_tarea = ttk.Entry(ventana_tarea, width=30)
        entrada_tarea.pack(pady=5)

        def guardar_tarea():
            tarea = entrada_tarea.get().strip()
            if tarea:
                self.tarea_actual.set(tarea)
                self.tiempo_cronometrado.set("00:00:00")
                self.cronometro_activo = False
                ventana_tarea.destroy()
            else:
                tk.messagebox.showwarning("Advertencia", "Por favor, ingresa un nombre de tarea.")

        ttk.Button(ventana_tarea, text="Guardar", command=guardar_tarea).pack(pady=10)

    def iniciar_cronometro(self):
        if not self.tarea_actual.get() or self.tarea_actual.get() == "Ninguna tarea":
            tk.messagebox.showwarning("Advertencia", "Primero agrega una tarea.")
            return

        if not self.cronometro_activo:
            self.tiempo_inicio = datetime.now()
            self.cronometro_activo = True
            self.actualizar_cronometro()

    def actualizar_cronometro(self):
        if self.cronometro_activo and self.tiempo_inicio:
            segundos_transcurridos = (datetime.now() - self.tiempo_inicio).total_seconds()
            horas = int(segundos_transcurridos // 3600)
            minutos = int((segundos_transcurridos % 3600) // 60)
            segundos = int(segundos_transcurridos % 60)
            formato_tiempo = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
            self.tiempo_cronometrado.set(formato_tiempo)
            self.root.after(1000, self.actualizar_cronometro)  # Actualiza cada segundo

    def ver_estadisticas(self):
        # Simulación de estadísticas
        tk.messagebox.showinfo(
            "Estadísticas",
            "Estadísticas de tareas:\n\n"
            "Tareas completadas: 5\n"
            "Tiempo total cronometrado: 2h 30m 15s\n"
            "Tareas pendientes: 2"
        )

# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
