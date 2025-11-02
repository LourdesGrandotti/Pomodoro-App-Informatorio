#Sonidos, alertas, y estadísticas.
import winsound
messagebox = __import__('tkinter.messagebox').messagebox

def reproducir_sonido(tipo="beep"):
    if tipo == "beep":
        winsound.Beep(1000, 300)  # frecuencia 1000Hz, duración 300ms
    elif tipo == "descanso":
        winsound.Beep(600, 500)
    elif tipo == "archivo":
        winsound.PlaySound("sonido.wav", winsound.SND_FILENAME)

def ver_estadisticas(self):
    tarea = self.tarea_actual.get()
    tareas_total = len(self.lista_tareas)
    ciclos = getattr(self, "ciclos_completados", 0)
    tiempo = self.tiempo_acumulado.get()

    mensaje = (
        f"📌 Tarea actual: {tarea}\n"
        f"📋 Tareas en lista: {tareas_total}\n"
        f"🔁 Ciclos Pomodoro completados: {ciclos}\n"
        f"⏱️ Tiempo acumulado: {tiempo}"
    )

    messagebox.showinfo("Estadísticas de sesión", mensaje)
