import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from modules.security_core import SecurityCore

def render_form_security(results):
    st.subheader("🛡️ Seguridad de Formularios (XSS/CSRF)")

    if not results or 'target' not in results:
        st.info("👋 Realiza un escaneo inicial para obtener el objetivo.")
        return

    # Inicializar el estado de la sesión si no existe
    if 'form_results' not in st.session_state:
        st.session_state.form_results = None

    st.markdown("Analiza el HTML en busca de formularios, campos de entrada y la presencia de tokens CSRF.")

    # --- LÓGICA DE URL ---
    # Limpiamos el target para evitar errores de conexión
    clean_host = results['target'].replace("http://", "").replace("https://", "").strip("/")
    # Intentamos HTTPS primero por seguridad y compatibilidad
    target_url = f"https://{clean_host}"

    # Botón de rastreo
    if st.button("🔍 Rastrear Puntos de Entrada", use_container_width=True):
        with st.spinner(f"Analizando: {target_url}"):
            try:
                # Realizamos la petición con un User-Agent para evitar bloqueos básicos
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ScanWeb/1.5'}
                r = requests.get(target_url, timeout=7, headers=headers, verify=False)
                
                # Usamos el SecurityCore para verificar si la respuesta es válida (WAF, 403, etc)
                if not SecurityCore.analyze_response(target_url, response=r):
                    st.session_state.form_results = None
                    return

                soup = BeautifulSoup(r.text, 'html.parser')
                forms = soup.find_all('form')
                
                if not forms:
                    st.warning("No se encontraron formularios en la página principal.")
                    st.session_state.form_results = []
                else:
                    data = []
                    for f in forms:
                        inputs = f.find_all('input')
                        
                        # Atributos del formulario
                        raw_action = f.get('action', ' (Misma página)')
                        raw_method = f.get('method', 'GET').upper()
                        
                        # Verificación de CSRF (Busca en inputs ocultos o nombres de campo)
                        form_str = str(f).lower()
                        csrf_detected = any(x in form_str for x in ["csrf", "xsrf", "token", "authenticity_token"])
                        
                        data.append({
                            "Acción": SecurityCore.sanitize_output(raw_action),
                            "Método": SecurityCore.sanitize_output(raw_method),
                            "Campos": len(inputs),
                            "Protección CSRF": "Detectado ✅" if csrf_detected else "No encontrado ❌"
                        })
                    
                    st.session_state.form_results = data
                
            except Exception as e:
                # Si falla HTTPS, intentamos HTTP como respaldo
                if "https" in target_url:
                    st.warning("Fallo en HTTPS, reintentando por HTTP...")
                    target_url = f"http://{clean_host}"
                    # (Podrías repetir la lógica o informar al usuario)
                
                if not SecurityCore.analyze_response(target_url, error=e):
                    st.session_state.form_results = None

    # --- RENDERIZADO DE RESULTADOS ---
    if st.session_state.form_results is not None:
        if len(st.session_state.form_results) > 0:
            st.markdown("### 📋 Análisis de Formularios Detectados")
            df = pd.DataFrame(st.session_state.form_results)
            st.table(df)
            
            # Alerta de seguridad
            missing_csrf = sum(1 for item in st.session_state.form_results if "No encontrado" in item["Protección CSRF"])
            if missing_csrf > 0:
                st.error(f"⚠️ ¡Atención! Se detectaron {missing_csrf} formularios que podrían ser vulnerables a ataques CSRF.")
                st.info("💡 Consejo: Asegúrate de que cada formulario POST incluya un token único e impredecible.")
        else:
            st.info("No se detectaron formularios visibles en la URL proporcionada.")

    st.divider()
    st.caption("Módulo de Auditoría de Formularios v1.2")
