import os
import sys

# Asegura que el directorio padre de 'api' esté en el PYTHONPATH.
# Esto permite importar 'app' como un módulo de nivel superior.
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Ahora, intenta importar desde 'app.main'
try:
    from app.main import app as fastapi_app
    # Exponemos la aplicación FastAPI con el nombre estándar 'app' para ASGI
    app = fastapi_app
    # Eliminamos 'handler = fastapi_app' para evitar conflictos con la detección de Vercel
except ImportError as e:
    # Imprime el error de importación para depuración en los logs de Vercel
    print(f"ImportError al intentar importar app.main: {e}")
    print(f"sys.path actual: {sys.path}")
    # Vuelve a lanzar la excepción para que Vercel la capture
    raise