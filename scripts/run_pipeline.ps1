# run_pipeline.ps1

$projectRoot = Split-Path $PSScriptRoot -Parent

if (!(Test-Path "$projectRoot/logs")) {
    New-Item -ItemType Directory -Path "$projectRoot/logs" | Out-Null
}
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logFile = "$projectRoot/logs/run_$timestamp.jsonl"

# Función para formato JSONL
function Write-JsonLog {
    param (
        [string]$stage,
        [string]$status,
        [string]$message = ""
    )
    $entry = @{
        timestamp = (Get-Date).ToString("o")   # ISO 8601
        stage     = $stage
        status    = $status
        message   = $message
    }
    $json = $entry | ConvertTo-Json -Compress
    Add-Content -Path $logFile -Value $json
}

Write-Host "--- Inicio de Pipeline ---"
Write-JsonLog -stage "pipeline" -status "info" -message "Pipeline iniciado"

try {
    # 1. Adquisición de datos
    Write-Host "`n[1] Ejecutando adquisición..."
    Write-JsonLog -stage "acquisition" -status "info" -message "Ejecutando adquisición"

    $output1 = python -m src.acquisition.run_acquisition 2>&1
    Write-JsonLog -stage "acquisition" -status "info" -message "Salida run_acquisition.py: $output1"

    $output2 = python -m src.acquisition.get_network_info 2>&1
    Write-JsonLog -stage "acquisition" -status "info" -message "Salida get_network_info.py: $output2"

    # 2. Análisis con Python
    Write-Host "`n[2] Ejecutando análisis..."
    Write-JsonLog -stage "analysis" -status "info" -message "Ejecutando análisis con Python"

    $output3 = python -m src.analysis.process_data 2>&1
    Write-JsonLog -stage "analysis" -status "info" -message "Salida process_data.py: $output3"

    # 3. Generación de reporte con IA
    Write-Host "`n[3] Llamando al módulo de reporte con IA..."
    Write-JsonLog -stage "reporting" -status "info" -message "Generando reporte"

    $output4 = python -m src.reporting.generate_report 2>&1
    Write-JsonLog -stage "reporting" -status "info" -message "Salida generate_report.py: $output4"

    Write-Host "`nPipeline completado correctamente."
    Write-JsonLog -stage "pipeline" -status "ok" -message "Pipeline terminado"
}
catch {
    Write-Host "`nERROR durante la ejecución del pipeline" -ForegroundColor Red
    Write-JsonLog -stage "pipeline" -status "error" -message "Error en pipeline: $($_.Exception.Message)"
}
Write-Host "`n--- Fin del Pipeline ---"


    
}

Write-Host "`n--- Fin del Pipeline ---"
