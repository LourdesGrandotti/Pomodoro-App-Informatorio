import json
import os
from datetime import datetime, timezone

# Constante para evitar "números mágicos" y facilitar el mantenimiento
DURACION_POMODORO_SEGUNDOS = 25 * 60  # 1500 segundos

# ------------------------------------------------------------------------------
# Sección 1: Excepciones Personalizadas
# ------------------------------------------------------------------------------


class TaskError(Exception):
    """Clase base para excepciones relacionadas con tareas en esta aplicación."""
    pass


class DuplicateTaskError(TaskError):
    """Se lanza al intentar agregar una tarea con un nombre que ya existe."""
    pass


class TaskNotFoundError(TaskError):
    """Se lanza cuando no se encuentra una tarea por su nombre."""
    pass


class InvalidTaskNameError(TaskError):
    """Se lanza cuando el nombre de una tarea es inválido (ej. vacío)."""
    pass

# ------------------------------------------------------------------------------
# Clase 2: Tarea (Task) - Modelo de Datos Extendido y Lógica Encapsulada
# ------------------------------------------------------------------------------


class Tarea:
    """
    Representa una tarea con atributos extendidos y lógica de cálculo propia.
    """

    def __init__(self, nombre, tiempo_acumulado=0, estado="Pendiente",
                 prioridad=1, fecha_vencimiento=None, etiquetas=None, subtareas=None,
                 pomodoros_objetivo=0):
        self.nombre = nombre
        self.tiempo_acumulado = tiempo_acumulado  # En segundos
        self.estado = estado
        self.prioridad = prioridad  # Ej: 1 (Baja), 2 (Media), 3 (Alta)
        self.fecha_creacion = datetime.now(timezone.utc)
        self.fecha_vencimiento = fecha_vencimiento  # Objeto datetime
        self.etiquetas = etiquetas if etiquetas is not None else []
        self.subtareas = subtareas if subtareas is not None else []
        self.pomodoros_objetivo = pomodoros_objetivo

    @property
    def pomodoros_completos(self):
        """Calcula y devuelve el número de sesiones Pomodoro completas."""
        return self.tiempo_acumulado // DURACION_POMODORO_SEGUNDOS

    @property
    def progreso_objetivo_porcentaje(self):
        """Calcula y devuelve el progreso hacia el objetivo de pomodoros."""
        if self.pomodoros_objetivo > 0:
            return round((self.pomodoros_completos / self.pomodoros_objetivo) * 100, 1)
        return 0

    def a_diccionario(self):
        """Convierte el objeto Tarea a un diccionario para la serialización JSON."""
        return {
            "nombre": self.nombre,
            "tiempo_acumulado": self.tiempo_acumulado,
            "estado": self.estado,
            "prioridad": self.prioridad,
            "fecha_creacion": self.fecha_creacion.isoformat(),
            "fecha_vencimiento": self.fecha_vencimiento.isoformat() if self.fecha_vencimiento else None,
            "etiquetas": self.etiquetas,
            "subtareas": self.subtareas,
            "pomodoros_objetivo": self.pomodoros_objetivo
        }

    @classmethod
    def desde_diccionario(cls, data):
        """Crea una instancia de Tarea a partir de un diccionario."""
        if data.get("fecha_vencimiento"):
            data["fecha_vencimiento"] = datetime.fromisoformat(
                data["fecha_vencimiento"])
        # La fecha de creación es obligatoria y debe estar fuera del if anterior
        data["fecha_creacion"] = datetime.fromisoformat(
            data["fecha_creacion"])
        fecha_creacion = data.pop("fecha_creacion")
        tarea = cls(**data)
        tarea.fecha_creacion = fecha_creacion
        return tarea

    def __str__(self):
        return f"[{self.prioridad}] {self.nombre} ({self.estado}) - {self.tiempo_acumulado // 60} min"

# ------------------------------------------------------------------------------
# Clase 3: GestorDeTareas (TaskManager)
# ------------------------------------------------------------------------------


