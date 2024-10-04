import sys
import os
from flask import Flask, jsonify

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Exposiciones1P.grupo1.import_threading import tarea
from Exposiciones1P.grupo2.threads import pedidos_concurrentes 
from Exposiciones1P.grupo3.condg3.CondiCarrera import CondicionDeCarreraEjemplo
import threading

app = Flask(__name__)

@app.route('/api/grupo1', methods=['GET'])
def ejecutar_grupo1():
    hilo1 = threading.Thread(target=tarea, args=('Tarea 1', 2))
    hilo2 = threading.Thread(target=tarea, args=('Tarea 2', 3))

    hilo1.start()
    hilo2.start()

    hilo1.join()
    hilo2.join()

    return jsonify({"message": "Tareas del grupo 1 completadas"}), 200

@app.route('/api/grupo2', methods=['GET'])
def ejecutar_grupo2():
    pedidos_concurrentes() 
    return jsonify({"message": "Simulacion de pedidos completada"}), 200

@app.route('/api/grupo3', methods=['GET'])
def ejecutar_grupo3():
    ejemplo = CondicionDeCarreraEjemplo()
    
    hilo1 = threading.Thread(target=ejemplo.incrementar_contador)
    hilo2 = threading.Thread(target=ejemplo.incrementar_contador)

    hilo1.start()
    hilo2.start()

    hilo1.join()
    hilo2.join()

    return jsonify({"contador_final": ejemplo.contador}), 200

if __name__ == '__main__':
    app.run(debug=True)
