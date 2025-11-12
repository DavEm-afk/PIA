# Sistema de Análisis Forense Automatizado para Windows

### Descripción general del proyecto
Este proyecto es una solución sencilla para la recolección, análisis y documentación de evidencias en equipos con sistema operativo Windows. En el proyecto se integran scripts de PowerShell para la adquisición de artefactos propios del sistema y módulos en Python para el procesamiento, comparación y análisis de los datos obtenidos. Finalmente, se hace uso de OpenAI API para enriquecer y redactar un informe detallado usando como base los hallazgos recaudados con Python.  
### Entregable 2

Dentro del **entregable número 2** del proyecto se completó la **tarea número 1**, relacionada principalmente con la **adquisición de datos**.  

Además, se busca agregar como **tercera tarea** el **análisis de conexiones de red**, siendo un añadido al análisis general que se busca generar con el proyecto, especialmente enfocado en los **procesos**.

---

Se agregó la Tarea 3 (adquisición extendida de red) en `/src/acquisition/get_network_info.py`, que obtiene información de conexiones TCP/UDP activas y las asocia con los procesos en ejecución.
