
<img width="1885" height="589" alt="Captura de pantalla_20260214_230110" src="https://github.com/user-attachments/assets/73ee1795-bb01-4e32-9012-b59baa5c39f9" />

# Hash_History.txt
<img width="1873" height="376" alt="Captura de pantalla_20260214_230304" src="https://github.com/user-attachments/assets/d084bb00-0f6c-4f3d-83c7-e1f2d9857e5c" />

# 🛡️ HashView: Integrity Checker & Forensic Tool

**HashView** es una herramienta forense ligera escrita en Python diseñada para verificar la integridad de archivos mediante el cálculo de algoritmos de hashing criptográfico. Es ideal para analistas de malware, auditores de sistemas o cualquier usuario que necesite asegurar que un archivo no ha sido alterado.

## ✨ Características Principales

* **Multi-Algoritmo:** Calcula simultáneamente los hashes **MD5**, **SHA-1** y **SHA-256**.
* **Optimización de Memoria:** Utiliza lectura por bloques (`BUF_SIZE = 65536`) para procesar archivos de gran tamaño (GBs) sin saturar la memoria RAM.
* **Auditoría Automática:** Genera y mantiene un historial local en `hash_history.txt` para comparaciones futuras.
* **Interfaz Intuitiva:** Diseño visual en terminal con colores ANSI y arte ASCII para una mejor experiencia de usuario.
* **Limpieza Automática:** Detecta y corrige rutas de archivos cuando se arrastran directamente a la terminal (eliminando comillas automáticas).

---

## 🚀 Instalación y Uso

### Requisitos previos

Solo necesitas tener instalado **Python 3.x**. No requiere librerías externas (usa `hashlib` y `os` de la librería estándar).

### Clonar el repositorio

```bash
git clone -b hashview https://github.com/Armaletal0898/herramientas.git
cd herramientas

```

### Ejecución

Para iniciar la herramienta, simplemente corre el script:

```bash
python3 hash_check.py

```

---

## 🛠️ Funcionamiento Técnico

La herramienta utiliza la técnica de **Hashing**, que convierte datos de entrada de cualquier tamaño en una cadena de caracteres de longitud fija.

| Algoritmo | Seguridad | Uso Recomendado |
| --- | --- | --- |
| **MD5** | Baja (Obsoleto para seguridad) | Verificación rápida de errores de descarga. |
| **SHA-1** | Media-Baja | Compatibilidad con sistemas legados. |
| **SHA-256** | **Alta** | Verificación de integridad forense y seguridad. |

### Flujo de Trabajo:

1. **Entrada:** El usuario proporciona la ruta del archivo.
2. **Procesamiento:** El archivo se lee en pedazos de 64KB.
3. **Actualización:** Los motores de `hashlib` se actualizan incrementalmente.
4. **Salida:** Se muestran los resultados en pantalla y se guarda el SHA-256 en un log.

---

## 📁 Estructura del Proyecto

* `hash_check.py`: El código fuente principal.
* `hash_history.txt`: Archivo generado automáticamente que guarda el registro de auditoría.
* `README.md`: Documentación del proyecto.

---

## 🛡️ Notas de Seguridad

Aunque MD5 y SHA-1 son incluidos por compatibilidad y análisis forense, recuerda que para garantizar la integridad contra ataques deliberados (colisiones), siempre debes priorizar el resultado de **SHA-256**.

---


