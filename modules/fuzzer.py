import streamlit as st
import requests
import time
from modules.security_core import SecurityCore

def render_fuzzer(results):
    st.subheader("🚀 Fuzzer de Directorios")
    
    if not results or 'target' not in results:
        st.info("👋 Realiza un escaneo inicial para obtener el objetivo.")
        return

    # --- LIMPIEZA DE URL (EL ARREGLO) ---
    # Eliminamos cualquier protocolo previo para evitar el error de red
    raw_target = results['target']
    clean_host = raw_target.replace("http://", "").replace("https://", "").strip("/")
    target_url = f"http://{clean_host}" 

    wordlist_default = ["admin", "login", "config", "backup", "db", "api"]
    
    col1, col2 = st.columns([2, 1])
    with col1:
        words_input = st.text_area("Wordlist", value="\n".join(wordlist_default), height=150)
        wordlist = [w.strip() for w in words_input.split("\n") if w.strip()]
    
    with col2:
        timeout_val = st.slider("Timeout", 1, 10, 3)

    if st.button("Iniciar Fuzzing", use_container_width=True):
        encontrados = []
        barra_progreso = st.progress(0)
        
        for i, path in enumerate(wordlist):
            # Aseguramos que la ruta no tenga doble slash //
            url = f"{target_url}/{path.lstrip('/')}"
            
            try:
                # Usamos verify=False por si el sitio tiene SSL roto
                res = requests.get(url, timeout=timeout_val, allow_redirects=False, verify=False)
                
                if not SecurityCore.analyze_response(url, response=res):
                    break # Detener si SecurityCore detecta bloqueo
                
                if res.status_code == 200:
                    encontrados.append({"Ruta": f"/{path}", "Status": 200})
                    st.success(f"✅ Encontrado: {url}")
                    
            except Exception as e:
                # Si falla la primera vez, SecurityCore mostrará el error que ves en tu captura
                if not SecurityCore.analyze_response(url, error=e):
                    break
            
            barra_progreso.progress((i + 1) / len(wordlist))
            time.sleep(0.1)

        if encontrados:
            st.table(encontrados)
        else:
            st.info("No se encontraron rutas abiertas.")
