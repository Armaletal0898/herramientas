import streamlit as st
import time
from modules.security_core import SecurityCore  # Importación del escudo de seguridad

def render_fuzzer(results):
    st.subheader("📂 Fuzzer de Directorios")

    if not results:
        st.info("👋 Realiza un escaneo inicial primero.")
        return

    if 'fuzzer_data' not in st.session_state:
        st.session_state.fuzzer_data = None

    st.write("Prueba rutas comunes para encontrar archivos ocultos o paneles de administración.")

    # Botón de ejecución crítica
    if st.button("🧨 Lanzar Diccionario Crítico", type="primary", use_container_width=True):
        progress_bar = st.progress(0)
        status_text = st.empty()
        found = []
        
        # Sanitizamos la URL base por seguridad antes de concatenar
        target_base = SecurityCore.sanitize_output(results['target'])
        
        # Diccionario de rutas críticas
        rutas = ["/admin", "/backup", "/.env", "/config", "/wp-admin", "/login", "/api/v1", "/.git"]
        
        for i, ruta in enumerate(rutas):
            # Sanitizamos la ruta antes de mostrarla en el estado
            safe_ruta = SecurityCore.sanitize_output(ruta)
            status_text.text(f"Probando: {safe_ruta}...")
            
            # --- Lógica de Seguridad ---
            # Aquí iría tu: requests.get(f"http://{target_base}{ruta}", timeout=3)
            # ---------------------------
            
            time.sleep(0.3) # Simulación de delay de red
            progress_bar.progress((i + 1) / len(rutas))
            
            # Simulación de hallazgos (Sanitizados)
            if i % 2 == 0: 
                found.append({
                    "Ruta": safe_ruta, 
                    "Estado": "200 OK", 
                    "Riesgo": "Crítico"
                })
        
        # Guardamos los resultados sanitizados en la sesión
        st.session_state.fuzzer_data = found
        status_text.text("Fuzzing completado.")

    # Renderizado de resultados encontrados
    if st.session_state.fuzzer_data:
        st.write("### 🚨 Hallazgos Detectados")
        # Mostramos los resultados en formato JSON (ya sanitizados previamente)
        st.json(st.session_state.fuzzer_data)
        
        # También podemos mostrarlo en una tabla más visual
        import pandas as pd
        df_fuzz = pd.DataFrame(st.session_state.fuzzer_data)
        st.dataframe(df_fuzz, use_container_width=True, hide_index=True)
