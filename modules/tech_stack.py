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
                
                h_dict = {item['Cabecera']: item.get('Valor', 'N/A') for item in h if isinstance(item, dict)}
                
                # Si el auditor no pasó los valores raw, intentamos una petición rápida (HEAD)
                if not h_dict:
                    try:
                        res_head = requests.head(target_url, timeout=3)
                        # --- INTEGRACIÓN SECURITY CORE (HEAD) ---
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
                
                # 2. Análisis Activo (Fingerprinting de Error y CMS)
                try:
                    # Forzamos error 404 para ver firmas
                    test_path = f"{target_url}/error_check_{int(pd.Timestamp.now().timestamp())}"
                    r = requests.get(test_path, timeout=5, verify=False)
                    
                    # --- INTEGRACIÓN SECURITY CORE (GET 404) ---
                    # Aunque sea un 404, queremos saber si el WAF bloqueó la petición
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
                                full_cms_url = f"{target_url}{path}"
                                cms_check = requests.get(full_cms_url, timeout=3, verify=False)
                                
                                # Si el WAF bloquea un path específico (muy común), avisamos y saltamos ese path
                                if not SecurityCore.analyze_response(full_cms_url, response=cms_check):
                                    continue 
                                    
                                if cms_check.status_code == 200:
                                    techs.append({
                                        "Categoría": "CMS Detectado", 
                                        "Valor": SecurityCore.sanitize_output(name), 
                                        "Tipo": "Activo"
                                    })
                            except Exception as e:
                                SecurityCore.analyze_response(full_cms_url, error=e)
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
        st.success("✅ Datos sincronizados con el Resumen Final en Auditoría.")
    else:
        st.warning("Presiona el botón superior para iniciar el análisis del stack.")

    st.divider()
    st.caption("Módulo de Identificación de Tecnologías V1.5 | Protected by SecurityCore")
