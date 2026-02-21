import os
import psutil
import platform
import time
from tabulate import tabulate

# Colores ANSI
GREEN  = "\033[1;32m"
BLUE   = "\033[1;34m"
RED    = "\033[1;31m"
CYAN   = "\033[1;36m"
YELLOW = "\033[1;33m"
WHITE  = "\033[1;37m"
RESET  = "\033[0m"

def mostrar_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"""{CYAN}
    ███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗     
    ██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║     
    ███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║     
    ╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║     
    ███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗
    ╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝
    {BLUE}          [ ADVANCED SYSTEM MONITOR & FORENSIC TOOL ]
    {RED}                      [ BY KYLORENSITH ]
    """)

def obtener_info_hardware():
    print(f"\n{YELLOW}🔍 [ ANÁLISIS DE HARDWARE ]{RESET}")
    cpu_uso = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    hw_data = [
        ["COMPONENTE", "ESTADO / USO", "DETALLE TÉCNICO"],
        ["CPU", f"{cpu_uso}%", f"{psutil.cpu_count()} Núcleos lógicos"],
        ["RAM", f"{ram.percent}%", f"{ram.used // (1024**2)}MB / {ram.total // (1024**2)}MB"],
        ["DISCO", f"{disk.percent}%", f"{disk.free // (1024**3)}GB Libres"]
    ]
    print(tabulate(hw_data, headers="firstrow", tablefmt="fancy_grid"))

def conexiones_red():
    print(f"\n{YELLOW}🌐 [ CONEXIONES DE RED ACTIVAS ]{RESET}")
    conns = psutil.net_connections(kind='inet')
    tabla_red = [["PID", "LOCAL ADDR", "REMOTE ADDR", "STATUS", "PROCESS"]]
    
    conns = sorted(conns, key=lambda x: x.status)
    for c in conns[:20]:
        try:
            p = psutil.Process(c.pid)
            nombre_p = p.name()
        except: nombre_p = "Sistema/Protegido"
            
        laddr = f"{c.laddr.ip}:{c.laddr.port}"
        raddr = f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else "LISTENING"
        st = f"{RED}{c.status}{RESET}" if c.status == "ESTABLISHED" else c.status
        tabla_red.append([c.pid, laddr, raddr, st, nombre_p])
    
    print(tabulate(tabla_red, headers="firstrow", tablefmt="simple"))

def escanear_persistencia():
    print(f"\n{YELLOW}🛡️ [ ESCÁNER DE PERSISTENCIA ]{RESET}")
    encontrados = []
    rutas = []
    if platform.system() == "Linux":
        rutas = ['/etc/init.d', '/etc/rc.local', os.path.expanduser('~/.config/autostart')]
    elif platform.system() == "Windows":
        rutas = [os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup')]

    for r in rutas:
        if os.path.exists(r):
            if os.path.isdir(r):
                for f in os.listdir(r): encontrados.append([f, r])
            else: encontrados.append([os.path.basename(r), os.path.dirname(r)])
    
    if encontrados:
        print(f"{RED}[!] Elementos detectados en inicio automático:{RESET}")
        print(tabulate(encontrados, headers=["Archivo", "Ubicación"], tablefmt="grid"))
    else:
        print(f"{GREEN}✔ No se detectaron entradas de persistencia comunes.{RESET}")

def centro_gestion_procesos():
    """Combina la visualización y eliminación de procesos en una sola interfaz."""
    while True:
        mostrar_banner()
        print(f"{YELLOW}📋 [ GESTIÓN DE PROCESOS (Ordenados por RAM) ]{RESET}")
        
        procs = []
        for p in sorted(psutil.process_iter(['pid', 'name', 'username', 'memory_percent']), 
                        key=lambda x: x.info['memory_percent'], reverse=True)[:18]:
            procs.append([p.info['pid'], p.info['name'], p.info['username'], f"{p.info['memory_percent']:.2f}%"])
        
        print(tabulate(procs, headers=["PID", "NOMBRE", "USUARIO", "MEM %"], tablefmt="psql"))
        
        print(f"\n{CYAN}COMANDOS: {WHITE}[PID] para matar proceso | [R] Refrescar | [S] Salir al Menú{RESET}")
        accion = input(f"{GREEN}Sentinel/Procesos > {RESET}").strip().lower()
        
        if accion == 's':
            break
        elif accion == 'r':
            continue
        else:
            try:
                pid_target = int(accion)
                p_kill = psutil.Process(pid_target)
                nombre_p = p_kill.name()
                p_kill.kill()
                print(f"{GREEN}✔ Proceso {pid_target} ({nombre_p}) eliminado con éxito.{RESET}")
                time.sleep(1.5)
            except ValueError:
                print(f"{RED}❌ Entrada no válida. Use un número de PID o 'S'.{RESET}")
                time.sleep(1)
            except Exception as e:
                print(f"{RED}❌ Error: {e}{RESET}")
                time.sleep(1.5)

def menu_principal():
    while True:
        mostrar_banner()
        print(f"{WHITE}SISTEMA: {platform.system()} | USUARIO: {os.getlogin()}{RESET}")
        print(f"{BLUE}{'='*75}{RESET}")
        
        print(f"{WHITE}[1]{RESET} {CYAN}ESTADO HARDWARE{RESET}   - Diagnóstico de salud")
        print(f"{WHITE}[2]{RESET} {CYAN}ANÁLISIS DE RED{RESET}   - Monitor forense de conexiones")
        print(f"{WHITE}[3]{RESET} {CYAN}PERSISTENCIA{RESET}      - Analizar inicio automático")
        print(f"{WHITE}[4]{RESET} {CYAN}GESTIÓN PROCESOS{RESET}  - Listar y Matar (Kill)")
        print(f"{WHITE}[5]{RESET} {WHITE}SALIR{RESET}")
        
        opcion = input(f"\n{GREEN}Sentinel OS > {RESET}").strip()
        
        if opcion == "1":
            obtener_info_hardware()
            input(f"\n{BLUE}Presiona Enter para volver...{RESET}")
        elif opcion == "2":
            conexiones_red()
            input(f"\n{BLUE}Presiona Enter para volver...{RESET}")
        elif opcion == "3":
            escanear_persistencia()
            input(f"\n{BLUE}Presiona Enter para volver...{RESET}")
        elif opcion == "4":
            centro_gestion_procesos()
        elif opcion == "5":
            break

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Interrumpido.{RESET}")
