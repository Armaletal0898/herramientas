
<img width="1881" height="991" alt="Captura de pantalla_20260216_003648" src="https://github.com/user-attachments/assets/9510ad91-25cc-41d3-92bb-04f2f5c77ed5" />



---

# 🔑 Passecure: Generator & Analyzer

**Passecure** es una herramienta de ciberseguridad defensiva diseñada para generar contraseñas criptográficamente seguras y auditar su fortaleza mediante el cálculo de entropía en bits. A diferencia de los generadores estándar, esta herramienta utiliza el módulo `secrets` de Python, ideal para aplicaciones donde la seguridad es crítica.

---

## ✨ Características Principales

* **Generación Segura:** Utiliza `secrets.choice` para asegurar que las contraseñas sean impredecibles (fuente de aleatoriedad del SO).
* **Análisis de Entropía:** Calcula la fuerza real de una contraseña basándose en el tamaño del conjunto de caracteres y su longitud.
* **Clasificación de Riesgo:** Categoriza las contraseñas desde "Muy Débil" hasta "Muy Fuerte" con tiempos estimados de crackeo.
* **Auditoría Local:** Registro automático de todas las operaciones en un historial (`password_history.txt`) con marcas de tiempo.
* **Interfaz Colorida:** Menú interactivo en terminal con códigos de colores ANSI para una mejor experiencia de usuario.

---

## 🛠️ Fundamentos Técnicos: ¿Qué es la Entropía?

La seguridad de una contraseña no solo depende de lo "rara" que sea, sino de su **entropía en bits**. Esta herramienta utiliza la fórmula:

E=L⋅log2​(R)

Donde:

* L: Longitud de la contraseña.
* R: Tamaño del conjunto de caracteres (letras, números, símbolos).

### Niveles de Seguridad en la Herramienta:

| Entropía (Bits) | Nivel de Seguridad | Tiempo de Crackeo (Aprox.) |
| --- | --- | --- |
| **< 40** | 🔴 Muy Débil | Instantáneo |
| **40 - 59** | 🟡 Media | Días / Meses |
| **60 - 79** | 🟢 Fuerte | Años |
| **> 80** | 🔵 Muy Fuerte | Siglos |

---

## 🚀 Instalación y Uso

### Requisitos

* Python 3.6 o superior.
* No requiere librerías externas (solo módulos nativos: `os`, `secrets`, `string`, `math`).

### Ejecución

1. Clona este repositorio en la terminal:

```bash
git clone -b passecure https://github.com/Armaletal0898/herramientas.git
cd herramientas

```

2. Abre una terminal en la carpeta del archivo.
3. Ejecuta el script:

```bash
python3 passecure.py

```



---

## 📂 Estructura del Proyecto

* `passecure.py`: Script principal con el generador y analizador.
* `password_history.txt`: Archivo generado automáticamente que almacena el historial de auditoría.

---

## 🛡️ Notas de Seguridad

El generador utiliza el módulo `secrets`, el cual es preferible al módulo `random` de Python para aplicaciones de seguridad, ya que `secrets` está diseñado para ser criptográficamente fuerte y resistente a la predicción.

---



