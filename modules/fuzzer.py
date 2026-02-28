import re
import socket
from urllib.parse import urlparse
import streamlit as st
from datetime import datetime

class SecurityCore:
    @staticmethod
    def log_activity(target, status, details=""):
        """Registra la actividad en un archivo local para auditoría interna"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] STATUS: {status} | TARGET: {target} | INFO: {details}\n"
        
        try:
            with open("audit_log.txt", "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Error crítico al escribir log: {e}")

    @staticmethod
    def validate_target(target):
        """Valida que el target no contenga caracteres maliciosos"""
        if not target:
            return False
        
        pattern = r'^[a-zA-Z0-9\-\.\/:]+$'
        if not re.match(pattern, str(target)):
            st.error("⚠️ Caracteres no permitidos detectados.")
            SecurityCore.log_activity(target, "BLOQUEADO", "Intento de Inyección de Caracteres")
            return False
        return True

    @staticmethod
    def prevent_ssrf(target):
        """Previene ataques de Server Side Request Forgery (SSRF)"""
        try:
            clean_url = str(target).replace('http://', '').replace('https://', '').split('/')[0]
            parsed = urlparse(f"http://{clean_url}")
            host = parsed.netloc
            
            ip = socket.gethostbyname(host)
            
            private_ranges = ["127.", "0.0.0.0", "localhost", "10.", "172.16.", "172.17.", 
                              "172.18.", "172.19.", "172.20.", "172.21.", "172.22.", 
                              "172.23.", "172.24.", "172.25.", "172.26.", "172.27.", 
                              "172.28.", "172.29.", "172.30.", "172.31.", "192.168.", "169.254."]
            
            if any(ip.startswith(prefix) for prefix in private_ranges):
                st.error(f"🚫 Acceso denegado a IP interna: {ip}")
                SecurityCore.log_activity(target, "BLOQUEADO", f"Intento de SSRF hacia {ip}")
                return False
            
            SecurityCore.log_activity(target, "EXITO", f"Escaneo permitido para IP: {ip}")
            return True
        except socket.gaierror:
            SecurityCore.log_activity(target, "ERROR", "No se pudo resolver el nombre de host (DNS)")
            st.warning("No se pudo resolver la dirección del objetivo.")
            return False
        except Exception as e:
            SecurityCore.log_activity(target, "ERROR", f"Error inesperado en prevent_ssrf: {str(e)}")
            return False

    @staticmethod
    def sanitize_output(text):
        """Limpia el texto de salida para evitar XSS o inyecciones de HTML"""
        if text is None:
            return ""
        
        clean_text = str(text).strip()
        replacements = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#x27;",
        }
        for char, replacement in replacements.items():
            clean_text = clean_text.replace(char, replacement)
        return clean_text

    @staticmethod
    def analyze_response(target, response=None, error=None):
        """
        Analiza la respuesta para detectar bloqueos de WAF o errores de red.
        Evita que la app falle si el servidor bloquea la petición.
        """
        if error:
            err_msg = str(error).lower()
            if "timeout" in err_msg:
                st.warning(f"⏳ Timeout en {target}. Posible bloqueo de Firewall.")
            return False

        if response is not None:
            status = response.status_code
            # Detectar bloqueos comunes (403 Forbidden, 429 Too Many Requests)
            if status in [403, 406, 429]:
                st.error(f"🛡️ Bloqueo detectado (Código {status}). Posible WAF activo.")
                SecurityCore.log_activity(target, "BLOQUEO", f"Status Code: {status}")
                return False
            if status >= 500:
                st.error(f"🔥 Error del servidor (Código {status}).")
                return False
        return True
