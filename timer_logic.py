# Lógica del cronómetro pomodoro

import tkinter as tk
from tkinter import ttk, messagebox
from tasks_manager import TaskNotFoundError
from menu import MainMenu
from extras import reproducir_sonido_alerta

# --- CONFIGURACIÓN DEL POMODORO ---
CONFIG = {
    "trabajo_min": 25,
    "descanso_corto_min": 5,
    "descanso_largo_min": 20,
    "ciclos_pomodoro": 4
}


class PomodoroApp:
    def __init__(self, root, gestor_tareas):
        self.root = root
        self.gestor_tareas = gestor_tareas
        self.estado_actual = "Inactivo"
        self.pomodoros_completados = 0
        self.segundos_restantes = CONFIG["trabajo_min"] * 60
        self.id_temporizador = None
        self.root.title("Gestor Pomodoro")
        self.root.geometry("400x550")
        self.root.resizable(False, False)
        self._crear_widgets()
        self.actualizar_lista_tareas_ui()

    def _crear_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(expand=True, fill="both")
        self.etiqueta_estado = ttk.Label(
            main_frame, text="Listo para empezar", font=("Helvetica", 16))
        self.etiqueta_estado.pack(pady=(10, 5))
        self.etiqueta_reloj = ttk.Label(
            main_frame, text=self.formatear_tiempo(), font=("Consolas", 48, "bold"))
        self.etiqueta_reloj.pack(pady=(5, 20))
        ttk.Label(main_frame, text="Lista de Tareas:",
                  font=("Helvetica", 12)).pack(pady=5)
        lista_frame = ttk.Frame(main_frame)
        lista_frame.pack(fill='both', expand=True, padx=10)
        scrollbar = ttk.Scrollbar(lista_frame)
        scrollbar.pack(side='right', fill='y')
        self.caja_tareas = tk.Listbox(
            lista_frame, yscrollcommand=scrollbar.set, height=8, font=("Helvetica", 11))
        self.caja_tareas.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.caja_tareas.yview)
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        self.boton_iniciar = ttk.Button(
            button_frame, text="Iniciar", command=self.iniciar_temporizador, width=10)
        self.boton_iniciar.pack(side="left", padx=5)
        self.boton_pausar = ttk.Button(
            button_frame, text="Pausar", state="disabled", command=self.pausar_temporizador, width=10)
        self.boton_pausar.pack(side="left", padx=5)
        self.boton_reiniciar = ttk.Button(
            button_frame, text="Reiniciar", state="disabled", command=self.reiniciar_temporizador, width=10)
        self.boton_reiniciar.pack(side="left", padx=5)
        ttk.Button(main_frame, text="Opciones",
                   command=self.abrir_menu).pack(pady=10)

    def transicion_de_estado(self):
        """Maneja la lógica de cambio entre trabajo y descanso."""
        # Llamamos a la función de sonido de nuestro módulo de utilidades.
        reproducir_sonido_alerta(self.root)

        seleccion = self.caja_tareas.curselection()
        tarea_activa = self.caja_tareas.get(seleccion) if seleccion else None

        if self.estado_actual == "Trabajo":
            self.pomodoros_completados += 1
            if tarea_activa:
                try:
                    self.gestor_tareas.add_pomodoro_session(tarea_activa)
                    print(
                        f"Sesión de Pomodoro para '{tarea_activa}' registrada.")
                except TaskNotFoundError:
                    print(
                        f"Error: No se pudo registrar la sesión para '{tarea_activa}'.")

            if self.pomodoros_completados % CONFIG["ciclos_pomodoro"] == 0:
                self.estado_actual = "Descanso Largo"
                self.segundos_restantes = CONFIG["descanso_largo_min"] * 60
                self.etiqueta_estado.config(text="¡Descanso largo!")
            else:
                self.estado_actual = "Descanso Corto"
                self.segundos_restantes = CONFIG["descanso_corto_min"] * 60
                self.etiqueta_estado.config(text="Descanso corto")

        elif self.estado_actual in ("Descanso Corto", "Descanso Largo"):
            self.estado_actual = "Trabajo"
            self.segundos_restantes = CONFIG["trabajo_min"] * 60
            self.etiqueta_estado.config(text="¡A trabajar!")

        self.cuenta_regresiva()

    def abrir_menu(self):
        MainMenu(self.root, self.gestor_tareas, self)

    def get_tarea_seleccionada(self):
        seleccion = self.caja_tareas.curselection()
        return self.caja_tareas.get(seleccion) if seleccion else None

    def formatear_tiempo(self):
        mins, secs = divmod(self.segundos_restantes, 60)
        return f"{mins:02d}:{secs:02d}"

    def actualizar_lista_tareas_ui(self):
        self.caja_tareas.delete(0, tk.END)
        nombres_tareas = self.gestor_tareas.get_task_names()
        for nombre in nombres_tareas:
            self.caja_tareas.insert(tk.END, nombre)

    def iniciar_temporizador(self):
        if not self.get_tarea_seleccionada():
            messagebox.showwarning(
                "Tarea no seleccionada", "Por favor, selecciona una tarea de la lista para comenzar.")
            return
        self.estado_actual = "Trabajo"
        self.etiqueta_estado.config(text="¡A trabajar!")
        self.actualizar_estado_botones(trabajando=True)
        self.cuenta_regresiva()

    def pausar_temporizador(self):
        if self.id_temporizador:
            self.root.after_cancel(self.id_temporizador)
            self.id_temporizador = None
            self.boton_pausar.config(text="Reanudar")
        else:
            self.boton_pausar.config(text="Pausar")
            self.cuenta_regresiva()

    def reiniciar_temporizador(self):
        if self.id_temporizador:
            self.root.after_cancel(self.id_temporizador)
            self.id_temporizador = None
        self.estado_actual = "Inactivo"
        self.segundos_restantes = CONFIG["trabajo_min"] * 60
        self.etiqueta_reloj.config(text=self.formatear_tiempo())
        self.etiqueta_estado.config(text="Listo para empezar")
        self.actualizar_estado_botones(trabajando=False)

    def cuenta_regresiva(self):
        self.etiqueta_reloj.config(text=self.formatear_tiempo())
        if self.segundos_restantes > 0:
            self.segundos_restantes -= 1
            self.id_temporizador = self.root.after(1000, self.cuenta_regresiva)
        else:
            self.transicion_de_estado()

    def actualizar_estado_botones(self, trabajando):
        self.boton_iniciar.config(state="disabled" if trabajando else "normal")
        self.boton_pausar.config(
            state="normal" if trabajando else "disabled", text="Pausar")
        self.boton_reiniciar.config(
            state="normal" if trabajando else "disabled")
        self.caja_tareas.config(state="disabled" if trabajando else "normal")
