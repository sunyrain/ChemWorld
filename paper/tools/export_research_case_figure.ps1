$ErrorActionPreference = 'Stop'
$figureRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$figurePptPath = Join-Path $figureRoot 'output\pptx\c-w05-research-paths-v16.pptx'
$figureDirectory = Join-Path $figureRoot 'output\figures\research-case-v16'
$figureTemp = Join-Path $env:TEMP 'chemworld-research-case-v16'
$figureCorrectedPath = Join-Path $figureTemp 'native-corrected.pptx'
$figureApp = $null
$figurePresentation = $null
$figureHadApp = @(Get-Process -Name POWERPNT -ErrorAction SilentlyContinue).Count -gt 0
try {
    Write-Output 'figure stage=PowerPoint-open completed=0/1'
    $figureApp = New-Object -ComObject PowerPoint.Application
    $figurePresentation = $figureApp.Presentations.Open($figurePptPath, 0, 0, 0)
    $figureChartCount = 0
    foreach ($figureShape in $figurePresentation.Slides.Item(1).Shapes) {
        if ($figureShape.HasChart -ne -1) { continue }
        $figureChartCount++
        $figureChart = $figureShape.Chart
        # PowerPoint repairs the exported chart style on import. Set these scientific
        # display properties explicitly in the native application before saving.
        $figureChart.ChartType = 74 # xlXYScatterLines: straight segments
        for ($figureSeriesIndex = 1; $figureSeriesIndex -le $figureChart.SeriesCollection().Count; $figureSeriesIndex++) {
            $figureSeries = $figureChart.SeriesCollection($figureSeriesIndex)
            $figureSeries.Smooth = $false
            if ($figureSeriesIndex -eq 4) {
                $figureSeries.MarkerStyle = -4168 # xlMarkerStyleX
                $figureSeries.MarkerSize = 7
                $figureSeries.Format.Line.Visible = 0
            } elseif ($figureSeriesIndex -eq 3) {
                $figureSeries.MarkerStyle = 8 # circle
                $figureSeries.MarkerSize = 7
                $figureSeries.Format.Line.Visible = 0
            } else {
                $figureSeries.MarkerStyle = -4142 # no marker
            }
        }
    }
    if ($figureChartCount -ne 4) { throw "Expected four editable charts, found $figureChartCount" }
    $figurePresentation.SaveCopyAs($figureCorrectedPath, 24)
    Write-Output 'figure stage=PowerPoint-native-style completed=1/1 charts=4'
} finally {
    if ($null -ne $figurePresentation) { $figurePresentation.Close(); [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($figurePresentation) }
    if ($null -ne $figureApp) {
        if (-not $figureHadApp) { $figureApp.Quit() }
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($figureApp)
    }
}
Copy-Item -LiteralPath $figureCorrectedPath -Destination $figurePptPath -Force
$env:UV_CACHE_DIR = Join-Path $env:TEMP 'chemworld-uv-cache'
Push-Location $figureRoot
try {
    & uv run --no-sync python (Join-Path $PSScriptRoot 'finalize_research_case_chart_style.py') $figurePptPath
    if ($LASTEXITCODE -ne 0) { throw 'Native marker styling failed' }
} finally { Pop-Location }
$figureApp = $null
$figurePresentation = $null
try {
    $figureApp = New-Object -ComObject PowerPoint.Application
    $figurePresentation = $figureApp.Presentations.Open($figurePptPath, -1, 0, 0)
    $figurePresentation.Slides.Item(1).Export((Join-Path $figureDirectory 'c-w05-research-paths-v16.png'), 'PNG', 3600, 6880)
    Write-Output 'figure stage=PowerPoint-export completed=1/1 charts=4'
} finally {
    if ($null -ne $figurePresentation) { $figurePresentation.Close(); [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($figurePresentation) }
    if ($null -ne $figureApp) {
        if (-not $figureHadApp) { $figureApp.Quit() }
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($figureApp)
    }
}
