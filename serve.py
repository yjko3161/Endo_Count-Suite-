from waitress import serve
from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting production server on http://{host}:{port}")
    serve(app, host=host, port=port)
