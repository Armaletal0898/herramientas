import os
import secrets
import string
import math
from datetime import datetime

# Colores para la terminal
G = '\033[92m' # Green
Y = '\033[93m' # Yellow
R = '\033[91m' # Red
B = '\033[94m' # Blue
CY = '\033[96m'# Cyan
W = '\033[0m'  # White

def mostrar_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"""{CY}
    ██████╗ ███████╗███████╗███████╗ ██████╗██╗   ██╗██████╗ ███████╗
    ██╔══██╗██╔════╝██╔════╝██╔════╝██╔════╝██║   ██║██╔══██╗██╔════╝
    ██████╔╝███████╗███████╗█████╗  ██║     ██║   ██║██████╔╝█████╗  
    ██╔═══╝ ╚════██║╚════██║██╔══╝  ██║     ██║   ██║██╔══██╗██╔══╝  
    ██║     ███████║███████║███████╗╚██████╗╚██████╔╝██║  ██║███████╗
    ╚═╝     ╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
    {Y}           [ PASSWORD GENERATOR & ANALYZER ] [ BY KYLORESITH ]{W}
    """)

def calcular_entropia(password):
    """Calcula la entropía de la contraseña en bits."""
    caracteres = 0
    if any(c in string.ascii_lowercase for c in password): caracteres += 26
    if any(c in string.ascii_uppercase for c in password): caracteres += 26
    if any(c in string.digits for c in password): caracteres += 10
    if any(c in string.punctuation for c in password): caracteres += 32
    
    if caracteres == 0: return 0
    # Fórmula: L * log2(Pool)
    entropia = len(password) * math.log2(caracteres)
    return round(entropia, 2)

def analizar_password(password):
    """Realiza un análisis profundo de una contraseña dada."""
    ent = calcular_entropia(password)
    print(f"\n{B}--- [ RESULTADOS DEL ANÁLISIS ] ---{W}")
    print(f"Contraseña: {password}")
    print(f"Entropía: {ent} bits")
    
    if ent < 40:
        nivel = f"{R}Muy Débil (Crackeo instantáneo){W}"
    elif ent < 60:
        nivel = f"{Y}Media (Días/Meses para crackeo){W}"
    elif ent < 80:
        nivel = f"{G}Fuerte (Años para crackeo){W}"
    else:
        nivel = f"{CY}Muy Fuerte (Siglos para crackeo){W}"
    
    print(f"Nivel de Seguridad: {nivel}")
    registrar_log(f"Análisis realizado - Entropía: {ent} bits")

def generar_password(longitud, incluir_simbolos=True):
    """Genera una contraseña usando el módulo secrets (seguro)."""
    caracteres = string.ascii_letters + string.digits
    if incluir_simbolos:
        caracteres += string.punctuation
    
    password = ''.join(secrets.choice(caracteres) for _ in range(longitud))
    registrar_log(f"Contraseña generada de {longitud} caracteres.")
    return password

def registrar_log(mensaje):
    """Guarda las acciones en un historial txt."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("password_history.txt", "a") as log:
        log.write(f"[{timestamp}] {mensaje}\n")

def menu():
    while True:
        mostrar_banner()
        print(f"{B}1.{W} Generar nueva contraseña segura")
        print(f"{B}2.{W} Analizar fuerza de una contraseña")
        print(f"{B}3.{W} Ver historial de generación (password_history.txt)")
        print(f"{B}4.{W} Salir")
        
        op = input(f"\n{Y}➔ Selecciona una opción: {W}")

        if op == "1":
            try:
                lon = int(input(f"\n{B}»{W} Longitud deseada: "))
                sim = input(f"{B}»{W} ¿Incluir símbolos? (s/n): ").lower() == 's'
                pw = generar_password(lon, sim)
                print(f"\n{G}✔ Generada:{W} {pw}")
                analizar_password(pw)
            except ValueError:
                print(f"{R}[!] Error: Ingresa un número válido.{W}")
            input("\nPresiona Enter para continuar...")
            
        elif op == "2":
            pw = input(f"\n{B}»{W} Ingresa la contraseña a analizar: ")
            analizar_password(pw)
            input("\nPresiona Enter para continuar...")

        elif op == "3":
            if os.path.exists("password_history.txt"):
                print(f"\n{B}--- HISTORIAL ---{W}")
                with open("password_history.txt", "r") as f:
                    print(f.read())
            else:
                print(f"{R}[!] Historial vacío.{W}")
            input("\nPresiona Enter para continuar...")

        elif op == "4":
            break

if __name__ == "__main__":
    menu()
