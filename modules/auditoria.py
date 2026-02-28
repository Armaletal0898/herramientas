import streamlit as st
import pandas as pd
import plotly.express as px
import socket, requests, ssl
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from modules.security_core import SecurityCore

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
        try: 
            self.target_ip = socket.gethostbyname(self.domain)
        except: 
            self.target_ip = None

    def get_subdomains(self):
        subdomains = set()
        try:
            url = f"https://crt.sh/?q=%25.{self.domain}&output=json"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                for entry in response.json():
                    name = SecurityCore.sanitize_output(entry['name_value'].lower())
                    for sub in name.split("\n"):
                        subdomains.add(sub.replace("*.", ""))
            return sorted(list(subdomains))
        except: return []

    def get_geo_info(self):
        if not self.target_ip: return {"País": "N/A", "Ciudad": "N/A", "ISP": "N/A"}
        try:
            response = requests.get(f"http://ip-api.com/json/{self.target_ip}", timeout=5).json()
            return {
                "País": SecurityCore.sanitize_output(response.get("country", "N/A")), 
                "Ciudad": SecurityCore.sanitize_output(response.get("city", "N/A")), 
                "ISP": SecurityCore.sanitize_output(response.get("isp", "N/A"))
            }
        except: return {"País": "Error", "Ciudad": "Error", "ISP": "Error"}

    def scan_ssl_pro(self):
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.domain, 443), timeout=3) as sock:
                with context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                    cert = ssock.getpeercert()
                    issuer = dict(x[0] for x in cert.get('issuer'))['commonName']
                    expiry = cert.get('notAfter')
                    return {
                        "Estado": "✅ Seguro", 
                        "Emisor": SecurityCore.sanitize_output(issuer), 
                        "Expiración": SecurityCore.sanitize_output(expiry), 
                        "TLS": SecurityCore.sanitize_output(ssock.version())
                    }
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
                action = SecurityCore.sanitize_output(form.get('action') or "Interno")
                method = SecurityCore.sanitize_output(form.get('method') or "GET")
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
            "Referrer-Policy": "Privacidad Ref"
        }
        try:
            res = requests.get(self.base_url, timeout=5)
            for h, desc in critical_headers.items():
                status = "✅ OK" if h in res.headers else "❌ Ausente"
                h_res.append({"Cabecera": h, "Estado": status, "Función": desc})
            for cookie in res.cookies:
                c_res.append({
                    "Nombre": SecurityCore.sanitize_output(cookie.name), 
                    "Seguro": "✅" if cookie.secure else "❌ Insegura"
                })
            return h_res, c_res
        except: return [], []

def render_auditoria(results):
    if not results:
        st.info("👋 Inicia un escaneo desde el panel lateral.")
        return

    r = results
    target_clean = SecurityCore.sanitize_output(r["target"])
    
    # 1. MÉTRICAS
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Riesgos SQLi", len(r["sqli"]))
    m2.metric("Puertos Abiertos", len(r["ports"]))
    m3.metric("IP", r["ip"])
    m4.metric("País", r["geo"]["País"])

    st.divider()

    # 2. RESUMEN VISUAL
    col1, col2 = st.columns([1, 1])
    with col1:
        missing_h = sum(1 for h in r["headers"] if "❌" in h['Estado'])
        fig_p = px.pie(values=[max(1, 20-missing_h), missing_h], names=['Seguro', 'Riesgos'], hole=.7,
                      color_discrete_sequence=[COLOR_SAFE, COLOR_RISK])
        fig_p.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', height=250)
        st.plotly_chart(fig_p, use_container_width=True)

    with col2:
        st.markdown(f"""
        <div style="background: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #334155;">
            <h4 style="margin:0">🔐 SSL & Red</h4>
            <p style="margin:5px 0"><b>Estado:</b> {r["ssl"]["Estado"]}</p>
            <p style="margin:5px 0"><b>ISP:</b> {r["geo"]["ISP"]}</p>
            <p style="margin:5px 0"><b>TLS:</b> {r["ssl"]["TLS"]}</p>
        </div>
        """, unsafe_allow_html=True)

    # 3. PESTAÑAS
    t1, t2, t3 = st.tabs(["📊 Score", "📡 Red", "📋 Resumen Consolidado"])
    
    with t1:
        st.dataframe(pd.DataFrame(r["headers"]), use_container_width=True, hide_index=True)
        st.write("**Vulnerabilidades detectadas:**")
        st.dataframe(pd.DataFrame(r["sqli"]), use_container_width=True)

    with t2:
        st.write("#### Puertos Detectados")
        st.table(pd.DataFrame(r["ports"]))

    with t3:
        st.subheader("📋 Consolidado de Hallazgos Globales")
        summary_list = []

        # --- Hallazgos de Auditoría (Siempre presentes) ---
        if r["sqli"]:
            summary_list.append({"Módulo": "Auditoría", "Hallazgo": "Posible SQLi/XSS en formularios", "Severidad": "Crítica"})
        if "❌" in r["ssl"]["Estado"]:
            summary_list.append({"Módulo": "Auditoría", "Hallazgo": "Falta cifrado SSL (HTTPS)", "Severidad": "Alta"})
        
        # --- Hallazgos de Stack Tecnológico ---
        tech_data = st.session_state.get('tech_results')
        if tech_data:
            for t in tech_data:
                summary_list.append({"Módulo": "Tech Stack", "Hallazgo": f"Detectado: {t.get('Valor')}", "Severidad": "Baja"})

        # --- Hallazgos de Seguridad de Formularios ---
        form_data = st.session_state.get('form_results')
        if form_data:
            for f in form_data:
                # Corregido: Buscamos en "Protección CSRF"
                if "No encontrado" in f.get("Protección CSRF", ""):
                    summary_list.append({"Módulo": "Formularios", "Hallazgo": f"Sin CSRF en {f.get('Acción')}", "Severidad": "Media"})

        # --- Hallazgos del Fuzzer ---
        fuzz_data = st.session_state.get('fuzzer_results')
        if fuzz_data:
            for entry in fuzz_data:
                summary_list.append({"Módulo": "Fuzzer", "Hallazgo": f"Directorio expuesto: {entry['Ruta']}", "Severidad": "Media"})

        if summary_list:
            df_sum = pd.DataFrame(summary_list)
            
            def style_severity(val):
                colors = {'Crítica': '#ef4444', 'Alta': '#f87171', 'Media': '#fbbf24', 'Baja': '#60a5fa'}
                return f'color: {colors.get(val, "white")}; font-weight: bold'

            st.dataframe(df_sum.style.applymap(style_severity, subset=['Severidad']), use_container_width=True, hide_index=True)
        else:
            st.info("🔎 No hay hallazgos adicionales. Navega a los otros módulos para profundizar el análisis.")

    st.caption(f"Security Report - {target_clean}")
