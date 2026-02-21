import os
import schedule
import time
import subprocess
from datetime import datetime

# Colores para la terminal
G = '\033[92m' # Green
Y = '\033[93m' # Yellow
R = '\033[91m' # Red
B = '\033[94m' # Blue
V = '\033[95m' # Violet
W = '\033[0m'  # White

def mostrar_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"""{V}
    ██████╗ ██╗   ██╗ ██████╗██████╗  ██████╗ ███╗   ██╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██╔══██╗██╔═══██╗████╗  ██║
    ██████╔╝ ╚████╔╝ ██║     ██████╔╝██║   ██║██╔██╗ ██║
    ██╔═══╝   ╚██╔╝  ██║     ██╔══██╗██║   ██║██║╚██╗██║
    ██║        ██║   ╚██████╗██║  ██║╚██████╔╝██║ ╚████║
    ╚═╝        ╚═╝    ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
    {Y}         [ MINI TASK SCHEDULER ] [ v1.0 ] [ BY KYLORESITH ]{W}
    """)

def ejecutar_tarea(comando, nombre_tarea):
    """Ejecuta un comando del sistema o script de Python."""
    print(f"\n{B}[*] Iniciando tarea: {nombre_tarea}...{W}")
    try:
        # Ejecuta el comando y espera a que termine
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_msg = f"Tarea '{nombre_tarea}' ejecutada con éxito."
        print(f"{G}✔ {log_msg}{W}")
        
        registrar_log(log_msg)
    except Exception as e:
        error_msg = f"Error al ejecutar '{nombre_tarea}': {e}"
        print(f"{R}[!] {error_msg}{W}")
        registrar_log(error_msg)

def registrar_log(mensaje):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("scheduler_log.txt", "a") as log:
        log.write(f"[{timestamp}] {mensaje}\n")

def menu():
    while True:
        mostrar_banner()
        print(f"{B}1.{W} Programar Monitor de Integridad (Cada 1 minuto - Test)")
        print(f"{B}2.{W} Programar Limpieza de Temporales (Cada hora)")
        print(f"{B}3.{W} Ejecutar comando personalizado ahora")
        print(f"{B}4.{W} Ver Log de ejecuciones (scheduler_log.txt)")
        print(f"{B}5.{W} Salir y detener scheduler")
        
        op = input(f"\n{Y}➔ Selecciona una opción: {W}")

        if op == "1":
            print(f"{G}[+] Monitor programado cada minuto.{W}")
            # Ejemplo: ejecutar tu script de integridad
            schedule.every(1).minutes.do(ejecutar_tarea, "python3 integrity_monitor.py", "HIDS Scan")
            
        elif op == "2":
            print(f"{G}[+] Limpieza programada cada hora.{W}")
            schedule.every().hour.do(ejecutar_tarea, "rm -rf /tmp/*", "System Cleanup")

        elif op == "3":
            cmd = input(f"\n{B}»{W} Ingrese comando o ruta de script: ")
            ejecutar_tarea(cmd, "Manual Task")

        elif op == "4":
            if os.path.exists("scheduler_log.txt"):
                with open("scheduler_log.txt", "r") as f:
                    print(f"\n{B}--- HISTORIAL DE TAREAS ---{W}")
                    print(f.read())
            input("\nPresiona Enter...")

        elif op == "5":
            break
            
        # Bucle de ejecución del scheduler
        print(f"\n{Y}[!] El Scheduler está activo. Presiona Ctrl+C para volver al menú.{W}")
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            continue

if __name__ == "__main__":
    menu()
