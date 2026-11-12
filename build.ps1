$ErrorActionPreference = 'Stop'
$compiler = Join-Path $env:WINDIR 'Microsoft.NET\Framework64\v4.0.30319\csc.exe'
if (-not (Test-Path -LiteralPath $compiler)) { throw '.NET Framework C# compiler was not found.' }
$buildDir = Join-Path $PSScriptRoot 'build'
New-Item -ItemType Directory -Force -Path $buildDir | Out-Null
$output = Join-Path $buildDir 'TopazPhotoMicaHost.exe'
& $compiler /nologo /target:winexe /reference:System.Windows.Forms.dll "/out:$output" (Join-Path $PSScriptRoot 'src\MicaHost.cs')
if ($LASTEXITCODE -ne 0) { throw 'C# compilation failed.' }
Write-Output "Built: $output"
