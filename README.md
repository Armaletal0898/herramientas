
<img width="1879" height="449" alt="Captura de pantalla_20260215_001011" src="https://github.com/user-attachments/assets/3f20c20b-cc5f-4dcd-a216-dd41520c28ca" />


# 📦 Descompres-2026

**Descompres Master** es una interfaz de línea de comandos (CLI) potente y simplificada para la gestión de archivos comprimidos. Utiliza el motor de `patoollib` para soportar casi cualquier formato de compresión existente sin que el usuario tenga que recordar comandos complejos.

---

## ✨ Características Principales

* **Soporte Multi-Formato:** Gracias a `patool`, maneja `.zip`, `.7z`, `.rar`, `.tar.gz`, `.bz2`, `.xz` y muchos más.
* **Detección Inteligente:** Solo necesitas escribir la extensión deseada al comprimir y la herramienta seleccionará el algoritmo adecuado automáticamente.
* **Extracción Organizada:** Crea automáticamente una carpeta de destino basada en el nombre del archivo original para evitar el desorden de archivos sueltos.
* **Interfaz Visual:** Banner personalizado en ASCII y uso de códigos de colores ANSI para una navegación clara en la terminal.

---

## 🛠️ Requisitos Técnicos

Para que esta herramienta funcione correctamente, necesitas:

1. **Python 3.x** instalado.
2. La librería **patool**:
```bash
pip install patool

```


3. **Herramientas de sistema:** `patool` es un "wrapper", lo que significa que utiliza los programas instalados en tu sistema (como `unzip`, `7z`, `tar`). Asegúrate de tener instalados los que necesites usar.

---

## 🚀 Guía de Uso

### 1. Clonar y Preparar

```bash
git clone -b descompres https://github.com/Armaletal0898/herramientas.git
cd herramietas

```

### 2. Ejecutar

```bash
python3 descompres.py

```

### 3. Opciones del Menú

* **[1] Descomprimir:** Ingresa el nombre del archivo. Se creará una carpeta llamada `nombre_extraido/` con el contenido.
* **[2] Comprimir:** Ingresa el nombre de la carpeta/archivo origen y luego el nombre del archivo final con su extensión (ejemplo: `mi_web.7z`).

---

## 📂 Estructura del Código

| Función | Descripción |
| --- | --- |
| `mostrar_banner()` | Limpia la pantalla y despliega el arte visual. |
| `comprimir()` | Maneja la creación de nuevos archivos comprimidos. |
| `descomprimir()` | Gestiona la extracción y creación de directorios de salida. |
| `menu()` | Lógica principal de interacción con el usuario. |

---

## ⚠️ Notas Importantes

> [!TIP]
> Si intentas descomprimir archivos `.rar` y recibes un error, asegúrate de tener instalado `unrar` o `7zip` en tu sistema operativo, ya que `patool` los invoca internamente.

---

