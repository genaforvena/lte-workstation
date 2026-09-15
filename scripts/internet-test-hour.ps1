param(
    [ValidateRange(1, 1440)]
    [int]$DurationMinutes = 60,
    [ValidateRange(1, 3600)]
    [int]$IntervalSeconds = 60
)

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
$log = Join-Path $desktop "internet-test-hour-$stamp.csv"
if (Test-Path -LiteralPath $log) {
    throw "Refusing to overwrite existing log: $log"
}

'timestamp_utc,elapsed_s,gateway,internet,dns' | Set-Content -LiteralPath $log -Encoding UTF8
Write-Host "One-hour test started. Gateway: $gateway; sample interval: ${IntervalSeconds}s."
Write-Host '0 means the probe passed; 1 means it failed. Press Ctrl+C to stop; partial CSV remains on Desktop.'

$durationSeconds = $DurationMinutes * 60
$clock = [System.Diagnostics.Stopwatch]::StartNew()
$nextSample = 0.0
$samples = 0
$gatewayFailures = 0
$internetFailures = 0
$dnsFailures = 0

while ($clock.Elapsed.TotalSeconds -lt $durationSeconds) {
    $elapsed = [int][Math]::Floor($clock.Elapsed.TotalSeconds)
    $gatewayResult = 1
    & ping.exe -n 1 -w 1500 $gateway *> $null
    if ($LASTEXITCODE -eq 0) { $gatewayResult = 0 }

    $internetResult = 1
    & ping.exe -n 1 -w 1500 '1.1.1.1' *> $null
    if ($LASTEXITCODE -eq 0) { $internetResult = 0 }

    $dnsResult = 1
    try {
        $null = Resolve-DnsName -Name 'example.com' -Type A -DnsOnly -QuickTimeout -ErrorAction Stop
        $dnsResult = 0
    }
    catch { }

    $now = [DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ')
    $row = '{0},{1},{2},{3},{4}' -f $now, $elapsed, $gatewayResult, $internetResult, $dnsResult
    Add-Content -LiteralPath $log -Value $row -Encoding UTF8
    $samples++
    if ($gatewayResult -eq 1) { $gatewayFailures++ }
    if ($internetResult -eq 1) { $internetFailures++ }
    if ($dnsResult -eq 1) { $dnsFailures++ }
    Write-Host "$now elapsed=${elapsed}s router=$gatewayResult internet=$internetResult DNS=$dnsResult"

    $nextSample += $IntervalSeconds
    $remaining = $nextSample - $clock.Elapsed.TotalSeconds
    if ($remaining -gt 0) {
        Start-Sleep -Milliseconds ([int][Math]::Ceiling($remaining * 1000))
    }
    else {
        $nextSample = $clock.Elapsed.TotalSeconds
    }
}

Write-Host "Finished: samples=$samples router_fail=$gatewayFailures internet_fail=$internetFailures DNS_fail=$dnsFailures"
Write-Host "CSV log: $log"
