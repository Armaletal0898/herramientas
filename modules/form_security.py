import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

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
                target_url = f"http://{results['target']}"
                r = requests.get(target_url, timeout=5)
                soup = BeautifulSoup(r.text, 'html.parser')
                forms = soup.find_all('form')
                
                data = []
                for f in forms:
                    inputs = f.find_all('input')
                    data.append({
                        "Acción": f.get('action', 'N/A'),
                        "Método": f.get('method', 'GET').upper(),
                        "Inputs": len(inputs),
                        "CSRF Token": "Detectado" if "csrf" in str(f).lower() else "No encontrado"
                    })
                st.session_state.form_results = data
            except Exception as e:
                st.error(f"Error de conexión: {e}")

    if st.session_state.form_results:
        st.table(pd.DataFrame(st.session_state.form_results))
