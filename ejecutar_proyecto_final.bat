@echo off
title Sistema de Gestion IPAP - Streamlit
set VENV_NAME=venv

echo ====================================================
echo    🚀 INICIANDO ENTORNO PARA SISTEMA DE GESTION
echo ====================================================

:: 1. Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado en el PATH.
    pause
    exit
)

:: 2. Crear el entorno virtual si no existe
if not exist %VENV_NAME% (
    echo [INFO] Creando entorno virtual en la carpeta %VENV_NAME%...
    python -m venv %VENV_NAME%
)

:: 3. Activar el entorno virtual
echo [INFO] Activando entorno virtual...
call %VENV_NAME%\Scripts\activate

:: 4. Verificar existencia de carpeta data
if not exist data (
    echo [INFO] Creando carpeta 'data' para almacenamiento...
    mkdir data
)

:: 5. Verificacion inteligente de paquetes instalados
echo [INFO] Verificando paquetes necesarios...

:: Comprobamos si streamlit, pandas y openpyxl ya estan en el entorno
python -c "import streamlit, pandas, openpyxl" >nul 2>&1

if %errorlevel% neq 0 (
    echo [INFO] Algunos paquetes faltan. Instalando dependencias...
    pip install --upgrade pip
    if exist requirements.txt (
        pip install -r requirements.txt
    ) else (
        pip install streamlit pandas openpyxl
    )
) else (
    echo [OK] Todos los paquetes estan instalados. Saltando actualizacion.
)

:: 6. Limpiar consola y lanzar la app
cls
echo ====================================================
echo    ✅ SERVIDOR LISTO - LANZANDO APLICACION
echo ====================================================
streamlit run app_final.py

pause