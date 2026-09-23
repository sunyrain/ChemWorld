$ErrorActionPreference = 'Stop'
$figureRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$figurePpt = Join-Path $figureRoot 'output/pptx/chemworld-figures-final.pptx'
$figureTemp = Join-Path $env:TEMP 'chemworld-final-ppt'
$figureMetadata = Get-Content -Raw -Encoding UTF8 (Join-Path $figureRoot 'paper/figures/final-ppt/style-and-export.json') | ConvertFrom-Json
$figureCorrected = Join-Path $figureTemp 'native-final.pptx'
$figureHadApp = @(Get-Process -Name POWERPNT -ErrorAction SilentlyContinue).Count -gt 0
$figureApp = $null
$figurePresentation = $null
try {
    $figureApp = New-Object -ComObject PowerPoint.Application
    $figurePresentation = $figureApp.Presentations.Open($figurePpt, 0, 0, 0)
    $figureCharts = 0
    foreach ($figureSlide in $figurePresentation.Slides) {
        foreach ($figureShape in $figureSlide.Shapes) {
            if ($figureShape.HasChart -ne -1) { continue }
            $figureCharts++
            foreach ($figureSeries in $figureShape.Chart.SeriesCollection()) {
                if ($figureShape.Chart.ChartType -ne 51) { $figureSeries.Smooth = $false }
                if ($figureSeries.Name -eq 'Infeasible observations') {
                    $figureSeries.MarkerStyle = -4168
                    $figureSeries.MarkerSize = 6
                    $figureSeries.Format.Line.Visible = 0
                }
            }
        }
        Write-Output "ppt stage=native-style completed=$($figureSlide.SlideIndex)/11 charts=$figureCharts"
    }
    $figurePresentation.SaveCopyAs($figureCorrected,24)
} finally {
    if ($null -ne $figurePresentation) { $figurePresentation.Close(); [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($figurePresentation) }
    if ($null -ne $figureApp) { if (-not $figureHadApp) { $figureApp.Quit() }; [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($figureApp) }
}
Copy-Item -LiteralPath $figureCorrected -Destination $figurePpt -Force
$env:UV_CACHE_DIR = Join-Path $env:TEMP 'chemworld-uv-cache'
Push-Location $figureRoot
try {
    & uv run --no-sync python (Join-Path $PSScriptRoot 'finish_final_figure_exports.py') --style
    if ($LASTEXITCODE -ne 0) { throw 'Final marker styling failed' }
} finally { Pop-Location }
$figureApp = $null
$figurePresentation = $null
try {
    $figureApp = New-Object -ComObject PowerPoint.Application
    $figurePresentation = $figureApp.Presentations.Open($figurePpt,-1,0,0)
    for ($figureIndex=1; $figureIndex -le $figurePresentation.Slides.Count; $figureIndex++) {
        $figureName = $figureMetadata.figures[$figureIndex-1].name
        $figurePresentation.Slides.Item($figureIndex).Export((Join-Path $figureTemp "$figureName-full.png"),'PNG',4320,5700)
        Write-Output "ppt stage=native-export completed=$figureIndex/11 figure=$figureName"
    }
} finally {
    if ($null -ne $figurePresentation) { $figurePresentation.Close(); [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($figurePresentation) }
    if ($null -ne $figureApp) { if (-not $figureHadApp) { $figureApp.Quit() }; [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($figureApp) }
}
$env:UV_CACHE_DIR = Join-Path $env:TEMP 'chemworld-uv-cache'
Push-Location $figureRoot
try {
    & uv run --no-sync python (Join-Path $PSScriptRoot 'finish_final_figure_exports.py')
    if ($LASTEXITCODE -ne 0) { throw 'Final figure crop/export failed' }
} finally { Pop-Location }
