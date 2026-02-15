<img width="1881" height="696" alt="Captura de pantalla_20260215_124941" src="https://github.com/user-attachments/assets/f1927a43-e227-407e-95ab-dd2ac3be46ef" />


# 🛡️ Sentinel OS - Advanced System Monitor & Forensic Tool

**Sentinel OS** es una potente herramienta de monitoreo y análisis forense desarrollada en Python. Diseñada para analistas de seguridad y administradores de sistemas, permite auditar el estado del hardware, detectar conexiones de red sospechosas (posibles backdoors) y gestionar procesos críticos en tiempo real.

![Sentinel OS Banner](https://img.shields.io/badge/Version-1.3-cyan)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Características Principales

* **🔍 Análisis de Hardware:** Monitoreo en tiempo real del uso de CPU, RAM y almacenamiento con detalles técnicos del sistema.
* **🌐 Monitor Forense de Red:** Listado de conexiones activas (IPv4/IPv6). Resalta conexiones en estado `ESTABLISHED` para identificar posibles filtraciones de datos o backdoors.
* **🛡️ Escáner de Persistencia:** Analiza rutas críticas del sistema (`init.d`, `autostart`, `Startup`) para detectar scripts que se ejecutan automáticamente al iniciar el SO.
* **📋 Centro de Gestión de Procesos:** Un administrador de tareas integrado que ordena procesos por consumo de memoria y permite la terminación inmediata (Kill) mediante PID.
* **🎨 Interfaz UI/UX Estabilizada:** Diseñada para terminales modernas con colores ANSI y tablas estructuradas, eliminando el parpadeo de refresco constante.

---

## 🛠️ Instalación y Requisitos

Sentinel OS utiliza librerías de bajo nivel para interactuar con el kernel del sistema.

### Requisitos previos
* Python 3.x
* Pip (gestor de paquetes) --break-system-packages (por si pip no funciona)

### Instalación de dependencias
Ejecuta el siguiente comando en tu terminal:

```bash
pip install psutil tabulate

```

### Instalacion del repositorio
Ejecuta el siguiente comando en tu terminal:

git clone -b sentinel 




