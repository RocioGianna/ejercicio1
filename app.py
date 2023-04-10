from ariadne.asgi import GraphQL
from schema import schema
import uvicorn

app = GraphQL(schema, debug=True)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
