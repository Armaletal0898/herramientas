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
        
        # Guardar en un archivo de texto (modo append)
        try:
            with open("audit_log.txt", "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Error al escribir log: {e}")

    @staticmethod
    def validate_target(target):
        if not target:
            return False
        
        pattern = r'^[a-zA-Z0-9\-\.\/:]+$'
        if not re.match(pattern, target):
            st.error("⚠️ Caracteres no permitidos detectados.")
            SecurityCore.log_activity(target, "BLOQUEADO", "Intento de Inyección de Caracteres")
            return False
        return True

    @staticmethod
    def prevent_ssrf(target):
        try:
            parsed = urlparse(f"http://{target.replace('http://', '').replace('https://', '')}")
            host = parsed.netloc
            ip = socket.gethostbyname(host)
            
            private_ranges = ["127.0.0.1", "0.0.0.0", "localhost", "10.", "172.16.", "192.168.", "169.254."]
            
            if any(ip.startswith(prefix) for prefix in private_ranges):
                st.error(f"🚫 Acceso denegado a IP interna: {ip}")
                SecurityCore.log_activity(target, "BLOQUEADO", f"Intento de SSRF hacia {ip}")
                return False
            
            # Si pasa las pruebas, registramos el inicio del escaneo
            SecurityCore.log_activity(target, "EXITO", f"Escaneo permitido para IP: {ip}")
            return True
        except:
            SecurityCore.log_activity(target, "ERROR", "No se pudo resolver el host")
            return False
