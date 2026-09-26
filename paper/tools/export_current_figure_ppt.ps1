param(
    [string]$Source,
    [string]$ExportDirectory = (Join-Path $env:TEMP 'chemworld-user-ppt-integration')
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
if (-not $Source) {
    $Source = Join-Path $repoRoot 'output/pptx/chemworld-current-figures-editable.pptx'
}
$Source = (Resolve-Path -LiteralPath $Source).Path
New-Item -ItemType Directory -Path $ExportDirectory -Force | Out-Null
$snapshot = Join-Path $ExportDirectory 'source.pptx'
Copy-Item -LiteralPath $Source -Destination $snapshot
$application = $null
$presentation = $null
try {
    $application = New-Object -ComObject PowerPoint.Application
    $presentation = $application.Presentations.Open($snapshot, -1, 0, 0)
    if ($presentation.Slides.Count -ne 7) {
        throw 'Expected Figures 1-6 and S4 in that order; review a changed selection before exporting.'
    }
    $width = 4320
    $height = [int][Math]::Round($width * $presentation.PageSetup.SlideHeight / $presentation.PageSetup.SlideWidth)
    $presentation.SaveAs((Join-Path $ExportDirectory 'all-slides.pdf'), 32)
    Write-Output 'Figure export: native PDF complete; PNG previews completed=0/7'
    for ($index = 1; $index -le 7; $index++) {
        $presentation.Slides.Item($index).Export(
            (Join-Path $ExportDirectory "slide-$index.png"), 'PNG', $width, $height
        )
        Write-Output "Figure export: PNG previews completed=$index/7"
    }
} finally {
    if ($null -ne $presentation) {
        try { $presentation.Close() } finally {
            [void][Runtime.InteropServices.Marshal]::ReleaseComObject($presentation)
        }
    }
    # Do not quit a shared presentation application that the user may be using.
    if ($null -ne $application) {
        [void][Runtime.InteropServices.Marshal]::ReleaseComObject($application)
    }
}
Write-Output "Export directory: $ExportDirectory"
