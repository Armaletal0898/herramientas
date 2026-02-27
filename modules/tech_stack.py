import streamlit as st
import requests
import pandas as pd
from modules.security_core import SecurityCore  # Importación del escudo de seguridad

def render_tech_stack(results):
    # Título y Subtítulo con estilo
    st.subheader("🛠️ Análisis de Stack Tecnológico")
    
    if not results:
        st.info("👋 Realiza un escaneo inicial en el panel lateral para habilitar este módulo.")
        return

    # Inicializar el estado de la sesión para este módulo si no existe
    if 'tech_results' not in st.session_state:
        st.session_state.tech_results = None

    st.markdown("""
        Este módulo realiza **Fingerprinting Activo**. Identifica servidores, frameworks y posibles CMS 
        analizando las respuestas del servidor ante peticiones específicas.
    """)

    # --- DISEÑO DE COLUMNAS PARA EL BOTÓN ---
    col1, col2 = st.columns([2, 1])
    with col1:
        st.info("⚠️ El escaneo activo puede ser registrado por WAFs o Firewalls.")
    
    with col2:
        # Botón con estilo de acción
        if st.button("🚀 Identificar Stack", use_container_width=True):
            with st.spinner("Ejecutando Fingerprinting..."):
                techs = []
                # Sanitizamos el target antes de construir la URL
                safe_target = SecurityCore.sanitize_output(results['target'])
                target_url = f"http://{safe_target}"
                
                # 1. Análisis de cabeceras (Pasivo)
                h = results.get("headers", {})
                check_map = {
                    'Server': 'Servidor Web',
                    'X-Powered-By': 'Lenguaje/Framework',
                    'Via': 'Proxy/CDN',
                    'X-AspNet-Version': 'Framework .NET'
                }
                
                # En el código original h es una lista de diccionarios del auditor, 
                # convertimos a dict simple para búsqueda rápida
                h_dict = {item['Cabecera']: item.get('Valor', 'N/A') for item in h if isinstance(item, dict)}
                # Si el auditor no pasó los valores raw, intentamos una petición rápida
                if not h_dict:
                    try:
                        res_head = requests.head(target_url, timeout=3)
                        h_dict = res_head.headers
                    except: pass

                for header, categoria in check_map.items():
                    if header in h_dict:
                        # SANITIZACIÓN del valor de la cabecera
                        safe_val = SecurityCore.sanitize_output(h_dict[header])
                        techs.append({
                            "Categoría": categoria, 
                            "Valor": safe_val, 
                            "Tipo": "Pasivo"
                        })
                
                # 2. Análisis Activo
                try:
                    # Forzamos error 404 para ver firmas
                    test_path = f"{target_url}/error_check_{int(pd.Timestamp.now().timestamp())}"
                    r = requests.get(test_path, timeout=3, verify=False)
                    
                    server_raw = r.headers.get('Server', '')
                    if server_raw:
                        techs.append({
                            "Categoría": "Servidor (Firma)", 
                            "Valor": SecurityCore.sanitize_output(server_raw.capitalize()), 
                            "Tipo": "Activo"
                        })
                    
                    # Detección de CMS
                    cms_paths = {
                        "/wp-includes/": "WordPress",
                        "/administrator/": "Joomla",
                        "/user/login": "Drupal"
                    }
                    for path, name in cms_paths.items():
                        try:
                            cms_check = requests.get(f"{target_url}{path}", timeout=2, verify=False)
                            if cms_check.status_code == 200:
                                techs.append({
                                    "Categoría": "CMS Detectado", 
                                    "Valor": SecurityCore.sanitize_output(name), 
                                    "Tipo": "Activo"
                                })
                        except: continue
                            
                except Exception as e:
                    st.error(f"Error en fingerprinting activo: {SecurityCore.sanitize_output(str(e))}")
                
                st.session_state.tech_results = techs

    # --- RENDERIZADO DE RESULTADOS ---
    if st.session_state.tech_results:
        st.divider()
        st.write("### Tecnologías Identificadas")
        
        df_tech = pd.DataFrame(st.session_state.tech_results)
        
        # Mostramos la tabla sanitizada
        st.dataframe(
            df_tech, 
            use_container_width=True, 
            hide_index=True
        )
        
        st.success("✅ Datos sincronizados con el Resumen Final en Auditoría.")
    else:
        st.warning("Presiona el botón superior para iniciar el análisis del stack.")

    st.divider()
    st.caption("Módulo de Identificación de Tecnologías V1.5 | Protected by SecurityCore")
