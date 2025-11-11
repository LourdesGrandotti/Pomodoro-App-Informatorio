import tkinter as tk
from tkinter import messagebox
import os
import random
import winsound

def reproducir_sonido(tipo="inicio"):
    if tipo == "inicio":
        winsound.Beep(1000, 200)
    elif tipo == "pausa":
        winsound.Beep(600, 300)
    elif tipo == "final":
        winsound.Beep(800, 500)


#Colores temáticos
COLOR_FONDO = "#caf6d8"
COLOR_TEXTO = "#293e55"
COLOR_RELOJ = "#5dade2"
COLOR_BOTON = "#f7c59f"
COLOR_BOTON_ACCION = "#82e0aa"
COLOR_BOTON_ALERTA = "#f1948a"

# 🪟 Ventana principal
ventana = tk.Tk()
ventana.title("🌈 Reloj con Tareas Seleccionables")
ventana.geometry("420x460")
ventana.resizable(False, False)
ventana.configure(bg=COLOR_FONDO)

# Variables del reloj
cronometro_activo = False
tiempo_segundos = 0
tarea_actual = tk.StringVar(value="(ninguna)")
tiempo_tareas = {}

#Mensajes motivadores
mensajes_divertidos = [
    "¡Vamos con todo! 💪",
    "¡Sos una máquina de enfoque! 🚀",
    "¡A romperla con esta tarea! 🔥",
    "¡Tu tiempo vale oro! ⏳",
    "¡Pomodoro power! 🍅"
]

# Cargar tiempos desde archivo
def cargar_tiempos():
    if os.path.exists("tareas_registradas.txt"):
        with open("tareas_registradas.txt", "r") as file:
            for linea in file:
                tarea, tiempo = linea.strip().split(": ")
                tiempo_tareas[tarea] = int(tiempo)

#Guardar tiempos
def guardar_tiempos():
    with open("tareas_registradas.txt", "w") as file:
        for tarea, tiempo in tiempo_tareas.items():
            file.write(f"{tarea}: {tiempo}\n")

#Formato de tiempo
def formato_tiempo(segundos):
    minutos = segundos // 60
    seg = segundos % 60
    return f"{minutos:02d}:{seg:02d}"

#Actualizar cronómetro
def actualizar_cronometro():
    global tiempo_segundos
    if cronometro_activo:
        tiempo_segundos += 1
        etiqueta_tiempo.config(text=formato_tiempo(tiempo_segundos))
        #Cambio de color dinámico
        colores = ["#5dade2", "#58d68d", "#f5b041", "#af7ac5",  "#f1948a"]
        etiqueta_tiempo.config(fg=random.choice(colores))
        ventana.after(1000, actualizar_cronometro)

# Iniciar
def iniciar():
    global cronometro_activo
    tarea = tarea_actual.get()
    if tarea == "(ninguna)":
        messagebox.showwarning("⛔ Atención", "Seleccioná una tarea antes de iniciar.")
        return
    if not cronometro_activo:
        cronometro_activo = True
        reproducir_sonido("inicio")
        actualizar_cronometro()
        messagebox.showinfo("🎉 ¡A trabajar!", random.choice(mensajes_divertidos))

# Pausar
def pausar():
    global cronometro_activo
    cronometro_activo = False

# Reiniciar
def reiniciar():
    global tiempo_segundos
    pausar()
    tiempo_segundos = 0
    etiqueta_tiempo.config(text="00:00", fg=COLOR_RELOJ)

#Finalizar tarea
def finalizar_tarea():
    global tiempo_segundos
    tarea = tarea_actual.get()
    if tarea == "(ninguna)":
        messagebox.showwarning("⛔ Atención", "Seleccioná una tarea para finalizar.")
        return
    pausar()
    if tarea not in tiempo_tareas:
        tiempo_tareas[tarea] = 0
    tiempo_tareas[tarea] += tiempo_segundos
    guardar_tiempos()
    messagebox.showinfo("✅ Tiempo registrado",
                        f"📝 Tarea: {tarea}\n⏱️ Tiempo total: {formato_tiempo(tiempo_tareas[tarea])}")
    reiniciar()

# Mostrar resumen
def mostrar_resumen():
    if not tiempo_tareas:
        messagebox.showinfo("📋 Resumen", "Todavía no hay tareas registradas.")
        return
    resumen = "⏱️ Tiempo total por tarea:\n\n"
    for tarea, segundos in tiempo_tareas.items():
        resumen += f"• {tarea}: {formato_tiempo(segundos)}\n"
    messagebox.showinfo("📈 Resumen de tiempo", resumen)

# Interfaz gráfica
etiqueta_titulo = tk.Label(ventana, text="🌟 Reloj con Menú de Tareas", font=("Comic Sans MS", 16, "bold"),
                           fg=COLOR_TEXTO, bg=COLOR_FONDO)
etiqueta_titulo.pack(pady=10)

# Menú de tareas
tareas = ["(ninguna)", "Estudiar", "Leer", "Ejercicio", "Descansar", "Otro"]
etiqueta_menu = tk.Label(ventana, text="Seleccioná una tarea:", font=("Helvetica", 11),
                         bg=COLOR_FONDO, fg=COLOR_TEXTO)
etiqueta_menu.pack()

menu_tareas = tk.OptionMenu(ventana, tarea_actual, *tareas)
menu_tareas.config(bg="#f9e79f", font=("Helvetica", 10))
menu_tareas.pack(pady=5)

# Cronómetro
etiqueta_tiempo = tk.Label(ventana, text="00:00", font=("Courier", 44, "bold"), fg=COLOR_RELOJ, bg=COLOR_FONDO)
etiqueta_tiempo.pack(pady=20)

# Botones de control
frame_botones = tk.Frame(ventana, bg=COLOR_FONDO)
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="▶ Iniciar", command=iniciar, width=10, bg=COLOR_BOTON_ACCION).grid(row=0, column=0, padx=5)
tk.Button(frame_botones, text="⏸ Pausar", command=pausar, width=10, bg="#f9e79f").grid(row=0, column=1, padx=5)
tk.Button(frame_botones, text="🔄 Reiniciar", command=reiniciar, width=10, bg="#d7bde2").grid(row=0, column=2, padx=5)

# Botón finalizar tarea
tk.Button(ventana, text="✅ Finalizar tarea actual", command=finalizar_tarea, width=25, bg="#d4efdf").pack(pady=5)

# Botón resumen
tk.Button(ventana, text="📊 Mostrar resumen total", command=mostrar_resumen, width=25, bg="#fadbd8").pack(pady=5)

# Iniciar aplicación
cargar_tiempos()
ventana.mainloop()