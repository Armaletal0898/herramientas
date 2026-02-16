import os
from cryptography.fernet import Fernet
from datetime import datetime

# Colores para la terminal
G = '\033[92m' # Green
Y = '\033[93m' # Yellow
R = '\033[91m' # Red
B = '\033[94m' # Blue
M = '\033[95m' # Magenta
W = '\033[0m'  # White

def mostrar_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"""{M}
    ███████╗███╗   ██╗ ██████╗██████╗ ██╗   ██╗██████╗ ████████╗ ██████╗ ██████╗ 
    ██╔════╝████╗  ██║██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
    █████╗  ██╔██╗ ██║██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ██║   ██║██████╔╝
    ██╔══╝  ██║╚██╗██║██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██║   ██║██╔══██╗
    ███████╗██║ ╚████║╚██████╗██║  ██║   ██║   ██║        ██║   ╚██████╔╝██║  ██║
    ╚══════╝╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝    ╚═════╝ ╚═╝  ╚═╝
    {Y}           [ AES-256 FILE ENCRYPTION SYSTEM ] [ BY KYLORESITH ]{W}
    """)

def generar_clave():
    """Genera una clave y la guarda en un archivo .key"""
    clave = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(clave)
    print(f"\n{G}[+] Clave generada y guardada en 'secret.key'.{W}")
    print(f"{R}[!] ADVERTENCIA: Si pierdes este archivo, no podrás descifrar nada.{W}")
    registrar_log("Nueva clave maestra generada.")

def cargar_clave():
    """Carga la clave del archivo actual."""
    return open("secret.key", "rb").read()

def cifrar_archivo(ruta_archivo):
    """Cifra el contenido de un archivo."""
    try:
        clave = cargar_clave()
        f = Fernet(clave)
        
        with open(ruta_archivo, "rb") as file:
            datos_archivo = file.read()
        
        datos_cifrados = f.encrypt(datos_archivo)
        
        with open(ruta_archivo, "wb") as file:
            file.write(datos_cifrados)
            
        print(f"\n{G}✔ Archivo '{ruta_archivo}' cifrado con éxito.{W}")
        registrar_log(f"Cifrado: {ruta_archivo}")
    except Exception as e:
        print(f"{R}[!] Error al cifrar: {e}{W}")

def descifrar_archivo(ruta_archivo):
    """Descifra el contenido de un archivo."""
    try:
        clave = cargar_clave()
        f = Fernet(clave)
        
        with open(ruta_archivo, "rb") as file:
            datos_cifrados = file.read()
            
        datos_descifrados = f.decrypt(datos_cifrados)
        
        with open(ruta_archivo, "wb") as file:
            file.write(datos_descifrados)
            
        print(f"\n{G}✔ Archivo '{ruta_archivo}' descifrado con éxito.{W}")
        registrar_log(f"Descifrado: {ruta_archivo}")
    except Exception as e:
        print(f"{R}[!] Error: Clave incorrecta o archivo dañado.{W}")

def registrar_log(mensaje):
    """Guarda las acciones en un historial txt."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("crypto_log.txt", "a") as log:
        log.write(f"[{timestamp}] {mensaje}\n")

def menu():
    while True:
        mostrar_banner()
        print(f"{B}1.{W} Generar Clave Maestra (Solo una vez)")
        print(f"{B}2.{W} Cifrar un archivo")
        print(f"{B}3.{W} Descifrar un archivo")
        print(f"{B}4.{W} Ver Log de operaciones")
        print(f"{B}5.{W} Salir")
        
        op = input(f"\n{Y}➔ Selecciona una opción: {W}")

        if op == "1":
            generar_clave()
            input("\nPresiona Enter...")
        
        elif op == "2":
            archivo = input(f"\n{B}»{W} Ruta del archivo a cifrar: ")
            if os.path.isfile(archivo):
                cifrar_archivo(archivo)
            else: print(f"{R}[!] Archivo no encontrado.{W}")
            input("\nPresiona Enter...")

        elif op == "3":
            archivo = input(f"\n{B}»{W} Ruta del archivo a descifrar: ")
            if os.path.isfile(archivo):
                descifrar_archivo(archivo)
            else: print(f"{R}[!] Archivo no encontrado.{W}")
            input("\nPresiona Enter...")

        elif op == "4":
            if os.path.exists("crypto_log.txt"):
                print(f"\n{B}--- HISTORIAL DE OPERACIONES ---{W}")
                with open("crypto_log.txt", "r") as f: print(f.read())
            else: print(f"{R}[!] Sin registros.{W}")
            input("\nPresiona Enter...")

        elif op == "5":
            print(f"{G}Saliendo del sistema...{W}")
            break

if __name__ == "__main__":
    menu()
