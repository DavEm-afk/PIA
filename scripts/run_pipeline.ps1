# run_pipeline.ps1 

$timestamp = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
if (!(Test-Path "logs")) { New-Item -ItemType Directory -Path "logs" | Out-Null }
$logFile = "logs/run_$timestamp.log"


Write-Host "--- Inicio de Pipeline ---" 
"[INFO] [$(Get-Date)] Pipeline iniciado" | Add-Content $logFile  

try {

    # --- 
    # 1. Adquisición de datos 
    
    Write-Host "`n[1] Ejecutando adquisición..." 
    "[INFO] [$(Get-Date)] Ejecutando adquisición" | Add-Content $logFile 
    
    # Llama a los scripts .ps1 para obtener informacion de archivos y procesos
    Add-Content $logFile "`n- Salida run_acquisition.py"
    $output1 = python3 "src/acquisition/run_acquisition.py" 2>&1 
    $output1 | Add-Content $logFile  
    
    Add-Content $logFile "`n- get_network_info.py"
    $output2 = python3 "src/acquisition/get_network_info.py" 2>&1
    $output2 | Add-Content $logFile


    # --- 
    # 2. Análisis con Python 
    
    Write-Host "`n[2] Ejecutando análisis..."
    "[INFO] [$(Get-Date)] Ejecutando análisis con Python" | Add-Content $logFile 
    
    Add-Content $logFile "`n- Salida process_data.py"
    $output3 = python3 "src/analysis/process_data.py" 2>&1 # Analisis/filtrado de datos 
    $output3 | Add-Content $logFile


    # --- 
    # 3. Generación de reporte con IA 
    
    Write-Host "`n[3] Llamando al módulo de reporte con IA..." 
    "[INFO] [$(Get-Date)] Generando reporte" | Add-Content $logFile 
    
    Add-Content $logFile "`n- Salida generate_report.py"
    $output4 = python3 "src/reporting/generate_report.py" 2>&1 # Llamado de API y generacion de reporte 
    $output4 | Add-Content $logFile

    Write-Host "`nPipeline completado correctamente." 
    "[OK] [$(Get-Date)] Pipeline terminado" | Add-Content $logFile  
    
} 
    
catch { 

    Write-Host "`nERROR durante la ejecución del pipeline" -ForegroundColor Red 

    Add-Content $logFile "[ERROR] $(Get-Date) Error en pipeline"
    Add-Content $logFile "Mensaje: $($_.Exception.Message)"
    Add-Content $logFile "StackTrace: $($_.ScriptStackTrace)"
    
} 
    
Write-Host "`n--- Fin del Pipeline ---"
