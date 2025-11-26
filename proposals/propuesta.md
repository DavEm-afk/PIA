### Este archivo representa la estructura inicial del proyecto. Avanzando en la creacion del proyecto se presentaron diversas modificaciones a las ideas originales.
---
# Sistema de Análisis Forense Automatizado para Windows

## Título
**Sistema de Análisis Forense Automatizado para Windows**

## Descripción general del proyecto
Este proyecto es una solución sencilla para la recolección, análisis y documentación de evidencias en equipos con sistema operativo Windows. En el proyecto se integran scripts de PowerShell para la adquisición de artefactos propios del sistema y módulos en Python para el procesamiento, comparación y análisis de los datos obtenidos. Finalmente, se hace uso de OpenAI API para enriquecer y redactar un informe detallado usando como base los hallazgos recaudados con Python.

El flujo planteado para este proyecto es el siguiente: **Adquisición → Análisis/Comparación → Uso de IA → Reporte.**

---

## Fichas técnicas de las tareas

### Tarea 1 — Adquisición de artefactos del sistema
**Título y propósito**  
Recolección de artefactos en el sistema Windows que sirvan para generar una base de evidencias que pueda ser analizado con fin a respuesta de incidentes.

**Función / Rol**  
DFIR — Evidence Acquisition

**Entradas esperadas**  
- Ninguna entrada externa requerida (colección local).  
- Parámetros opcionales: lista de rutas a inspeccionar (JSON), rango temporal para logs.

**Salidas esperadas**  
- `/src/acquisition/raw/process_list.json` (lista de procesos con metadata)  
- `/src/acquisition/raw/net_connections.json` (conexiones TCP/UDP actuales)  
- `/src/acquisition/raw/event_logs.evtx` o exportación en JSON `/src/acquisition/raw/event_logs.json`

**Descripción del procedimiento**  
Se ejecutan scripts PowerShell que: enumeran procesos (`Get-Process`), listan conexiones de red (`Get-NetTCPConnection`), extraen eventos relevantes del Visor de Eventos (Sistema/Seguridad/Aplicación) y listan servicios y tareas programadas. Las salidas se normalizan y guardan como JSON para su posterior análisis.

**Complejidad técnica**  
- Procesamiento/parsing de salidas (evtx → JSON)  
- Automatización básica (scripts PS + wrapper en Python)  
- Uso de librerías (p. ej. `xml.etree`, `json` en Python)

**Controles éticos**  
- Recolección en ambientes autorizados o con datos sintéticos.  
- No se recopilarán credenciales ni datos personales identificables.  
- Se documenta autoría y consentimiento de pruebas en `docs/ethical_controls.md`.

**Dependencias**  
- PowerShell (Windows 10/11)  
- Python 3.10+ (wrapper)  

---

### Tarea 2 — Verificación de integridad de archivos mediante hashing
**Título y propósito**  
Calcular y comparar hashes criptográficos (SHA-256) de archivos críticos para detectar modificaciones no autorizadas y conservar evidencia de integridad.

**Función / Rol**  
DFIR — Integrity Analysis

**Entradas esperadas**  
- Lista de rutas a verificar (`/src/analysis/config/targets.json`) — formato JSON con ejemplos.  
- Opcional: base de referencia de hashes `src/analysis/reference_hashes.json`

**Salidas esperadas**  
- `/reporting/findings_hashes.csv` (archivo, ruta, hash_actual, hash_referencia, estado)  
- `/src/analysis/results/hashes.json`

**Descripción del procedimiento**  
PowerShell o Python enumeran los archivos objetivo; Python calcula SHA-256 para cada archivo y compara con la base de referencia cuando exista. Se genera un CSV/JSON con el estado (unchanged / modified / new / missing).

**Complejidad técnica**  
- Uso de librerías para manipulación de archivos (`hashlib`, `os`, `pathlib`)  
- Correlación mínima contra una base de datos local de hashes  
- Automatización de procesos (invocación desde pipeline)

**Controles éticos**  
- No se transfieren archivos sensibles fuera del entorno controlado.  
- Los hashes no contienen datos del archivo (solo valores resumidos).  
- Se usan archivos de prueba/sintéticos en entornos de evaluación.

**Dependencias**  
- Python 3.10+ (`hashlib`, `pandas` recomendado)  

---

### Tarea 3 — Adquisición extendida de red
**Título y propósito**  
Ampliar la adquisición de artefactos del sistema incorporando información sobre las conexiones de red activas y su relación con los procesos en ejecución.
El objetivo es permitir una correlación temprana entre actividad de procesos y tráfico de red, facilitando la detección de comportamientos anómalos o sospechosos en etapas posteriores del análisis.

