import streamlit as st
import requests
import time
from modules.security_core import SecurityCore

def render_fuzzer(results):
    st.subheader("🚀 Fuzzer Automatizado de Directorios")
    
    if not results or 'target' not in results:
        st.info("👋 Realiza un escaneo inicial para obtener el objetivo.")
        return

    # --- LÓGICA DE URL ROBUSTA ---
    # Limpiamos el target para evitar el error de "Max retries / Connection Timeout"
    raw_target = results['target']
    clean_host = raw_target.replace("http://", "").replace("https://", "").strip("/")
    # Intentamos HTTPS por defecto para mayor compatibilidad
    target_url = f"https://{clean_host}" 

    # --- WORDLIST AUTOMATIZADA ---
    default_wordlist_text = """
    admin
    administrator
    admin_panel
    panel
    login
    wp-login.php
    wp-admin
    config
    config.php
    .env
    .git
    backup
    db
    database
    sql
    api
    v1
    test
    dev
    uploads
    files
    robots.txt
    sitemap.xml
    public
    """

    st.markdown(f"**Objetivo actual:** `{target_url}`")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        # El área de texto ya viene precargada con tu lista profesional
        words_input = st.text_area("Rutas a escanear:", value=default_wordlist_text.strip(), height=200)
        # Procesamos la lista: quitamos espacios, líneas vacías y comentarios
        wordlist = [
            w.strip() for w in words_input.split("\n") 
            if w.strip() and not w.strip().startswith("#")
        ]
    
    with col2:
        timeout_val = st.slider("Sensibilidad (Timeout)", 1, 15, 7)
        delay_val = st.slider("Retraso entre peticiones (s)", 0.0, 2.0, 0.2)

    if st.button("🚀 Iniciar Escaneo Automático", use_container_width=True):
        encontrados = []
        barra_progreso = st.progress(0)
        status_text = st.empty()
        
        # Contenedor para resultados en tiempo real
        resultados_container = st.container()

        for i, path in enumerate(wordlist):
            # Construcción limpia de la ruta
            url = f"{target_url}/{path.lstrip('/')}"
            status_text.text(f"🔍 Probando: /{path}")
            
            try:
                # Petición con verify=False para evitar errores de certificados SSL
                res = requests.get(url, timeout=timeout_val, allow_redirects=False, verify=False)
                
                # --- FILTRO DE SEGURIDAD ---
                if not SecurityCore.analyze_response(url, response=res):
                    st.error(f"🛑 Escaneo detenido preventivamente en `/{path}`.")
                    break
                
                # Detección de éxito
                if res.status_code == 200:
                    item = {"Ruta": f"/{path}", "Código": 200, "Tamaño": f"{len(res.content)} bytes"}
                    encontrados.append(item)
                    with resultados_container:
                        st.success(f"📂 **Encontrado:** {url} (200 OK)")
                
                elif res.status_code == 301 or res.status_code == 302:
                    with resultados_container:
                        st.warning(f"↪️ **Redirección:** /{path} -> {res.headers.get('Location', '')}")

            except requests.exceptions.Timeout:
                st.error(f"⏳ El servidor no respondió a tiempo en `/{path}`. Bajando velocidad...")
                time.sleep(2) # Pausa extra si hay timeout
            except Exception as e:
                if not SecurityCore.analyze_response(url, error=e):
                    break
            
            # Actualizar progreso
            barra_progreso.progress((i + 1) / len(wordlist))
            # Delay para evitar detección del WAF
            time.sleep(delay_val)

        status_text.empty()
        
        if encontrados:
            st.divider()
            st.write("### 📜 Resumen de Hallazgos")
            st.dataframe(encontrados, use_container_width=True, hide_index=True)
            SecurityCore.log_activity(target_url, "FIN_FUZZER", f"Encontrados: {len(encontrados)}")
        else:
            st.info("🏁 Escaneo finalizado sin hallazgos públicos.")

    st.divider()
    st.caption("Fuzzer Engine v2.5 | Wordlist Pro Integrada")
