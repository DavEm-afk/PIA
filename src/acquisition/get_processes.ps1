<#
    get_processes.ps1
    Obtiene la lista de procesos activos con información básica.
    Genera salida JSON estructurada.
#>

# Obtener procesos activos
try {
    $processes = Get-Process | Select-Object `
        @{Name='Nombre'; Expression={$_.ProcessName}},
        @{Name='ID'; Expression={$_.Id}},
        @{Name='CPU'; Expression={$_.CPU}},
        @{Name='MemoriaMB'; Expression={[math]::Round($_.WorkingSet / 1MB, 2)}},
        @{Name='Usuario'; Expression={
            try {
                (Get-WmiObject Win32_Process -Filter "ProcessId=$($_.Id)").GetOwner().User
            } catch { "Sistema" }
        }},
        @{Name='RutaEjecutable'; Expression={
            try {
                (Get-Process -Id $_.Id -ErrorAction Stop).Path
            } catch { "Desconocida" }
        }}
    
} catch {
    Write-Host "Error al obtener procesos: $($_.Exception.Message)"
    $processes = @()
}

# Estructurar salida
$data = [PSCustomObject]@{
    FechaEjecucion = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    Usuario        = $env:USERNAME
    TotalProcesos  = $processes.Count
    Procesos       = $processes
}

# Crear carpeta 'raw' si no existe
$rawPath = Join-Path $PSScriptRoot "raw"
if (-not (Test-Path $rawPath)) {
    New-Item -ItemType Directory -Path $rawPath | Out-Null
}

# Definir la ruta de salida
$jsonPath = Join-Path $rawPath "process_list.json"

# Guardar el JSON en carpeta 'raw'
try {
    $data | ConvertTo-Json -Depth 5 | Out-File -FilePath $jsonPath -Encoding utf8
    Write-Output "Archivo generado: $jsonPath"
} catch {
    Write-Host "Error al guardar archivo JSON: $($_.Exception.Message)"
}
