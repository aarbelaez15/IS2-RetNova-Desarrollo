@echo off
echo ==========================================
echo      Iniciando Servicios de RetNova 🔥
echo ==========================================

REM ==============================
REM 1️⃣  Ejecutar Streamlit
REM ==============================
echo Lanzando Streamlit...
cd /d "C:\Users\MrDroky\Desktop\RetNova-Desarrollo\IS2-RetNova-Desarrollo\co\edu\uco\retnova"
start cmd /k "streamlit run app.py"

REM ==============================
REM 2️⃣  Ejecutar Cloudflare Tunnel
REM ==============================
echo Iniciando Cloudflare Tunnel...
cd /d "C:\Users\MrDroky\Desktop\RetNova-Desarrollo\IS2-RetNova-Desarrollo"
start cmd /k "cloudflared --config C:\Users\MrDroky\.cloudflared\config.yml tunnel run retnova"

REM ==============================
REM 3️⃣  Ejecutar Uvicorn (FastAPI)
REM ==============================
echo Iniciando Uvicorn...
cd /d "C:\Users\MrDroky\Desktop\RetNova-Desarrollo\IS2-RetNova-Desarrollo"
start cmd /k "uvicorn co.edu.uco.retnova.interfaces.api.main:app --reload"

echo ==========================================
echo     Todos los servicios fueron iniciados
echo ==========================================
pause
