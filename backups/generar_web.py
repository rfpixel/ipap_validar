import streamlit as st
import pandas as pd
import io

# Configuración de la página
st.set_page_config(page_title="Procesador de Inscripciones", layout="wide")

st.title("🚀 Validador y Generador de Planillas")

# 1. Cargar el archivo
uploaded_file = st.file_uploader("Cargar archivo CSV (separado por ;)", type="csv")

def transformar_datos(df_original):
    """Aplica las transformaciones solicitadas para el Excel final"""
    df_proc = pd.DataFrame()
    
    # N° de documento: Sin puntos ni guiones
    df_proc['N° de documento'] = df_original['Número de documento'].astype(str).str.replace(r'[\.\-]', '', regex=True)
    
    # Comisión: Vacío
    df_proc['Comisión'] = ""
    
    # CUIL: Sin puntos ni guiones
    df_proc['CUIL'] = df_original['CUIL'].astype(str).str.replace(r'[\.\-]', '', regex=True)
    
    # Apellido: En MAYÚSCULAS
    df_proc['Apellido'] = df_original['apellido'].str.upper()
    
    # Mapeo de columnas restantes
    df_proc['Nombre'] = df_original['nombres']
    df_proc['Organismo/Municipio'] = df_original['Organismo']
    df_proc['Fecha de Nacimiento'] = df_original['Fecha de nacimiento']
    df_proc['Correo electrónico'] = df_original['Casilla de correo']
    df_proc['Ultimos estudios finalizados'] = df_original['Último estudio finalizado']
    df_proc['Partido de Residencia'] = df_original['Partido de residencia']
    df_proc['Teléfono'] = df_original['Teléfono celular de referencia']
    
    return df_proc

if uploaded_file is not None:
    # Leer el CSV
    df = pd.read_csv(uploaded_file, sep=';')
    
    # --- SECCIÓN DE VALIDACIÓN ---
    st.header("🔍 1. Validación de Datos")
    
    # Verificación de Errores
    duplicados = df[df.duplicated(subset=['Casilla de correo', 'Confirmar correo electrónico'], keep=False)]
    email_mismatch = df[df['Casilla de correo'] != df['Confirmar correo electrónico']]
    doc_mismatch = df[df['Número de documento'] != df['Confirmar el número de documento']]
    
    hay_errores = not duplicados.empty or not email_mismatch.empty or not doc_mismatch.empty

    if not hay_errores:
        st.success("✅ No se detectaron errores de concordancia ni duplicados.")
    else:
        st.error("⚠️ Se detectaron inconsistencias en los datos:")
        if not duplicados.empty:
            st.warning(f"Duplicados: {len(duplicados)} filas")
            st.dataframe(duplicados[['Nro Respuesta', 'Casilla de correo']])
        if not email_mismatch.empty:
            st.warning("Correos que no coinciden:")
            st.dataframe(email_mismatch[['Nro Respuesta', 'Casilla de correo', 'Confirmar correo electrónico']])
        if not doc_mismatch.empty:
            st.warning("Documentos que no coinciden:")
            st.dataframe(doc_mismatch[['Nro Respuesta', 'Número de documento', 'Confirmar el número de documento']])

    st.divider()

    # --- SECCIÓN DE PROCESAMIENTO Y DESCARGA ---
    st.header("📦 2. Generar Planilla Excel")
    
    if hay_errores:
        st.info("💡 Se recomienda corregir los errores antes de generar la planilla final.")

    # Botón para procesar
    if st.button("Preparar planilla procesada"):
        df_final = transformar_datos(df)
        
        st.subheader("Vista previa del resultado:")
        st.dataframe(df_final.head())

        # Crear el archivo Excel en memoria (buffer)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_final.to_excel(writer, index=False, sheet_name='Inscriptos')
        
        # Botón de descarga real
        st.download_button(
            label="⬇️ Descargar Excel Procesado",
            data=output.getvalue(),
            file_name="datos_procesados_curso.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )