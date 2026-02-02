import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Validador de CSV", layout="wide")

st.title("📊 Validador de Datos de Inscripción")
st.markdown("Carga tu archivo CSV para verificar duplicados y errores en correos o documentos.")

# 1. Cargar el archivo
uploaded_file = st.file_uploader("Elige el archivo CSV", type="csv")

if uploaded_file is not None:
    # Leer el CSV (usando el separador ;)
    df = pd.read_csv(uploaded_file, sep=';')
    
    st.success("Archivo cargado correctamente")
    
    # --- 0) Verificar Duplicados ---
    st.subheader("0) Verificación de Duplicados")
    duplicados = df[df.duplicated(subset=['Casilla de correo', 'Confirmar correo electrónico'], keep=False)]
    
    if duplicados.empty:
        st.info("✅ No se encontraron filas duplicadas.")
    else:
        st.warning(f"Se encontraron {len(duplicados)} filas duplicadas.")
        st.dataframe(duplicados[['Nro Respuesta', 'Casilla de correo', 'Confirmar correo electrónico']])

    col1, col2 = st.columns(2)

    with col1:
        # --- 1) Verificar Correos ---
        st.subheader("1) Errores en Correo Electrónico")
        email_nulls = df[df['Casilla de correo'].isna() | df['Confirmar correo electrónico'].isna()]
        email_mismatch = df[df['Casilla de correo'] != df['Confirmar correo electrónico']]

        if email_nulls.empty and email_mismatch.empty:
            st.info("✅ Todos los correos coinciden.")
        else:
            if not email_nulls.empty:
                st.error("Correos nulos detectados:")
                st.write(email_nulls[['Nro Respuesta', 'Casilla de correo']])
            
            if not email_mismatch.empty:
                st.error("Correos que NO coinciden:")
                st.write(email_mismatch[['Nro Respuesta', 'Casilla de correo', 'Confirmar correo electrónico']])

    with col2:
        # --- 2) Verificar Documentos ---
        st.subheader("2) Errores en Documentos")
        doc_nulls = df[df['Número de documento'].isna() | df['Confirmar el número de documento'].isna()]
        doc_mismatch = df[df['Número de documento'] != df['Confirmar el número de documento']]

        if doc_nulls.empty and doc_mismatch.empty:
            st.info("✅ Todos los documentos coinciden.")
        else:
            if not doc_nulls.empty:
                st.error("Documentos nulos detectados:")
                st.write(doc_nulls[['Nro Respuesta', 'Número de documento']])
            
            if not doc_mismatch.empty:
                st.error("Documentos que NO coinciden:")
                st.write(doc_mismatch[['Nro Respuesta', 'Número de documento', 'Confirmar el número de documento']])

    # Mostrar data completa opcional
    with st.expander("Ver datos completos"):
        st.dataframe(df)