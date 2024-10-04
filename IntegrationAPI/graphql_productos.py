from flask import Flask, request, jsonify
from ariadne import QueryType, MutationType, gql, make_executable_schema, graphql_sync

app = Flask(__name__)

productos = [
    {"id": 1, "nombre": "Producto A", "precio": 10.0, "categoria": "Categoria 1"},
    {"id": 2, "nombre": "Producto B", "precio": 20.0, "categoria": "Categoria 2"}
]

type_defs = gql("""
    type Producto {
        id: Int
        nombre: String
        precio: Float
        categoria: String
    }
    
    type Query {
        productos: [Producto]
        producto(id: Int!): Producto
    }

    type Mutation {
        crearProducto(nombre: String!, precio: Float!, categoria: String!): Producto
    }
""")

query = QueryType()

@query.field("productos")
def resolve_productos(_, info):
    return productos

@query.field("producto")
def resolve_producto(_, info, id):
    return next((p for p in productos if p["id"] == id), None)

mutation = MutationType()

@mutation.field("crearProducto")
def resolve_crear_producto(_, info, nombre, precio, categoria):
    nuevo_producto = {
        "id": len(productos) + 1,
        "nombre": nombre,
        "precio": precio,
        "categoria": categoria
    }
    productos.append(nuevo_producto)
    return nuevo_producto

schema = make_executable_schema(type_defs, query, mutation)

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return """
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <title>GraphiQL</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/graphiql/0.17.5/graphiql.min.css" rel="stylesheet" />
      </head>
      <body style="margin: 0;">
        <div id="graphiql" style="height: 100vh;"></div>
        <script crossorigin src="https://cdnjs.cloudflare.com/ajax/libs/react/16.8.3/umd/react.production.min.js"></script>
        <script crossorigin src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/16.8.3/umd/react-dom.production.min.js"></script>
        <script crossorigin src="https://cdnjs.cloudflare.com/ajax/libs/graphiql/0.17.5/graphiql.min.js"></script>
        <script>
          const graphQLFetcher = graphQLParams =>
            fetch('/graphql', {
              method: 'post',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(graphQLParams),
            })
            .then(response => response.json())
            .catch(() => response.text());
          ReactDOM.render(
            React.createElement(GraphiQL, { fetcher: graphQLFetcher }),
            document.getElementById('graphiql'),
          );
        </script>
      </body>
    </html>
    """, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=request, debug=True)
    status_code = 200 if success else 400
    return jsonify(result), status_code

if __name__ == "__main__":
    app.run(debug=True)
