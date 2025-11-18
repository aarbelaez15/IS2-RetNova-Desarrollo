import sys
import os

# Obtiene la ruta absoluta de la raíz del proyecto
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

# Si no está en el path, lo agregamos
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
