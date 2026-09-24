$ErrorActionPreference = 'Stop'
$caseRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$casePpt = Join-Path $caseRoot 'output/pptx/chemworld-figure2-typography.pptx'
$caseTemp = Join-Path $env:TEMP 'chemworld-case-typography'
New-Item -ItemType Directory -Path $caseTemp -Force | Out-Null
$caseHadApp = @(Get-Process -Name POWERPNT -ErrorAction SilentlyContinue).Count -gt 0
$caseApp = $null
$casePresentation = $null
try {
    $caseApp = New-Object -ComObject PowerPoint.Application
    $casePresentation = $caseApp.Presentations.Open($casePpt,0,0,0)
    foreach ($caseShape in $casePresentation.Slides.Item(1).Shapes) {
        if ($caseShape.HasChart -ne -1) { continue }
        foreach ($caseSeries in $caseShape.Chart.SeriesCollection()) { $caseSeries.Smooth = $false }
    }
    $casePresentation.Save()
} finally {
    if ($null -ne $casePresentation) { $casePresentation.Close(); [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($casePresentation) }
    if ($null -ne $caseApp) { if (-not $caseHadApp) { $caseApp.Quit() }; [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($caseApp) }
}
$env:UV_CACHE_DIR = Join-Path $env:TEMP 'chemworld-ncs-preview-uv-cache'
Push-Location $caseRoot
try {
    & uv run --no-sync python paper/tools/finish_final_figure_exports.py --style --pptx $casePpt --regular-chart-text
    if ($LASTEXITCODE -ne 0) { throw 'Case marker styling failed' }
} finally { Pop-Location }
$caseApp = $null
$casePresentation = $null
try {
    $caseApp = New-Object -ComObject PowerPoint.Application
    $casePresentation = $caseApp.Presentations.Open($casePpt,-1,0,0)
    $casePresentation.Slides.Item(1).Export((Join-Path $caseTemp 'figure2-full.png'),'PNG',4320,3480)
    Write-Output 'case stage=native-export completed=1/1'
} finally {
    if ($null -ne $casePresentation) { $casePresentation.Close(); [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($casePresentation) }
    if ($null -ne $caseApp) { if (-not $caseHadApp) { $caseApp.Quit() }; [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($caseApp) }
}
Push-Location $caseRoot
try {
    & uv run --no-sync python -c "from PIL import Image; from pathlib import Path; import tempfile; t=Path(tempfile.gettempdir())/'chemworld-case-typography'; im=Image.open(t/'figure2-full.png'); assert im.size==(4320,3480), im.size; im.save('paper/figures/final-ppt/figure02-research-paths-typography.png'); im.thumbnail((1440,1160)); im.save(t/'preview.png')"
    if ($LASTEXITCODE -ne 0) { throw 'Case figure crop failed' }
} finally { Pop-Location }
