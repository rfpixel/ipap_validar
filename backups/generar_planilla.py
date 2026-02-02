import pandas as pd
import os

# Configuración de rutas
ruta_entrada = os.path.join('data', 'curso_politicas_ok.csv')
ruta_salida = os.path.join('data', 'datos_procesados_curso_politicas.xlsx')

# 1. Cargar el archivo CSV
try:
    df = pd.read_csv(ruta_entrada, sep=';')
except FileNotFoundError:
    print(f"Error: No se encontró el archivo en {ruta_entrada}")
    exit()

# 2. Crear un nuevo DataFrame con las transformaciones solicitadas
df_final = pd.DataFrame()

# N° de documento: Sin puntos ni guiones (convertimos a string y limpiamos)
df_final['N° de documento'] = df['Número de documento'].astype(str).str.replace(r'[\.\-]', '', regex=True)

# Comisión: Dejar vacio
df_final['Comisión'] = ""

# CUIL: Sin puntos ni guiones
df_final['CUIL'] = df['CUIL'].astype(str).str.replace(r'[\.\-]', '', regex=True)

# Apellido: En MAYÚSCULAS
df_final['Apellido'] = df['apellido'].str.upper()

# Mapeo directo de las demás columnas
df_final['Nombre'] = df['nombres']
df_final['Organismo/Municipio'] = df['Organismo']
df_final['Fecha de Nacimiento'] = df['Fecha de nacimiento']
df_final['Correo electrónico'] = df['Casilla de correo']
df_final['Ultimos estudios finalizados'] = df['Último estudio finalizado']
df_final['Partido de Residencia'] = df['Partido de residencia']
df_final['Teléfono'] = df['Teléfono celular de referencia']

# 3. Exportar a Excel
# Nota: Requiere tener instalada la librería 'openpyxl' (pip install openpyxl)
try:
    df_final.to_excel(ruta_salida, index=False)
    print(f"¡Éxito! El archivo se ha generado correctamente como: {ruta_salida}")
except Exception as e:
    print(f"Hubo un error al generar el Excel: {e}")

# Mostrar previsualización en consola
print("\nPrimeras filas del resultado:")
print(df_final.head())