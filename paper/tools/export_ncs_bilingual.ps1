# Export current bilingual Word manuscripts using native Word. No source rewriting.
param(
  [Parameter(Mandatory=$true)][string]$InputDirectory,
  [Parameter(Mandatory=$true)][string]$OutputDirectory
)
$ErrorActionPreference='Stop'
$sourceDirectory=(Resolve-Path -LiteralPath $InputDirectory).Path
New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
$targetDirectory=(Resolve-Path -LiteralPath $OutputDirectory).Path
foreach ($language in @('en','zh')) {
  $wordApplication=$null
  $wordDocument=$null
  try {
    $stem='chemworld-ncs-'+$language+'-final'
    $wordApplication=New-Object -ComObject Word.Application
    $wordApplication.Visible=$false
    $wordApplication.DisplayAlerts=0
    Write-Output ('Native Word export: '+$language+' opening')
    $wordDocument=$wordApplication.Documents.Open((Join-Path $sourceDirectory ($stem+'.docx')),$false,$true)
    $wordDocument.Repaginate()
    Write-Output ('Native Word export: '+$language+' pages='+$wordDocument.ComputeStatistics(2))
    $wordDocument.ExportAsFixedFormat((Join-Path $targetDirectory ($stem+'.pdf')),17)
    Write-Output ('Native Word export: '+$language+' complete')
  } finally {
    if ($null -ne $wordDocument) {
      try {$wordDocument.Close(0)} catch {}
      [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($wordDocument)
    }
    if ($null -ne $wordApplication) {
      [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($wordApplication)
    }
  }
}
