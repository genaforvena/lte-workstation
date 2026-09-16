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
$log = Join-Path $desktop "internet-test-dns-$stamp.csv"
if (Test-Path -LiteralPath $log) {
    throw "Refusing to overwrite existing log: $log"
}

$dnsTarget = 'example.com'
$cloudflare = '1.1.1.1'
$google = '8.8.8.8'
'timestamp_utc,elapsed_s,gateway,internet,router_dns,cloudflare_dns,google_dns,system_dns,failure_reason' |
    Set-Content -LiteralPath $log -Encoding UTF8
Write-Host "DNS diagnostic started. Gateway/router DNS: $gateway; public DNS: $cloudflare, $google; interval: ${IntervalSeconds}s."
Write-Host '0 means the probe passed; 1 means it failed. Press Ctrl+C to stop; partial CSV remains on Desktop.'

function Test-DnsServer {
    param([string]$Server)
    try {
        $null = Resolve-DnsName -Name $dnsTarget -Type A -Server $Server -DnsOnly -QuickTimeout -ErrorAction Stop
        return @{ Result = 0; Reason = '' }
    }
    catch {
        $reason = $_.Exception.Message -replace '[\r\n,]+', ' '
        return @{ Result = 1; Reason = "${Server}:$reason" }
    }
}

$durationSeconds = $DurationMinutes * 60
$clock = [System.Diagnostics.Stopwatch]::StartNew()
$nextSample = 0.0
$samples = 0
while ($clock.Elapsed.TotalSeconds -lt $durationSeconds) {
    $elapsed = [int][Math]::Floor($clock.Elapsed.TotalSeconds)
    $gatewayResult = 1
    & ping.exe -n 1 -w 1500 $gateway *> $null
    if ($LASTEXITCODE -eq 0) { $gatewayResult = 0 }

    $internetResult = 1
    & ping.exe -n 1 -w 1500 '1.1.1.1' *> $null
    if ($LASTEXITCODE -eq 0) { $internetResult = 0 }

    $routerProbe = Test-DnsServer -Server $gateway
    $cloudflareProbe = Test-DnsServer -Server $cloudflare
    $googleProbe = Test-DnsServer -Server $google
    $systemProbe = @{ Result = 0; Reason = '' }
    try {
        $null = Resolve-DnsName -Name $dnsTarget -Type A -DnsOnly -QuickTimeout -ErrorAction Stop
    }
    catch {
        $systemProbe.Result = 1
        $systemProbe.Reason = "system:$($_.Exception.Message -replace '[\r\n,]+', ' ')"
    }

    $reasons = @($routerProbe.Reason, $cloudflareProbe.Reason, $googleProbe.Reason, $systemProbe.Reason) |
        Where-Object { $_ }
    if ($gatewayResult -eq 1) { $reasons += 'gateway:ping-failed' }
    if ($internetResult -eq 1) { $reasons += 'internet:ping-failed' }
    $reasonText = ($reasons -join ';')
    $now = [DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ')
    $row = '{0},{1},{2},{3},{4},{5},{6},{7},"{8}"' -f $now, $elapsed, $gatewayResult, $internetResult,
        $routerProbe.Result, $cloudflareProbe.Result, $googleProbe.Result, $systemProbe.Result, $reasonText
    Add-Content -LiteralPath $log -Value $row -Encoding UTF8
    $samples++
    Write-Host "$now elapsed=${elapsed}s router=$gatewayResult internet=$internetResult router_dns=$($routerProbe.Result) cloudflare_dns=$($cloudflareProbe.Result) google_dns=$($googleProbe.Result) system_dns=$($systemProbe.Result)"

    $nextSample += $IntervalSeconds
    $remaining = $nextSample - $clock.Elapsed.TotalSeconds
    if ($remaining -gt 0) {
        Start-Sleep -Milliseconds ([int][Math]::Ceiling($remaining * 1000))
    }
    else {
        $nextSample = $clock.Elapsed.TotalSeconds
    }
}

Write-Host "Finished: samples=$samples"
Write-Host "CSV log: $log"
