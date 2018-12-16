Create a new file called `Metin2Client_CompileRelease.bat` inside `\Srcs\Client\` containing:
```batch
@echo off
CALL "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\Common7\Tools\VsDevCmd.bat"
msbuild metin2client.sln /property:Configuration=Release
pause
```
_Note: this is for vs2017; if you use other versions, be sure to match the correct path_
_Note2: you can do this for server (for windows) as well._
