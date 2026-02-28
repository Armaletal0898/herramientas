import streamlit as st
import requests
import pandas as pd
from modules.security_core import SecurityCore

def render_tech_stack(results):
    """Módulo de Identificación de Tecnologías con Protección SecurityCore"""
    
    st.subheader("🛠️ Análisis de Stack Tecnológico")
    
    if not results:
        st.info("👋 Realiza un escaneo inicial en el panel lateral para habilitar este módulo.")
        return

    # Inicializar el estado de la sesión
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
        if st.button("🚀 Identificar Stack", use_container_width=True):
            with st.spinner("Ejecutando Fingerprinting..."):
                techs = []
                safe_target = SecurityCore.sanitize_output(results.get('target', ''))
                target_url = f"http://{safe_target}"
                
                # 1. Análisis de cabeceras
                h = results.get("headers", {})
                check_map = {
                    'Server': 'Servidor Web',
                    'X-Powered-By': 'Lenguaje/Framework',
                    'Via': 'Proxy/CDN',
                    'X-AspNet-Version': 'Framework .NET'
                }
                
                # Convertimos cabeceras a diccionario simple
                h_dict = {item['Cabecera']: item.get('Valor', 'N/A') for item in h if isinstance(item, dict)}
                
                if not h_dict:
                    try:
                        res_head = requests.head(target_url, timeout=3)
                        SecurityCore.analyze_response(target_url, response=res_head)
                        h_dict = res_head.headers
                    except Exception as e:
                        SecurityCore.analyze_response(target_url, error=e)

                for header, categoria in check_map.items():
                    if header in h_dict:
                        safe_val = SecurityCore.sanitize_output(h_dict[header])
                        techs.append({
                            "Categoría": categoria, 
                            "Valor": safe_val, 
                            "Tipo": "Pasivo"
                        })
                
                # 2. Análisis Activo
                try:
                    # Test de error 404 para firmas de servidor
                    test_path = f"{target_url}/error_check_{int(pd.Timestamp.now().timestamp())}"
                    r = requests.get(test_path, timeout=5, verify=False)
                    
                    if SecurityCore.analyze_response(target_url, response=r):
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
                                full_url = f"{target_url}{path}"
                                cms_check = requests.get(full_url, timeout=3, verify=False)
                                if SecurityCore.analyze_response(full_url, response=cms_check):
                                    if cms_check.status_code == 200:
                                        techs.append({
                                            "Categoría": "CMS Detectado", 
                                            "Valor": SecurityCore.sanitize_output(name), 
                                            "Tipo": "Activo"
                                        })
                            except:
                                continue
                                
                except Exception as e:
                    SecurityCore.analyze_response(target_url, error=e)
                
                st.session_state.tech_results = techs

    # --- RENDERIZADO DE RESULTADOS ---
    if st.session_state.tech_results:
        st.divider()
        st.write("### Tecnologías Identificadas")
        df_tech = pd.DataFrame(st.session_state.tech_results)
        st.dataframe(df_tech, use_container_width=True, hide_index=True)
        st.success("✅ Datos sincronizados correctamente.")
    else:
        st.warning("Presiona el botón superior para iniciar el análisis.")

    st.divider()
    st.caption("Módulo Tech Stack V1.5 | Protected by SecurityCore")
