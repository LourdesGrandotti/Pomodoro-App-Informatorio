# Menu desplegable de selección de tarea

import tkinter as tk
from tkinter import ttk, messagebox
from tasks_manager import DuplicateTaskError, InvalidTaskNameError
from extras import mostrar_estadisticas


class MainMenu:
    def __init__(self, root, gestor_tareas, app_pomodoro):
        self.root = root
        self.gestor_tareas = gestor_tareas
        self.app_pomodoro = app_pomodoro
        self.ventana_opciones = tk.Toplevel(self.root)
        self.ventana_opciones.title("Opciones")
        self.ventana_opciones.geometry("300x200")
        self.ventana_opciones.resizable(False, False)
        self.ventana_opciones.transient(self.root)
        self.ventana_opciones.grab_set()
        self._crear_widgets()

    def _crear_widgets(self):
        ttk.Label(self.ventana_opciones, text="Selecciona una opción:",
                  font=("Helvetica", 10)).pack(pady=10)
        ttk.Button(self.ventana_opciones, text="Agregar Tarea",
                   command=self.abrir_ventana_agregar_tarea).pack(pady=5)
        ttk.Button(self.ventana_opciones, text="Ver Estadísticas",
                   command=self.ver_estadisticas).pack(pady=5)
        ttk.Button(self.ventana_opciones, text="Cerrar",
                   command=self.ventana_opciones.destroy).pack(pady=10)

    def ver_estadisticas(self):
        """
        Este método ahora actúa como un intermediario:
        1. Obtiene la tarea seleccionada.
        2. Pide las estadísticas al gestor de tareas.
        3. Llama a la función de 'extras' para que las MUESTRE.
        """
        tarea_seleccionada = self.app_pomodoro.get_tarea_seleccionada()
        if not tarea_seleccionada:
            messagebox.showinfo(
                "Estadísticas", "Selecciona una tarea para ver sus detalles.", parent=self.ventana_opciones)
            return

        try:
            stats = self.gestor_tareas.get_task_stats(tarea_seleccionada)
            # Llama a la función de presentación de extras.py
            mostrar_estadisticas(self.ventana_opciones, stats)
        except Exception as e:
            messagebox.showerror(
                "Error", f"No se pudieron obtener las estadísticas: {e}", parent=self.ventana_opciones)

    def abrir_ventana_agregar_tarea(self):
        ventana_agregar = tk.Toplevel(self.ventana_opciones)
        ventana_agregar.title("Agregar Tarea")
        ventana_agregar.geometry("300x150")
        ventana_agregar.resizable(False, False)
        ventana_agregar.transient(self.ventana_opciones)
        ventana_agregar.grab_set()
        ttk.Label(ventana_agregar, text="Nombre de la tarea:").pack(pady=10)
        entrada = ttk.Entry(ventana_agregar, width=30)
        entrada.pack(pady=5)
        entrada.focus()

        def guardar_y_cerrar():
            nombre_tarea = entrada.get().strip()
            try:
                self.gestor_tareas.add_task(nombre_tarea)
                self.app_pomodoro.actualizar_lista_tareas_ui()
                ventana_agregar.destroy()
            except (DuplicateTaskError, InvalidTaskNameError) as e:
                messagebox.showerror("Error al guardar",
                                     str(e), parent=ventana_agregar)
        ttk.Button(ventana_agregar, text="Guardar",
                   command=guardar_y_cerrar).pack(pady=10)
