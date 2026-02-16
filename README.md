
<img width="1880" height="859" alt="Captura de pantalla_20260216_004203" src="https://github.com/user-attachments/assets/6b8141a3-b9b4-4bea-8256-7558283c452b" />

<img width="1920" height="1080" alt="Captura de pantalla_20260216_004346" src="https://github.com/user-attachments/assets/fe0ba2cd-250c-4e36-9390-7327992d98de" />

<img width="1877" height="809" alt="Captura de pantalla_20260216_004552" src="https://github.com/user-attachments/assets/b9c12b8a-2efe-4773-a4d3-ee1300011e3d" />

<img width="1920" height="1080" alt="Captura de pantalla_20260216_004625" src="https://github.com/user-attachments/assets/a61254a1-a291-443b-94a1-a42f544e3dac" />

<img width="1888" height="905" alt="Captura de pantalla_20260216_004711" src="https://github.com/user-attachments/assets/8d48299a-1691-48e4-9ff9-89584df25699" />






---

# 🔐 ENCRYPTOR - AES-256 File Encryption System


**ENCRYPTOR** es una herramienta de ciberseguridad desarrollada en Python que permite cifrar y descifrar archivos de forma segura utilizando el estándar **AES-256** (a través de la implementación Fernet). Es ideal para proteger información sensible localmente con un sistema de grado militar.

---

## ✨ Características Principales

* **Cifrado Simétrico AES-256:** Utiliza una única clave robusta para transformar tus archivos en datos ilegibles.
* **Gestión de Claves:** Genera automáticamente una clave maestra segura (`secret.key`).
* **Integridad de Datos:** Gracias a Fernet, el script detecta si el archivo cifrado ha sido manipulado y evita el descifrado si los datos están corruptos.
* **Sistema de Logs:** Registro automático de todas las operaciones en `crypto_log.txt` para auditoría de seguridad.
* **Interfaz CLI:** Menú interactivo con colores y arte ASCII para una experiencia de usuario fluida.

---

## 🛠️ Cómo funciona

El script se basa en la **criptografía simétrica**. Esto significa que se utiliza la misma clave tanto para "cerrar" (cifrar) como para "abrir" (descifrar) el archivo.

### El Proceso:

1. **Generación:** Se crea una clave aleatoria de 32 bytes codificada en Base64.
2. **Cifrado:** El archivo se lee en modo binario, se le añade un IV (Vector de Inicialización) y se cifra. El archivo original es reemplazado por la versión cifrada.
3. **Descifrado:** Se verifica la clave, se valida la integridad (HMAC) y se restaura el archivo original.

---

## 🚀 Instalación y Uso

### 1. Requisitos previos

Necesitas tener Python instalado y la librería `cryptography`:

```bash
pip install cryptography

```

### 2. Ejecución

Clona el repositorio o descarga el script:

```bash
git clone -b encryptor https://github.com/Armaletal0898/herramientas.git
cd herramientas


```
Ejecutalo:


```bash
python encryptor.py

```

### 3. Pasos recomendados

1. **Opción 1:** Genera tu Clave Maestra dentro del directorio en donde esta el archivo que quieres encryptar. (Solo haz esto una vez, o perderás acceso a archivos cifrados con claves anteriores).
2. **Opción 2:** Ingresa el nombre del archivo con su extension estando dentro del directorio del archivo.
3. **Opción 3:** Usa la misma clave para restaurar tu archivo cuando lo necesites.

##  NOTA:

> **PUNTO IMPORTANTE:** Sugiero que crees una carpeta en donde vayas a guardar los archivos que quieras encryptar y la `secret.key` como tambien el `crypto_log.txt`. 


---

## 📂 Archivos del Proyecto

| Archivo | Descripción |
| --- | --- |
| `encryptor.py` | El script principal del sistema. |
| `secret.key` | **CRÍTICO:** La llave maestra. Si se pierde, no hay forma de recuperar los datos. |
| `crypto_log.txt` | Historial de actividades con fecha y hora. |

---

## ⚠️ Advertencias de Seguridad

> [!CAUTION]
> **PÉRDIDA DE CLAVE:** El cifrado AES-256 es computacionalmente imposible de romper por fuerza bruta hoy en día. Si pierdes o borras el archivo `secret.key`, tus archivos cifrados quedarán bloqueados para siempre. **Haz una copia de seguridad de tu clave en un lugar seguro.**

---


