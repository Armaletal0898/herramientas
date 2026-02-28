import streamlit as st
import requests
import time
from modules.security_core import SecurityCore

def render_fuzzer(results):
    """Módulo de Fuzzing de Directorios con Protección de SecurityCore"""
    
    st.subheader("🚀 Fuzzer de Directorios")
    
    if not results or 'target' not in results:
        st.info("👋 Por favor, realiza un escaneo inicial en el panel lateral para obtener el objetivo.")
        return

    st.markdown("""
        Este módulo busca directorios y archivos ocultos utilizando una **Wordlist**. 
        Si el servidor detecta demasiadas peticiones, el escudo de seguridad detendrá el proceso.
    """)

    # Configuración del Fuzzer
    target = SecurityCore.sanitize_output(results['target'])
    target_url = f"http://{target}"
    
    # Lista de palabras común para fuzzeo rápido (puedes ampliarla)
    wordlist_default = ["admin", "login", "config", "backup", "db", "uploads", "api", "v1", "test", "dev"]
    
    col1, col2 = st.columns([2, 1])
    with col1:
        words_input = st.text_area("Wordlist (una palabra por línea)", value="\n".join(wordlist_default), height=150)
        wordlist = [w.strip() for w in words_input.split("\n") if w.strip()]
    
    with col2:
        timeout_val = st.slider("Timeout (segundos)", 1, 10, 3)
        allow_redirects = st.checkbox("Seguir redirecciones", value=False)

    if st.button("Iniciar Fuzzing", use_container_width=True):
        encontrados = []
        barra_progreso = st.progress(0)
        status_text = st.empty()
        
        with st.spinner("Escaneando rutas..."):
            for i, path in enumerate(wordlist):
                # Construir URL limpia
                url = f"{target_url}/{path}".replace("//", "/")
                status_text.text(f"Probando: /{path}")
                
                try:
                    # Petición con el timeout configurado
                    res = requests.get(url, timeout=timeout_val, allow_redirects=allow_redirects, verify=False)
                    
                    # --- INTEGRACIÓN CON EL ESCUDO DE SEGURIDAD ---
                    # Si analyze_response detecta un WAF o bloqueo (403, 429), detendrá el fuzzer
                    if not SecurityCore.analyze_response(url, response=res):
                        st.error(f"🛑 Fuzzer abortado en la ruta '/{path}' para proteger tu IP de un baneo permanente.")
                        SecurityCore.log_activity(target, "FUZZER_STOPPED", f"Bloqueo en /{path}")
                        break 
                    
                    # Si el código es 200, encontramos algo
                    if res.status_code == 200:
                        encontrados.append({
                            "Ruta": f"/{path}",
                            "Status": res.status_code,
                            "Tamaño": f"{len(res.content)} bytes"
                        })
                        st.success(f"✅ ¡Encontrado! {url} [200 OK]")
                    
                except Exception as e:
                    # Analizar si es un error de red o timeout
                    if not SecurityCore.analyze_response(url, error=e):
                        st.error("❌ Error de red crítico. Deteniendo fuzzer.")
                        break
                
                # Actualizar barra de progreso
                barra_progreso.progress((i + 1) / len(wordlist))
                time.sleep(0.1) # Pequeño delay para no saturar el servidor demasiado rápido

        status_text.empty()
        
        # Mostrar resumen final
        if encontrados:
            st.divider()
            st.write("### 📂 Resultados del Fuzzing")
            st.table(encontrados)
            st.success(f"Escaneo finalizado. Se encontraron {len(encontrados)} rutas.")
        else:
            st.info("ℹ️ No se encontraron rutas abiertas. El servidor podría estar devolviendo 404 para todo o estar bien protegido.")

    st.divider()
    st.caption("Módulo Fuzzer V2.0 | Conectado a SecurityCore Engine")
