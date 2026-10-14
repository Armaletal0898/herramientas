

---

```markdown
# 🚀 High-Performance Multi-Format CLI Search Engine

Herramienta de análisis forense y búsqueda masiva de alto rendimiento desarrollada en **Python** para entornos **Linux**. Diseñada para procesar y filtrar archivos gigantescos (de varios Gigabytes) en tiempo real con un **consumo de memoria RAM casi nulo** gracias al mapeo de memoria (`mmap`) y punteros por bytes (`offsets`).

---

## 📋 Características Principales

* **Ahorro Masivo de RAM (`mmap`):** No carga archivos pesados completos en la memoria de Python; indexa únicamente las posiciones de bytes en disco para ofrecer una velocidad de respuesta inmediata.
* **Soporte Multi-Formato Universal:** Capaz de analizar y estructurar texto plano, `.txt`, `.csv`, `.json`, `.xml`, `.html`, reportes de red como `.nmap`, archivos `.log` y archivos sin extensión.
* **Búsqueda Dual Interactiva:** 
  * *Tiempo real:* Filtrado carácter por carácter sin necesidad de presionar *Enter* para consultas de texto comunes.
  * *Modo comandos:* Ejecución avanzada de comandos interactivos escribiendo un guion (`-`) y presionando *Enter*.
* **Modos de Búsqueda Avanzados:**
  * Expresiones Regulares (`regex:`)
  * Búsqueda Difusa / Tolerante a errores (`fuzzy:`)
  * Lógica Booleana (`AND`, `OR`, `NOT`)

---

## 🛠️ Requisitos del Sistema

* **Sistema Operativo:** Linux (Probado en Linux Mint / Ubuntu / Debian). Utiliza librerías nativas del sistema (`termios` y `tty`) para la captura de teclado de bajo nivel.
* **Python:** Versión 3.x (No requiere la instalación de dependencias externas o paquetes de terceros mediante `pip`).

---

## ⚙️ Instalación y Configuración

1. Clona el repositorio o descarga el script `search.py` en tu directorio de trabajo:
   ```bash
   git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
   cd tu-repositorio

```

2. Dale permisos de ejecución al script (opcional):
```bash
chmod +x search.py

```



---

## 💻 Uso

Ejecuta la herramienta pasando como argumento el archivo que deseas analizar:

```bash
python3 search.py <nombre_del_archivo>

```

### Ejemplos de uso:

```bash
python3 search.py syslogs.txt
python3 search.py escaneo_red.nmap
python3 search.py datos_usuarios.csv

```

---

## ⌨️ Guía de Comandos Interactivos

Mientras la herramienta esté activa, puedes utilizar los siguientes comandos especiales escribiendo un guion (`-`) y presionando **Enter**:

| Comando | Descripción | Ejemplo de Uso |
| --- | --- | --- |
| `-all` | Muestra el listado completo de las primeras líneas del archivo. | `-all` (Enter) |
| `-stats` | Despliega metadatos, tamaño exacto en disco y estado de indexación. | `-stats` (Enter) |
| `-export <archivo>` | Guarda todas las líneas/resultados actuales en un nuevo archivo de salida. | `-export reporte.txt` (Enter) |
| `-count` | Muestra el conteo total exacto de registros indexados en disco. | `-count` (Enter) |
| `-top <número>` | Cambia de forma dinámica el límite de resultados visibles en pantalla. | `-top 25` (Enter) |
| `-help` | Abre el panel de ayuda interactiva dentro de la terminal. | `-help` (Enter) |

---

## ⌨️ Atajos y Salida

* **Búsqueda de texto:** Simplemente escribe las palabras o letras que deseas filtrar; la terminal actualizará los resultados al instante carácter por carácter.
* **Salir de la aplicación:** Presiona la tecla **[ESC]** o la combinación **[Ctrl + C]** en cualquier momento para cerrar el programa de forma segura y liberar los recursos del sistema.

---

## 🛡️ Contribuciones y Licencia

Este proyecto es de código abierto. Si deseas proponer mejoras, optimizaciones de algoritmos o nuevos parsers de formatos, siembra una rama o abre un *Pull Request*.

```

```
