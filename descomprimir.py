import patoolib
import os
import sys
import time

def mostrar_banner():
    os.system('clear')
    banner = """
    \033[1;32m
     ██████╗ ███████╗███████╗ ██████╗ ██████╗ ███╗   ███╗██████╗ ██████╗ ███████╗███████╗
     ██╔══██╗██╔════╝██╔════╝██╔════╝██╔═══██╗████╗ ████║██╔══██╗██╔══██╗██╔════╝██╔════╝
     ██║  ██║█████╗  ███████╗██║     ██║   ██║██╔████╔██║██████╔╝██████╔╝█████╗  ███████╗
     ██║  ██║██╔══╝  ╚════██║██║     ██║   ██║██║╚██╔╝██║██╔═══╝ ██╔══██╗██╔══╝  ╚════██║
     ██████╔╝███████╗███████║╚██████╗╚██████╔╝██║ ╚═╝ ██║██║     ██║  ██║███████╗███████║
     ╚═════╝ ╚══════╝╚══════╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝
    \033[1;34m [ ARCHIVE MASTER 2026 ] [ COMPRESS & DECOMPRESS ] [ BY KYLORESITH ] \033[0m
    """
    print(banner)

def comprimir():
    print("\033[1;37m» Ingrese el nombre del archivo o carpeta a COMPRIMIR: \033[0m", end="")
    objetivo = input().strip()
    
    if not os.path.exists(objetivo):
        print(f"\033[1;31m\n❌ Error: '{objetivo}' no existe.\033[0m")
        return

    print("\033[1;37m» Ingrese el nombre final con extensión (ej: backup.7z, datos.zip, soft.tar.gz): \033[0m", end="")
    nombre_final = input().strip()

    try:
        print(f"\n\033[1;33m[*] Comprimiendo '{objetivo}' en '{nombre_final}'...\033[0m")
        # patool crea el archivo basándose en la extensión que escribas
        patoolib.create_archive(nombre_final, (objetivo,))
        print(f"\n\033[1;32m✅ ¡COMPRESIÓN EXITOSA! Archivo creado: {nombre_final}\033[0m")
    except Exception as e:
        print(f"\n\033[1;31m🔥 ERROR: {e}\033[0m")

def descomprimir():
    print("\033[1;37m» Ingrese el nombre del archivo a DESCOMPRIMIR: \033[0m", end="")
    archivo = input().strip()

    if not os.path.exists(archivo):
        print(f"\033[1;31m\n❌ Error: El archivo '{archivo}' no existe.\033[0m")
        return

    nombre_base = os.path.splitext(archivo)[0]
    carpeta_destino = f"{nombre_base}_extraido"

    try:
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)
        
        print(f"\033[1;33m[*] Descomprimiendo en '{carpeta_destino}'...\033[0m")
        patoolib.extract_archive(archivo, outdir=carpeta_destino)
        print(f"\n\033[1;32m✅ ¡EXTRACCIÓN EXITOSA! Guardado en: {carpeta_destino}/\033[0m")
    except Exception as e:
        print(f"\n\033[1;31m🔥 ERROR: {e}\033[0m")

def menu():
    mostrar_banner()
    print("\033[1;36m [1] \033[1;37mDescomprimir archivo")
    print("\033[1;36m [2] \033[1;37mComprimir archivo o carpeta")
    print("\033[1;36m [3] \033[1;37mSalir")
    
    opcion = input("\n\033[1;32m➔ Seleccione una opción: \033[0m")

    if opcion == "1":
        descomprimir()
    elif opcion == "2":
        comprimir()
    elif opcion == "3":
        print("\n\033[1;34m[!] Saliendo del programa...\033[0m")
        sys.exit()
    else:
        print("\033[1;31m\n[!] Opción no válida.\033[0m")

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\n\n\033[1;31m[!] Abortado por el usuario.\033[0m")
