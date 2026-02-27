import streamlit as st
import requests
import pandas as pd

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
        # Botón con estilo de acción (usa el color primario de tu tema)
        if st.button("🚀 Identificar Stack", use_container_width=True):
            with st.spinner("Ejecutando Fingerprinting..."):
                techs = []
                target_url = f"http://{results['target']}"
                
                # 1. Análisis de cabeceras (Pasivo pero detallado)
                h = results.get("headers", {})
                # Mapeo de cabeceras comunes a categorías
                check_map = {
                    'Server': 'Servidor Web',
                    'X-Powered-By': 'Lenguaje/Framework',
                    'Via': 'Proxy/CDN',
                    'X-AspNet-Version': 'Framework .NET'
                }
                
                for header, categoria in check_map.items():
                    if header in h:
                        # IMPORTANTE: Usamos la clave "Valor" para el resumen final
                        techs.append({
                            "Categoría": categoria, 
                            "Valor": h[header], 
                            "Tipo": "Pasivo"
                        })
                
                # 2. Análisis Activo (Provocando un error 404 para ver firmas)
                try:
                    # Intentamos forzar una página inexistente
                    test_path = f"{target_url}/error_check_{int(pd.Timestamp.now().timestamp())}"
                    r = requests.get(test_path, timeout=3, verify=False)
                    
                    # Revisamos si el cuerpo del error revela el servidor (ej: nginx/1.18.0)
                    server_raw = r.headers.get('Server', '').lower()
                    if server_raw:
                        techs.append({
                            "Categoría": "Servidor (Firma)", 
                            "Valor": server_raw.capitalize(), 
                            "Tipo": "Activo"
                        })
                    
                    # Detección básica de CMS por rutas comunes
                    cms_paths = {
                        "/wp-includes/": "WordPress",
                        "/administrator/": "Joomla",
                        "/user/login": "Drupal"
                    }
                    for path, name in cms_paths.items():
                        cms_check = requests.get(f"{target_url}{path}", timeout=2, verify=False)
                        if cms_check.status_code == 200:
                            techs.append({
                                "Categoría": "CMS Detectado", 
                                "Valor": name, 
                                "Tipo": "Activo"
                            })
                            
                except Exception as e:
                    st.error(f"Error en fingerprinting activo: {e}")
                
                # Guardar resultados en el estado de la sesión
                st.session_state.tech_results = techs

    # --- RENDERIZADO DE RESULTADOS ---
    if st.session_state.tech_results:
        st.divider()
        st.write("### Tecnologías Identificadas")
        
        # Convertimos a DataFrame para una visualización limpia
        df_tech = pd.DataFrame(st.session_state.tech_results)
        
        # Mostramos la tabla con tu estilo
        st.dataframe(
            df_tech, 
            use_container_width=True, 
            hide_index=True
        )
        
        st.success("✅ Datos sincronizados con el Resumen Final en Auditoría.")
    else:
        st.warning("Presiona el botón superior para iniciar el análisis del stack.")

    st.divider()
    st.caption("Módulo de Identificación de Tecnologías V1.5")
