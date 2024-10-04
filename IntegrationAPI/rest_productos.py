from flask import Flask, jsonify, request

app = Flask(__name__)

productos = [
    {"id": 1, "nombre": "Producto A", "precio": 10.0, "categoria": "Categoria 1"},
    {"id": 2, "nombre": "Producto B", "precio": 20.0, "categoria": "Categoria 2"}
]

@app.route('/api/productos', methods=['GET'])
def listar_productos():
    return jsonify(productos), 200

@app.route('/api/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = next((p for p in productos if p["id"] == id), None)
    if producto:
        return jsonify(producto), 200
    return jsonify({"error": "Producto no encontrado"}), 404

@app.route('/api/productos', methods=['POST'])
def crear_producto():
    data = request.get_json()
    nuevo_producto = {
        "id": len(productos) + 1,
        "nombre": data["nombre"],
        "precio": data["precio"],
        "categoria": data["categoria"]
    }
    productos.append(nuevo_producto)
    return jsonify(nuevo_producto), 201

if __name__ == '__main__':
    app.run(debug=True)
