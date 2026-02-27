import streamlit as st
from modules.styles import apply_styles
from modules.auditoria import render_auditoria, UniversalSecurityScanner
from modules.subdominios import render_subdominios
from modules.guia import render_guia
from modules.fuzzer import render_fuzzer
from modules.tech_stack import render_tech_stack  
from modules.form_security import render_form_security

# --- 1. CONFIGURACIÓN INICIAL (DARK MODE FORZADO) ---
st.set_page_config(
    page_title="Scan-Web Pro", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyectamos CSS para forzar el tema oscuro y ocultar menús innecesarios
# Manteniendo visible el botón de la barra lateral (sidebar toggle)
st.markdown("""
    <style>
        /* Forzar fondo oscuro en toda la aplicación */
        .stApp {
            background-color: #0e1117;
            color: #ffffff;
        }
        
        /* Ocultar el menú de ajustes superior derecho (3 puntos) */
        #MainMenu {visibility: hidden;}
        
        /* Ocultar el pie de página de Streamlit */
        footer {visibility: hidden;}
        
        /* Ajuste del Header: Ocultar barra superior pero mantener botón lateral */
        header {
            background-color: rgba(0,0,0,0) !important;
        }
        
        /* Estilo personalizado para el botón de abrir/cerrar sidebar */
        .st-emotion-cache-zq5wmm {
            background-color: #6d28d9 !important;
            color: white !important;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. APLICACIÓN DE ESTILOS ---
apply_styles()

# --- 3. ESTADO DE LA SESIÓN ---
if 'results' not in st.session_state: 
    st.session_state.results = None

# --- 4. BARRA LATERAL (CONTROL Y NAVEGACIÓN) ---
with st.sidebar:
    # Banner Principal
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #6d28d9 0%, #1f2937 100%);
            padding: 12px;
            border-radius: 10px;
            border: 1px solid #7c3aed;
            text-align: center;
            margin-bottom: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        ">
            <h2 style="color: #ffffff; margin: 0; font-size: 20px; font-family: 'Courier New', Courier, monospace;">⚡ SCAN-WEB</h2>
            <p style="color: #a78bfa; font-size: 10px; margin: 0; font-weight: bold;">V1.5 | DARK MODE ONLY</p>
        </div>
    """, unsafe_allow_html=True)

    # Menú de Radio con todas las opciones
    menu = st.radio(
        "Navegación:", 
        [
            "🧪 Auditoría Web", 
            "🔗 Subdominios", 
            "🛠️ Stack Tecnológico", 
            "🛡️ Seguridad de Formularios", 
            "📂 Fuzzing Directorios",
            "🛡️ Guía de Seguridad"
        ]
    )
    
    st.markdown("---")
    
    # Formulario de entrada
    with st.form("sc_form"):
        target_input = st.text_input("URL o Dominio:", "testphp.vulnweb.com")
        submit = st.form_submit_button("🚀 INICIAR ESCANEO", use_container_width=True)

# --- 5. LÓGICA DE ESCANEO ---
if submit:
    # Limpieza del input para evitar fallos de resolución DNS
    clean_target = target_input.replace("https://", "").replace("http://", "").strip("/")
    
    scanner = UniversalSecurityScanner(clean_target)
    if scanner.target_ip:
        with st.spinner('Analizando infraestructura...'):
            h, c = scanner.audit_web_advanced()
            # Almacenamos resultados en la sesión
            st.session_state.results = {
                "ports": scanner.scan_ports(), 
                "sqli": scanner.scan_sqli_pro(),
                "geo": scanner.get_geo_info(), 
                "ssl": scanner.scan_ssl_pro(),
                "headers": h, 
                "cookies": c, 
                "subs": scanner.get_subdomains(),
                "ip": scanner.target_ip, 
                "target": clean_target
            }
            # Limpieza de datos antiguos de módulos específicos
            if 'tech_data' in st.session_state: del st.session_state.tech_data
            if 'form_data' in st.session_state: del st.session_state.form_data
            if 'fuzzer_results' in st.session_state: del st.session_state.fuzzer_results
            
            st.toast(f"Escaneo finalizado: {clean_target}", icon='✅')
    else:
        st.error("No se pudo resolver el dominio. Verifica la conexión.")

# --- 6. RENDERIZADO DE CONTENIDO SEGÚN EL MENÚ ---
# Definimos 'res' para pasarlo a todas las funciones de renderizado
res = st.session_state.results

if menu == "🧪 Auditoría Web":
    render_auditoria(res)

elif menu == "🔗 Subdominios":
    render_subdominios(res)

elif menu == "🛠️ Stack Tecnológico":
    render_tech_stack(res)

elif menu == "🛡️ Seguridad de Formularios":
    render_form_security(res)

elif menu == "📂 Fuzzing Directorios":
    render_fuzzer(res)

elif menu == "🛡️ Guía de Seguridad":
    render_guia()
