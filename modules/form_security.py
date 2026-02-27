import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from modules.security_core import SecurityCore  # Importación del escudo de seguridad

def render_form_security(results):
    st.subheader("🛡️ Seguridad de Formularios (XSS/CSRF)")

    if not results:
        st.info("👋 Esperando datos del objetivo...")
        return

    if 'form_results' not in st.session_state:
        st.session_state.form_results = None

    st.markdown("Busca campos de entrada vulnerables y falta de tokens de seguridad en el código fuente.")

    # Botón de ataque (estilo advertencia)
    if st.button("🔍 Rastrear Puntos de Entrada", type="secondary", use_container_width=True):
        with st.spinner("Analizando HTML del objetivo..."):
            try:
                # Sanitizamos el target antes de construir la URL de petición
                safe_target = SecurityCore.sanitize_output(results['target'])
                target_url = f"http://{safe_target}"
                
                r = requests.get(target_url, timeout=5)
                soup = BeautifulSoup(r.text, 'html.parser')
                forms = soup.find_all('form')
                
                data = []
                for f in forms:
                    inputs = f.find_all('input')
                    
                    # SANITIZACIÓN DE ATRIBUTOS EXTRAÍDOS
                    # Limpiamos 'action' y 'method' porque vienen directamente del HTML externo
                    raw_action = f.get('action', 'N/A')
                    raw_method = f.get('method', 'GET').upper()
                    
                    safe_action = SecurityCore.sanitize_output(raw_action)
                    safe_method = SecurityCore.sanitize_output(raw_method)
                    
                    data.append({
                        "Acción": safe_action,
                        "Método": safe_method,
                        "Inputs": len(inputs),
                        "CSRF Token": "Detectado ✅" if "csrf" in str(f).lower() else "No encontrado ❌"
                    })
                
                st.session_state.form_results = data
                
            except Exception as e:
                # Sanitizamos el mensaje de error por si contiene fragmentos de la URL maliciosa
                safe_error = SecurityCore.sanitize_output(str(e))
                st.error(f"Error de conexión: {safe_error}")

    # Renderizado de resultados
    if st.session_state.form_results:
        st.markdown("### 📋 Análisis de Formularios Detectados")
        # Los datos ya están limpios en el session_state
        st.table(pd.DataFrame(st.session_state.form_results))
        
        # Añadimos una advertencia si hay falta de CSRF
        missing_csrf = sum(1 for item in st.session_state.form_results if "No encontrado" in item["CSRF Token"])
        if missing_csrf > 0:
            st.warning(f"⚠️ Se detectaron {missing_csrf} formularios sin protección CSRF aparente.")
