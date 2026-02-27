import streamlit as st
import pandas as pd
import plotly.express as px
import socket, requests, ssl
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# --- COLORES ---
COLOR_SAFE, COLOR_RISK, COLOR_WARN = "#475569", "#e59a94", "#f7d08a"
COLOR_TEXT_SAFE = "#cbd5e1"

class UniversalSecurityScanner:
    def __init__(self, target_url):
        url = target_url.strip()
        if not url.startswith(('http://', 'https://')):
            url = f'http://{url}'
        parsed = urlparse(url)
        self.domain = parsed.netloc if parsed.netloc else parsed.path.split('/')[0]
        self.base_url = f"{parsed.scheme}://{self.domain}"
        try: self.target_ip = socket.gethostbyname(self.domain)
        except: self.target_ip = None

    def get_subdomains(self):
        subdomains = set()
        try:
            url = f"https://crt.sh/?q=%25.{self.domain}&output=json"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                for entry in response.json():
                    name = entry['name_value'].lower()
                    for sub in name.split("\n"):
                        subdomains.add(sub.replace("*.", ""))
            return sorted(list(subdomains))
        except: return []

    def get_geo_info(self):
        if not self.target_ip: return {"País": "N/A", "Ciudad": "N/A", "ISP": "N/A"}
        try:
            response = requests.get(f"http://ip-api.com/json/{self.target_ip}", timeout=5).json()
            return {"País": response.get("country", "N/A"), "Ciudad": response.get("city", "N/A"), "ISP": response.get("isp", "N/A")}
        except: return {"País": "Error", "Ciudad": "Error", "ISP": "Error"}

    def scan_ssl_pro(self):
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.domain, 443), timeout=3) as sock:
                with context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                    cert = ssock.getpeercert()
                    issuer = dict(x[0] for x in cert.get('issuer'))['commonName']
                    expiry = cert.get('notAfter')
                    return {"Estado": "✅ Seguro", "Emisor": issuer, "Expiración": expiry, "TLS": ssock.version()}
        except: return {"Estado": "❌ No disponible", "Emisor": "N/A", "Expiración": "N/A", "TLS": "N/A"}

    def scan_ports(self):
        results = []
        for port, serv in {21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS", 3306: "MySQL"}.items():
            if not self.target_ip: break
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.3)
                if s.connect_ex((self.target_ip, port)) == 0:
                    results.append({"Puerto": port, "Servicio": serv, "Estado": "Abierto 🔘"})
        return results

    def scan_sqli_pro(self):
        vuls = []
        try:
            r = requests.get(self.base_url, timeout=5)
            soup = BeautifulSoup(r.text, 'html.parser')
            forms = soup.find_all('form')
            for form in forms:
                action = form.get('action') or "Interno"
                method = form.get('method') or "GET"
                vuls.append({"Formulario": action, "Método": method.upper(), "Tipo": "SQLi/XSS Risk", "Severidad": "Crítica"})
            return vuls
        except: return []

    def audit_web_advanced(self):
        h_res, c_res = [], []
        critical_headers = {
            "Content-Security-Policy": "Protección XSS",
            "Strict-Transport-Security": "HSTS Seguridad",
            "X-Frame-Options": "Clickjacking",
            "X-Content-Type-Options": "Sniffing",
            "Referrer-Policy": "Privacidad Ref",
            "Permissions-Policy": "Control API"
        }
        try:
            res = requests.get(self.base_url, timeout=5)
            for h, desc in critical_headers.items():
                status = "✅ OK" if h in res.headers else "❌ Ausente"
                h_res.append({"Cabecera": h, "Estado": status, "Función": desc})
            for cookie in res.cookies:
                c_res.append({"Nombre": cookie.name, "Seguro": "✅" if cookie.secure else "❌ Insegura"})
            return h_res, c_res
        except: return [], []

