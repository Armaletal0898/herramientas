import re
import socket
import requests
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
            # En Streamlit Cloud, print() se ve en los logs de la consola
            print(f"Error crítico al escribir log: {e}")

    @staticmethod
    def validate_target(target):
        """Valida que el target no contenga caracteres maliciosos"""
        if not target:
            return False
        
        # Patrón robusto para dominios, IPs y rutas básicas
        pattern = r'^[a-zA-Z0-9\-\.\/:]+$'
        if not re.match(pattern, str(target)):
            st.error("⚠️ Caracteres no permitidos detectados en el objetivo.")
            SecurityCore.log_activity(target, "BLOQUEADO", "Intento de Inyección de Caracteres")
            return False
        return True

    @staticmethod
    def prevent_ssrf(target):
        """Previene ataques de Server Side Request Forgery (SSRF)"""
        try:
            # Extraer solo el host (sin http ni paths)
            clean_url = str(target).replace('http://', '').replace('https://', '').split('/')[0]
            if ":" in clean_url: clean_url = clean_url.split(":")[0] # Quitar puerto si existe
            
            ip = socket.gethostbyname(clean_url)
            
            # Lista completa de rangos privados
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
            SecurityCore.log_activity(target, "ERROR", "No se pudo resolver DNS")
            st.warning("No se pudo resolver la dirección del objetivo.")
            return False
        except Exception as e:
            SecurityCore.log_activity(target, "ERROR", f"Error en prevent_ssrf: {str(e)}")
            return False

    @staticmethod
    def sanitize_output(text):
        """Limpia el texto para evitar XSS (Mantiene '/' para rutas de fuzzer)"""
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
        Analiza la respuesta para detectar WAF, bloqueos o errores de red.
        Retorna False si el escaneo debe detenerse.
        """
        # CASO 1: Errores de red (Timeout / Connection Refused)
        if error:
            error_str = str(error).lower()
            if "timeout" in error_str:
                st.warning(f"⏳ **Timeout:** El servidor tardó mucho. Posible Firewall/IDS activo.")
                SecurityCore.log_activity(target, "AVISO", "Timeout detectado")
            else:
                st.error(f"❌ **Error de Red:** No hay conexión con el objetivo.")
                SecurityCore.log_activity(target, "ERROR", f"Fallo de conexión: {error_str[:50]}")
            return False

        # CASO 2: Análisis de Respuesta HTTP
        if response is not None:
            sc = response.status_code
            
            # Códigos de bloqueo
            if sc in [403, 406, 429]:
                server_header = response.headers.get('Server', '').lower()
                body_text = response.text.lower()
                
                waf_signatures = ["cloudflare", "mod_security", "imperva", "sucuri", "incapsula", "akamai"]
                
                # Buscar firmas de WAF
                found_waf = next((sig for sig in waf_signatures if sig in body_text or sig in server_header), None)
                
                if found_waf:
                    st.error(f"🛡️ **WAF Detectado:** Bloqueo por {found_waf.capitalize()} (Status {sc}).")
                    SecurityCore.log_activity(target, "WAF", f"Bloqueo detectado: {found_waf}")
                else:
                    st.warning(f"🚫 **Acceso Denegado (403):** El servidor bloqueó la petición.")
                    SecurityCore.log_activity(target, "BLOQUEO", "Status 403 sin firma clara")
                return False
            
            # Errores graves de servidor
            if sc >= 500:
                st.error(f"🔥 **Error de Servidor (Código {sc}):** El objetivo no puede procesar más peticiones.")
                return False

        return True
