import os
import subprocess
import time
from pyngrok import ngrok

# Configura el puerto de Streamlit
PORT = 8501

# 1. Arrancar Streamlit
print("🚀 Iniciando Streamlit...")
streamlit_proc = subprocess.Popen(
    ["streamlit", "run", "app.py", f"--server.port={PORT}"]
)

# Esperar unos segundos a que Streamlit inicie
time.sleep(5)

# 2. Conectar ngrok
print("🌍 Conectando con ngrok...")
public_url = ngrok.connect(PORT, "http")
print(f"✅ Tu app está disponible en: {public_url}")

print("Presiona Ctrl+C para detener.")

try:
    # Mantener el script vivo mientras corre Streamlit
    streamlit_proc.wait()
except KeyboardInterrupt:
    print("\n🛑 Cerrando procesos...")
    ngrok.kill()
    streamlit_proc.terminate()
