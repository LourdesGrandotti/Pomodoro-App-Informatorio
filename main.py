import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class GestorPomodoro:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas - Pomodoro")
        self.root.geometry("500x500")
        self.root.resizable(False, False)

        # Variables
        self.tarea_actual = tk.StringVar(value="Ninguna tarea")
        self.tiempo_acumulado = tk.StringVar(value="00:00:00")
        self.tiempo_inicio = None
        self.cronometro_activo = False
        self.lista_tareas = []

        # Reloj central acumulado
        reloj_frame = ttk.Frame(root)
        reloj_frame.pack(fill='x', pady=10)
        ttk.Label(reloj_frame, text="Tiempo acumulado:", font=("Helvetica", 12)).pack()
        self.reloj_label = ttk.Label(reloj_frame, textvariable=self.tiempo_acumulado, font=("Consolas", 24))
        self.reloj_label.pack()

        # Tarea actual
        ttk.Label(root, text="Tarea actual:", font=("Helvetica", 12)).pack(pady=5)
        ttk.Label(root, textvariable=self.tarea_actual, font=("Helvetica", 12)).pack()

        # Lista de tareas con scroll
        ttk.Label(root, text="Lista de tareas:", font=("Helvetica", 12)).pack(pady=10)
        lista_frame = ttk.Frame(root)
        lista_frame.pack(fill='both', expand=True, padx=10)

        scrollbar = ttk.Scrollbar(lista_frame)
        scrollbar.pack(side='right', fill='y')

        self.caja_tareas = tk.Listbox(lista_frame, yscrollcommand=scrollbar.set, height=8)
        self.caja_tareas.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.caja_tareas.yview)

        # Botón "+"
        ttk.Button(root, text="+", command=self.mostrar_menu).pack(pady=10)

        # Iniciar reloj acumulado
        self.iniciar_cronometro()

    def iniciar_cronometro(self):
        if not self.cronometro_activo:
            self.tiempo_inicio = datetime.now()
            self.cronometro_activo = True
            self.actualizar_cronometro()

    def actualizar_cronometro(self):
        if self.cronometro_activo and self.tiempo_inicio:
            transcurrido = (datetime.now() - self.tiempo_inicio).total_seconds()
            horas = int(transcurrido // 3600)
            minutos = int((transcurrido % 3600) // 60)
            segundos = int(transcurrido % 60)
            self.tiempo_acumulado.set(f"{horas:02d}:{minutos:02d}:{segundos:02d}")
            self.root.after(1000, self.actualizar_cronometro)

    def mostrar_menu(self):
        menu = tk.Toplevel(self.root)
        menu.title("Opciones")
        menu.geometry("300x200")
        menu.resizable(False, False)

        ttk.Label(menu, text="Selecciona una opción:", font=("Helvetica", 10)).pack(pady=10)
        ttk.Button(menu, text="Agregar Tarea", command=self.agregar_tarea).pack(pady=5)
        ttk.Button(menu, text="Ver Estadísticas", command=self.ver_estadisticas).pack(pady=5)
        ttk.Button(menu, text="Cerrar", command=menu.destroy).pack(pady=10)

    def agregar_tarea(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar Tarea")
        ventana.geometry("300x150")
        ventana.resizable(False, False)

        ttk.Label(ventana, text="Nombre de la tarea:").pack(pady=10)
        entrada = ttk.Entry(ventana, width=30)
        entrada.pack(pady=5)

        def guardar():
            tarea = entrada.get().strip()
            if tarea:
                self.tarea_actual.set(tarea)
                self.lista_tareas.append(tarea)
                self.caja_tareas.insert(tk.END, tarea)
                ventana.destroy()
            else:
                messagebox.showwarning("Advertencia", "Por favor, ingresa una tarea.")

        ttk.Button(ventana, text="Guardar", command=guardar).pack(pady=10)

    def ver_estadisticas(self):
        messagebox.showinfo(
            "Estadísticas",
            f"Tarea actual: {self.tarea_actual.get()}\n"
            f"Tareas en lista: {len(self.lista_tareas)}\n"
            f"Tiempo acumulado: {self.tiempo_acumulado.get()}"
        )

# Ejecutar aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = GestorPomodoro(root)
    root.mainloop()
    