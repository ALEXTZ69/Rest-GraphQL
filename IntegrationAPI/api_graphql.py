import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Exposiciones1P.grupo1.import_threading import tarea
from Exposiciones1P.grupo2.threads import pedidos_concurrentes
from Exposiciones1P.grupo3.condg3.CondiCarrera import CondicionDeCarreraEjemplo
from flask import Flask, request, jsonify
from ariadne import gql, QueryType, MutationType, make_executable_schema, graphql_sync
import threading

type_defs = gql("""
    type Query {
        sistema_3: Int
    }
    type Mutation {
        ejecutar_grupo1: String
        ejecutar_grupo2: String
    }
""")

query = QueryType()

@query.field("sistema_3")
def resolve_sistema_3(_, info):
    ejemplo = CondicionDeCarreraEjemplo()
    hilo1 = threading.Thread(target=ejemplo.incrementar_contador)
    hilo2 = threading.Thread(target=ejemplo.incrementar_contador)

    hilo1.start()
    hilo2.start()

    hilo1.join()
    hilo2.join()

    return ejemplo.contador

mutation = MutationType()

@mutation.field("ejecutar_grupo1")
def resolve_ejecutar_grupo1(_, info):
    hilo1 = threading.Thread(target=tarea, args=('Tarea 1', 2))
    hilo2 = threading.Thread(target=tarea, args=('Tarea 2', 3))

    hilo1.start()
    hilo2.start()

    hilo1.join()
    hilo2.join()

    return "Tareas del grupo 1 completadas"

@mutation.field("ejecutar_grupo2")
def resolve_ejecutar_grupo2(_, info):
    pedidos_concurrentes()
    return "Simulación de pedidos completada"

schema = make_executable_schema(type_defs, query, mutation)

app = Flask(__name__)

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
