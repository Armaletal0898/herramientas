import requests
import streamlit as st

def fuzzer_module(url_base, wordlist):
    st.subheader("🚀 Ejecutando Fuzzer de Directorios")
    encontrados = []
    
    # Usamos una barra de progreso de Streamlit
    progress_bar = st.progress(0)
    
    for i, path in enumerate(wordlist):
        url = f"{url_base}/{path}".replace("//", "/")
        try:
            # Realizar la petición
            res = requests.get(url, timeout=5, allow_redirects=False)
            
            # --- INTEGRACIÓN DE SECURITY CORE ---
            if not SecurityCore.analyze_response(url, response=res):
                st.error(f"🛑 Fuzzer detenido en '{path}' debido a un bloqueo de seguridad.")
                break # Salimos del bucle si detectamos un WAF o bloqueo 403
            # ------------------------------------

            if res.status_code == 200:
                encontrados.append(path)
                st.success(f"📂 Directorio encontrado: /{path}")
            
        except Exception as e:
            # --- INTEGRACIÓN DE SECURITY CORE ---
            SecurityCore.analyze_response(url, error=e)
            # ------------------------------------
            break # Si el servidor deja de responder, no seguimos intentando
        
        # Actualizar barra de progreso
        progress_bar.progress((i + 1) / len(wordlist))

    if not encontrados:
        st.info("ℹ️ No se encontraron directorios abiertos. Es posible que el servidor use un WAF silencioso o no existan estas rutas.")
