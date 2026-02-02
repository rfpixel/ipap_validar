import streamlit as st
import pandas as pd
import io

# Configuración inicial
st.set_page_config(page_title="Sistema de Gestión IPAP - DPID", layout="wide")

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

# --- 1. CARGA DE ARCHIVO (Fuera del menú para validar primero) ---
st.title("🚀 Sistema de Gestión de Inscripciones IPAP")
uploaded_file = st.file_uploader("Cargar archivo CSV de inscripciones", type="csv")

# Inicializamos variables de estado
hay_errores = False
opciones_menu = ["🔍 Verificación de Datos"] # Opción por defecto

if uploaded_file:
    # Leemos el archivo inmediatamente para validar
    df = pd.read_csv(uploaded_file, sep=';')
    
    # --- 2. VALIDACIÓN AUTOMÁTICA ---
    duplicados = df[df.duplicated(subset=['Casilla de correo', 'Confirmar correo electrónico'], keep=False)]
    email_mismatch = df[df['Casilla de correo'] != df['Confirmar correo electrónico']]
    doc_mismatch = df[df['Número de documento'] != df['Confirmar el número de documento']]
    
    # Verificamos si hay algún problema
    hay_errores = not duplicados.empty or not email_mismatch.empty or not doc_mismatch.empty

    if not hay_errores:
        # Si NO hay errores, habilitamos la segunda opción en el menú
        opciones_menu.append("📊 Generación de Planilla Excel")
    
    # --- 3. MENÚ LATERAL DINÁMICO ---
    with st.sidebar:
        st.header("⚙️ Menú Principal")
        opcion = st.radio("Seleccione un proceso:", opciones_menu)
        
        if hay_errores:
            st.error("❌ Errores detectados. La generación de Excel está bloqueada hasta que se corrija el archivo.")
        else:
            st.success("✅ Archivo validado. Generación habilitada.")

    # --- 4. LÓGICA DE PÁGINAS ---
    if opcion == "🔍 Verificación de Datos":
        st.subheader("Informe de Auditoría")
        
        if not hay_errores:
            st.success("✨ ¡Todo perfecto! Los datos no presentan inconsistencias. Ya puedes ir al menú lateral y seleccionar 'Generación de Planilla'.")
        else:
            if not duplicados.empty:
                st.warning(f"Filas duplicadas detectadas: {len(duplicados)}")
                st.dataframe(duplicados)
            
            col1, col2 = st.columns(2)
            with col1:
                if not email_mismatch.empty:
                    st.error(f"Correos no coinciden ({len(email_mismatch)} casos)")
                    st.dataframe(email_mismatch[['Nro Respuesta', 'Casilla de correo', 'Confirmar correo electrónico']])
            with col2:
                if not doc_mismatch.empty:
                    st.error(f"Documentos no coinciden ({len(doc_mismatch)} casos)")
                    st.dataframe(doc_mismatch[['Nro Respuesta', 'Número de documento', 'Confirmar el número de documento']])

    elif opcion == "📊 Generación de Planilla Excel":
        st.subheader("Transformación y exportación de datos")
        
        if st.button("Procesar y Previsualizar"):
            df_final = transformar_datos(df)
            st.dataframe(df_final.head(10))
            
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_final.to_excel(writer, index=False, sheet_name='Inscriptos')
            
            st.download_button(
                label="⬇️ Descargar Excel Final",
                data=output.getvalue(),
                file_name="planilla_procesada_ok.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

else:
    st.info("👋 Bienvenid@. Por favor, cargue un archivo CSV para comenzar.")
    with st.sidebar:
        st.write("Esperando archivo...")