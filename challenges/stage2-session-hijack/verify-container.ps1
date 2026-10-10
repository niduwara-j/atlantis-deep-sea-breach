$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$containerId = docker compose ps -q web
if ($LASTEXITCODE -ne 0 -or -not $containerId) { throw 'Challenge container is not running.' }
$details = (docker inspect $containerId | ConvertFrom-Json)[0]
if ($LASTEXITCODE -ne 0) { throw 'Could not inspect the challenge container.' }
if ($details.Config.User -ne '10001:10001') { throw 'Unexpected container user.' }
if (-not $details.HostConfig.ReadonlyRootfs) { throw 'Root filesystem is not read-only.' }
if ($details.HostConfig.CapDrop -notcontains 'ALL') { throw 'Linux capabilities have not all been dropped.' }
if ($details.HostConfig.SecurityOpt -notcontains 'no-new-privileges:true') { throw 'No-new-privileges is missing.' }
if ($details.HostConfig.Memory -ne 268435456) { throw 'Unexpected memory limit.' }
Write-Host 'PASS: non-root user, read-only filesystem, dropped capabilities, privilege and memory limits.'
$networkNames = @($details.NetworkSettings.Networks.PSObject.Properties.Name)
if ($networkNames.Count -ne 1) { throw 'Challenge is attached to more than one network.' }
$networkDetails = (docker network inspect $networkNames[0] | ConvertFrom-Json)[0]
if (-not $networkDetails.Internal) { throw 'Challenge network is not internal.' }
Write-Host 'PASS: single internal Docker network.'
if ($details.HostConfig.PortBindings.'8092/tcp') { throw 'Backend must not publish its own port.' }
$gatewayId = docker compose ps -q gateway
if (-not $gatewayId) { throw 'Gateway is not running.' }
$gatewayDetails = (docker inspect $gatewayId | ConvertFrom-Json)[0]
$portBinding = $gatewayDetails.HostConfig.PortBindings.'8092/tcp'
if ($portBinding.Count -ne 1 -or $portBinding[0].HostIp -ne '127.0.0.1') { throw 'Challenge port is not loopback-only.' }
Write-Host 'PASS: loopback-only published port.'
if ($gatewayDetails.Config.User -ne '101:101' -or -not $gatewayDetails.HostConfig.ReadonlyRootfs) { throw 'Gateway user/filesystem protection is incorrect.' }
if ($gatewayDetails.HostConfig.CapDrop -notcontains 'ALL') { throw 'Gateway capabilities are not dropped.' }
Write-Host 'PASS: non-root read-only gateway with dropped capabilities.'
@'
import os, socket, urllib.request
assert os.getuid() == 10001
try:
    with open('/app/unexpected-write-check', 'w') as f:
        f.write('unexpected')
except OSError:
    print('PASS: application filesystem rejects writes')
else:
    raise SystemExit('FAIL: application filesystem was writable')
try:
    connection = socket.create_connection(('1.1.1.1', 443), timeout=3)
except OSError:
    print('PASS: direct external TCP probe blocked (one destination tested)')
else:
    connection.close()
    raise SystemExit('FAIL: direct external TCP connection succeeded')
assert urllib.request.urlopen('http://127.0.0.1:8092/healthz', timeout=5).status == 200
print('PASS: container health endpoint')
'@ | docker compose exec -T web python -
if ($LASTEXITCODE -ne 0) { throw 'Runtime isolation checks failed.' }
Write-Host 'Container checks passed. Test CTFd submission separately.'
