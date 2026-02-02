@echo off
title Sistema de Gestion DPID - Streamlit
set VENV_NAME=venv

echo ====================================================
echo   🚀 INICIANDO ENTORNO PARA SISTEMA DE GESTION
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

:: 4. Instalar o actualizar dependencias
if exist requirements.txt (
    echo [INFO] Verificando y actualizando dependencias...
    pip install --upgrade pip
    pip install -r requirements.txt
) else (
    echo [ADVERTENCIA] No se encontro requirements.txt. 
    echo Instalando dependencias basicas...
    pip install streamlit pandas openpyxl
)

:: 5. Limpiar consola y lanzar la app
cls
echo ====================================================
echo   ✅ SERVIDOR LISTO - ABRIENDO NAVEGADOR
echo ====================================================
streamlit run app.py

pause