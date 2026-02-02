@echo off
title Git Update Automático
echo ------------------------------------------
echo 🚀 Sincronizando cambios con GitHub...
echo ------------------------------------------

:: Agregar cambios
git add .

:: Pedir al usuario el mensaje del commit
set /p mensaje="Introduce el mensaje del cambio: "

:: Commit y Push
git commit -m "%mensaje%"
git push origin main

echo ------------------------------------------
echo ✅ Proceso finalizado con éxito!
echo ------------------------------------------
pause