class GestorDeTareas:
    """
    Gestiona la colección de tareas con alto rendimiento y persistencia escalable.
    """

    def __init__(self, filename="tasks.jsonl"):
        self.filename = filename
        self.tasks = {}
        self.load_tasks()

    def _save_all_tasks(self):
        """(Re)escribe el archivo.jsonl completo."""
        try:
            with open(self.filename, 'w') as f:
                for task in self.tasks.values():
                    f.write(json.dumps(task.a_diccionario()) + '\n')
        except PermissionError:
            print(
                f"Error Crítico: Permiso denegado para escribir en '{self.filename}'.")
        except OSError as e:
            print(
                f"Error Crítico del sistema al escribir en el archivo: {e}")

    def _append_task(self, task):
        """Añade una única tarea al final del archivo.jsonl."""
        try:
            with open(self.filename, 'a') as f:
                f.write(json.dumps(task.a_diccionario()) + '\n')
        except PermissionError:
            del self.tasks[task.nombre]
            raise TaskError(
                f"Permiso denegado. No se pudo guardar la tarea '{task.nombre}'.")
        except OSError as e:
            del self.tasks[task.nombre]
            raise TaskError(
                f"Error del sistema al guardar la tarea '{task.nombre}': {e}")

    def load_tasks(self):
        """Carga tareas desde el archivo.jsonl con manejo de errores específico."""
        self.tasks = {}
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        task = Tarea.desde_diccionario(data)
                        self.tasks[task.nombre] = task
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            print(
                f"Advertencia: '{self.filename}' está corrupto. Se iniciará una lista vacía.")
        except PermissionError:
            print(
                f"Error Crítico: Permiso denegado para leer '{self.filename}'.")
        except OSError as e:
            print(f"Error Crítico del sistema al leer el archivo: {e}")

    def add_task(self, nombre_tarea, **kwargs):
        """Agrega una nueva tarea. Lanza excepciones en caso de error."""
        if not nombre_tarea.strip():
            raise InvalidTaskNameError(
                "El nombre de la tarea no puede estar vacío.")
        if nombre_tarea in self.tasks:
            raise DuplicateTaskError(
                f"Ya existe una tarea con el nombre '{nombre_tarea}'.")

        nueva_tarea = Tarea(nombre_tarea, **kwargs)
        self.tasks[nueva_tarea.nombre] = nueva_tarea
        self._append_task(nueva_tarea)
        return nueva_tarea

    def get_task(self, nombre_tarea):
        """Obtiene una tarea por su nombre. Lanza TaskNotFoundError si no existe."""
        if nombre_tarea not in self.tasks:
            raise TaskNotFoundError(
                f"No se encontró la tarea '{nombre_tarea}'.")
        return self.tasks[nombre_tarea]

    def update_task_time(self, nombre_tarea, segundos_a_agregar):
        """Actualiza el tiempo de una tarea."""
        task = self.get_task(nombre_tarea)
        task.tiempo_acumulado += segundos_a_agregar
        self._save_all_tasks()
        return task

    def delete_task(self, nombre_tarea):
        """Elimina una tarea por su nombre."""
        self.get_task(nombre_tarea)  # Valida que la tarea exista
        del self.tasks[nombre_tarea]
        self._save_all_tasks()

    def get_task_names(self):
        """Devuelve una lista con los nombres de todas las tareas."""
        return list(self.tasks.keys())

    def filter_tasks(self, estado=None, etiqueta=None):
        """Filtra tareas por estado o etiqueta de forma eficiente en una sola pasada."""
        resultados_filtrados = []
        for tarea in self.tasks.values():
            cumple_estado = (estado is None) or (tarea.estado == estado)
            cumple_etiqueta = (etiqueta is None) or (
                etiqueta in tarea.etiquetas)
            if cumple_estado and cumple_etiqueta:
                resultados_filtrados.append(tarea)
        return resultados_filtrados

    def get_sorted_tasks(self, by='prioridad', reverse=True):
        """Devuelve una lista de tareas ordenadas por un atributo."""
        if by not in ('prioridad', 'fecha_vencimiento', 'fecha_creacion'):
            raise ValueError("Clave de ordenamiento no válida.")

        def key_func(t): return getattr(
            t, by) if getattr(t, by) is not None else datetime.min.replace(tzinfo=timezone.utc)
        return sorted(self.tasks.values(), key=key_func, reverse=reverse)

    def add_pomodoro_session(self, nombre_tarea, duracion=DURACION_POMODORO_SEGUNDOS):
        """Registra una sesión Pomodoro completa."""
        return self.update_task_time(nombre_tarea, duracion)

    def get_task_stats(self, nombre_tarea):
        """Retorna estadísticas de una tarea, delegando los cálculos a la propia tarea."""
        task = self.get_task(nombre_tarea)
        return {
            "nombre": task.nombre,
            "tiempo_total_min": task.tiempo_acumulado // 60,
            "tiempo_total_horas": round(task.tiempo_acumulado / 3600, 2),
            "pomodoros_completos": task.pomodoros_completos,
            "pomodoros_objetivo": task.pomodoros_objetivo,
            "progreso_porcentaje": task.progreso_objetivo_porcentaje
        }

