Param(
    [string]$HostAddress = "0.0.0.0",
    [int]$Port = 8000
)

$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "Starting backend from: $(C:\Users\RUDRAMUNISWAMY\Desktop\Stuttering_classifier\backend\app\main.py)"
uvicorn app.main:app --host $HostAddress --port $Port --reload
