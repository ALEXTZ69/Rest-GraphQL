import threading
import time

# Función que simula una tarea que toma tiempo
def tarea(nombre, tiempo_duracion):
    print(f'Iniciando la tarea {nombre}')
    time.sleep(tiempo_duracion)  # Simula que la tarea toma tiempo en ejecutarse
    print(f'Tarea {nombre} completada en {tiempo_duracion} segundos')

# Crear hilos (threads) para ejecutar las tareas en paralelo
hilo1 = threading.Thread(target=tarea, args=('Tarea 1', 2))
hilo2 = threading.Thread(target=tarea, args=('Tarea 2', 3))

# Iniciar ambos hilos
hilo1.start()
hilo2.start()

# Esperar a que los hilos terminen de ejecutarse antes de continuar
hilo1.join()
hilo2.join()

print("Todas las tareas han sido completadas")