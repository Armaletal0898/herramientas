import os
import wave
import json
import base64
from PIL import Image
import stepic

# --- MÓDULO DE IMAGEN ---
class EstegoImagen:
    def ocultar(self, ruta_img, ruta_data, salida):
        try:
            img = Image.open(ruta_img)
            with open(ruta_data, "rb") as f:
                secreto = f.read()
            img_encoded = stepic.encode(img, secreto)
            # Forzamos PNG para evitar pérdida de datos por compresión
            if not salida.lower().endswith('.png'):
                salida += ".png"
            img_encoded.save(salida)
            print(f"\n✅ Imagen creada: {salida}")
        except Exception as e:
            print(f"❌ Error en imagen: {e}")

    def extraer(self, ruta_img, salida_doc):
        try:
            img = Image.open(ruta_img)
            datos = stepic.decode(img)
            # En stepic, los datos pueden venir como string o bytes
            if isinstance(datos, str):
                datos = datos.encode()
            with open(salida_doc, "wb") as f:
                f.write(datos)
            print(f"\n🔓 Archivo extraído: {salida_doc}")
        except Exception:
            print("❌ No se encontró información oculta en esta imagen.")

# --- MÓDULO DE AUDIO ---
class EstegoAudio:
    def ocultar(self, ruta_wav, ruta_data, salida):
        try:
            audio = wave.open(ruta_wav, mode='rb')
            parms = audio.getparams()
            frames = bytearray(list(audio.readframes(audio.getnframes())))
            
            with open(ruta_data, "rb") as f:
                datos = f.read()
            
            # Delimitador para saber dónde termina el archivo real
            datos += b"##FIN##"
            bits = ''.join(format(byte, '08b') for byte in datos)

            if len(bits) > len(frames):
                print("❌ El audio es demasiado pequeño para este archivo.")
                return

            for i in range(len(bits)):
                frames[i] = (frames[i] & 254) | int(bits[i])

            with wave.open(salida, 'wb') as f:
                f.setparams(parms)
                f.write(frames)
            audio.close()
            print(f"\n✅ Audio creado: {salida}")
        except Exception as e:
            print(f"❌ Error en audio: {e}")

    def extraer(self, ruta_wav, salida_doc):
        try:
            audio = wave.open(ruta_wav, mode='rb')
            frames = bytearray(list(audio.readframes(audio.getnframes())))
            bits = [frames[i] & 1 for i in range(len(frames))]
            
            bytes_recup = bytearray()
            for i in range(0, len(bits), 8):
                byte = bits[i:i+8]
                if len(byte) < 8: break
                bytes_recup.append(int(''.join(map(str, byte)), 2))

            resultado = bytes_recup.split(b"##FIN##")[0]
            with open(salida_doc, "wb") as f:
                f.write(resultado)
            audio.close()
            print(f"\n🔓 Archivo extraído del audio: {salida_doc}")
        except Exception:
            print("❌ Error al procesar el audio.")

# --- ANALIZADOR FORENSE ---
def analizador(ruta):
    print(f"\n--- 🔍 ESCANEO DE SEGURIDAD: {os.path.basename(ruta)} ---")
    size = os.path.getsize(ruta)
    print(f"📦 Tamaño: {size / 1024:.2f} KB")
    
    with open(ruta, "rb") as f:
        f.seek(0)
        contenido = f.read()
        
        # Detección de firmas (Magic Bytes) anidadas
        alertas = 0
        firmas = {
            b"%PDF": "Documento PDF",
            b"PK\x03\x04": "Archivo comprimido (ZIP/DOCX/XLSX)",
            b"\x89PNG\x0d\x0a\x1a\x0a": "Imagen PNG",
            b"\xff\xd8\xff": "Imagen JPEG"
        }
        
        for firma, tipo in firmas.items():
            # Buscamos la firma después de los primeros 100 bytes (donde no debería estar)
            if firma in contenido[100:]:
                print(f"⚠️ ALERTA: Se encontró un {tipo} oculto dentro del archivo.")
                alertas += 1
        
        if alertas == 0:
            print("✅ No se detectaron archivos anidados obvios.")
        print("-" * 40)

# --- INTERFAZ PRINCIPAL ---
def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    img_tool = EstegoImagen()
    aud_tool = EstegoAudio()

    while True:
        limpiar()
        print("========================================")
        print("   🎭 ESTEGOMASTER: SUITE INVISIBLE  ")
        print("========================================")
        print("1. 🖼️ OCULTAR en Imagen (PNG)")
        print("2. 🎵 OCULTAR en Audio (WAV)")
        print("3. 🔓 EXTRAER de Imagen")
        print("4. 🔓 EXTRAER de Audio")
        print("5. 🔍 ANALIZAR Archivo (Steganalysis)")
        print("6. 🚪 Salir")
        
        op = input("\nSelecciona una opción: ")

        if op == "1":
            while True:
                limpiar()
                img = input("Imagen portadora: ")
                sec = input("Archivo secreto (.txt, .pdf, .docx): ")
                out = input("Nombre de salida (ej: secreto.png): ")
                img_tool.ocultar(img, sec, out)
                if input("\n¿Otro? (s/n): ").lower() != 's': break

        elif op == "2":
            while True:
                limpiar()
                wav = input("Audio portador (.wav): ")
                sec = input("Archivo secreto: ")
                out = input("Nombre de salida (.wav): ")
                aud_tool.ocultar(wav, sec, out)
                if input("\n¿Otro? (s/n): ").lower() != 's': break

        elif op == "3":
            limpiar()
            img = input("Imagen con el secreto: ")
            out = input("Nombre del archivo a recuperar (ej: datos.pdf): ")
            img_tool.extraer(img, out)
            input("\nPresiona ENTER para volver...")

        elif op == "4":
            limpiar()
            wav = input("Audio con el secreto: ")
            out = input("Nombre del archivo a recuperar: ")
            aud_tool.extraer(wav, out)
            input("\nPresiona ENTER para volver...")

        elif op == "5":
            limpiar()
            arch = input("Archivo a analizar: ")
            analizador(arch)
            input("\nPresiona ENTER para volver...")

        elif op == "6":
            print("\nCerrando herramientas... Mantente invisible.")
            break

if __name__ == "__main__":
    main()