**Función / Rol**  
DFIR — Network & Process Correlation Analyst

**Entradas esperadas**  
- Sistema local en ejecución (requiere permisos de lectura de procesos y sockets).
- Módulo psutil para enumerar procesos y conexiones.
- Configuración de ruta de salida (/src/acquisition/raw/).

**Salidas esperadas**  
- /src/acquisition/raw/process_network.json — Lista de procesos con conexiones activas (TCP/UDP).
- /src/acquisition/raw/net_connections.json — Conexiones globales del sistema.
- /logs/acquisition_net_<timestamp>.log — Registro de ejecución y errores.

**Descripción del procedimiento**  
Enumerar todos los procesos con psutil.process_iter() y recopilar metadatos básicos, despues, para cada proceso, obtener sus conexiones activas mediante proc.connections(kind='inet'). Extraer información de cada conexión para al final: asociar las conexiones encontradas al proceso correspondiente y serializar la información en JSON.

**Complejidad técnica**  
- Enumeración y correlación de procesos con sockets de red.
- Manejo de permisos y errores de acceso a procesos del sistema.
- Serialización de datos anidados en estructuras JSON legibles.
- Posible extensión futura: geolocalización o clasificación de IPs externas.

**Controles éticos**  
- Los datos recolectados deben provenir de sistemas propios o entornos de práctica.
- Las direcciones IP externas serán anonimizadas o truncadas en ejemplos públicos.
- No se realizará tráfico activo ni escaneo de red, solo observación pasiva de conexiones.

**Dependencias**  
- Python 3.10+
- psutil
- json / logging

---

## Estructura inicial del repositorio
Estructura del repositorio:
- /src
  - /acquisition
    - README.md
    - ps_acquire_system.ps1
  - /analysis
    - README.md
    - hash_check.py
    - ioc_detector.py
    - config/
    - targets.json
    - iocs.json
  - /integration
    - README.md
    - orchestration.py # wrapper que orquesta PS ↔ Python y llamadas IA
  - /reporting
    - README.md
    - findings.csv
    - findings.json
    - executive_summary.md
  - /utils
    - README.md
    - logger.py
- /scripts
  - run_pipeline.ps1
  - run_pipeline.sh
  - /prompts
  - report_prompt_v1.txt
- /docs
  - ethical_controls.md
  - schema.md
- /examples
  - anon_example_output.json
  - /tests
    - test_hash_check.py
    - README.md
- /proposals
  - propuesta.md
- /.gitignore

**Outputs obligatorios**  
- `/reporting/findings.json` o `/reporting/findings.csv`  
- `/reporting/executive_summary.md`  
- `/logs/run_<timestamp>.log`  
- `/prompts/report_prompt_v1.txt`

---

## Asignación de roles del equipo

- **David Emiliano Rangel Tovar — Adquisición y Orquestación**  
  - Responsable de `/src/acquisition/` y `run_pipeline.ps1`  
  - Implementa y prueba los scripts PowerShell para recolección de artefactos  
  - Colabora en el wrapper de orquestación para invocar los módulos Python

- **Marcelo Hernandez Chavez — Análisis y Reporte**  
  - Responsable de `/src/analysis/`, `/src/integration/` y `/src/reporting/`  
  - Implementa cálculo de hashes, detectores de IoCs y la integración con OpenAI API  
  - Prepara `executive_summary.md` final y save prompts en `/prompts/`

---

## Declaración ética y legal
- El desarrollo y las pruebas se realizarán exclusivamente en entornos controlados y con datos sintéticos o con equipos autorizados por sus propietarios.  
- No se utilizarán ni se subirán a GitHub claves privadas, credenciales reales ni información personal identificable (PII). Las claves para la OpenAI API se almacenarán mediante variables de entorno (ej. `OPENAI_API_KEY`) y no se versionarán en el repositorio.  
- Se documentará en `/docs/ethical_controls.md` el consentimiento, límites de prueba y las mitigaciones tomadas para evitar uso indebido.

---

## Dependencias y requisitos técnicos
**Python**  
- Python 3.10+  
- Dependencias sugeridas: `pandas`, `requests`, `openai`, `python-dotenv`, `tenacity`, `psutil`, `hashlib` (builtin)  
- Packaging: PyInstaller

**PowerShell**  
- PowerShell 5+ / PowerShell Core en Windows  
- No se requieren módulos externos obligatorios.