# ------------------------------------------------------------------------------
# Ejemplo de Uso y Pruebas
# ------------------------------------------------------------------------------


if __name__ == "__main__":
    # Limpiar archivo de prueba anterior si existe
    if os.path.exists("test_tasks_profesional.jsonl"):
        os.remove("test_tasks_profesional.jsonl")

    gestor = GestorDeTareas("test_tasks_profesional.jsonl")

    print("--- 1. Agregando Tareas con Manejo de Excepciones ---")
    try:
        gestor.add_task("Diseñar UI", prioridad=3, etiquetas=[
                        "diseño", "urgente"], pomodoros_objetivo=4)
        gestor.add_task("Implementar Lógica de Timer", prioridad=3, etiquetas=[
                        "código", "urgente"], pomodoros_objetivo=6)
        gestor.add_task("Escribir Documentación", prioridad=1,
                        etiquetas=["docs"], pomodoros_objetivo=2)
        gestor.add_task("Diseñar UI")  # Esto lanzará una excepción
    except DuplicateTaskError as e:
        print(f"Error capturado: {e}")
    except InvalidTaskNameError as e:
        print(f"Error capturado: {e}")

    print("\nTareas actuales:", gestor.get_task_names())
    print("\n--- 2. Actualizando y Obteniendo Tareas (Rendimiento O(1)) ---")
    try:
        gestor.update_task_time("Implementar Lógica de Timer", 1500)
        tarea_actualizada = gestor.get_task("Implementar Lógica de Timer")
        print(f"Tarea actualizada: {tarea_actualizada}")
        gestor.get_task("Tarea Inexistente")  # Esto lanzará una excepción
    except TaskNotFoundError as e:
        print(f"Error capturado: {e}")

    print("\n--- 3. Eliminando una Tarea ---")
    try:
        gestor.delete_task("Escribir Documentación")
        print("Tarea 'Escribir Documentación' eliminada.")
        print("Tareas restantes:", gestor.get_task_names())
    except TaskNotFoundError as e:
        print(f"Error al eliminar: {e}")

    print("\n--- 4. Usando Funcionalidades Avanzadas (Filtrado y Ordenamiento) ---")
    try:
        gestor.add_task("Revisar PRs", prioridad=2, etiquetas=[
                        "código", "revisión"], pomodoros_objetivo=3)
        gestor.add_task("Planificar Sprint", prioridad=2,
                        etiquetas=["planning"], pomodoros_objetivo=2)
    except TaskError as e:
        print(f"Error agregando tareas de ejemplo: {e}")

    print("\nFiltrando por etiqueta 'código':")
    tareas_codigo = gestor.filter_tasks(etiqueta="código")
    for t in tareas_codigo:
        print(f" - {t}")

    print("\nTodas las tareas ordenadas por prioridad (de mayor a menor):")
    tareas_ordenadas = gestor.get_sorted_tasks(by='prioridad', reverse=True)
    for t in tareas_ordenadas:
        print(f" - {t}")

    print("\n--- 5. Funcionalidades Pomodoro ---")
    print("\nRegistrando 3 Pomodoros para 'Diseñar UI':")
    for i in range(3):
        gestor.add_pomodoro_session("Diseñar UI")
        print(f"  Pomodoro {i+1} registrado")

    print("\nEstadísticas de 'Diseñar UI':")
    stats = gestor.get_task_stats("Diseñar UI")
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\nEstadísticas de 'Implementar Lógica de Timer':")
    stats_timer = gestor.get_task_stats("Implementar Lógica de Timer")
    for key, value in stats_timer.items():
        print(f"  {key}: {value}")

    print("\nEl archivo 'test_tasks_profesional.jsonl' ha sido creado/actualizado.")
