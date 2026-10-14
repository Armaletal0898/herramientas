#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Herramienta CLI de Búsqueda Masiva en Tiempo Real (Versión Definitiva)
Servidor de trabajo: local-dev-node01 (Servidor Local)
Optimización: Mmap + Comandos Interactivos Interactivos Robustos.
"""

import sys
import os
import csv
import json
import xml.etree.ElementTree as ET
import re
import termios
import tty
import mmap
import time

# --- COLORES ANSI PARA LA TERMINAL ---
COLOR_BANNER = "\033[1;36m"  # Cian brillante
COLOR_SUCCESS = "\033[1;32m" # Verde brillante
COLOR_WARN = "\033[1;33m"    # Amarillo
COLOR_INFO = "\033[1;34m"    # Azul
COLOR_RESET = "\033[0m"      # Reset

def mostrar_banner():
    """Muestra un banner estético al iniciar la herramienta."""
    banner = f"""
{COLOR_BANNER}========================================================
    __  ___                 __               ____              
   /  |/  /__  _  _______  / /_____  ____   / __ \\__  _  __ 
  / /|_/ / _ \\| |/_/ ___/ / __/ __ \\/ __ \\ / /_/ / / / / / / / 
 / /  / /  __/>  <(__  ) / /_/ /_/ / /_/ // ____/ /_/ / /_/ /  
/_/  /_/\\___/_/|_/____/  \\__/\\____/\\____//_/    \\__,_/\\__, /   
                                                     /____/    
       [ High-Performance Multi-Format CLI Search ]
       [ Servidor Asignado: local-dev-node01      ]
