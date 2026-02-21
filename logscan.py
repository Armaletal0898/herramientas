import os
import re
from collections import Counter
from datetime import datetime

# Colores para la terminal
G = '\033[92m' # Green
Y = '\033[93m' # Yellow
R = '\033[91m' # Red
B = '\033[94m' # Blue
C = '\033[96m' # Cyan
W = '\033[0m'  # White

def mostrar_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"""{C}
    ██╗      ██████╗  ██████╗      ██████╗ ███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗     
    ██║     ██╔═══██╗██╔════╝     ██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║     
    ██║     ██║   ██║██║  ███╗    ███████╗ █████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║     
    ██║     ██║   ██║██║   ██║    ╚════██║ ██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║     
    ███████╗╚██████╔╝╚██████╔╝    ███████║ ███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗
    ╚══════╝ ╚═════╝  ╚═════╝     ╚══════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝
    {Y}             [ INTELLIGENT LOG ANALYZER ] [ v1.0 ] [ BY KYLORESITH ]{W}
    """)

def analizar_log(ruta_archivo):
    """Analiza un archivo de log buscando IPs, errores y patrones de ataque."""
    if not os.path.exists(ruta_archivo):
        print(f"{R}[!] El archivo no existe.{W}")
        return

    # Patrón Regex para IPs y errores comunes (404, 500, Failed password)
    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    error_patterns = [r'404', r'500', r'[Ff]ailed', r'[Dd]enied', r'[Uu]nauthorized']

    ips_encontradas = []
    total_errores = 0
    lineas_sospechosas = []

    print(f"\n{B}[*]{W} Procesando {ruta_archivo}...")

    with open(ruta_archivo, 'r') as f:
        for linea in f:
            # Buscar IPs
            ip = re.findall(ip_pattern, linea)
            if ip:
                ips_encontradas.extend(ip)
            
            # Buscar Errores
            for pat in error_patterns:
                if re.search(pat, linea):
                    total_errores += 1
                    lineas_sospechosas.append(linea.strip())
                    break

    # Procesar resultados
    conteo_ips = Counter(ips_encontradas)
    ips_top = conteo_ips.most_common(5)

    print(f"\n{G}--- [ RESULTADOS DEL ANÁLISIS ] ---{W}")
    print(f"Total de líneas analizadas: {len(ips_encontradas) + total_errores}")
    print(f"Total de eventos críticos/errores: {R}{total_errores}{W}")
    
    print(f"\n{Y}Top 5 IPs más activas (Posibles atacantes):{W}")
    for ip, count in ips_top:
        alerta = f"{R}[!] ALTA ACTIVIDAD{W}" if count > 50 else ""
        print(f" ➔ {ip}: {count} veces {alerta}")

    # Generar reporte TXT
    generar_reporte(ruta_archivo, total_errores, ips_top, lineas_sospechosas)

def generar_reporte(archivo_orig, errores, ips, detalles):
    """Crea un archivo de reporte detallado."""
    reporte_name = f"reporte_analisis_{datetime.now().strftime('%H%M%S')}.txt"
    with open(reporte_name, "w") as r:
        r.write(f"REPORTE DE SEGURIDAD - SENTINEL LOGS\n")
        r.write(f"Fecha: {datetime.now()}\n")
        r.write(f"Archivo analizado: {archivo_orig}\n")
        r.write(f"{'-'*40}\n")
        r.write(f"Resumen: {errores} errores detectados.\n")
        r.write(f"Top IPs:\n")
        for ip, count in ips:
            r.write(f"- {ip}: {count} logs\n")
        r.write(f"\nDETALLES DE EVENTOS SOSPECHOSOS:\n")
        for d in detalles[:50]: # Solo las primeras 50 para no saturar el TXT
            r.write(f"{d}\n")
            
    print(f"\n{G}[+] Reporte detallado guardado como: {reporte_name}{W}")
    registrar_log(f"Análisis completo de {archivo_orig}. Detectados {errores} errores.")

def registrar_log(mensaje):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log_history.txt", "a") as log:
        log.write(f"[{timestamp}] {mensaje}\n")

def menu():
    while True:
        mostrar_banner()
        print(f"{B}1.{W} Analizar un archivo de Log (Apache, Auth, SSH, etc.)")
        print(f"{B}2.{W} Ver historial de análisis (log_history.txt)")
        print(f"{B}3.{W} Salir")
        
        op = input(f"\n{Y}➔ Selecciona una opción: {W}")

        if op == "1":
            archivo = input(f"\n{B}»{W} Ruta del archivo log a analizar: ")
            analizar_log(archivo)
            input("\nPresiona Enter para continuar...")
        
        elif op == "2":
            if os.path.exists("log_history.txt"):
                with open("log_history.txt", "r") as f:
                    print(f"\n{B}--- HISTORIAL ---{W}")
                    print(f.read())
            else:
                print(f"{R}[!] No hay historial.{W}")
            input("\nPresiona Enter para continuar...")

        elif op == "3":
            break

if __name__ == "__main__":
    menu()