def render_auditoria(results):
    if not results:
        st.info("👋 Inicia un escaneo desde el panel lateral.")
        return

    r = results
    
    # 1. MÉTRICAS RÁPIDAS
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f'<div class="metric-card"><div class="metric-label">Riesgos SQLi</div><div class="metric-value">{len(r["sqli"])}</div></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="metric-card"><div class="metric-label">Puertos Abiertos</div><div class="metric-value">{len(r["ports"])}</div></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="metric-card"><div class="metric-label">Dirección IP</div><div class="metric-value" style="font-size:18px">{r["ip"]}</div></div>', unsafe_allow_html=True)
    m4.markdown(f'<div class="metric-card"><div class="metric-label">País</div><div class="metric-value" style="font-size:18px">{r["geo"]["País"]}</div></div>', unsafe_allow_html=True)

    st.divider()

    # 2. RESUMEN VISUAL (PASTEL + INFO BOX)
    col_main_1, col_main_2 = st.columns([1, 1])
    with col_main_1:
        missing_h = sum(1 for h in r["headers"] if "❌" in h['Estado'])
        risk_count = len(r["sqli"]) + len(r["ports"]) + missing_h
        fig_p = px.pie(values=[max(1, 20-risk_count), risk_count], names=['Puntos Seguros', 'Riesgos'], hole=.7,
                      color_discrete_sequence=[COLOR_SAFE, COLOR_RISK])
        fig_p.update_layout(showlegend=True, paper_bgcolor='rgba(0,0,0,0)', height=300, 
                            margin=dict(t=0, b=0, l=0, r=0), font=dict(color=COLOR_TEXT_SAFE))
        st.plotly_chart(fig_p, use_container_width=True)

    with col_main_2:
        st.markdown(f"""
        <div class="info-box">
            <h4>🌐 Infraestructura de Red</h4>
            <p><b>📍 Ubicación:</b> {r["geo"]["Ciudad"]}, {r["geo"]["País"]}</p>
            <p><b>🖥️ Dirección IP:</b> {r["ip"]}</p>
            <p><b>🏢 Proveedor (ISP):</b> {r["geo"]["ISP"]}</p>
            <hr style="border-color: #334155;">
            <h4>🔐 Certificación de Seguridad</h4>
            <p><b>Estado SSL:</b> {r["ssl"]["Estado"]}</p>
            <p><b>Expiración:</b> {r["ssl"]["Expiración"]}</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # 3. PESTAÑAS TÉCNICAS
    t1, t2, t3 = st.tabs(["📊 Score & Cabeceras", "📡 Puertos & Servicios", "📋 Resumen Consolidado"])
    
    with t1:
        st.subheader("📊 Análisis Detallado de Seguridad")
        sec_df = pd.DataFrame({
            "Categoría": ["SQLi", "Cabeceras", "Cookies", "Puertos", "SSL"], 
            "Score": [
                100 if not r["sqli"] else 20, 
                max(0, 100-(missing_h*16)), 
                80 if r["cookies"] else 100, 
                max(0, 100-(len(r["ports"])*15)), 
                100 if "✅" in r["ssl"]["Estado"] else 0
            ]
        })
        fig_b = px.bar(sec_df, x="Score", y="Categoría", orientation='h', range_x=[0,100], color="Score", 
                      color_continuous_scale=[COLOR_RISK, COLOR_WARN, COLOR_SAFE], text_auto=True)
        fig_b.update_layout(showlegend=False, coloraxis_showscale=False, paper_bgcolor='rgba(0,0,0,0)', height=300, font=dict(color=COLOR_TEXT_SAFE))
        st.plotly_chart(fig_b, use_container_width=True)

        st.divider()
        col_a, col_b = st.columns(2)
        with col_a:
            st.write("**🛡️ Auditoría de Cabeceras**")
            st.dataframe(pd.DataFrame(r["headers"]), use_container_width=True, hide_index=True)
            st.write("**🔐 Detalle Técnico SSL**")
            st.json(r["ssl"])
        with col_b:
            st.write("**💉 Vulnerabilidades SQL**")
            if r["sqli"]: st.dataframe(pd.DataFrame(r["sqli"]), use_container_width=True, hide_index=True)
            else: st.success("No se detectaron formularios vulnerables.")
            st.write("**🍪 Cookies**")
            if r["cookies"]: st.dataframe(pd.DataFrame(r["cookies"]), use_container_width=True, hide_index=True)
            else: st.info("No se detectaron cookies.")

    with t2:
        st.write("#### Puertos y Servicios de Red")
        if r["ports"]: st.dataframe(pd.DataFrame(r["ports"]), use_container_width=True, hide_index=True)
        else: st.success("No se encontraron puertos críticos abiertos.")

    with t3:
        st.subheader("📋 Consolidado de Seguridad")
        st.write("Resultados integrados de todos los módulos activos.")
        
        summary_list = []

        # A. HALLAZGOS AUDITORÍA BASE
        if r["sqli"]:
            summary_list.append({"Módulo": "Auditoría", "Hallazgo": "Posible Inyección SQL/XSS", "Severidad": "Crítica", "Impacto": "Acceso a Datos"})
        if "❌" in r["ssl"]["Estado"]:
            summary_list.append({"Módulo": "Auditoría", "Hallazgo": "Falta cifrado SSL", "Severidad": "Alta", "Impacto": "Man-in-the-Middle"})
        
        # B. HALLAZGOS TECH STACK
        if 'tech_results' in st.session_state and st.session_state.tech_results:
            for t in st.session_state.tech_results:
                summary_list.append({"Módulo": "Tech Stack", "Hallazgo": f"Software: {t.get('Valor')}", "Severidad": "Baja", "Impacto": "Enumeración"})

        # C. HALLAZGOS FORMULARIOS
        if 'form_results' in st.session_state and st.session_state.form_results:
            for f in st.session_state.form_results:
                if f.get("CSRF Token") == "No encontrado":
                    summary_list.append({"Módulo": "Formularios", "Hallazgo": f"Falta CSRF en {f.get('Acción')}", "Severidad": "Media", "Impacto": "Ataque CSRF"})

        # D. HALLAZGOS FUZZER
        if 'fuzzer_data' in st.session_state and st.session_state.fuzzer_data:
            for entry in st.session_state.fuzzer_data:
                summary_list.append({"Módulo": "Fuzzer", "Hallazgo": f"Ruta: {entry['Ruta']}", "Severidad": entry.get('Riesgo', 'Media'), "Impacto": "Acceso Directo"})

        if summary_list:
            df_sum = pd.DataFrame(summary_list)
            
            def style_severity(val):
                if val == 'Crítica': color = COLOR_RISK
                elif val == 'Alta': color = '#fca5a5'
                elif val == 'Media': color = COLOR_WARN
                else: color = COLOR_SAFE
                return f'color: {color}; font-weight: bold'

            st.dataframe(df_sum.style.applymap(style_severity, subset=['Severidad']), use_container_width=True, hide_index=True)
        else:
            st.info("⚠️ No hay hallazgos adicionales. Ejecuta los módulos individuales para ver resultados aquí.")

    st.divider()
    st.caption(f"Security Analyst Report - Target: {r['target']}")
