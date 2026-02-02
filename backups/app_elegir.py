import streamlit as st
import pandas as pd
import io

# Configuración inicial
st.set_page_config(page_title="Sistema de Gestión - DPID", layout="wide")

# --- FUNCIONES DE PROCESAMIENTO ---
def transformar_datos(df_original):
    df_proc = pd.DataFrame()
    df_proc['N° de documento'] = df_original['Número de documento'].astype(str).str.replace(r'[\.\-]', '', regex=True)
    df_proc['Comisión'] = ""
    df_proc['CUIL'] = df_original['CUIL'].astype(str).str.replace(r'[\.\-]', '', regex=True)
    df_proc['Apellido'] = df_original['apellido'].str.upper()
    df_proc['Nombre'] = df_original['nombres']
    df_proc['Organismo/Municipio'] = df_original['Organismo']
    df_proc['Fecha de Nacimiento'] = df_original['Fecha de nacimiento']
    df_proc['Correo electrónico'] = df_original['Casilla de correo']
    df_proc['Ultimos estudios finalizados'] = df_original['Último estudio finalizado']
    df_proc['Partido de Residencia'] = df_original['Partido de residencia']
    df_proc['Teléfono'] = df_original['Teléfono celular de referencia']
    return df_proc

# --- MENÚ LATERAL ---
with st.sidebar:
    st.title("⚙️ Menú Principal")
    opcion = st.radio(
        "Seleccione un proceso:",
        ["🔍 Verificación de Datos", "📊 Generación de Planilla Excel"]
    )
    st.info("Sugerencia: Primero verifica los datos y luego genera la planilla.")

# --- LÓGICA DE LAS PÁGINAS ---

st.title(f"🚀 {opcion}")

uploaded_file = st.file_uploader("Cargar archivo CSV de inscripciones", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file, sep=';')

    if opcion == "🔍 Verificación de Datos":
        st.subheader("Auditoría de consistencia")
        
        # Lógica de Validación
        duplicados = df[df.duplicated(subset=['Casilla de correo', 'Confirmar correo electrónico'], keep=False)]
        email_mismatch = df[df['Casilla de correo'] != df['Confirmar correo electrónico']]
        doc_mismatch = df[df['Número de documento'] != df['Confirmar el número de documento']]
        
        if duplicados.empty and email_mismatch.empty and doc_mismatch.empty:
            st.success("✨ ¡Todo perfecto! Los datos no presentan inconsistencias.")
        else:
            if not duplicados.empty:
                st.warning(f"Filas duplicadas detectadas: {len(duplicados)}")
                st.dataframe(duplicados)
            
            col1, col2 = st.columns(2)
            with col1:
                if not email_mismatch.empty:
                    st.error("Correos no coinciden")
                    st.dataframe(email_mismatch[['Nro Respuesta', 'Casilla de correo', 'Confirmar correo electrónico']])
            with col2:
                if not doc_mismatch.empty:
                    st.error("Documentos no coinciden")
                    st.dataframe(doc_mismatch[['Nro Respuesta', 'Número de documento', 'Confirmar el número de documento']])

    elif opcion == "📊 Generación de Planilla Excel":
        st.subheader("Transformación y exportación")
        
        if st.button("Procesar y Previsualizar"):
            df_final = transformar_datos(df)
            st.dataframe(df_final.head(10))
            
            # Generar Excel en memoria
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_final.to_excel(writer, index=False, sheet_name='Sheet1')
            
            st.download_button(
                label="⬇️ Descargar Excel Final",
                data=output.getvalue(),
                file_name="planilla_inscriptos_procesada.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

else:
    st.info("Esperando que se cargue un archivo CSV...")