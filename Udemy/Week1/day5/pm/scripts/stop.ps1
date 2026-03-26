$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$rootDir = Resolve-Path (Join-Path $scriptDir "..")

Set-Location $rootDir
docker compose down --remove-orphans

Write-Output "PM MVP containers stopped."
