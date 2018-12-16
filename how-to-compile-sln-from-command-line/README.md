### Intro
Create a new file called `Metin2Client_CompileRelease.bat` inside `\Srcs\Client\` containing:
```batch
@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\Common7\Tools\VsDevCmd.bat"
REM msbuild metin2client.sln /property:Configuration=Release -target:Clean
msbuild metin2client.sln /property:Configuration=Release
pause
```
_Note: this is for vs2017 - target Release; if you use other versions, be sure to match the correct path_

_Note2: you can do this for server (for windows) as well._

### Links:
[msbuild documentation](https://docs.microsoft.com/it-it/visualstudio/msbuild/msbuild-command-line-reference?view=vs-2017)
