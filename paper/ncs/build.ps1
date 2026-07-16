$ErrorActionPreference = "Stop"

$PaperDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent (Split-Path -Parent $PaperDir)
$Python = Join-Path $Root ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $Python)) { $Python = "python" }

& $Python (Join-Path $Root "scripts\audit_ncs_manuscript.py") --allow-missing-pdf
if ($LASTEXITCODE -ne 0) { throw "NCS manuscript pre-build audit failed" }

$Tectonic = Get-Command tectonic -ErrorAction SilentlyContinue
if (-not $Tectonic) {
    $Fallback = Join-Path $env:TEMP "chemworld-tectonic\tectonic.exe"
    if (Test-Path -LiteralPath $Fallback) { $Tectonic = Get-Item -LiteralPath $Fallback }
}
if (-not $Tectonic) {
    throw "Tectonic 0.16+ is required"
}

Push-Location $PaperDir
try {
    New-Item -ItemType Directory -Force build | Out-Null
    & $Tectonic.FullName main.tex --outdir build --keep-logs --keep-intermediates
    if ($LASTEXITCODE -ne 0) { throw "Tectonic failed with exit code $LASTEXITCODE" }
    Copy-Item build\main.pdf main.pdf -Force
} finally {
    Pop-Location
}

& $Python (Join-Path $Root "scripts\audit_ncs_manuscript.py")
if ($LASTEXITCODE -ne 0) { throw "NCS manuscript post-build audit failed" }