========================================================{COLOR_RESET}
    """
    print(banner)

def parsear_archivo_gigante(ruta_archivo):
    """Indexa archivos masivos usando Mmap para consumo mínimo de RAM."""
    if not os.path.exists(ruta_archivo):
        print(f"{COLOR_WARN}[X] Error: El archivo '{ruta_archivo}' no existe en local-dev-node01.{COLOR_RESET}")
        sys.exit(1)

    print(f"[*] Analizando e indexando archivo con Mmap (Ahorro masivo de RAM)...")

    archivo_obj = open(ruta_archivo, "r", encoding="utf-8", errors="ignore")
    mm = mmap.mmap(archivo_obj.fileno(), 0, access=mmap.ACCESS_READ)
    
    lineas_offsets = []
    posicion = 0
    while True:
        siguiente_salto = mm.find(b"\n", posicion)
        if siguiente_salto == -1:
            if mm[posicion:]:
                lineas_offsets.append((posicion, len(mm)))
            break
        lineas_offsets.append((posicion, siguiente_salto))
        posicion = siguiente_salto + 1

    print(f"{COLOR_SUCCESS}[✓] Indexación completa: {len(lineas_offsets):,} líneas listas con consumo de RAM mínimo.{COLOR_RESET}\n")
    print("Iniciando buscador interactivo en 1.5 segundos...")
    time.sleep(1.5)
    
    return archivo_obj, mm, lineas_offsets, ruta_archivo

def obtener_linea(mm, offset):
    """Extrae una línea específica del disco/mmap."""
    inicio, fin = offset
    return mm[inicio:fin].decode("utf-8", errors="ignore").strip()

def leer_tecla_raw():
    """Captura pulsaciones individuales en tiempo real sin presionar Enter."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def buscador_tiempo_real(mm, lineas_offsets, ruta_archivo):
    """Buscador interactivo optimizado con soporte dual: Tiempo real para texto y Enter para comandos."""
    filtro_actual = ""
    max_resultados_visibles = 15
    mensaje_notificacion = ""
    modo_comando = False # Bandera para saber si estamos ingresando un comando con '-'

    while True:
        # 1. Limpiar pantalla completa y colocar el cursor arriba
        sys.stdout.write("\033[H\033[2J")
        sys.stdout.flush()

        # 2. Dibujar interfaz
        print(f"{COLOR_BANNER}--- MOTOR DE BÚSQUEDA OPTIMIZADO (RAM EFICIENTE) ---{COLOR_RESET}")
        print("Comandos (Escribe '-' y presiona ENTER): -all, -stats, -export <path>, -count, -top <num>, -help")
        print("Presiona [ESC] o [Ctrl+C] para salir.\n")
        
        if mensaje_notificacion:
            print(f"{COLOR_SUCCESS}{mensaje_notificacion}{COLOR_RESET}")
            mensaje_notificacion = ""

        print(f"Búsqueda / Comando: {filtro_actual}█")
        print("-" * 60)

        query_limpia = filtro_actual.strip().lower()

        # Si el usuario introdujo un comando completo y presionó Enter (detectado por salto de línea o ejecución)
        if modo_comando:
            modo_comando = False
            
            # ==========================================
            # [COMANDO 1] -all: Muestra el archivo completo
            # ==========================================
            if query_limpia == "-all":
                print(f"{COLOR_INFO}[!] Mostrando archivo completo ({len(lineas_offsets):,} líneas en total):{COLOR_RESET}\n")
                limite_display = 100
                for offset in lineas_offsets[:limite_display]:
                    print(f" -> {obtener_linea(mm, offset)}")
                if len(lineas_offsets) > limite_display:
                    print(f"\n ... [ Se muestran solo los primeros {limite_display} registros para evitar bloqueo ]")
                input("\nPresiona [Enter] para continuar...")
                filtro_actual = ""
                continue

            # ==========================================
            # [COMANDO 2] -stats: Estadísticas del archivo
            # ==========================================
            elif query_limpia == "-stats":
                tamano_bytes = os.path.getsize(ruta_archivo)
                tamano_mb = tamano_bytes / (1024 * 1024)
                print(f"{COLOR_INFO}[📊 ESTADÍSTICAS DEL ARCHIVO]{COLOR_RESET}")
                print(f" • Archivo analizado : {ruta_archivo}")
                print(f" • Total de líneas   : {len(lineas_offsets):,}")
                print(f" • Tamaño en disco   : {tamano_mb:.2f} MB ({tamano_bytes:,} bytes)")
                print(f" • Límite visible    : {max_resultados_visibles} líneas (ajustable con -top)")
                input("\nPresiona [Enter] para continuar...")
                filtro_actual = ""
                continue

            # ==========================================
            # [COMANDO 3] -export <nombre>: Exporta resultados
            # ==========================================
            elif query_limpia.startswith("-export"):
                partes = filtro_actual.strip().split()
                if len(partes) > 1:
                    nombre_salida = partes[1]
                    print(f"{COLOR_INFO}[💾 EXPORTANDO] Guardando coincidencias en '{nombre_salida}'...{COLOR_RESET}")
                    try:
                        with open(nombre_salida, "w", encoding="utf-8") as f_out:
                            for offset in lineas_offsets:
                                linea = obtener_linea(mm, offset)
                                f_out.write(linea + "\n")
                        print(f"{COLOR_SUCCESS}[✓] Exportación exitosa en local-dev-node01.{COLOR_RESET}")
                    except Exception as e:
                        print(f"{COLOR_WARN}[X] Error al exportar: {e}{COLOR_RESET}")
                else:
                    print(f"{COLOR_WARN}[!] Uso incorrecto. Ejemplo: -export resultado.txt{COLOR_RESET}")
                input("\nPresiona [Enter] para continuar...")
                filtro_actual = ""
                continue

            # ==========================================
            # [COMANDO 4] -count: Conteo rápido de líneas
            # ==========================================
            elif query_limpia == "-count":
                print(f"{COLOR_INFO}[#] Conteo total de registros indexados:{COLOR_RESET} {len(lineas_offsets):,} líneas.")
                input("\nPresiona [Enter] para continuar...")
                filtro_actual = ""
                continue

            # ==========================================
            # [COMANDO 5] -top <número>: Cambia límite visual
            # ==========================================
            elif query_limpia.startswith("-top"):
                partes = filtro_actual.strip().split()
                if len(partes) > 1 and partes[1].isdigit():
                    max_resultados_visibles = int(partes[1])
                    mensaje_notificacion = f"[✓] Límite visual actualizado a: {max_resultados_visibles} resultados."
                else:
                    mensaje_notificacion = "[!] Uso incorrecto de -top. Ejemplo: -top 25"
                filtro_actual = ""
                continue

            # ==========================================
            # [COMANDO 6] -help: Panel de ayuda interactiva
            # ==========================================
            elif query_limpia == "-help":
                print(f"{COLOR_INFO}[?] PANEL DE AYUDA E INTERACCIÓN CLI{COLOR_RESET}")
                print(" • Escribe texto normal   : Filtra en tiempo real por subcadena.")
                print(" • -all (con Enter)       : Despliega las primeras líneas del archivo.")
                print(" • -stats (con Enter)     : Muestra metadatos y tamaño en disco.")
                print(" • -export <file> (Enter) : Guarda las líneas en un nuevo archivo.")
                print(" • -count (con Enter)     : Muestra el total exacto de registros.")
                print(" • -top <num> (Enter)     : Cambia cuántas líneas se muestran en pantalla.")
                print(" • -help (con Enter)      : Abre esta ventana de ayuda.")
                print(" • ESC o Ctrl+C           : Sale de la aplicación.")
                input("\nPresiona [Enter] para continuar...")
                filtro_actual = ""
                continue

        # ==========================================
        # Búsqueda normal en tiempo real (por texto)
        # ==========================================
        if filtro_actual and not filtro_actual.startswith("-"):
            resultados_offsets = []
            filtro_lower = filtro_actual.lower()
            for offset in lineas_offsets:
                linea_texto = obtener_linea(mm, offset)
                if filtro_lower in linea_texto.lower():
                    resultados_offsets.append(offset)
                    if len(resultados_offsets) >= 2000: 
                        break

            print(f"Coincidencias encontradas: {len(resultados_offsets):,}\n")
            
            for offset in resultados_offsets[:max_resultados_visibles]:
                texto_linea = obtener_linea(mm, offset)
                print(f" -> {texto_linea}")
                
            if len(resultados_offsets) > max_resultados_visibles:
                print(f" ... [ y {len(resultados_offsets) - max_resultados_visibles} resultados más ocultos ]")
        elif not filtro_actual:
            print(" (Empieza a escribir texto para filtrar en tiempo real, o escribe '-' para comandos...)")
        elif filtro_actual.startswith("-"):
            print(f" [Modo Comando Activo: Presiona ENTER para ejecutar '{filtro_actual}']")

        sys.stdout.flush()

        # 3. Capturar la tecla presionada de inmediato
        char = leer_tecla_raw()

        # Tecla Escape (27) o Ctrl+C (3) para salir
        if ord(char) == 27 or ord(char) == 3:  
            sys.stdout.write("\033[H\033[2J")
            print("\nSaliendo del buscador. ¡Hasta luego!")
            break
        # Tecla Enter (10 o 13)
        elif ord(char) == 10 or ord(char) == 13:
            if filtro_actual.startswith("-"):
                modo_comando = True # Activamos la ejecución del comando al presionar Enter
        # Tecla Backspace (127 o 8) para borrar caracteres
        elif ord(char) == 127 or ord(char) == 8:
            if len(filtro_actual) > 0:
                filtro_actual = filtro_actual[:-1]
        # Caracteres válidos de texto imprimible
        elif ord(char) >= 32 and ord(char) <= 126:
            filtro_actual += char

def main():
    if len(sys.argv) < 2:
        print(f"{COLOR_WARN}Uso correcto: python3 search.py <archivo_datos>{COLOR_RESET}")
        sys.exit(1)

    ruta_archivo = sys.argv[1]

    # Mostrar Banner inicial
    mostrar_banner()

    # Cargar archivo usando mapeo de memoria eficiente
    archivo_obj, mm, lineas_offsets, ruta_archivo = parsear_archivo_gigante(ruta_archivo)

    # Activar motor de búsqueda interactivo
    try:
        buscador_tiempo_real(mm, lineas_offsets, ruta_archivo)
    except KeyboardInterrupt:
        sys.stdout.write("\033[H\033[2J")
        print("\n[!] Operación cancelada por el usuario.")
    finally:
        mm.close()
        archivo_obj.close()

if __name__ == "__main__":
    main()
