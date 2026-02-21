import os
import subprocess

# Colores ANSI
VERDE = "\033[1;32m"
CIAN = "\033[1;36m"
ROJO = "\033[1;31m"
RESET = "\033[0m"

def mostrar_banner():
    print(f"""{VERDE}
    ██╗   ██╗     ███████╗     ██████╗          ██████╗     ███████╗
    ██║   ██║     ██╔════╝     ██╔══██╗        ██╔═══██╗    ██╔════╝
    ██║   ██║     ███████╗     ██████╔╝        ██║   ██║    ███████╗
    ██║   ██║     ╚════██║     ██╔══██╗        ██║   ██║    ╚════██║
    ╚██████╔╝     ███████║     ██████╔╝        ╚██████╔╝    ███████║
     ╚═════╝      ╚══════╝     ╚═════╝          ╚═════╝     ╚══════╝
           {CIAN}>> Automator: ISO to Live USB <<{RESET}
    """)

def run_command(command):
    process = subprocess.Popen(command, shell=True)
    process.wait()

def main():
    mostrar_banner()
    
    # 1. Directorio
    current_dir = os.getcwd()
    print(f"{CIAN}[*]{RESET} Buscando ISOs en: {current_dir}")

    # 2. Selección de ISO
    isos = [f for f in os.listdir('.') if f.endswith('.iso')]
    if not isos:
        print(f"{ROJO}[!] No hay archivos .iso aquí.{RESET}")
        iso_name = input("Escribe el nombre del archivo manual: ")
    else:
        for i, f in enumerate(isos):
            print(f"  [{VERDE}{i}{RESET}] {f}")
        idx = input(f"\n{CIAN}[?]{RESET} Selecciona el número de ISO: ")
        iso_name = isos[int(idx)] if idx.isdigit() and int(idx) < len(isos) else idx

    # 3. Dispositivos
    print(f"\n{VERDE}--- DISPOSITIVOS CONECTADOS ---{RESET}")
    run_command("lsblk -o NAME,SIZE,MODEL,TYPE,MOUNTPOINT | grep -v 'loop'")
    
    target = input(f"\n{CIAN}[?]{RESET} Escribe el dispositivo (ej: sdb): ").strip()
    target_path = f"/dev/{target}"

    # Alerta de seguridad
    if "sda" in target:
        print(f"{ROJO}¡PELIGRO! sda suele ser tu sistema principal.{RESET}")
        if input("¿Seguro? (s/N): ").lower() != 's': return

    # 4. Instalación
    print(f"\n{ROJO}[!] ADVERTENCIA:{RESET} Se borrará {target_path}")
    if input(f"{CIAN}[?]{RESET} ¿Confirmar acción? (s/n): ").lower() == 's':
        print(f"\n{VERDE}[+] Iniciando proceso... Ten paciencia.{RESET}\n")
        cmd = f"sudo dd if='{iso_name}' of='{target_path}' bs=4M status=progress oflag=sync"
        run_command(cmd)
        print(f"\n{VERDE}[OK] ¡USB OS Creado con éxito!{RESET}")
    else:
        print("\nOperación cancelada.")

if __name__ == "__main__":
    main()
