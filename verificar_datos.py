import pandas as pd
import os

# Definimos la ruta a la carpeta 'data' y el nombre del archivo
ruta_archivo = os.path.join('data', 'curso_politicas_ok.csv')

# 1. Cargar el archivo CSV desde la carpeta 'data'
try:
    df = pd.read_csv(ruta_archivo, sep=';')
    print(f"Archivo cargado exitosamente desde: {ruta_archivo}\n")
except FileNotFoundError:
    print(f"Error: No se encontró el archivo en {ruta_archivo}. Asegúrate de que la carpeta 'data' exista.")
    exit()

# --- 0) Verificar Duplicados ---
# Buscamos filas duplicadas considerando ambas columnas de correo
duplicados = df[df.duplicated(subset=['Casilla de correo', 'Confirmar correo electrónico'], keep=False)]

print("--- 0) Duplicados encontrados ---")
if duplicados.empty:
    print("No se encontraron filas duplicadas.\n")
else:
    print(duplicados[['Nro Respuesta', 'Casilla de correo', 'Confirmar correo electrónico']])
    print("\n")


# --- 1) Verificar Correos (Nulls y Coincidencia) ---
# Verificar si hay nulos
email_nulls = df[df['Casilla de correo'].isna() | df['Confirmar correo electrónico'].isna()]

# Verificar si coinciden (filtramos los que NO son iguales)
# Usamos .strip() y .lower() opcionalmente si queremos ignorar espacios o mayúsculas, 
# pero aquí comparamos exactos como pide la consigna.
email_mismatch = df[df['Casilla de correo'] != df['Confirmar correo electrónico']]

print("--- 1) Errores en Correo Electrónico ---")
if email_nulls.empty and email_mismatch.empty:
    print("Todos los correos son válidos y coinciden.\n")
else:
    if not email_nulls.empty:
        print("Filas con correos nulos:")
        print(email_nulls[['Nro Respuesta', 'Casilla de correo', 'Confirmar correo electrónico']])
    
    if not email_mismatch.empty:
        print("Filas donde los correos NO coinciden:")
        print(email_mismatch[['Nro Respuesta', 'Casilla de correo', 'Confirmar correo electrónico']])
    print("\n")


# --- 2) Verificar Documentos (Nulls y Coincidencia) ---
# Verificar si hay nulos
doc_nulls = df[df['Número de documento'].isna() | df['Confirmar el número de documento'].isna()]

# Verificar si coinciden
doc_mismatch = df[df['Número de documento'] != df['Confirmar el número de documento']]

print("--- 2) Errores en Documentos ---")
if doc_nulls.empty and doc_mismatch.empty:
    print("Todos los documentos son válidos y coinciden.\n")
else:
    if not doc_nulls.empty:
        print("Filas con documentos nulos:")
        print(doc_nulls[['Nro Respuesta', 'Número de documento', 'Confirmar el número de documento']])
    
    if not doc_mismatch.empty:
        print("Filas donde los documentos NO coinciden:")
        print(doc_mismatch[['Nro Respuesta', 'Número de documento', 'Confirmar el número de documento']])