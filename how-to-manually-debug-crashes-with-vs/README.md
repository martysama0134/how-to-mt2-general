# How to manually debug crashes with VisualStudio

1. Go to Debug -> Options and Settings... [ClickMe](https://i.imgur.com/N6l5hUE.png)

	Go inside Debugging -> General [ClickMe](https://i.imgur.com/tzlVBdA.png)

	[v] Show disassembly if source is not available

2. On UserInterface -> Properties [ClickMe](https://i.imgur.com/LSi4xHl.png)

	Go inside Linker -> Debugging [ClickMe](https://i.imgur.com/vf6Y6yU.png)
	
	* Generate Debug Info -> Yes (/DEBUG)
	* ~Map Exports -> Yes (/MAPINFO:EXPORTS)~ _(not required)_
	* Debuggable Assembly -> Yes (/ASSEMBLYDEBUG)

3. Compile and execute the launcher.

4. Debug -> Attach to Process... [ClickMe](https://i.imgur.com/Mskhvaq.png)

	metin2client.exe -> Attach [ClickMe](https://i.imgur.com/50WDcYa.png)

5. When you will get a crash (or "??????") you will get the Call Stack [ClickMe](https://i.imgur.com/LGXpzz5.png)

6. To disable all: [ClickMe](https://i.imgur.com/aV29aB0.png)

	On UserInterface -> Properties

	Go inside Linker -> Debugging
	
	* Generate Debug Info -> No
	* Map Exports -> No
	* Debuggable Assembly -> No (/ASSEMBLYDEBUG:DISABLE)

_Note: Whether the target is set on Release or Debug, it's irrelevant_

## How to start a debugging session without attaching
1. Go to the Solution's property and choose UserInterface as the main project. [ClickMe](https://i.imgur.com/IzcSgDT.png)

2. On UserInterface -> Properties -> Debug, change the working directory to your client path. [ClickMe](https://i.imgur.com/YLzEWlc.png)

3. Now 1) press the green arrow or 2) f5 or 3) Debug->Start debug (visual studio will ask admin privileges due to the launcher's manifests) and enjoy the debugging.

## How to copy the built launcher and start a debugging session automatically elsewhere
Lazy to copy the launcher from bin to client (local debugging path), then start the debugger? This can be automated.

1. On UserInterface -> Properties -> General -> Output Directory, the path must have `\\` slashes and NO `/` ones.

2. On UserInterface -> Properties -> Build Events -> Post compilation events -> Command-line: [ClickMe](https://i.imgur.com/WJAV9Zi.png)

	`copy /y "$(TargetPath)" "$(LocalDebuggerWorkingDirectory)$(TargetFileName)"`

Now you can press Play (F5) directly.

## Issues
1. The debugger can't attach properly to the launcher if the "python" module of Visual Studio has been installed from Visual Studio Installer.

2. If it doesn't start the debugger at all, disable the Microsoft Symbols from Debug -> Debug -> Symbols [ClickMe](https://i.imgur.com/2ymAPIE.png)
