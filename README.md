Este es el archivo **README.md** profesional para tu herramienta. Está diseñado para que cualquier persona que visite tu repositorio entienda de inmediato qué hace el script, cómo instalarlo y, lo más importante, las precauciones de seguridad que debe tener.

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

Clona el repositorio o descarga el script y ejecútalo:

```bash
python encryptor.py

```


```bash
python encryptor.py

```

### 3. Pasos recomendados

1. **Opción 1:** Genera tu Clave Maestra. (Solo haz esto una vez, o perderás acceso a archivos cifrados con claves anteriores).
2. **Opción 2:** Ingresa la ruta del archivo que deseas proteger.
3. **Opción 3:** Usa la misma clave para restaurar tu archivo cuando lo necesites.

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



---

**¿Te gustaría que añadiera una sección sobre cómo automatizar el respaldo de la clave `secret.key` en una ubicación en la nube o externa?**
