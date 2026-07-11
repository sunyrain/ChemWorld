$ErrorActionPreference = "Stop"

$PaperDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $PaperDir
$Python = Join-Path $Root ".venv\Scripts\python.exe"
if (-not (Test-Path $Python)) { $Python = "python" }

& $Python (Join-Path $Root "scripts\build_nature_figures.py")
& $Python (Join-Path $Root "scripts\audit_manuscript_claims.py") --allow-missing-pdf

$Tectonic = Get-Command tectonic -ErrorAction SilentlyContinue
if (-not $Tectonic) {
    $Fallback = Join-Path $env:TEMP "chemworld-tectonic\tectonic.exe"
    if (Test-Path $Fallback) { $Tectonic = Get-Item $Fallback }
}
if (-not $Tectonic) {
    throw "Tectonic 0.16+ is required. See https://tectonic-typesetting.github.io/book/latest/installation/"
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

& $Python (Join-Path $Root "scripts\audit_manuscript_claims.py")
