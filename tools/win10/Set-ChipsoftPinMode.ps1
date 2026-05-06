<#
.SYNOPSIS
    Switch the Chipsoft Pro driver between SWCAN-on-pin-1 mode and HSCAN-on-pins-3-11 mode.

.DESCRIPTION
    The Chipsoft Pro hardware cannot expose SWCAN (pin 1) and HSCAN (pins 3-11)
    simultaneously. CSTech2Win.dll reads three DWORD values from
        HKLM\SOFTWARE\CHIPSOFT\Tech2Win
    to decide which channel to drop:
        Tech2Win_DropCAN3_11  = 1   ->  SWCAN on pin 1 active   (SAAB Trionic 8)
        Tech2Win_DropSWCAN1   = 1   ->  HSCAN on pins 3-11 active
    These are mutually exclusive. CST2WinConfig.exe is the official GUI; this
    script does the same edit non-interactively for scripted bench work.

    NOTE: this affects Tech2Win / J2534-mode flows. The registry layer is read
    by the host driver only. The runtime J2534-2 path (PassThruIoctl with
    J1962_PINS) is independent and per-channel.

.PARAMETER Mode
    SWCAN_PIN1     -> Drop CAN 3-11, keep SWCAN on pin 1 (use this for SAAB Trionic 8)
    HSCAN_3_11     -> Drop SWCAN on pin 1, keep HSCAN on pins 3-11

.PARAMETER ShowOnly
    Print current state, do not write.

.EXAMPLE
    .\Set-ChipsoftPinMode.ps1 -Mode SWCAN_PIN1

.EXAMPLE
    .\Set-ChipsoftPinMode.ps1 -ShowOnly

.NOTES
    Run elevated (HKLM writes require admin). Restart Tech2Win / J2534 client
    after switching for the change to take effect.
#>
[CmdletBinding(DefaultParameterSetName = 'Set')]
param(
    [Parameter(Mandatory, ParameterSetName = 'Set')]
    [ValidateSet('SWCAN_PIN1', 'HSCAN_3_11')]
    [string]$Mode,

    [Parameter(Mandatory, ParameterSetName = 'Show')]
    [switch]$ShowOnly
)

$ErrorActionPreference = 'Stop'
$key = 'HKLM:\SOFTWARE\CHIPSOFT\Tech2Win'

function Show-State {
    if (-not (Test-Path $key)) {
        Write-Host "key $key does not exist (run CST2WinConfig.exe at least once first?)" -ForegroundColor Yellow
        return
    }
    $p = Get-ItemProperty -Path $key
    [pscustomobject]@{
        Path                  = $key
        Tech2Win_DropCAN3_11  = $p.Tech2Win_DropCAN3_11
        Tech2Win_DropSWCAN1   = $p.Tech2Win_DropSWCAN1
        Tech2Win_UseAsyncMode = $p.Tech2Win_UseAsyncMode
    } | Format-List
}

if ($ShowOnly) {
    Show-State
    return
}

if (-not (Test-Path $key)) {
    New-Item -Path $key -Force | Out-Null
}

switch ($Mode) {
    'SWCAN_PIN1' {
        Set-ItemProperty -Path $key -Name 'Tech2Win_DropCAN3_11' -Value 1 -Type DWord
        Set-ItemProperty -Path $key -Name 'Tech2Win_DropSWCAN1'  -Value 0 -Type DWord
        Write-Host "OK: SWCAN on pin 1 active (SAAB Trionic 8 mode)" -ForegroundColor Green
    }
    'HSCAN_3_11' {
        Set-ItemProperty -Path $key -Name 'Tech2Win_DropCAN3_11' -Value 0 -Type DWord
        Set-ItemProperty -Path $key -Name 'Tech2Win_DropSWCAN1'  -Value 1 -Type DWord
        Write-Host "OK: HSCAN on pins 3-11 active" -ForegroundColor Green
    }
}

Write-Host ""
Show-State
Write-Host ""
Write-Host "Restart Tech2Win / your J2534 client for the change to take effect." -ForegroundColor Cyan
