param(
    [string]$Source,
    [string]$ExportDirectory,
    [ValidateSet('main', 'supplementary')]
    [string]$Kind = 'main'
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
if (-not $Source) {
    $name = if ($Kind -eq 'main') { 'current' } else { 'supplementary' }
    $Source = Join-Path $repoRoot "output/pptx/chemworld-$name-figures-editable.pptx"
}
if (-not $ExportDirectory) {
    $folder = if ($Kind -eq 'main') { 'chemworld-user-ppt-integration' } else { 'chemworld-supplementary-ppt-integration' }
    $ExportDirectory = Join-Path $env:TEMP $folder
}
$expected = if ($Kind -eq 'main') { 7 } else { 9 }
$Source = (Resolve-Path -LiteralPath $Source).Path
New-Item -ItemType Directory -Path $ExportDirectory -Force | Out-Null
$snapshot = Join-Path $ExportDirectory 'source.pptx'
Copy-Item -LiteralPath $Source -Destination $snapshot
$application = $null
$presentation = $null
try {
    $application = New-Object -ComObject PowerPoint.Application
    $presentation = $application.Presentations.Open($snapshot, -1, 0, 0)
    if ($presentation.Slides.Count -ne $expected) {
        throw "Expected $expected pages in the $Kind collection; review a changed selection before exporting."
    }
    $width = 4320
    $height = [int][Math]::Round($width * $presentation.PageSetup.SlideHeight / $presentation.PageSetup.SlideWidth)
    $presentation.SaveAs((Join-Path $ExportDirectory 'all-slides.pdf'), 32)
    Write-Output "Figure export: native PDF complete; PNG previews completed=0/$expected"
    for ($index = 1; $index -le $expected; $index++) {
        $presentation.Slides.Item($index).Export(
            (Join-Path $ExportDirectory "slide-$index.png"), 'PNG', $width, $height
        )
        Write-Output "Figure export: PNG previews completed=$index/$expected"
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
