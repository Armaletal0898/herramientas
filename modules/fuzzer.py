import streamlit as st
import requests
import time
from modules.security_core import SecurityCore

def render_fuzzer(results):
    st.subheader("🚀 Fuzzer Automatizado de Directorios")
    
    if not results or 'target' not in results:
        st.info("👋 Realiza un escaneo inicial para obtener el objetivo.")
        return

    # --- PERSISTENCIA DE RESULTADOS ---
    # Inicializamos la llave en session_state para que no se borre al cambiar de pestaña
    if 'fuzzer_results' not in st.session_state:
        st.session_state.fuzzer_results = None

    # --- LÓGICA DE URL ROBUSTA ---
    raw_target = results['target']
    clean_host = raw_target.replace("http://", "").replace("https://", "").strip("/")
    target_url = f"https://{clean_host}" 

    # --- WORDLIST AUTOMATIZADA ---
    default_wordlist_text = """admin
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
public"""

    st.markdown(f"**Objetivo actual:** `{target_url}`")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        words_input = st.text_area("Rutas a escanear:", value=default_wordlist_text.strip(), height=200)
        wordlist = [
            w.strip() for w in words_input.split("\n") 
            if w.strip() and not w.strip().startswith("#")
        ]
    
    with col2:
        timeout_val = st.slider("Sensibilidad (Timeout)", 1, 15, 7)
        delay_val = st.slider("Retraso entre peticiones (s)", 0.0, 2.0, 0.2)
        
        # Botón para limpiar resultados manualmente
        if st.session_state.fuzzer_results:
            if st.button("🗑️ Limpiar Resultados", use_container_width=True):
                st.session_state.fuzzer_results = None
                st.rerun()

    if st.button("🚀 Iniciar Escaneo Automático", use_container_width=True):
        encontrados = []
        barra_progreso = st.progress(0)
        status_text = st.empty()
        resultados_container = st.container()

        for i, path in enumerate(wordlist):
            url = f"{target_url}/{path.lstrip('/')}"
            status_text.text(f"🔍 Probando: /{path}")
            
            try:
                # Petición controlada
                res = requests.get(url, timeout=timeout_val, allow_redirects=False, verify=False)
                
                if not SecurityCore.analyze_response(url, response=res):
                    st.error(f"🛑 Escaneo detenido preventivamente en `/{path}`.")
                    break
                
                if res.status_code == 200:
                    item = {
                        "Ruta": f"/{path}", 
                        "Código": 200, 
                        "Tamaño": f"{len(res.content)} bytes",
                        "Riesgo": "Alto" if "admin" in path or "config" in path else "Medio"
                    }
                    encontrados.append(item)
                    with resultados_container:
                        st.success(f"📂 **Encontrado:** {url} (200 OK)")
                
                elif res.status_code in [301, 302]:
                    with resultados_container:
                        st.warning(f"↪️ **Redirección:** /{path} (HTTP {res.status_code})")

            except requests.exceptions.Timeout:
                st.error(f"⏳ Timeout en `/{path}`. Ajustando...")
                time.sleep(1)
            except Exception as e:
                if not SecurityCore.analyze_response(url, error=e):
                    break
            
            barra_progreso.progress((i + 1) / len(wordlist))
            time.sleep(delay_val)

        status_text.empty()
        
        # GUARDAR EN SESSION STATE para que persista
        st.session_state.fuzzer_results = encontrados if encontrados else []
        st.rerun() # Refrescamos para mostrar la tabla final

    # --- RENDERIZADO DE RESULTADOS PERSISTENTES ---
    if st.session_state.fuzzer_results is not None:
        st.divider()
        if st.session_state.fuzzer_results:
            st.write("### 📜 Resumen de Hallazgos (Persistente)")
            st.dataframe(st.session_state.fuzzer_results, use_container_width=True, hide_index=True)
            
            # Botón de descarga rápido
            df_export = pd.DataFrame(st.session_state.fuzzer_results)
            st.download_button(
                "📥 Exportar CSV",
                df_export.to_csv(index=False).encode('utf-8'),
                "fuzzer_report.csv",
                "text/csv",
                use_container_width=True
            )
        else:
            st.info("🏁 Escaneo finalizado. No se encontraron rutas públicas.")

    st.divider()
    st.caption("Fuzzer Engine v2.5 | Persistencia de datos activada")
