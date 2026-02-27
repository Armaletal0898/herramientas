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
# Cargamos los estilos adaptativos desde modules/styles.py
apply_styles()

# Pequeños ajustes globales de interfaz
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
    # Banner Principal del Sidebar
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

    # Menú de Navegación
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
    
    # Formulario de Entrada
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
            # Limpiar caché de sub-módulos para nuevos escaneos
            keys_to_clear = ['tech_data', 'form_data', 'fuzzer_results', 'tech_results', 'form_results']
            for k in keys_to_clear:
                if k in st.session_state: del st.session_state[k]
            
            st.toast(f"Escaneo finalizado: {clean_target}", icon='✅')
    else:
        st.error("No se pudo resolver el dominio. Verifica la conexión.")

# --- 6. RENDERIZADO DE CONTENIDO ---
res = st.session_state.results

if not res:
    # BANNER COMPACTO DE BIENVENIDA (Cuando no hay resultados)
    st.markdown("""
        <div style="
            background: linear-gradient(90deg, rgba(109, 40, 217, 0.1) 0%, rgba(31, 41, 55, 0.2) 100%);
            padding: 20px 30px;
            border-radius: 12px;
            border-left: 5px solid #6d28d9;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin: 10px 0 20px 0;
        ">
            <div style="text-align: left;">
                <h2 style="color: #6d28d9; margin: 0; font-size: 22px; font-family: 'Courier New', monospace;">🛡️ SCAN-WEB  </h2>
                <p style="margin: 0; color: #a78bfa; font-size: 14px; opacity: 0.8;">Framework listo. Inicia un escaneo para comenzar.</p>
            </div>
            <div style="text-align: right;">
                <div class="pulse-dot" style="color: #94a3b8; font-size: 13px; font-weight: bold;">
                    <span style="color: #7c3aed; font-size: 18px;">●</span> SISTEMA EN ESPERA
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("👈 Ingresa una URL o dominio en el panel lateral para iniciar el análisis de seguridad.")

    # Si se selecciona la guía sin resultados, se muestra aquí
    if menu == "🛡️ Guía de Seguridad":
        render_guia()

else:
    # CABECERA DE RESULTADOS Y BOTÓN DE LIMPIEZA
    col_title, col_clear = st.columns([0.80, 0.20])
    
    with col_title:
        st.subheader(f"📊 Análisis: {res['target']}")
    
    with col_clear:
        # Popover para confirmación de limpieza
        with st.popover("🗑️ Limpiar", use_container_width=True):
            st.warning("¿Borrar todos los resultados?")
            if st.button("Confirmar", type="primary", use_container_width=True):
                st.session_state.results = None
                keys_to_clear = ['tech_data', 'form_data', 'fuzzer_results', 'tech_results', 'form_results']
                for k in keys_to_clear:
                    if k in st.session_state: del st.session_state[k]
                st.rerun()

    st.divider()

    # RENDERIZADO DEL MÓDULO SELECCIONADO
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
