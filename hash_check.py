import hashlib
import os
import sys

def mostrar_banner():
    os.system('clear')
    print("""
    \033[1;35m
     ██╗  ██╗ █████╗ ███████╗██╗  ██╗    ██╗   ██╗██╗███████╗██╗    ██╗
     ██║  ██║██╔══██╗██╔════╝██║  ██║    ██║   ██║██║██╔════╝██║    ██║
     ███████║███████║███████╗███████║    ██║   ██║██║█████╗  ██║ █╗ ██║
     ██╔══██║██╔══██║╚════██║██╔══██║    ╚██╗ ██╔╝██║██╔══╝  ██║███╗██║
     ██║  ██║██║  ██║███████║██║  ██║     ╚████╔╝ ██║███████╗╚███╔███╔╝
     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝      ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝
    \033[1;34m [ INTEGRITY CHECKER ] [ FORENSIC TOOL ] [ BY KILORENSITH ] \033[0m
    """)

def calcular_hashes(ruta_archivo):
    if not os.path.isfile(ruta_archivo):
        print(f"\033[1;31m[!] Error: '{ruta_archivo}' no es un archivo válido.\033[0m")
        return

    # Bloques de lectura para no saturar la RAM con archivos grandes
    BUF_SIZE = 65536 
    
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()

    try:
        with open(ruta_archivo, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                md5.update(data)
                sha1.update(data)
                sha256.update(data)

        print(f"\033[1;37mResultados para: \033[1;32m{ruta_archivo}\033[0m\n")
        print(f"\033[1;36m[MD5]    :\033[0m {md5.hexdigest()}")
        print(f"\033[1;36m[SHA-1]  :\033[0m {sha1.hexdigest()}")
        print(f"\033[1;36m[SHA-256]:\033[0m {sha256.hexdigest()}")
        
        # Guardar en un log para futuras comparaciones
        with open("hash_history.txt", "a") as log:
            log.write(f"{ruta_archivo} | SHA256: {sha256.hexdigest()}\n")
            print(f"\n\033[1;33m[i] Hash guardado en 'hash_history.txt' para auditoría.\033[0m")

    except Exception as e:
        print(f"🔥 Error: {e}")

if __name__ == "__main__":
    mostrar_banner()
    archivo_a_revisar = input("\033[1;37m➔ Arrastra el archivo aquí o escribe su nombre: \033[0m").strip()
    # Limpiar comillas si el usuario arrastra el archivo a la terminal
    archivo_a_revisar = archivo_a_revisar.replace("'", "").replace('"', "")
    calcular_hashes(archivo_a_revisar)
