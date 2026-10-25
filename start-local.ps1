$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$previewScript = Join-Path $repoRoot "scripts\local-preview.py"
$url = "http://127.0.0.1:8080/"

Write-Host "Starting Troy Condo Garages static site preview..."
Write-Host "Serving folder: $(Join-Path $repoRoot 'site')"
Start-Process python $previewScript
Start-Sleep -Seconds 2
Start-Process $url
Write-Host "Preview opened at $url"
Write-Host "Pages: /  /units/  /design-your-space/  /gallery/  /events/  /rentals/  /about/  /contact/  /financing/  /pricing/"
Write-Host "To stop the server, close the Python window or end the python process."
