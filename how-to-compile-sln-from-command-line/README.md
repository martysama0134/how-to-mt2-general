### Intro
Create a new file called `Metin2Client_CompileRelease.bat` inside `\Srcs\Client\` containing:
```batch
@echo off
REM CALL "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\Common7\Tools\VsDevCmd.bat"
CALL "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvarsall.bat" x86
cd %~dp0
REM msbuild metin2client.sln /property:Configuration=Release /maxcpucount -target:Clean
REM msbuild metin2client.sln /property:Configuration=Release /maxcpucount
MSBuild.exe metin2client.sln /p:Configuration=Release /p:Platform=Win32 /maxcpucount

pause
```
It is currently cleaning and compiling in Release mode. Disable "Clean" if you don't need it.

The flag additional option `/maxcpucount` for `msbuild` will use more threads for compilation. Remove it if you don't use it.

_Note: this is for vs2017; if you use other versions, be sure to match the correct path_

_Note2: you can do this for server (for windows) as well._

### Links:
[msbuild documentation](https://docs.microsoft.com/it-it/visualstudio/msbuild/msbuild-command-line-reference?view=vs-2017)
