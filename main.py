import streamlit as st
from modules.styles import apply_styles
from modules.auditoria import render_auditoria, UniversalSecurityScanner
from modules.subdominios import render_subdominios
from modules.guia import render_guia
from modules.fuzzer import render_fuzzer
from modules.tech_stack import render_tech_stack  
from modules.form_security import render_form_security

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="Scan-Web Pro", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. APLICACIÓN DE ESTILOS EXTERNOS ---
# Llamamos a la función de tu archivo modules/styles.py
# He quitado el bloque st.markdown de CSS que tenías aquí para evitar conflictos
apply_styles()

# Ocultamos solo elementos globales mínimos que no dependen del tema
st.markdown("""
    <style>
        #MainMenu { visibility: visible; }
        footer { visibility: hidden; }
        header { background: rgba(0,0,0,0); }
    </style>
""", unsafe_allow_html=True)

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
            <p style="color: #a78bfa; font-size: 10px; margin: 0; font-weight: bold;">V1.5 | PROFESSIONAL EDITION</p>
        </div>
    """, unsafe_allow_html=True)

    # Menú de Radio
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
    clean_target = target_input.replace("https://", "").replace("http://", "").strip("/")
    scanner = UniversalSecurityScanner(clean_target)
    
    if scanner.target_ip:
        with st.spinner('Analizando infraestructura...'):
            h, c = scanner.audit_web_advanced()
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
            # Limpiar caché de módulos
            keys = ['tech_data', 'form_data', 'fuzzer_results', 'tech_results', 'form_results']
            for k in keys:
                if k in st.session_state: del st.session_state[k]
            
            st.toast(f"Escaneo finalizado: {clean_target}", icon='✅')
    else:
        st.error("No se pudo resolver el dominio. Verifica la conexión.")



# --- 6. ÁREA DE RESULTADOS Y BOTÓN DE LIMPIEZA ---
res = st.session_state.results

if res:
    # Creamos dos columnas: una para el título y otra para el botón de limpiar
    col_title, col_clear = st.columns([0.85, 0.15])
    
    with col_title:
        st.subheader(f"📊 Resultados para: {res['target']}")
    
    with col_clear:
        # Botón para resetear la sesión
        if st.button("🗑️ Limpiar", use_container_width=True, help="Borra los resultados actuales"):
            st.session_state.results = None
            # También limpiamos las claves específicas de los módulos
            keys = ['tech_data', 'form_data', 'fuzzer_results', 'tech_results', 'form_results']
            for k in keys:
                if k in st.session_state: del st.session_state[k]
            st.rerun() # Recarga la app para volver al estado inicial

# --- 7. RENDERIZADO DE CONTENIDO SEGÚN EL MENÚ ---
if not res:
    # Mensaje de bienvenida cuando no hay escaneo activo
    st.info("👋 Bienvenido a Scan-Web Pro. Introduce un dominio en el panel lateral para comenzar.")
else:
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

# Solo mostramos la Guía de Seguridad si no hay resultados, ya que no depende de un escaneo
if menu == "🛡️ Guía de Seguridad" and not res:
    render_guia()
