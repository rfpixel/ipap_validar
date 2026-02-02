import streamlit as st
import pandas as pd
import io

# Configuración inicial
st.set_page_config(page_title="Sistema de Gestión IPAP - DPID", layout="wide")

# --- DEFINICIÓN DE COLUMNAS REQUERIDAS ---
COLUMNAS_REQUERIDAS = [
    'fecha carga', 'Nro Respuesta', 'Casilla de correo', 'Confirmar correo electrónico',
    'apellido', 'nombres', 'Tipo de documento', 'Número de documento',
    'Confirmar el número de documento', 'CUIL', 'Fecha de nacimiento', 'Edad',
    'Último estudio finalizado', 'Teléfono celular de referencia', 'Organismo',
    'Repartición / oficina', 'Partido de residencia', 'Curso en el que desea inscribirse', 'Cargo'
]

# --- FUNCIONES DE APOYO ---
def detectar_separador(file):
    """Detecta si el archivo usa punto y coma o coma"""
    file.seek(0) # Asegurar inicio
    linea = file.readline().decode('utf-8')
    file.seek(0) # Volver al inicio para la siguiente lectura
    return ';' if ';' in linea else ','

def transformar_datos(df_original):
    """Aplica la lógica de negocio para la planilla final"""
    df_proc = pd.DataFrame()
    df_proc['N° de documento'] = df_original['Número de documento'].astype(str).str.replace(r'[\.\-]', '', regex=True)
    df_proc['Comisión'] = ""
    df_proc['CUIL'] = df_original['CUIL'].astype(str).str.replace(r'[\.\-]', '', regex=True)
    df_proc['Apellido'] = df_original['apellido'].astype(str).str.upper()
    df_proc['Nombre'] = df_original['nombres']
    df_proc['Organismo/Municipio'] = df_original['Organismo']
    df_proc['Fecha de Nacimiento'] = df_original['Fecha de nacimiento']
    df_proc['Correo electrónico'] = df_original['Casilla de correo']
    df_proc['Ultimos estudios finalizados'] = df_original['Último estudio finalizado']
    df_proc['Partido de Residencia'] = df_original['Partido de residencia']
    df_proc['Teléfono'] = df_original['Teléfono celular de referencia']
    return df_proc

# --- 1. INTERFAZ DE CARGA ---
st.title("🚀 Sistema de Gestión de Inscripciones IPAP")
uploaded_file = st.file_uploader("Cargar archivo CSV de inscripciones", type="csv")

if uploaded_file:
    # A. Detectar formato y separador
    sep_detectado = detectar_separador(uploaded_file)
    
    # B. Validar Columnas (Usando seek para asegurar que lee desde el inicio)
    uploaded_file.seek(0)
    df_temp = pd.read_csv(uploaded_file, sep=sep_detectado, nrows=0)
    faltantes = [c for c in COLUMNAS_REQUERIDAS if c not in df_temp.columns]
    
    if faltantes:
        st.error(f"❌ **Error de Formato:** El CSV no tiene las columnas esperadas.")
        st.write("Faltan los siguientes campos:", faltantes)
    else:
        # C. Carga completa (Volvemos a hacer seek antes de la lectura final)
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file, sep=sep_detectado)
        
        # Validaciones de concordancia
        duplicados = df[df.duplicated(subset=['Casilla de correo', 'Confirmar correo electrónico'], keep=False)]
        email_mismatch = df[df['Casilla de correo'].astype(str).str.strip() != 
                            df['Confirmar correo electrónico'].astype(str).str.strip()]
        doc_mismatch = df[df['Número de documento'].astype(str).str.strip() != 
                           df['Confirmar el número de documento'].astype(str).str.strip()]
        
        hay_errores = not duplicados.empty or not email_mismatch.empty or not doc_mismatch.empty

        # --- 2. MENÚ LATERAL DINÁMICO ---
        opciones_menu = ["🔍 Verificación de Datos"]
        if not hay_errores:
            opciones_menu.append("📊 Generación de Planilla Excel")
        
        with st.sidebar:
            st.header("⚙️ Menú Principal")
            opcion = st.radio("Seleccione un proceso:", opciones_menu)
            
            if hay_errores:
                st.error("❌ Errores detectados. Generación bloqueada.")
            else:
                st.success("✅ Datos válidos. Generación habilitada.")

        # --- 3. LÓGICA DE PÁGINAS ---
        if opcion == "🔍 Verificación de Datos":
            st.subheader("Informe de Auditoría")
            if not hay_errores:
                st.success("✨ ¡Todo perfecto! No hay inconsistencias.")
            else:
                # Mostrar tablas de errores... (igual que antes)
                if not duplicados.empty:
                    st.warning(f"Filas duplicadas: {len(duplicados)}")
                    st.dataframe(duplicados)
                
                col1, col2 = st.columns(2)
                with col1:
                    if not email_mismatch.empty:
                        st.error(f"Emails no coinciden ({len(email_mismatch)})")
                        st.dataframe(email_mismatch[['Nro Respuesta', 'Casilla de correo', 'Confirmar correo electrónico']])
                with col2:
                    if not doc_mismatch.empty:
                        st.error(f"DNI no coinciden ({len(doc_mismatch)})")
                        st.dataframe(doc_mismatch[['Nro Respuesta', 'Número de documento', 'Confirmar el número de documento']])

        elif opcion == "📊 Generación de Planilla Excel":
            st.subheader("Transformación y exportación")
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
    st.info("👋 Por favor, cargue un archivo CSV para comenzar.")