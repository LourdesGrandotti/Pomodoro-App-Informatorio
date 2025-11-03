# Sonidos, alertas, y estadísticas.

from tkinter import messagebox


def reproducir_sonido_alerta(root):
    """
    Reproduce un sonido de alerta simple de forma multiplataforma.
    Recibe el objeto 'root' de la ventana de tkinter para usar su método.bell().
    """
    try:
        root.bell()
    except Exception as e:
        print(f"No se pudo reproducir el sonido de alerta: {e}")


def mostrar_estadisticas(parent_window, stats_dict):
    """
    Muestra una ventana de messagebox con las estadísticas de una tarea.
    Recibe la ventana "padre" sobre la que mostrarse y un diccionario con las estadísticas.
    Esta función solo se encarga de la PRESENTACIÓN de los datos.
    """
    if not stats_dict:
        messagebox.showinfo(
            "Estadísticas",
            "No hay datos de estadísticas para mostrar.",
            parent=parent_window
        )
        return

    mensaje = (
        f"Estadísticas para: {stats_dict.get('nombre', 'N/A')}\n\n"
        f"Pomodoros Completados: {stats_dict.get('pomodoros_completos', 0)} de {stats_dict.get('pomodoros_objetivo', 0)}\n"
        f"Progreso: {stats_dict.get('progreso_porcentaje', 0)}%\n"
        f"Tiempo Total Invertido: {stats_dict.get('tiempo_total_min', 0)} minutos"
    )
    messagebox.showinfo("Estadísticas de Tarea", mensaje, parent=parent_window)
