param(
    [ValidateRange(1, 1440)]
    [int]$DurationMinutes = 30,
    [ValidateRange(5, 3600)]
    [int]$IntervalSeconds = 15
)

# DNS-flap localization test for Rozalia (2026-09-15).
# Copy-paste ready: nothing to edit. Run in Windows PowerShell:
#   powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\Downloads\internet-dns-localize.ps1"
#
# What it does, once per sample: pings the router, pings 1.1.1.1, then asks
# FOUR resolvers for example.com A — the system default, the router itself,
# 1.1.1.1 and 8.8.8.8 — and logs WHY each DNS leg failed.
# 0 = probe passed, 1 = probe failed (same convention as internet-test-hour.ps1).
# Result: CSV on the Desktop. Send that file back to the mesh.

$ErrorActionPreference = 'Stop'

if (-not (Get-Command Get-NetRoute -ErrorAction SilentlyContinue)) {
    throw 'Get-NetRoute is unavailable; run this on Windows 10/11 with the NetTCPIP module.'
}
if (-not (Get-Command Resolve-DnsName -ErrorAction SilentlyContinue)) {
    throw 'Resolve-DnsName is unavailable; run this in Windows PowerShell 5.1 or PowerShell 7 on Windows.'
}

$route = Get-NetRoute -DestinationPrefix '0.0.0.0/0' -ErrorAction Stop |
    Sort-Object -Property RouteMetric
$gateway = $route | Select-Object -First 1 -ExpandProperty NextHop
if ([string]::IsNullOrWhiteSpace($gateway) -or $gateway -eq '0.0.0.0') {
    throw 'Could not identify an IPv4 default gateway.'
}

$desktop = [Environment]::GetFolderPath('Desktop')
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$log = Join-Path $desktop "dns-localize-$stamp.csv"
if (Test-Path -LiteralPath $log) {
    throw "Refusing to overwrite existing log: $log"
}

'timestamp_utc,elapsed_s,router,internet,dns_default,dns_router,dns_1111,dns_8888,note' | Set-Content -LiteralPath $log -Encoding UTF8
Write-Host "DNS-localization started. Gateway: $gateway; sample every ${IntervalSeconds}s for ~${DurationMinutes} min."
Write-Host '0 = probe passed, 1 = probe failed. Press Ctrl+C to stop; partial CSV remains on Desktop.'

function Test-DnsLeg {
    param([string]$Name, [string]$Server)
    try {
        if ($Server) {
            $null = Resolve-DnsName -Name 'example.com' -Type A -DnsOnly -Server $Server -QuickTimeout -ErrorAction Stop
        } else {
            $null = Resolve-DnsName -Name 'example.com' -Type A -DnsOnly -QuickTimeout -ErrorAction Stop
        }
        return @(0, '')
    }
    catch {
        $msg = ($_.Exception.Message -replace '[\r\n]+', ' ').Trim()
        if ($msg.Length -gt 80) { $msg = $msg.Substring(0, 80) }
        return @(1, "$Name($msg)")
    }
}

$durationSeconds = $DurationMinutes * 60
$clock = [System.Diagnostics.Stopwatch]::StartNew()
$nextSample = 0.0
$samples = 0
$routerFails = 0
$internetFails = 0
$dnsFails = 0

while ($clock.Elapsed.TotalSeconds -lt $durationSeconds) {
    $elapsed = [int][Math]::Floor($clock.Elapsed.TotalSeconds)

    $routerResult = 1
    & ping.exe -n 1 -w 1500 $gateway *> $null
    if ($LASTEXITCODE -eq 0) { $routerResult = 0 }

    $internetResult = 1
    & ping.exe -n 1 -w 1500 '1.1.1.1' *> $null
    if ($LASTEXITCODE -eq 0) { $internetResult = 0 }

    $d0 = Test-DnsLeg -Name 'default' -Server ''
    $d1 = Test-DnsLeg -Name 'router' -Server $gateway
    $d2 = Test-DnsLeg -Name '1.1.1.1' -Server '1.1.1.1'
    $d3 = Test-DnsLeg -Name '8.8.8.8' -Server '8.8.8.8'

    $notes = @($d0[1], $d1[1], $d2[1], $d3[1]) | Where-Object { $_ -ne '' }
    $note = ($notes -join '; ' -replace '"', "'")

    $now = [DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ')
    $row = '{0},{1},{2},{3},{4},{5},{6},{7},"{8}"' -f $now, $elapsed, $routerResult, $internetResult, $d0[0], $d1[0], $d2[0], $d3[0], $note
    Add-Content -LiteralPath $log -Value $row -Encoding UTF8
    $samples++
    if ($routerResult -eq 1) { $routerFails++ }
    if ($internetResult -eq 1) { $internetFails++ }
    if (($d0[0] -eq 1) -or ($d1[0] -eq 1) -or ($d2[0] -eq 1) -or ($d3[0] -eq 1)) { $dnsFails++ }
    Write-Host "$now elapsed=${elapsed}s router=$routerResult internet=$internetResult dns_default=$($d0[0]) dns_router=$($d1[0]) dns_1111=$($d2[0]) dns_8888=$($d3[0])"

    $nextSample += $IntervalSeconds
    $remaining = $nextSample - $clock.Elapsed.TotalSeconds
    if ($remaining -gt 0) {
        Start-Sleep -Milliseconds ([int][Math]::Ceiling($remaining * 1000))
    }
    else {
        $nextSample = $clock.Elapsed.TotalSeconds
    }
}

Write-Host "Finished: samples=$samples router_fail=$routerFails internet_fail=$internetFails samples_with_any_dns_fail=$dnsFails"
Write-Host "CSV log: $log"
