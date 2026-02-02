# 🚀 Sistema de Gestión e Inscripciones - IPAP / DPID

Este proyecto es una herramienta de automatización desarrollada para la **DPID** (Dirección Provincial de Innovación Digital). Su objetivo es auditar archivos CSV de inscripciones del IPAP, detectar errores de carga y generar planillas Excel normalizadas listas para procesos administrativos.

## 🛠️ Funcionalidades Principales

* **Detección Automática de Formato:** Soporta archivos CSV con separador `;` o `,`.
* **Validación de Esquema:** Verifica que el archivo subido contenga todas las columnas oficiales requeridas.
* **Auditoría de Datos:**
    * Identificación de filas duplicadas (por correo).
    * Verificación de concordancia en correos electrónicos.
    * Verificación de concordancia en números de documento (DNI).
* **Generación de Planilla Excel:** Exporta un archivo `.xlsx` con limpieza de datos (DNI/CUIL sin puntos ni guiones y apellidos en mayúsculas).
* **Bloqueo de Seguridad:** La opción de generar el Excel solo se habilita si el archivo pasa el test de integridad.

## 📁 Estructura del Proyecto

* `app_final.py`: Aplicación principal de Streamlit.
* `generar_test_csv.py`: Script para generar datos sintéticos con errores para pruebas de QA.
* `ejecutar_proyecto_final.bat`: Script de arranque automático para Windows (configura venv e instala dependencias).
* `requirements.txt`: Lista de librerías necesarias (Pandas, Streamlit, Openpyxl).
* `data/`: Carpeta (local) para almacenamiento de archivos temporales (ignorada por Git).
* `backup/`: Historial de versiones previas del código.

## 🚀 Instalación y Ejecución (Windows)

No es necesario configurar el entorno manualmente. El proyecto incluye un automatizador:

1.  Asegúrate de tener **Python 3.10+** instalado.
2.  Clona este repositorio o descarga los archivos.
3.  Haz doble clic en el archivo **`ejecutar_proyecto_final.bat`**.
4.  El script creará un entorno virtual (`venv`), instalará las dependencias y abrirá la aplicación en tu navegador predeterminado.

## 🧪 Testing y QA

Para probar la robustez del sistema, puedes generar un archivo de prueba con errores aleatorios:

1.  Activa el entorno virtual: `.\venv\Scripts\activate`
2.  Ejecuta: `python generar_test_csv.py`
3.  Sube el archivo generado (`data/datos_prueba_masivos.csv`) a la aplicación para observar la detección de errores.

## 📝 Notas de Mantenimiento
* El archivo `.gitignore` está configurado para no subir datos sensibles ni la carpeta `venv`.
* Cualquier cambio en las columnas del CSV original debe actualizarse en la constante `COLUMNAS_REQUERIDAS` dentro de `app_final.py`.

---
**Desarrollado por:** Rafael Caceres Petkowicz ([rcpetkowicz@gmail.com](mailto:rcpetkowicz@gmail.com))  
**Área:** DPID - DATOS ([rafael.caceres@gba.gob.ar](mailto:rafael.caceres@gba.gob.ar))