<#
    get_files.ps1
    Escanea archivos en carpetas relevantes (Documentos, Escritorio, Descargas).
    Incluye tamaño, fecha de modificación y hash SHA256.
#>

# Carpetas a escanear
$paths = @(
    "$env:USERPROFILE\Documents",
    "$env:USERPROFILE\Desktop",
    "$env:USERPROFILE\Downloads"
)

# Calcular hash SHA256
function Get-FileHashSafe($filePath) {
    try {
        return (Get-FileHash -Path $filePath -Algorithm SHA256).Hash
    } catch {
        return "Error"
    }
}

# Recolectar archivos
try {
    $files = @()
    foreach ($path in $paths) {
        if (Test-Path $path) {
            $files += Get-ChildItem -Path $path -File -Recurse -ErrorAction SilentlyContinue |
            Select-Object `
                @{Name='Ruta'; Expression={$_.FullName}},
                @{Name='TamañoKB'; Expression={[math]::Round($_.Length / 1KB, 2)}},
                @{Name='ÚltimaModificación'; Expression={$_.LastWriteTime}},
                @{Name='HashSHA256'; Expression={Get-FileHashSafe $_.FullName}}
        }
    }
} catch {
    Write-Host "Error al obtener archivos: $($_.Exception.Message)"
    $files = @()
}

# Estructurar salida
$data = [PSCustomObject]@{
    FechaEjecucion = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    Usuario        = $env:USERNAME
    TotalArchivos  = $files.Count
    Archivos       = $files
}

# Crear carpeta 'raw' si no existe
$rawPath = Join-Path $PSScriptRoot "raw"
if (-not (Test-Path $rawPath)) {
    New-Item -ItemType Directory -Path $rawPath | Out-Null
}

# Guardar el JSON en esa carpeta
$jsonPath = Join-Path $rawPath "files_list.json"
try {
    $data | ConvertTo-Json -Depth 5 | Out-File -FilePath $jsonPath -Encoding utf8
    Write-Output "Archivo generado: $jsonPath"
} catch {
    Write-Host "Error al guardar archivo JSON: $($_.Exception.Message)"
}


