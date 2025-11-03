# Control general (El Orquestador)

import tkinter as tk

# 1. Importar los "actores" de sus respectivos módulos.
from tasks_manager import GestorDeTareas
from timer_logic import PomodoroApp

# --- PUNTO DE ENTRADA DE LA APLICACIÓN ---
if __name__ == "__main__":

    # 2. Crear la instancia ÚNICA del gestor de tareas.
    # Esta será la "única fuente de verdad" para los datos.
    gestor_de_tareas = GestorDeTareas("pomodoro_tasks.jsonl")

    # 3. Crear la ventana principal de la aplicación.
    ventana_principal = tk.Tk()

    # 4. Crear la instancia de la aplicación de la UI (el temporizador).
    # Se le "inyecta" la ventana principal y el gestor de tareas.
    app = PomodoroApp(ventana_principal, gestor_de_tareas)

    # 5. Iniciar el bucle principal de la aplicación.
    ventana_principal.mainloop()
