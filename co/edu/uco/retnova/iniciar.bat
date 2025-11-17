@echo off
echo ==========================================
echo      Iniciando Servicios de RetNova 🔥
echo ==========================================

REM ==============================
REM 1️⃣  Ejecutar Streamlit
REM ==============================
echo Lanzando Streamlit...
cd /d "E:\ALEJO\retnova\co\edu\uco\retnova"
start cmd /k "streamlit run app.py"

REM ==============================
REM 2️⃣  Ejecutar Cloudflare Tunnel
REM ==============================
echo Iniciando Cloudflare Tunnel...
cd /d "E:\ALEJO\retnova"
start cmd /k "cloudflared --config C:\Users\MrDroky\.cloudflared\config.yml tunnel run retnova"

REM ==============================
REM 3️⃣  Ejecutar Uvicorn (FastAPI)
REM ==============================
echo Iniciando Uvicorn...
cd /d "E:\ALEJO\retnova"
start cmd /k "uvicorn co.edu.uco.retnova.interfaces.api.main:app --reload"

echo ==========================================
echo     Todos los servicios fueron iniciados
echo ==========================================
pause
